# standalone helper script, used for testing

import sqlite3
import pandas as pd
import math

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql_query('SELECT * FROM per_round_data;', conn)
# data_df = pd.read_sql_query('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', conn)
# data_df = data_df.drop([x for x in range(20, 49)])
# data_df = data_df.reset_index(drop=True)
print(data_df)

# df_list = []
# idx_range = sorted(set([0] + data_df[data_df['Map Status'] == 'gameover'].index.tolist() + [data_df.index[-1]]))
# print(idx_range)
#
# for i in range(len(idx_range) - 1):
#     if i == 0:
#         df_list.append(data_df.iloc[idx_range[i]:idx_range[i + 1] + 1])
#     else:
#         df_list.append(data_df.iloc[idx_range[i] + 1:idx_range[i + 1] + 1])
#
# if len(idx_range) == 1:
#     df_list = [data_df]

# total_kills = 0
# total_assists = 0
# total_deaths = 0
# kas_counter = 0
# round_counter = 0
#
# for match_df in df_list:
#     for i in range(len(match_df.index)):
#         if match_df.iloc[i]['Player Name'] is None and match_df.iloc[i]['Player Team'] is None:  # check if row is None and NaN values
#             continue
#         else:
#             if i == 0:
#                 if match_df.iloc[i]['Kills'] > 0 or match_df.iloc[i]['Assists'] > 0 or match_df.iloc[i]['Deaths'] == 0:
#                     kas_counter += 1
#                 round_counter += 1
#             else:
#                 if match_df.iloc[i]['Kills'] > match_df.iloc[i - 1]['Kills'] or match_df.iloc[i]['Assists'] > match_df.iloc[i - 1]['Assists'] or match_df.iloc[i]['Deaths'] == match_df.iloc[i - 1]['Deaths']:
#                     kas_counter += 1
#                 round_counter += 1
#
# print(kas_counter)
# print(round_counter)

#     total_kills += int(max_df['Kills'])
#     total_assists += int(max_df['Assists'])
#     total_deaths += int(max_df['Deaths'])
#
# print('\n')
# print(total_kills)
# print(total_assists)
# print(total_deaths)
#
# total_kdr = float(round(total_kills / total_deaths, 3))
# total_kda = float(round((total_kills + total_assists) / total_deaths, 3))
# print('KDR: %s' % total_kdr)
# print('KDA: %s' % total_kda)


