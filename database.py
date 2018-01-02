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
# data_df = data_df.iloc[39:]

# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

ct_df = data_df[(data_df['Player Team'] == 'CT')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'T'))]
t_df = data_df[(data_df['Player Team'] == 'T')].reset_index(drop=True)  # | ((data_df['Map Status'] == 'gameover') & (data_df['Player Team'] != 'CT'))]
# current ideas for CT vs T: mean equip. value, mean # of kills per round (# of rounds = length of dataframe)
# maybe have tabs/navs or carousel slides for tables and graphs separately?
# tabs for tables and carousel for graphs?

print(ct_df)
print('\n')
print(t_df)
print('\n')

ct_kills_sum = ct_df['Round Kills'].sum()
ct_hs_sum = ct_df['Round HS Kills'].sum()
ct_round_count = len(ct_df.index)
ct_kills_per_round = round(ct_kills_sum / ct_round_count, 2)
ct_equip_value = int(ct_df['Current Equip. Value'].mean())
ct_hsr = round(ct_hs_sum / ct_kills_sum, 2)

t_kills_sum = t_df['Round Kills'].sum()
t_hs_sum = t_df['Round HS Kills'].sum()
t_round_count = len(t_df.index)
t_kills_per_round = round(t_kills_sum / t_round_count, 2)
t_equip_value = int(t_df['Current Equip. Value'].mean())
t_hsr = round(t_hs_sum / t_kills_sum, 2)

print(ct_kills_per_round)
print(t_kills_per_round)
print('\n')
print(ct_equip_value)
print(t_equip_value)
print('\n')
print(ct_hsr)
print(t_hsr)
print('\n')


