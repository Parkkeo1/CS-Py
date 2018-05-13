from flask import Flask, request, render_template, g, session, redirect, url_for

# database management
import sqlite3
import os

# cfg file setup
import winreg as registry
from shutil import copyfile

# data processing
import pandas as pd

# string constants
GS_CFG_DEST_PATH = '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg/gamestate_integration_main.cfg'
GS_CFG_SRC_PATH = 'req_files/gamestate_integration_main.cfg'
GS_ON = 'GS is currently ON'
GS_OFF = 'GS is currently OFF'


cs_py = Flask(__name__)
cs_py.config['SECRET_KEY'] = 'half-life 3 confirmed'
cs_py.config['DATABASE'] = os.path.join(cs_py.root_path, 'data/player_data.db')
cs_py.config['STATE'] = False

# ---------------------------

# database connection handling
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(cs_py.config['DATABASE'])
    return g.sqlite_db

@cs_py.teardown_appcontext
def close_db():
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
    steam_key = registry.CreateKey(registry.HKEY_CURRENT_USER, "Software\Valve\Steam")
    cfg_destination = registry.QueryValueEx(steam_key, "SteamPath")[0] + GS_CFG_DEST_PATH
    copyfile(GS_CFG_SRC_PATH, cfg_destination)

def init_table_if_not_exists(sql_db):
    zero_df = pd.DataFrame(columns=['Time', 'Map', 'Map Status', 'Player Name', 'Player Team',
                                    'Kills', 'Assists', 'Deaths', 'MVPs', 'Score',
                                    'Current Equip. Value', 'Round Kills', 'Round HS Kills'])
    zero_df.to_sql("per_round_data", sql_db, if_exists="fail", index=False)

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
            pass # TODO: Handle resetting.
        else:
            pass # TODO: Handle processing user queries for data

    else:
        # updating frontend status of CS-Py
        status = GS_ON if cs_py.config['STATE'] else GS_OFF
        return render_template('index.html', status=status)