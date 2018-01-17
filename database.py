# standalone helper script, used for testing

import sqlite3
import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import time
from run import *
# import requests
import json
from pprint import pprint

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
# cur = conn.cursor()
# cur.execute("select * from per_round_data;")
# results = cur.fetchall()
# pprint(results)
data_df = pd.read_sql('SELECT * FROM per_round_data', conn)

print(data_df)

# print(type(data_df.iloc[-1]['Kills']))

# last_df = data_df.iloc[-1]
# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)
#
# data = json.load(open('test.json'))
#
# r = requests.post("http://127.0.0.1:5000/GS", json=data, headers={'content-type': 'application/json'})
# print(r.status_code, r.reason)
#
# result_df = pd.read_sql('SELECT * FROM per_round_data', conn)
# print(result_df)


# data_df.to_csv('player_data.txt', sep='\t', index=False)
