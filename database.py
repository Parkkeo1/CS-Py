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
data_df = data_df.iloc[39:]

# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

ct_df = data_df[(data_df['Player Team'] == 'CT')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'T'))]
t_df = data_df[(data_df['Player Team'] == 'T')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'CT'))]
# current ideas for CT vs T: mean equip. value, mean # of kills per round (# of rounds = length of dataframe)

print(ct_df)
print('\n')
print(t_df)
print('\n')

ct_kills_sum = ct_df['Round Kills'].sum()
ct_round_count = len(ct_df.index)
ct_kills_per_round = round(ct_kills_sum / ct_round_count, 2)
t_kills_sum = t_df['Round Kills'].sum()
t_round_count = len(t_df.index)
t_kills_per_round = round(t_kills_sum / t_round_count, 2)
print(ct_kills_per_round)
print(t_kills_per_round)

