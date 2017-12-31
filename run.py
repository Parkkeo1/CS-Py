import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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
    if 'team' in payload['player']:
        player_team = payload['player']['team']
    else:
        player_team = None

    data_df = pd.DataFrame({
        'Time': [payload['provider']['timestamp']],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
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
                       'Current Equip. Value', 'Round Kills', 'Round HS Kills']]

    return data_df


def endgame_payload(payload):
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
# calculate & collect: HSR, KDR, KDA, KAS
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
            result['kdr_kda'] = [0, 0]
            result['kas'] = 0
            # rounds_per_map_plot(data_df)
            result['timeframe'] = 'Current Match'

            return result
        else:
            result['hsr'] = hsr(data_df)
            result['equip'] = int(data_df['Current Equip. Value'].mean())
            result['correl'] = correl(data_df)
            result['kdr_kda'] = kdr_kda(data_df)
            result['kas'] = kas(data_df)
            rounds_per_map_plot(data_df)
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
            result['kdr_kda'] = kdr_kda(data_df)
            result['kas'] = kas(data_df)
            rounds_per_map_plot(data_df)
            result['timeframe'] = 'Last Match'

            return result
        else:
            return query_db_time(conn, 'lifetime')  # because there have been no 'gameover' events ever.
    else:
        data_df = data_df.iloc[idx_range[0] + 1:idx_range[1] + 1]
        result['hsr'] = hsr(data_df)
        result['equip'] = int(data_df['Current Equip. Value'].mean())
        result['correl'] = correl(data_df)
        result['kdr_kda'] = kdr_kda(data_df)
        result['kas'] = kas(data_df)
        rounds_per_map_plot(data_df)
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
    test_df = data_df[['Player Name', 'Player Team']]
    if data_df.empty or test_df.isnull().all().all():  # if there are no entries that match the time criteria (i.e. no games in the past 24 hours)
        result['hsr'] = 0
        result['equip'] = 0
        result['correl'] = 0
        result['kdr_kda'] = [0, 0]
        result['kas'] = 0
        # rounds_per_map_plot(data_df)

        return result
    else:
        result['hsr'] = hsr(data_df)
        result['equip'] = int(data_df['Current Equip. Value'].mean())
        result['correl'] = correl(data_df)
        result['kdr_kda'] = kdr_kda(data_df)
        result['kas'] = kas(data_df)
        rounds_per_map_plot(data_df)

        return result


# querying db helper function, returns list of indices of the rows of the dataframe where map status == 'gameover'.
# This function is used to separate data into individual matches.
def separate(data_df):
    data_df = data_df.reset_index(drop=True)  # fixes IndexError: single positional indexer is out-of-bounds in kdr_kda
    df_list = []
    idx_range = sorted(set([0] + data_df[data_df['Map Status'] == 'gameover'].index.tolist() + [data_df.index[-1]]))

    if len(idx_range) == 1:
        return [data_df]

    for i in range(len(idx_range) - 1):
        if i == 0:
            df_list.append(data_df.iloc[idx_range[i]:idx_range[i + 1] + 1])
        else:
            df_list.append(data_df.iloc[idx_range[i] + 1:idx_range[i + 1] + 1])

    return df_list


def remove_empty(df_list):
    new_list = []

    for df in df_list:
        if not df.empty:
            new_list.append(df)

    return new_list


def hsr(data_df):
    total_kills = data_df['Round Kills'].sum()
    total_hs = data_df['Round HS Kills'].sum()
    return float(round(total_hs / total_kills, 3))


def correl(data_df):
    coeff = data_df['Round Kills'].corr(data_df['Current Equip. Value'])
    return float(round(coeff, 3))


def kdr_kda(data_df):
    total_kills = 0
    total_assists = 0
    total_deaths = 0

    df_list = separate(data_df)
    df_list = remove_empty(df_list)

    for match_df in df_list:
        if match_df.iloc[-1]['Player Name'] is None and match_df.iloc[-1]['Player Team'] is None:
            try:
                max_df = match_df.iloc[-2]
            except IndexError:
                max_df = match_df.iloc[-1].fillna(0)
        else:
            max_df = match_df.iloc[-1]
        total_kills += int(max_df['Kills'])
        total_assists += int(max_df['Assists'])
        total_deaths += int(max_df['Deaths'])

    if total_deaths == 0:
        return ['Undef', 'Undef']

    total_kdr = float(round(total_kills / total_deaths, 3))
    total_kda = float(round((total_kills + total_assists) / total_deaths, 3))

    return [total_kdr, total_kda]


def kas(data_df):
    kas_counter = 0
    round_counter = 0

    df_list = separate(data_df)
    df_list = remove_empty(df_list)

    for match_df in df_list:
        for i in range(len(match_df.index)):
            if match_df.iloc[i]['Player Name'] is None and match_df.iloc[i]['Player Team'] is None:  # check if row is None and NaN values
                continue
            else:
                if i == 0:
                    if match_df.iloc[i]['Round Kills'] > 0 or match_df.iloc[i]['Assists'] > 0 or match_df.iloc[i]['Deaths'] == 0:
                        kas_counter += 1
                    round_counter += 1
                else:
                    if match_df.iloc[i]['Round Kills'] > 0 or match_df.iloc[i]['Assists'] > match_df.iloc[i - 1]['Assists'] or match_df.iloc[i]['Deaths'] == match_df.iloc[i - 1]['Deaths']:
                        kas_counter += 1
                    round_counter += 1

    if round_counter == 0:
        return 'Undef'

    kas_r = round((kas_counter / round_counter), 2)
    return kas_r * 100


def rounds_per_map_plot(data_df):
    df_list = separate(data_df)
    df_list = remove_empty(df_list)

    map_list = list(set(data_df['Map'].tolist()))
    map_list = [x for x in map_list if x != 'RESET POINT']

    round_count_dict = dict.fromkeys(map_list, 0)

    for df in df_list:
        for cs_map in map_list:
            round_count_dict[cs_map] += len(df[df['Map'] == cs_map].index)

    fig = plt.figure()
    plt.bar(range(len(round_count_dict)), list(round_count_dict.values()), align='center')
    plt.xticks(range(len(round_count_dict)), list(round_count_dict.keys()))
    fig.suptitle('Rounds Played by Map')
    plt.xlabel('Map')
    plt.ylabel('Count')

    plt.savefig('static/images/rounds_per_map.png')
