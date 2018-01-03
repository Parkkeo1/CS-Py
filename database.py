# standalone helper script, used for testing

import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
from run import *

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data', conn)
# data_df = data_df.iloc[39:]
data_df = data_df[data_df['Time'] >= int(time.time()) - 604800]

df_list = remove_empty(separate(data_df))
print(data_df)
print('\n')

pistol_df = pd.DataFrame()
for df in df_list:
    df = df.reset_index(drop=True)
    try:
        temp_df = df.iloc[[0, 15]]
        pistol_df = pistol_df.append(temp_df, ignore_index=True)
    except:
        continue

pistol_df = pistol_df[(pistol_df['Current Equip. Value'] <= 850) & (pistol_df['Current Equip. Value'] > 0)]
ct_pistol_df = pistol_df[(pistol_df['Player Team'] == 'CT')].reset_index(drop=True)
t_pistol_df = pistol_df[(pistol_df['Player Team'] == 'T')].reset_index(drop=True)
print(pistol_df)
print('\n')
print(ct_pistol_df)
print('\n')
print(t_pistol_df)
print('\n')
print(hsr(pistol_df))
print(kpr(pistol_df))
print(pistol_k_ratio(pistol_df))
print('\n')
print(hsr(ct_pistol_df))
print(kpr(ct_pistol_df))
print(pistol_k_ratio(ct_pistol_df))
print('\n')
print(hsr(t_pistol_df))
print(kpr(t_pistol_df))
print(pistol_k_ratio(t_pistol_df))
print('\n')


# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

# ct_df = data_df[(data_df['Player Team'] == 'CT')].reset_index(drop=True)
# t_df = data_df[(data_df['Player Team'] == 'T')].reset_index(drop=True)


# current ideas for CT vs T: mean equip. value, mean # of kills per round (# of rounds = length of dataframe)
# maybe have tabs/navs or carousel slides for tables and graphs separately?
# tabs for tables and carousel for graphs?

