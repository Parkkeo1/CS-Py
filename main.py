from flask import Flask, request, render_template, session, g
from run import check_payload, parse_payload
import os
import sqlite3
import pandas as pd


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


# the to-be frontend
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# backend POST request handler
@app.route('/GS', methods=['POST'])
def GSHandler():
    if request.is_json:
        payload = request.get_json()
        conn = get_db()
        if check_payload(payload):
            stats_df = parse_payload(payload)
            stats_df.to_sql("per_round_data", conn, if_exists="append")
            print('this dataframe contains per-round values')
            print(pd.read_sql_query('select * from per_round_data;', conn))
            if str(stats_df.iloc[0]['Map Status']) == 'gameover':
                stats_df.to_sql("per_map_data", conn, if_exists="append")
                print('this dataframe also contains overall match values')
                print(pd.read_sql_query('select * from per_map_data;', conn))

    return 'JSON Posted'


if __name__ == "__main__":
    app.run(debug=True)
