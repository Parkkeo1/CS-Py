from flask import Flask, request, render_template, g, session, redirect, url_for
from run import *
import os
import sqlite3
import pandas as pd
import webbrowser
import time
import winreg as registry
from shutil import copyfile


app = Flask(__name__)
app.config['SECRET_KEY'] = 'half-life 3 confirmed'
app.config['DATABASE'] = os.path.join(app.root_path, 'player_data.db')


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def reset_match():
    data_df = pd.DataFrame({
        'Time': [int(time.time())],
        'Map': ['RESET POINT'],
        'Map Status': ['gameover'],
    })

    data_df = data_df[['Time', 'Map', 'Map Status']]

    return data_df


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def setup_gamestate_cfg():
    key = registry.CreateKey(registry.HKEY_CURRENT_USER, "Software\Valve\Steam")
    steam_path = registry.QueryValueEx(key, "SteamPath")[0]

    steam_path = steam_path + '/steamapps/common/Counter-Strike Global Offensive/csgo/cfg'

    src = 'gamestate_integration_main.cfg'
    dst = steam_path + '/gamestate_integration_main.cfg'

    copyfile(src, dst)


def table_exists(con):
    zero_df = pd.DataFrame(columns=['Time', 'Map', 'Map Status', 'Player Name', 'Player Team',
                                    'Kills', 'Assists', 'Deaths', 'MVPs', 'Score',
                                    'Current Equip. Value', 'Round Kills', 'Round HS Kills'])
    zero_df.to_sql("per_round_data", con, if_exists="fail", index=False)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# the frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        post_input = str(request.form.get('input'))
        if post_input == 'starter':
            app.config['STARTER'] = True
            return redirect(url_for('index'))
        else:
            if post_input == 'ender':
                app.config['STARTER'] = False
                return redirect(url_for('index'))
            else:
                if post_input == 'reset':
                    conn = get_db()
                    reset_df = reset_match()
                    last_df = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', conn)
                    if last_df.iloc[0]['Map Status'] != 'gameover':
                        reset_df.to_sql("per_round_data", conn, if_exists="append", index=False)
                    return redirect(url_for('index'))
                else:
                    conn = get_db()
                    value = str(request.form.get('choose'))
                    if value == 'last match':
                        result = query_db_match(conn)
                    else:
                        if value == 'current match':
                            result = query_db_current(conn)
                        else:
                            result = query_db_time(conn, value)
                    session['result'] = result
                    session.modified = True
                    return redirect(url_for('results'))
    else:
        if app.config['STARTER']:
            status = 'GS is currently ON'
        else:
            status = 'GS is currently OFF'
        return render_template('index.html', status=status)


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'CS-Py is shutting down. You may now close this browser window/tab.'


@app.route('/results')
def results():
    result = session['result']
    return render_template('results.html', result=result)


# backend POST request handler
@app.route('/GS', methods=['POST'])
def GSHandler():
    if request.is_json and app.config['STARTER']:
        payload = request.get_json()
        conn = get_db()
        counter = check_payload(payload)
        if counter == 1 or counter == 2:
            if counter == 1:
                stats_df = parse_payload(payload)
            else:
                stats_df = endgame_payload(payload)
            print(stats_df)
            print('\n')
            last_df = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', conn)
            if counter == 2:
                # makes sure that, if we are attempting to enter in an endgame-stats_df,
                # check that the current last entry in the table is not also a 'gameover' entry.
                # This prevents having two 'gameover' events in a row, where the latter is a None/NaN entry.
                if len(last_df.index) == 0 or last_df.iloc[0]['Map Status'] != 'gameover':
                    stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
                    clean_db(conn)
                    print('successful 2')
            else:  # if counter == 1; parse payload
                if len(last_df.index) == 0 or abs(int(stats_df.iloc[0]['Time']) - int(last_df.iloc[0]['Time'])) > 1:
                    stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
                    clean_db(conn)
                    print('successful 1')
                else:  # time difference is 1 second or less
                    # TODO: test this fix
                    total_df = pd.read_sql('SELECT * FROM per_round_data', conn)
                    new_df = total_df.iloc[:-1]  # excluding last entry AKA last_df
                    new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

                    # Inserting new entry, stats_df
                    stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
                    clean_db(conn)
                    print('successful, last_df replaced')

                    # To prevent cases such as this:
                    #
                    # 52  1515805253  de_cache       live   dumby  T  23.0  3.0  17.0  3.0  56.0  5000.0  1.0  0.0
                    # 53  1515805254  de_cache   gameover   dumby  T  23.0  4.0  17.0  3.0  57.0  5000.0  1.0  0.0

    return 'JSON Posted'


@app.after_request  # temp fix for matplotlib plot images not refreshing unless page is manually refreshed.
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == "__main__":
    connn = sqlite3.connect(app.config['DATABASE'])
    try:
        table_exists(connn)
        print('table created')
    except ValueError:
        print('table already exists')
    try:
        setup_gamestate_cfg()
    except:
        print('auto cfg failed')
    webbrowser.open_new('http://127.0.0.1:5000')  # for deployment
    app.config['STARTER'] = False  # starter variable
    app.run(debug=False)
