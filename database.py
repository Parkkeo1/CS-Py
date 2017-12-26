import sqlite3
import pandas as pd

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('legacy/player_data.db')
df = pd.read_sql('select * from per_round_data;', conn)
print(df)
