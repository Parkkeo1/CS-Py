import pandas as pd
import sqlite3

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

conn = sqlite3.connect('users_and_matches.db')
all_matches_df = pd.read_sql('SELECT * FROM all_matches;', conn)
all_users_df = pd.read_sql('SELECT * FROM all_users;', conn)

print(all_users_df, file=open('all_data.txt', 'w'))
print('\n', file=open('all_data.txt', 'a'))
print(all_matches_df, file=open('all_data.txt', 'a'))

# Deletes Last Entered Entry
# cur = conn.cursor()
# cur.execute('DELETE FROM all_matches WHERE Match_ID = (SELECT MAX(Match_ID) FROM all_matches)')
# conn.commit()
