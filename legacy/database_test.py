# standalone helper script, used for testing

import sqlite3
import pandas as pd
import math

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)


for count in range(1, 6):
    name = 'player_data_test%s.db' % count
    conn = sqlite3.connect(name)
    data_df = pd.read_sql_query('SELECT * FROM per_round_data;', conn)
    data_df.to_csv('player_data_' + str(count) + '.txt', sep='\t', index=False)

# data_df = pd.read_sql_query('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', conn)
# data_df = data_df.drop([x for x in range(20, 49)])
# data_df = data_df.reset_index(drop=True)
