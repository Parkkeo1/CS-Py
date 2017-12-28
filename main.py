from flask import Flask, request, render_template, g, session, redirect, url_for
from run import *
import os
import sqlite3
import pandas as pd
import webbrowser


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


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# the frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        starter = str(request.form.get('starter'))
        ender = str(request.form.get('ender'))
        if starter == 'starter':
            app.config['STARTER'] = True
            return redirect(url_for('index'))
        else:
            if ender == 'ender':
                app.config['STARTER'] = False
                return redirect(url_for('index'))
            else:
                conn = get_db()
                value = str(request.form.get('choose'))
                if value == 'last match':
                    result = query_db_match(conn)
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


@app.route('/results')
def results():
    result = session['result']
    print(result)
    return render_template('results.html', result=result)


@app.route('/docs')
def docs():
    return render_template('docs.html')


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
            stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
            clean_db(conn)
            print(pd.read_sql('select * from per_round_data;', conn))
    print(app.config['STARTER'])
    return 'JSON Posted'


if __name__ == "__main__":
    webbrowser.open_new('http://127.0.0.1:5000')  # for deployment
    app.config['STARTER'] = False  # starter variable
    app.run(debug=False)
