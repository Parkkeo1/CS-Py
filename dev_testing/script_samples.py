# standalone helper script, used for testing

import sys
import json
import requests
import sqlite3
from pprint import pprint
import pandas as pd

# # testing with round_data json file instead of match_data
# with open('dead_midround_data.json') as json_file:
#     data = json.load(json_file)
#
# # backup
# # data2 = {'steamid': 76561198158189084, 'start': 1515881036, 'end': 1515881038, 'round_count': 2, 'map_name': 'de_cache', 'rating1': 0, 'ct_rating1': 0, 't_rating1': 0, 'hsr': 1.0, 'ct_hsr': 1.0, 't_hsr': 0, 'mdc': 0, 'ct_mdc': 0, 't_mdc': 0, 'kpr': 1.0, 'ct_kpr': 1.0, 't_kpr': 0, 'kas': 0, 'ct_kas': 0, 't_kas': 0, 'kdr': 1.5, 'ct_kdr': 1.5, 't_kdr': 0, 'kda': 2.5, 'ct_kda': 2.5, 't_kda': 0, 'mean_equip': 850, 'ct_mean_equip': 850, 't_mean_equip': 0}
#
# round_db = sqlite3.connect('../cspy_client_app/rounds_data.db')
# data_for_match_df = pd.read_sql('SELECT * FROM per_round_data;', round_db)
#
# match_data = MatchAnalysis(data_for_match_df)
# del match_data.data_frame
# print(match_data.__dict__)

sys.stdout = open('testing_log.txt', 'a')
print('\n')

# valid user 1
r1 = requests.get('http://127.0.0.1:5001/api/user_data/76561198268849559')
pprint(r1.json())

# valid user 2
r2 = requests.get('http://127.0.0.1:5001/api/user_data/76561198158189084')
pprint(r2.json())

# invalid user
r3 = requests.get('http://127.0.0.1:5001/api/user_data/12345')
pprint(r3.json())




