# standalone helper script, used for testing

import sqlite3
import pandas as pd
import time

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
# lower = int(time.time()) - 86400
#
# data_df = data_df[data_df['Time'] >= lower]
#
# total_kills = data_df['Round Kills'].sum()
# total_hs = data_df['Round HS Kills'].sum()
#
# hsr = float(round(total_hs / total_kills, 2))
print(data_df)

