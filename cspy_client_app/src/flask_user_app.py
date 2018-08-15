import copy
import json
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
        # print('Auto CFG File Passed')
    except (OSError, shutil.SameFileError):
        # print('Auto CFG File Failed')
        return

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
            send_match_to_remote(get_db(), API_ADDRESS)

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
        game_data = GameStatePayload(copy.deepcopy(request.get_json()))
        json_log = open('../logs/rounds_json.txt', 'a')

        if game_data.gamestate_code == GameStateCode.INVALID:
            round_db.close()
            json_log.close()
            return 'Invalid Data Received'
        elif game_data.gamestate_code == GameStateCode.ENDGAME_DIFF_PLAYER:
            json_log.write('----\n\n')

            send_match_to_remote(round_db, API_ADDRESS)
        else:
            if check_prev_entries(game_data, round_db):  # checks for duplicate entries.
                # saving raw json of accepted data to file
                json_log.write(json.dumps(request.get_json()))
                json_log.write('\n\n')

                insert_round_data(game_data, round_db)
            if game_data.map.phase == 'gameover':  # automatic reset if player was alive by end of game.
                json_log.write('----\n\n')

                send_match_to_remote(round_db, API_ADDRESS)
        round_db.close()
        json_log.close()
        return 'Request Received'
    return 'GS is OFF or non-JSON Received'


@cs_py_client.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'CS-Py is shutting down. You may now close this browser window/tab.'


@cs_py_client.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    # setup
    sql_db = sqlite3.connect(cs_py_client.config['DATABASE'])
    init_table_if_not_exists(sql_db)
    setup_gamestate_cfg()

    # auto-opens browser window to CS-Py frontend
    webbrowser.open_new('http://127.0.0.1:5000')
    cs_py_client.run(debug=False, threaded=True)
