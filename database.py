# standalone helper script, used for testing

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from run import *

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql_query('SELECT * FROM per_round_data;', conn)


df_list = separate(data_df)
map_list = list(set(data_df['Map'].tolist()))
map_list = [x for x in map_list if x != 'RESET POINT']

print(map_list)

round_count_dict = dict.fromkeys(map_list, 0)

for df in df_list:
    print(df)
    for cs_map in map_list:
        round_count_dict[cs_map] += len(df[df['Map'] == cs_map].index)

print(round_count_dict)
