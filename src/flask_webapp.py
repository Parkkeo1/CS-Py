from flask import Flask, request, render_template, g, session, redirect, url_for

# database management
import sqlite3
import os

# cfg file setup
import winreg as registry
from shutil import copyfile, SameFileError

# data processing
import json
from gsi_data_payload import GameStateCode, GameStatePayload
from match_analysis import MatchAnalysis
import pandas as pd


# string constants
GS_CFG_DEST_PATH = '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/gamestate_integration_main.cfg'
GS_CFG_SRC_PATH = '../req_files/gamestate_integration_main.cfg'
GS_ON = 'GS is currently ON'
GS_OFF = 'GS is currently OFF'

# the CS-Py Flask object
cs_py = Flask(__name__, template_folder='../templates', static_folder='../static')
cs_py.config['SECRET_KEY'] = 'half-life 3 confirmed'
cs_py.config['DATABASE'] = os.path.join(cs_py.root_path, '..', 'player_data.db')
cs_py.config['STATE'] = False


# ---------------------------

# database connection handling
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(cs_py.config['DATABASE'])
    return g.sqlite_db


@cs_py.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# ---------------------------

# manual shutdown method
# derived from: http://flask.pocoo.org/snippets/67/
def shutdown_server():
    quit_cspy = request.environ.get('werkzeug.server.shutdown')
    if quit_cspy is None:
        raise RuntimeError('Flask Server Not Running')
    quit_cspy()


# ---------------------------

# checks and setup on startup
def setup_gamestate_cfg():
    try:
        steam_key = registry.CreateKey(registry.HKEY_CURRENT_USER, "Software\Valve\Steam")
        cfg_destination = registry.QueryValueEx(steam_key, "SteamPath")[0] + GS_CFG_DEST_PATH
        copyfile(GS_CFG_SRC_PATH, cfg_destination)
        print('Auto CFG File Passed')
    except (OSError, SameFileError):
        print('Auto CFG File Failed')


def init_table_if_not_exists(sql_db):
    create_round_table_sql = '''CREATE TABLE IF NOT EXISTS per_round_data (Time INTEGER, SteamID INTEGER, Map TEXT, 
                                                                     'Map Status' TEXT, 'Player Name' TEXT,
                                                                     'Player Team' TEXT, Kills INTEGER, Assists INTEGER,
                                                                     Deaths INTEGER, MVPs INTEGER, Score INTEGER,
                                                                     'Current Equip. Value' INTEGER, 'Round Kills' INTEGER,
                                                                     'Round HS Kills' INTEGER);'''

    # create_match_table_sql = '''CREATE TABLE IF NOT EXISTS per_match_data (Match_ID INTEGER PRIMARY KEY, Duration REAL,
    #                                                                        'Round Count' INTEGER, Map TEXT, Rating1 REAL,
    #                                                                        HSR REAL, MDC REAL, KPR REAL, KAS REAL,
    #                                                                        KDR REAL, KDA REAL, MEAN REAL, CT_Rating1 REAL,
    #                                                                        CT_HSR REAL, CT_MDC REAL, CT_KPR REAL,
    #                                                                        CT_KAS REAL, CT_KDR REAL, CT_KDA REAL,
    #                                                                        CT_MEAN REAL, T_Rating1 REAL, T_HSR REAL,
    #                                                                        T_MDC REAL, T_KPR REAL, T_KAS REAL, T_KDR REAL,
    #                                                                        T_KDA REAL, T_MEAN REAL);'''

    sql_db.cursor().execute(create_round_table_sql)
    sql_db.commit()
    print("SQL Table Check Passed")


# ---------------------------

# utility methods for processing in flask routes

# clears per_round_data table to indicate end of game
def send_match_to_remote():
    round_db = get_db()

    # parse current per_round_data into dataframe
    data_for_match_df = pd.read_sql('SELECT * FROM per_round_data;', round_db)
    if data_for_match_df.empty or data_for_match_df.shape[0] == 0:
        return

    # TODO: Implement methods in match_analysis.py to enter data summary into per_match_data table.
    match_data = MatchAnalysis(data_for_match_df)

    del match_data.data_frame
    match_json = json.dumps(match_data.__dict__)
    # TODO: send match_json to remote server.(include steamID of user in header?)

    # clear per_round_data table
    round_db.cursor().execute('DELETE FROM per_round_data;')
    round_db.commit()
    print("Match Data Sent; Rounds Reset")


