# standalone helper script, used for testing

import json
import requests
import sqlite3

import pandas as pd

from match_analysis import MatchAnalysis

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
#
# r1 = requests.post('http://127.0.0.1:5001/api/data_receiver', json=data)
# print(r1.status_code)
# print(r1.headers)
# print(r1.text)
#
# r2 = requests.post('http://127.0.0.1:5001/api/data_receiver', json=match_data.__dict__)
# print(r2.status_code)
# print(r2.headers)
# print(r2.text)

from enum import Enum


class GameStateCode(Enum):
    INVALID = -1
    ENDGAME_DIFF_PLAYER = 0
    ALIVE_END_ROUND = 1
    DEAD_MID_ROUND = 2
