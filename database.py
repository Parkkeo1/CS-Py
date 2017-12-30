# standalone helper script, used for testing

import sqlite3
import pandas as pd
import math

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
# data_df = data_df.drop([x for x in range(20, 49)])
# data_df = data_df.reset_index(drop=True)
# # print(data_df)
# # print('\n')

df_list = []
idx_range = sorted(set([0] + data_df[data_df['Map Status'] == 'gameover'].index.tolist() + [data_df.index[-1]]))
print(idx_range)

for i in range(len(idx_range) - 1):
    if i == 0:
        df_list.append(data_df.iloc[idx_range[i]:idx_range[i + 1] + 1])
    else:
        df_list.append(data_df.iloc[idx_range[i] + 1:idx_range[i + 1] + 1])

if len(idx_range) == 1:
    df_list = [data_df]

total_kills = 0
total_assists = 0
total_deaths = 0

for match_df in df_list:
    print(match_df)
    print('\n')
    if match_df.iloc[-1]['Player Name'] is None and match_df.iloc[-1]['Player Team'] is None and math.isnan(match_df.iloc[-1]['Score']):
        try:
            max_df = match_df.iloc[-2]
        except IndexError:
            max_df = match_df.iloc[-1].fillna(0)
    else:
        max_df = match_df.iloc[-1]
    total_kills += int(max_df['Kills'])
    total_assists += int(max_df['Assists'])
    total_deaths += int(max_df['Deaths'])

print('\n')
print(total_kills)
print(total_assists)
print(total_deaths)

total_kdr = float(round(total_kills / total_deaths, 3))
total_kda = float(round((total_kills + total_assists) / total_deaths, 3))
print('KDR: %s' % total_kdr)
print('KDA: %s' % total_kda)


