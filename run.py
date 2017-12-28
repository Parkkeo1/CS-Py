import pandas as pd
import time


def check_payload(payload):
    if 'map' in payload and 'provider' in payload and 'player' in payload:
        if 'activity' in payload['player'] and payload['player']['activity'] == 'playing':
            if 'mode' in payload['map'] and payload['map']['mode'] == 'competitive':
                if 'phase' in payload['map'] and (payload['map']['phase'] == 'live' or payload['map']['phase'] == 'intermission' or payload['map']['phase'] == 'gameover'):
                    if 'round' in payload['map']:
                        if 'round' in payload and 'phase' in payload['round']:
                            client = str(payload['provider']['steamid'])
                            target = str(payload['player']['steamid'])
                            if payload['round']['phase'] == 'over' and (client == target):
                                if 'previously' in payload:
                                    if 'round' in payload['previously']:
                                        if 'phase' in payload['previously']['round'] and payload['previously']['round']['phase'] == 'live':
                                            return 1
                            else:
                                if payload['round']['phase'] == 'live' and (client == target):
                                    if 'state' in payload['player'] and 'health' in payload['player']['state']:
                                        if int(payload['player']['state']['health']) == 0:
                                            if 'previously' in payload:
                                                if 'player' in payload['previously']:
                                                    if 'state' in payload['previously']['player']:
                                                        if 'health' in payload['previously']['player']['state'] and (
                                                                payload['previously']['player']['state']['health'] > 0):
                                                            return 1
                                else:
                                    if payload['map']['phase'] == 'gameover' and payload['round']['phase'] == 'over' and (client != target):
                                        if 'previously' in payload:
                                            if 'round' in payload['previously']:
                                                if 'phase' in payload['previously']['round'] and \
                                                        payload['previously']['round'][
                                                            'phase'] == 'live':
                                                    return 2
    return 0


def parse_payload(payload):
    # time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
    # format_time = str(time.strftime('%b %d, %Y'))

    if 'team' in payload['player']:
        player_team = payload['player']['team']
    else:
        player_team = None

    data_df = pd.DataFrame({
        'Time': [payload['provider']['timestamp']],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
        # 'Round #': [payload['map']['round']],
        # 'Round Winner': [payload['round']['win_team']],
        'Player Name': [payload['player']['name']],
        'Player Team': [player_team],
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


def endgame_payload(payload):
    # time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
    # format_time = str(time.strftime('%b %d, %Y'))

    data_df = pd.DataFrame({
        'Time': [payload['provider']['timestamp']],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
    })

    data_df = data_df[['Time', 'Map', 'Map Status']]

    return data_df


# remove duplicates
def clean_db(conn):
    temp_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    temp_df = temp_df.drop_duplicates(subset=['Map', 'Map Status', 'Player Name', 'Player Team', 'Kills', 'Assists',
                                              'Deaths', 'MVPs', 'Score', 'Current Equip. Value', 'Round Kills',
                                              'Round HS Kills'])
    temp_df.to_sql("per_round_data", conn, if_exists="replace", index=False)


# query database with pandas to gather statistical data.
# calculate & collect: HSR, KDR, KDA, KAST
# graph: CT vs. T, player stats on various maps, player stats over rounds in a match and/or over other metrics of time
def query_db_current(conn):
    result = {}
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()
    if not idx_range:
        return query_db_time(conn, 'lifetime')  # because there have been no 'gameover' events ever.
    else:
        idx = idx_range[-1]
        data_df = data_df.iloc[idx + 1:]
        if data_df.empty:  # if there haven't been any rounds played since the last complete match.
            result['hsr'] = 0
            result['equip'] = 0
            result['correl'] = 0
            result['timeframe'] = 'Current Match'

            return result
        else:
            result['hsr'] = hsr(data_df)
            result['equip'] = int(data_df['Current Equip. Value'].mean())
            result['correl'] = correl(data_df)
            result['timeframe'] = 'Current Match'

            return result


def query_db_match(conn):
    result = {}
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()[-2:]
    length = len(idx_range)
    if length < 2:
        if length == 1:  # there has only been one 'gameover' event.
            data_df = data_df.iloc[0:idx_range[0] + 1]
            result['hsr'] = hsr(data_df)
            result['equip'] = int(data_df['Current Equip. Value'].mean())
            result['correl'] = correl(data_df)
            result['timeframe'] = 'Last Match'

            return result
        else:
            return query_db_time(conn, 'lifetime')  # because there have been no 'gameover' events ever.
    else:
        data_df = data_df.iloc[idx_range[0] + 1:idx_range[1] + 1]
        result['hsr'] = hsr(data_df)
        result['equip'] = int(data_df['Current Equip. Value'].mean())
        result['correl'] = correl(data_df)
        result['timeframe'] = 'Last Match'

        return result


def query_db_time(conn, time_value):
    result = {}
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    offset = 0
    if time_value == 'today':
        offset = 86400
        result['timeframe'] = 'Past 24 Hours'
    if time_value == 'week':
        offset = 604800
        result['timeframe'] = 'Past 7 Days'
    if time_value == 'month':
        offset = 2592000
        result['timeframe'] = 'Past 30 Days'
    lower = int(time.time()) - offset
    if time_value == 'lifetime':
        result['timeframe'] = 'Lifetime'
        lower = 0

    data_df = data_df[data_df['Time'] >= lower]
    result['hsr'] = hsr(data_df)
    result['equip'] = int(data_df['Current Equip. Value'].mean())
    result['correl'] = correl(data_df)

    return result


# querying db helper function, returns list of indices of the rows of the dataframe where map status == 'gameover'.
# This function is used to separate data into individual matches.
def separate(data_df):
    pass


def hsr(data_df):
    total_kills = data_df['Round Kills'].sum()
    total_hs = data_df['Round HS Kills'].sum()
    return float(round(total_hs / total_kills, 3))


def correl(data_df):
    coeff = data_df['Round Kills'].corr(data_df['Current Equip. Value'])
    return float(round(coeff, 3))


def kdr(data_df):
    pass


def kas(data_df):
    pass