# checks previous entries in database to make sure there are no duplicates.
def check_prev_entries(game_data):
    player_db = get_db()
    last_entry = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', player_db)

    # time difference is 1 second or less
    if last_entry.shape[0] != 0 and abs(int(game_data.provider.timestamp - last_entry.iloc[0]['Time'])) <= 1:
        sql_delete = 'DELETE FROM per_round_data WHERE Time = (SELECT MAX(Time) FROM per_round_data);'
        player_db.cursor().execute(sql_delete)
        player_db.commit()
        print("Time Duplicate Replaced")
    else:
        print("Not a Duplicate")


def insert_round_data(round_data):
    match_stats = round_data.player.match_stats
    player_state = round_data.player.state

    new_round_data = (
        round_data.provider.timestamp, round_data.provider.steamid, round_data.map.name, round_data.map.phase,
        round_data.player.name, round_data.player.team, match_stats.kills, match_stats.assists, match_stats.deaths,
        match_stats.mvps, match_stats.score, player_state.equip_value, player_state.round_kills, player_state.round_killhs)

    round_insert_sql = ''' INSERT INTO per_round_data(Time, SteamID, Map, "Map Status", "Player Name", "Player Team",
                                                Kills, Assists, Deaths, MVPs, Score, "Current Equip. Value",
                                                "Round Kills", "Round HS Kills")
                                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    print(new_round_data)
    conn = get_db()
    conn.cursor().execute(round_insert_sql, new_round_data)
    conn.commit()


# def insert_match_data(match_data):
#     new_match_data = (int(match_data.duration), match_data.round_count, match_data.map_name, match_data.rating1, match_data.hsr,
#                       match_data.mdc, match_data.kpr, match_data.kas, match_data.kdr, match_data.kda, match_data.mean_equip,
#                       match_data.ct_rating1, match_data.ct_hsr, match_data.ct_mdc, match_data.ct_kpr, match_data.ct_kas,
#                       match_data.ct_kdr, match_data.ct_kda, match_data.ct_mean_equip, match_data.t_rating1, match_data.t_hsr,
#                       match_data.t_mdc, match_data.t_kpr, match_data.t_kas, match_data.t_kdr, match_data.t_kda,
#                       match_data.t_mean_equip)
#
#     match_insert_sql = ''' INSERT INTO per_match_data (Duration, 'Round Count', Map, Rating1, HSR, MDC, KPR, KAS, KDR, KDA,
#                                                        MEAN, CT_Rating1, CT_HSR, CT_MDC, CT_KPR, CT_KAS,
#                                                        CT_KDR, CT_KDA, CT_MEAN, T_Rating1, T_HSR, T_MDC, T_KPR, T_KAS,
#                                                        T_KDR, T_KDA, T_MEAN) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
#                                                         ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
#
#     print(new_match_data)
#     conn = get_db()
#     conn.cursor().execute(match_insert_sql, new_match_data)
#     conn.commit()


# ---------------------------

# flask server routes

# the home page, handles frontend user interaction
@cs_py.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = str(request.form.get('input'))

        # user chooses to start or end active data collection
        if user_input == 'start' or user_input == 'end':
            cs_py.config['STATE'] = True if user_input == 'start' else False
            return redirect(url_for('index'))

        # user chooses to reset, ending collection for current match
        elif user_input == 'reset':
            send_match_to_remote()
            return redirect(url_for('index'))
    else:
        # updating frontend status of CS-Py
        status = GS_ON if cs_py.config['STATE'] else GS_OFF
        return render_template('index.html', status=status)


# route that receives JSON payloads from the game client
# noinspection PyTypeChecker
@cs_py.route('/GS', methods=['POST'])
def gamestate_handler():
    if request.is_json and cs_py.config['STATE']:
        game_data = GameStatePayload(request.get_json())
        print(game_data.gamestate_code)

        if game_data.gamestate_code == GameStateCode.INVALID:
            return 'Invalid Data Received'
        elif game_data.gamestate_code == GameStateCode.ENDGAME_DIFF_PLAYER:
            print("End Game Payload Received")
            send_match_to_remote()
        else:
            check_prev_entries(game_data)
            insert_round_data(round_data=game_data)
            if game_data.map.phase == 'gameover':  # automatic reset if player was alive by end of game.
                send_match_to_remote()

    return 'Request Received'


@cs_py.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'CS-Py is shutting down. You may now close this browser window/tab.'


@cs_py.route('/results')
def results():
    result = session['result']
    return render_template('results.html', result=result)


# ---------------------------

# temp fix for matplotlib plot images not refreshing unless page is manually refreshed.
@cs_py.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
