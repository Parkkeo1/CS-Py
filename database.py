# standalone helper script, used for testing

import sqlite3
import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import time
# from run import *
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

print(type(data_df.iloc[0]['Kills']))

# data_df['Time'] = pd.to_numeric(data_df['Time'], errors='coerce')
# data_df['Kills'] = pd.to_numeric(data_df['Kills'], errors='coerce')
# data_df['Assists'] = pd.to_numeric(data_df['Assists'], errors='coerce')
# data_df['Deaths'] = pd.to_numeric(data_df['Deaths'], errors='coerce')
# data_df['MVPs'] = pd.to_numeric(data_df['MVPs'], errors='coerce')
# data_df['Score'] = pd.to_numeric(data_df['Score'], errors='coerce')
# data_df['Current Equip. Value'] = pd.to_numeric(data_df['Current Equip. Value'], errors='coerce')
# data_df['Round Kills'] = pd.to_numeric(data_df['Round Kills'], errors='coerce')
# data_df['Round HS Kills'] = pd.to_numeric(data_df['Round HS Kills'], errors='coerce')
#
# data_df.to_sql("per_round_data", conn, if_exists="replace", index=False)


# # last_df = data_df.iloc[-1]
# # new_df = data_df.iloc[:-1]
# # new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)
#
# data = json.load(open('test.json'))
#
# r = requests.post("http://127.0.0.1:5000/GS", json=data, headers={'content-type': 'application/json'})
# print(r.status_code, r.reason)
#
# result_df = pd.read_sql('SELECT * FROM per_round_data', conn)
# print(result_df)

# Method 2 for fixing edge case issue.
# remove_list = []
# for i in range(1, len(data_df.index) - 1):
#     time1 = data_df.iloc[i]['Time']
#     time2 = data_df.iloc[i + 1]['Time']
#     check1 = data_df.iloc[i]['Player Name'] is not None
#     check2 = data_df.iloc[i + 1]['Player Name'] is not None
#     if abs(time2 - time1) <= 2 and check1 and check2 and data_df.iloc[i]['Map Status'] != 'gameover':
#         remove_list.append(i)
#
# data_df.drop(data_df.index[remove_list], inplace=True)
# data_df.reset_index(drop=True, inplace=True)
# print(data_df)


# data_df.to_csv('player_data.txt', sep='\t', index=False)

# ct_df = data_df[(data_df['Player Team'] == 'CT')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'T'))]
# t_df = data_df[(data_df['Player Team'] == 'T')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'CT'))]

# ct_kills_sum = ct_df['Round Kills'].sum()
# ct_hs_sum = ct_df['Round HS Kills'].sum()
# ct_round_count = len(ct_df.index)
# ct_kills_per_round = round(ct_kills_sum / ct_round_count, 2)
# ct_equip_value = int(ct_df['Current Equip. Value'].mean())
# ct_hsr = round(ct_hs_sum / ct_kills_sum, 2)
#
# t_kills_sum = t_df['Round Kills'].sum()
# t_hs_sum = t_df['Round HS Kills'].sum()
# t_round_count = len(t_df.index)
# t_kills_per_round = round(t_kills_sum / t_round_count, 2)
# t_equip_value = int(t_df['Current Equip. Value'].mean())
# t_hsr = round(t_hs_sum / t_kills_sum, 2)

# multi_list = [0, 1, 2, 3, 4, 5]
#
# multi_count_dict = {count: len(data_df[data_df['Round Kills'] == count]) for count in multi_list}

