# standalone helper script, used for testing

import json
import sqlite3
import pandas as pd
from pprint import pprint
import numpy as np
from match_analysis import MatchAnalysis

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

round_db = sqlite3.connect('../player_data.db')
data_for_match_df = pd.read_sql('SELECT * FROM per_round_data;', round_db)

match_data = MatchAnalysis(data_for_match_df)
del match_data.data_frame
match_data_dict = match_data.__dict__
print(match_data_dict)

match_json = json.dumps(match_data_dict)
print(match_json)
print(type(match_json))
