import pandas as pd
from datetime import datetime
import sqlite3


def check_payload(payload):
    if 'map' in payload and 'provider' in payload and 'player' in payload:
        if 'activity' in payload['player'] and payload['player']['activity'] == 'playing':  # check if player is playing
            if 'mode' in payload['map'] and payload['map']['mode'] == 'competitive':  # check if map is comepetitive mode
                if 'phase' in payload['map'] and (payload['map']['phase'] == 'live' or payload['map']['phase'] == 'intermission' or payload['map']['phase'] == 'gameover'):  # check map phase
                    if 'round' in payload['map']:
                        if 'round' in payload and 'phase' in payload['round']:
                            if payload['round']['phase'] == 'over' and (str(payload['provider']['steamid']) == (str(payload['player']['steamid']))):
                                if 'previously' in payload:
                                    if 'round' in payload['previously']:
                                        if 'phase' in payload['previously']['round'] and payload['previously']['round']['phase'] == 'live':
                                            return True
                            else:
                                if payload['round']['phase'] == 'live' and (str(payload['provider']['steamid']) == (str(payload['player']['steamid']))):
                                    if 'state' in payload['player'] and 'health' in payload['player']['state']:
                                        if int(payload['player']['state']['health']) == 0:
                                            if 'previously' in payload:
                                                if 'player' in payload['previously']:
                                                    if 'state' in payload['previously']['player']:
                                                        if 'health' in payload['previously']['player']['state'] and (payload['previously']['player']['state']['health'] > 0):
                                                            return True

    return False


def parse_payload(payload):
    time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
    format_time = str(time.strftime('%b %d, %Y'))

    data_df = pd.DataFrame({
        'Time': [format_time],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
        # 'Round #': [payload['map']['round']],
        # 'Round Winner': [payload['round']['win_team']],
        'Player Name': [payload['player']['name']],
        'Player Team': [payload['player']['team']],
        'Kills': [payload['player']['match_stats']['kills']],
        'Assists': [payload['player']['match_stats']['assists']],
        'Deaths': [payload['player']['match_stats']['deaths']],
        'MVPs': [payload['player']['match_stats']['mvps']],
        'Score': [payload['player']['match_stats']['score']],
        'Current Equip. Value': [payload['player']['state']['equip_value']],
        'Round Kills': [payload['player']['state']['round_kills']],
        'Round HS Kills': [payload['player']['state']['round_killhs']]
    })

    data_df = data_df[['Time', 'Map', 'Map Status', 'Player Name', 'Player Team',
                       'Kills', 'Assists', 'Deaths', 'MVPs', 'Score',
                       'Current Equip. Value', 'Round Kills', 'Round HS Kills']]  # 'Round Winner', 'Round #'

    return data_df


# remove duplicates
def clean_db(conn):
    temp_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    temp_df = temp_df.drop_duplicates()
    temp_df.to_sql("per_round_data", conn, if_exists="replace", index=False)


# query database with pandas to gather statistical data.
# calculate & collect: HSR, KDR, KDA, KAST
# graph: CT vs. T, player stats on various maps, player stats over rounds in a match and/or over other metrics of time
def query_db_match(conn):
    pass


def query_db_today(conn):
    pass


def query_db_week(conn):
    pass


def query_db_month(conn):
    pass


def query_db_lifetime(conn):
    pass

