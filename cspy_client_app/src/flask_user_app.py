import os
import shutil
import sqlite3
import sys
import webbrowser
import winreg

from flask import Flask, request, render_template, g, redirect, url_for

from game_state_payload import GameStateCode, GameStatePayload
from sql_data_processing import init_table_if_not_exists, check_prev_entries, insert_round_data, send_match_to_remote

# string constants
GS_CFG_DEST_PATH = '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/gamestate_integration_main.cfg'
GS_CFG_SRC_PATH = '../../required_user_files/gamestate_integration_main.cfg'
GS_ON = 'GS is currently ON'
GS_OFF = 'GS is currently OFF'

# Web address of RESTful API server to which match data is sent
API_ADDRESS = 'http://Parkkeo1.pythonanywhere.com/api/data_receiver'

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

def setup_gamestate_cfg():
    try:
        steam_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Software\Valve\Steam")
        cfg_destination = winreg.QueryValueEx(steam_key, "SteamPath")[0] + GS_CFG_DEST_PATH
        shutil.copyfile(GS_CFG_SRC_PATH, cfg_destination)
        print('Auto CFG File Passed')
    except (OSError, shutil.SameFileError):
        print('Auto CFG File Failed')

# ---------------------------


# flask server routes

# the home page, handles frontend user interaction
@cs_py_client.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = str(request.form.get('input'))

        # user chooses to start or end active data collection
        if user_input == 'start':
            cs_py_client.config['STATE'] = True

        elif user_input == 'stop':
            cs_py_client.config['STATE'] = False

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
        round_db = get_db()
        game_data = GameStatePayload(request.get_json())
        print(game_data.gamestate_code)

        if game_data.gamestate_code == GameStateCode.INVALID:
            return 'Invalid Data Received'
        elif game_data.gamestate_code == GameStateCode.ENDGAME_DIFF_PLAYER:
            print("End Game Payload Received")
            send_match_to_remote(round_db, API_ADDRESS)
            return 'Request Received'
        else:
            if check_prev_entries(game_data, round_db):  # checks for time duplicate entries.
                insert_round_data(game_data, round_db)
                if game_data.map.phase == 'gameover':  # automatic reset if player was alive by end of game.
                    send_match_to_remote(round_db, API_ADDRESS)
        round_db.close()
        return 'Request Received'
    return 'GS is OFF or non-JSON Received'


@cs_py_client.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'CS-Py is shutting down. You may now close this browser window/tab.'


if __name__ == "__main__":
    # setup
    sql_db = sqlite3.connect(cs_py_client.config['DATABASE'])
    init_table_if_not_exists(sql_db)
    setup_gamestate_cfg()

    # redirecting stdout for logging purposes
    sys.stdout = open('server_log.txt', 'a')
    print('---')

    # auto-opens browser window to CS-Py frontend
    webbrowser.open_new('http://127.0.0.1:5000')
    cs_py_client.run(debug=False, threaded=True)
