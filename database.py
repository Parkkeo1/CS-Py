# standalone helper script, used for testing

import sqlite3
import pandas as pd
import time

pd.options.display.max_rows = 999
pd.set_option('display.width', 1000)

conn = sqlite3.connect('player_data.db')
data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
# data_df = data_df.drop_duplicates(subset=['Map', 'Map Status', 'Player Name', 'Player Team', 'Kills', 'Assists',
#                                             'Deaths', 'MVPs', 'Score', 'Current Equip. Value', 'Round Kills',
#                                             'Round HS Kills'])
# data_df.to_sql("per_round_data", conn, if_exists="replace", index=False)

print(data_df)

# # selecting last match
# idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()[-2:]
# length = len(idx_range)
# if length < 2:
#     if length == 1:  # there has only been one 'gameover' event.
#         data_df = data_df.iloc[:idx_range[0] + 1]
#     else:
#         pass  # return query_db_time(conn, 'lifetime') because there have been no gameovers ever.
# else:
#     data_df = data_df.iloc[idx_range[0] + 1:idx_range[1] + 1]
#     print(data_df)
#     print(int(data_df['Current Equip. Value'].mean()))
# idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()
# result = {}
# if not idx_range:
#     pass
# else:
#     idx = idx_range[-1]
#     data_df = data_df.iloc[idx + 1:]
#     if data_df.empty:  # if there haven't been any rounds played since the last complete match.
#         result['hsr'] = 0
#         result['equip'] = 0
#         result['correl'] = 0
#         result['timeframe'] = 'Current Match'
#
#         print(result)
#     else:
#         result['hsr'] = hsr(data_df)
#         result['equip'] = int(data_df['Current Equip. Value'].mean())
#         result['correl'] = correl(data_df)
#         result['timeframe'] = 'Current Match'
#
#         print(result)
