# standalone helper script, used for testing

import sqlite3
import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import time
from run import *
# import requests
import json
from pprint import pprint

# pd.options.display.max_rows = 999
# pd.set_option('display.width', 1000)
#
# conn = sqlite3.connect('player_data.db')
# # cur = conn.cursor()
# # cur.execute("select * from per_round_data;")
# # results = cur.fetchall()
# # pprint(results)
# data_df = pd.read_sql('SELECT * FROM per_round_data', conn)
#
# print(data_df)

# print(type(data_df.iloc[-1]['Kills']))

# last_df = data_df.iloc[-1]
# new_df = data_df.iloc[:-1]
# new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)
#
# data = json.load(open('sample_data.json'))
#
# r = requests.post("http://127.0.0.1:5000/GS", json=data, headers={'content-type': 'application/json'})
# print(r.status_code, r.reason)
#
# result_df = pd.read_sql('SELECT * FROM per_round_data', conn)
# print(result_df)


# data_df.to_csv('player_data.txt', sep='\t', index=False)

class TestPayload(object):
    def __init__(self, payload):
        self.__dict__ = payload

def get_properties_list(obj):
    return [x for x in dir(obj) if not x.startswith('__') and not callable(getattr(obj, x))]

def load_nested_data(root_payload):
    for prop in get_properties_list(root_payload):
        if type(root_payload.__getattribute__(prop)) is dict:
            subsection = TestPayload(root_payload.__getattribute__(prop))
            root_payload.__setattr__(prop, subsection)
            load_nested_data(subsection)

class Payload:

    def __init__(self, payload):
        self.__dict__ = payload
        self.load_nested_data()

    def get_properties_list(self):
        return [x for x in dir(self) if not x.startswith('__') and not callable(getattr(self, x))]

    def load_nested_data(self):
        for prop in self.get_properties_list():
            if type(self.__getattribute__(prop)) is dict:
                subsection = Payload(self.__getattribute__(prop))
                self.__setattr__(prop, subsection)
                subsection.load_nested_data()


a = Payload(json.load(open('midround_alive_data.json')))
print(a.map.name)
print(a.provider.steamid)
print(a.player.name)
print(a.player.state.health)
print(a.player.match_stats.kills)
print(a.previously.player.match_stats.deaths)
print(a.previously.player.state.armor)

a = TestPayload(json.load(open('midround_alive_data.json')))
load_nested_data(a)
print(a.map.name)
print(a.provider.steamid)
print(a.player.name)
print(a.player.state.health)
print(a.player.match_stats.kills)
print(a.previously.player.match_stats.deaths)
print(a.previously.player.state.armor)
