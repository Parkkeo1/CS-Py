from flask import Flask, request, render_template, g, session, redirect, url_for

# database management
import sqlite3
import os

# cfg file setup
import winreg as registry
from shutil import copyfile, SameFileError

# data processing
from payload import GameStateCode, Payload
import pandas as pd
import time

# string constants
GS_CFG_DEST_PATH = '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/gamestate_integration_main.cfg'
GS_CFG_SRC_PATH = 'req_files/gamestate_integration_main.cfg'
GS_ON = 'GS is currently ON'
GS_OFF = 'GS is currently OFF'

# the CS-Py Flask object
cs_py = Flask(__name__)
cs_py.config['SECRET_KEY'] = 'half-life 3 confirmed'
cs_py.config['DATABASE'] = os.path.join(cs_py.root_path, 'player_data.db')
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
    except (OSError, SameFileError):
        print('auto cfg failed')


def init_table_if_not_exists(sql_db):
    try:
        zero_df = pd.DataFrame(columns=['Time', 'Map', 'Map Status', 'Player Name', 'Player Team',
                                        'Kills', 'Assists', 'Deaths', 'MVPs', 'Score',
                                        'Current Equip. Value', 'Round Kills', 'Round HS Kills'])
        zero_df.to_sql("per_round_data", sql_db, if_exists="fail", index=False)
        print('table created')
    except ValueError:
        print('table already exists')

# ---------------------------

# utility methods for processing in flask routes

# handles resetting current match
def reset_match():
    blank_df = pd.DataFrame({
        'Time': [int(time.time())],
        'Map': ['RESET POINT'],
        'Map Status': ['gameover'],
    })
    blank_df = blank_df[['Time', 'Map', 'Map Status']]

    player_db = get_db()
    # TODO: Ensure types?
    last_entry = pd.read_sql_query('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', player_db)

    if len(last_entry.index) > 0 and last_entry.iloc[0]['Map Status'] != 'gameover':
        blank_df.to_sql("per_round_data", player_db, if_exists="append", index=False)


# handles calculating user's requested data results
def query_for_results(user_input):
    player_db = get_db()

    # TODO: Import and refactor run.py functions
    # if user_input == 'current match':
    #     return query_current_match(player_db)
    # elif user_input == 'last match':
    #     return query_last_match(player_db)
    # else:
    #     return query_on_time(player_db, user_input)
    return 0


# checks previous entries in database to make sure there are no duplicates or erroneous data
def check_prev_entries(game_data):
    player_db = get_db()
    last_entry = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', player_db)

    if game_data.gamestate_code == GameStateCode.ENDGAME:
        # makes sure that, if we are attempting to enter in an endgame-stats_df,
        # check that the current last entry in the table is not also a 'gameover' entry.
        # This prevents having two 'gameover' events in a row, where the latter is a None/NaN entry.
        return len(last_entry.index) == 0 or last_entry.iloc[0]['Map Status'] != 'gameover'
    else:
        # time difference is 1 second or less
        if len(last_entry.index) != 0 and abs(int(game_data.client['timestamp'] - last_entry.iloc[0]['Time'])) <= 1:
            sql_delete = 'DELETE FROM per_round_data WHERE Time = (SELECT MAX(Time) FROM per_round_data);'
            player_db.cursor().execute(sql_delete)
        return True

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
            reset_match()
            return redirect(url_for('index'))
        # user chose to query for performance data
        else:
            session['result'] = query_for_results(str(request.form.get('choose')))
            session.modified = True
            return redirect(url_for('results'))
    else:
        # updating frontend status of CS-Py
        status = GS_ON if cs_py.config['STATE'] else GS_OFF
        return render_template('index.html', status=status)


# route that receives JSON payloads from the game client
@cs_py.route('/GS', methods=['POST'])
def gamestate_handler():
    if request.is_json and cs_py.config['STATE']:
        game_data = Payload(request.get_json())
        gs_code = game_data.gamestate_code

        if gs_code == GameStateCode.INVALID:
            return 'Invalid Data Received'
        else:
            if check_prev_entries(game_data):
                game_data.insert_data_to_db(get_db())

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