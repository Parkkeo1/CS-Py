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

# sys.stdout = open('testing_log.txt', 'a')
# print('\n')
#
# # valid user 1
# r1 = requests.get('http://127.0.0.1:5001/api/user_data/76561198268849559')
# pprint(r1.json())
#
# # valid user 2
# r2 = requests.get('http://127.0.0.1:5001/api/user_data/76561198158189084')
# pprint(r2.json())
#
# # invalid user
# r3 = requests.get('http://127.0.0.1:5001/api/user_data/12345')
# pprint(r3.json())

d = json.loads('{"provider": {"name": "Counter-Strike: Global Offensive", "appid": 730, "version": 13647, "steamid": "76561198268849559", "timestamp": 1534361906}, "map": {"mode": "competitive", "name": "de_overpass", "phase": "gameover", "round": 26, "team_ct": {"score": 15, "timeouts_remaining": 1, "matches_won_this_series": 0}, "team_t": {"score": 10, "timeouts_remaining": 1, "matches_won_this_series": 0}, "num_matches_to_win_series": 0, "current_spectators": 0, "souvenirs_total": 0}, "round": {"phase": "over", "win_team": "CT", "bomb": "defused"}, "player": {"steamid": "76561198268849559", "name": "post office malone", "observer_slot": 6, "team": "CT", "activity": "playing", "state": {"health": 100, "armor": 100, "helmet": false, "flashed": 0, "smoked": 0, "burning": 0, "money": 4550, "round_kills": 2, "round_killhs": 0, "equip_value": 3550}, "match_stats": {"kills": 29, "assists": 8, "deaths": 16, "mvps": 6, "score": 79}}, "previously": {"map": {"phase": "live", "round": 25}, "round": {"phase": "live", "bomb": "planted"}, "player": {"observer_slot": 5, "state": {"money": 750}, "match_stats": {"mvps": 5, "score": 77}}}, "added": {"round": {"win_team": true}}}')
r = requests.post('http://127.0.0.1:5000/GS', json=d)




