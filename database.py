# standalone helper script, used for testing

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from run import *

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data', conn)

# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

print(data_df)

# df_list = separate(data_df)
# map_list = list(set(data_df['Map'].tolist()))
# map_list = [x for x in map_list if x != 'RESET POINT']
#
# round_count_dict = dict.fromkeys(map_list, 0)
#
# for df in df_list:
#     print(df)
#     for cs_map in map_list:
#         round_count_dict[cs_map] += len(df[df['Map'] == cs_map].index)
#
# print(round_count_dict)
#
# fig = plt.figure()
# plt.bar(range(len(round_count_dict)), list(round_count_dict.values()), align='center')
# plt.xticks(range(len(round_count_dict)), list(round_count_dict.keys()))
# fig.suptitle('Rounds Played by Map')
# plt.xlabel('Map')
# plt.ylabel('Count')
#
# plt.savefig('images/rounds_per_map.png')
