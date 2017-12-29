# standalone helper script, used for testing

import sqlite3
import pandas as pd
import time

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)

df_list = []
idx_range = sorted(set([0] + data_df[data_df['Map Status'] == 'gameover'].index.tolist() + [data_df.index[-1]]))

print(idx_range)

df_list = []
idx_range = sorted(set([0] + data_df[data_df['Map Status'] == 'gameover'].index.tolist() + [data_df.index[-1]]))

for i in range(len(idx_range) - 1):
    if i == 0:
        df_list.append(data_df.iloc[idx_range[i]:idx_range[i + 1] + 1])
    else:
        df_list.append(data_df.iloc[idx_range[i] + 1:idx_range[i + 1] + 1])

print(df_list)
