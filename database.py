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
# data_df = data_df[data_df['Time'] >= int(time.time()) - 604800]

print(data_df)
multi_list = [0, 1, 2, 3, 4, 5]

multi_count_dict = {count: len(data_df[data_df['Round Kills'] == count]) for count in multi_list}
print(multi_count_dict)

