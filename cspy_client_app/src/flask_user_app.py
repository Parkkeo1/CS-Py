import os
import shutil
import sqlite3
import webbrowser
import winreg

from flask import Flask, request, render_template, g, redirect, url_for
import pandas as pd
import requests

from match_analysis import MatchAnalysis
from game_state_payload import GameStateCode, GameStatePayload


# string constants
GS_CFG_DEST_PATH = '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/gamestate_integration_main.cfg'
GS_CFG_SRC_PATH = '../../required_user_files/gamestate_integration_main.cfg'
GS_ON = 'GS is currently ON'
GS_OFF = 'GS is currently OFF'

# Web address of RESTful API server to which match data is sent
API_ADDRESS = 'http://127.0.0.1:5001/api/data_receiver'  # TODO: For Testing

# the CS-Py Flask object
cs_py_client = Flask(__name__, template_folder='../templates', static_folder='../static')
cs_py_client.config['DATABASE'] = os.path.join(cs_py_client.root_path, '..', 'rounds_data.db')
cs_py_client.config['STATE'] = False


# ---------------------------

# database connection handling
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(cs_py_client.config['DATABASE'])
    return g.sqlite_db


@cs_py_client.teardown_appcontext
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
        steam_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
        cfg_destination = winreg.QueryValueEx(steam_key, "SteamPath")[0] + GS_CFG_DEST_PATH
        shutil.copyfile(GS_CFG_SRC_PATH, cfg_destination)
        print('Auto CFG File Passed')
    except (OSError, shutil.SameFileError):
        print('Auto CFG File Failed')


def init_table_if_not_exists(sql_db):
    create_round_table_sql = '''CREATE TABLE IF NOT EXISTS per_round_data (Time INTEGER, SteamID INTEGER, Map TEXT, 
                                                                     'Map Status' TEXT, Round INTEGER, 'Player Name' TEXT,
                                                                     'Player Team' TEXT, Kills INTEGER, Assists INTEGER,
                                                                     Deaths INTEGER, MVPs INTEGER, Score INTEGER,
                                                                     'Current Equip. Value' INTEGER, 'Round Kills' INTEGER,
                                                                     'Round HS Kills' INTEGER);'''

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
        return  # cancel if there's no data to analyze or send

    match_data = MatchAnalysis(data_for_match_df)
    del match_data.data_frame
    # TODO: May include client's steamid also in the headers as well as in the json data in the future. TBD
    print(match_data.__dict__)
    send_match_request = requests.post(API_ADDRESS, json=match_data.__dict__)

    # checking if request was successful
    if send_match_request.status_code == 202:  # CS-Py's API should send 202: Accepted as response code upon success.
        # clear per_round_data table
        round_db.cursor().execute('DELETE FROM per_round_data;')
        round_db.commit()
        print("Match Data Sent; Rounds Reset")
    else:
        print("API Request Failed. Not Clearing Round Data. Code: " + str(send_match_request.status_code))


# checks previous entries in database to make sure there are no duplicates.
def check_prev_entries(game_data):
    player_db = get_db()
    last_entry = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', player_db)

    if last_entry.shape[0] != 0:
        if abs(int(game_data.provider.timestamp - last_entry.iloc[0]['Time'])) <= 1:
            sql_delete = 'DELETE FROM per_round_data WHERE Time = (SELECT MAX(Time) FROM per_round_data);'
            player_db.cursor().execute(sql_delete)
            player_db.commit()
            print("Time Duplicate Replaced")
            return True

        # TODO: Temp removal while testing
        # if int(last_entry['Round'].iloc[0]) == game_data.map.round:  # checking for duplicates by round number.
        #     return False

    print("Not a Duplicate")
    return True


def insert_round_data(round_data):
    match_stats = round_data.player.match_stats
    player_state = round_data.player.state

    new_round_data = (
        round_data.provider.timestamp, round_data.provider.steamid, round_data.map.name, round_data.map.phase, round_data.map.round,
        round_data.player.name, round_data.player.team, match_stats.kills, match_stats.assists, match_stats.deaths,
        match_stats.mvps, match_stats.score, player_state.equip_value, player_state.round_kills, player_state.round_killhs)

    round_insert_sql = ''' INSERT INTO per_round_data(Time, SteamID, Map, "Map Status", Round, "Player Name", "Player Team",
                                                Kills, Assists, Deaths, MVPs, Score, "Current Equip. Value",
                                                "Round Kills", "Round HS Kills")
                                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    print(new_round_data)
    conn = get_db()
    conn.cursor().execute(round_insert_sql, new_round_data)
    conn.commit()


# ---------------------------

# flask server routes

# the home page, handles frontend user interaction
@cs_py_client.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = str(request.form.get('input'))

        # user chooses to start or end active data collection
        if user_input == 'start' or user_input == 'end':
            cs_py_client.config['STATE'] = True if user_input == 'start' else False

        # user chooses to reset, ending collection for current match
        elif user_input == 'reset':
            send_match_to_remote()

        return redirect(url_for('index'))
    else:
        # updating frontend status of CS-Py
        status = GS_ON if cs_py_client.config['STATE'] else GS_OFF
        return render_template('index.html', status=status)


# route that receives JSON payloads from the game client
# noinspection PyTypeChecker
@cs_py_client.route('/GS', methods=['POST'])
def gamestate_handler():
    if request.is_json and cs_py_client.config['STATE']:
        game_data = GameStatePayload(request.get_json())
        print(game_data.gamestate_code)

        if game_data.gamestate_code == GameStateCode.INVALID:
            return 'Invalid Data Received'
        elif game_data.gamestate_code == GameStateCode.ENDGAME_DIFF_PLAYER:
            print("End Game Payload Received")
            send_match_to_remote()
            return 'Request Received'
        else:
            if check_prev_entries(game_data):  # checks for round AND time duplicate entries.
                insert_round_data(round_data=game_data)
            if game_data.map.phase == 'gameover':  # automatic reset if player was alive by end of game.
                send_match_to_remote()

    return 'Request Received'


@cs_py_client.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'CS-Py is shutting down. You may now close this browser window/tab.'


if __name__ == "__main__":
    # setup
    db_conn = sqlite3.connect(cs_py_client.config['DATABASE'])
    init_table_if_not_exists(db_conn)
    setup_gamestate_cfg()

    # auto-opens browser window to CS-Py frontend
    webbrowser.open_new('http://127.0.0.1:5000/index')
    cs_py_client.run(debug=False, threaded=True)
