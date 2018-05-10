import time
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import math


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
                                            return 1  # parse payload; when player is alive by the end of the round/game
                            else:
                                if payload['round']['phase'] == 'live' and (client == target):
                                    if 'state' in payload['player'] and 'health' in payload['player']['state']:
                                        if int(payload['player']['state']['health']) == 0:
                                            if 'previously' in payload:
                                                if 'player' in payload['previously']:
                                                    if 'state' in payload['previously']['player']:
                                                        if 'health' in payload['previously']['player']['state'] and (
                                                                payload['previously']['player']['state']['health'] > 0):
                                                            return 1  # parse payload; when player dies mid-round
                                else:
                                    if payload['map']['phase'] == 'gameover' and payload['round']['phase'] == 'over' and (client != target):
                                        if 'previously' in payload:
                                            if 'round' in payload['previously']:
                                                if 'phase' in payload['previously']['round'] and \
                                                        payload['previously']['round'][
                                                            'phase'] == 'live':
                                                    return 2  # triggers endgame payload
    return 0


def parse_payload(payload):
    if 'team' in payload['player']:
        player_team = payload['player']['team']
    else:
        player_team = None

    data_df = pd.DataFrame({
        'Time': [int(payload['provider']['timestamp'])],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
        'Player Name': [payload['player']['name']],
        'Player Team': [player_team],
        'Kills': [int(payload['player']['match_stats']['kills'])],
        'Assists': [int(payload['player']['match_stats']['assists'])],
        'Deaths': [int(payload['player']['match_stats']['deaths'])],
        'MVPs': [int(payload['player']['match_stats']['mvps'])],
        'Score': [int(payload['player']['match_stats']['score'])],
        'Current Equip. Value': [int(payload['player']['state']['equip_value'])],
        'Round Kills': [int(payload['player']['state']['round_kills'])],
        'Round HS Kills': [int(payload['player']['state']['round_killhs'])]
    })

    data_df = data_df[['Time', 'Map', 'Map Status', 'Player Name', 'Player Team',
                       'Kills', 'Assists', 'Deaths', 'MVPs', 'Score',
                       'Current Equip. Value', 'Round Kills', 'Round HS Kills']]

    return data_df


def endgame_payload(payload):
    data_df = pd.DataFrame({
        'Time': [int(payload['provider']['timestamp'])],
        'Map': [payload['map']['name']],
        'Map Status': [payload['map']['phase']],
    })

    data_df = data_df[['Time', 'Map', 'Map Status']]

    return data_df


# remove duplicates (deprecated, and possibly faulty in edge cases)
# def clean_db(conn):
#     temp_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
#     temp_df = temp_df.drop_duplicates(subset=['Map', 'Map Status', 'Player Name', 'Player Team', 'Kills', 'Assists',
#                                               'Deaths', 'MVPs', 'Score', 'Current Equip. Value', 'Round Kills',
#                                               'Round HS Kills'])
#     temp_df.to_sql("per_round_data", conn, if_exists="replace", index=False)


def ensure_types(conn):
    data_df = pd.read_sql('SELECT * FROM per_round_data', conn)

    data_df['Time'] = pd.to_numeric(data_df['Time'], errors='coerce')
    data_df['Kills'] = pd.to_numeric(data_df['Kills'], errors='coerce')
    data_df['Assists'] = pd.to_numeric(data_df['Assists'], errors='coerce')
    data_df['Deaths'] = pd.to_numeric(data_df['Deaths'], errors='coerce')
    data_df['MVPs'] = pd.to_numeric(data_df['MVPs'], errors='coerce')
    data_df['Score'] = pd.to_numeric(data_df['Score'], errors='coerce')
    data_df['Current Equip. Value'] = pd.to_numeric(data_df['Current Equip. Value'], errors='coerce')
    data_df['Round Kills'] = pd.to_numeric(data_df['Round Kills'], errors='coerce')
    data_df['Round HS Kills'] = pd.to_numeric(data_df['Round HS Kills'], errors='coerce')

    data_df.to_sql("per_round_data", conn, if_exists="replace", index=False)


# query database with pandas to gather statistical data.
# calculate & collect: HSR, KDR, KDA, KAS
# graph: CT vs. T, player stats on various maps, player stats over rounds in a match and/or over other metrics of time
def query_db_current(conn):
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()
    if not idx_range:
        return query_db_time(conn, 'lifetime')  # because there have been no 'gameover' events ever.
    else:
        idx = idx_range[-1]
        data_df = data_df.iloc[idx + 1:]
        if data_df.empty:  # if there haven't been any rounds played since the last complete match.
            result = calculate_empty()
            result['money_plot'] = blank_plot()
            result['rounds_map_plot'] = blank_plot()
            result['multi_kills_plot'] = blank_plot()
            result['timeframe'] = 'Current Match'

            return result
        else:
            result = calculate_stats(data_df)
            result['money_plot'] = money_scatter_plot(data_df)
            result['rounds_map_plot'] = rounds_per_map_plot(data_df)
            result['multi_kills_plot'] = multi_kills_bar(data_df)
            result['timeframe'] = 'Current Match'

            return result


def query_db_match(conn):
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    idx_range = data_df[data_df['Map Status'] == 'gameover'].index.tolist()[-2:]
    length = len(idx_range)
    if length < 2:
        if length == 1:  # there has only been one 'gameover' event.
            data_df = data_df.iloc[0:idx_range[0] + 1]
            result = calculate_stats(data_df)
            result['money_plot'] = money_scatter_plot(data_df)
            result['rounds_map_plot'] = rounds_per_map_plot(data_df)
            result['multi_kills_plot'] = multi_kills_bar(data_df)
            result['timeframe'] = 'Last Match'

            return result
        else:
            return query_db_time(conn, 'lifetime')  # because there have been no 'gameover' events ever.
    else:
        data_df = data_df.iloc[idx_range[0] + 1:idx_range[1] + 1]
        result = calculate_stats(data_df)
        result['money_plot'] = money_scatter_plot(data_df)
        result['rounds_map_plot'] = rounds_per_map_plot(data_df)
        result['multi_kills_plot'] = multi_kills_bar(data_df)
        result['timeframe'] = 'Last Match'

        return result


def query_db_time(conn, time_value):
    timeframe = {}
    data_df = pd.read_sql('SELECT * FROM per_round_data;', conn)
    offset = 0
    if time_value == 'today':
        offset = 86400
        timeframe['timeframe'] = 'Past 24 Hours'
    if time_value == 'week':
        offset = 604800
        timeframe['timeframe'] = 'Past 7 Days'
    if time_value == 'month':
        offset = 2592000
        timeframe['timeframe'] = 'Past 30 Days'
    lower = int(time.time()) - offset
    if time_value == 'lifetime':
        timeframe['timeframe'] = 'Lifetime'
        lower = 0

    data_df = data_df[data_df['Time'] >= lower]
    test_df = data_df[['Player Name', 'Player Team']]
    if data_df.empty or test_df.isnull().all().all():  # if there are no entries that match the time criteria (i.e. no games in the past 24 hours)
        result = calculate_empty()
        result['money_plot'] = blank_plot()
        result['rounds_map_plot'] = blank_plot()
        result['multi_kills_plot'] = blank_plot()
        result['timeframe'] = timeframe['timeframe']

        return result
    else:
        result = calculate_stats(data_df)
        result['money_plot'] = money_scatter_plot(data_df)
        result['rounds_map_plot'] = rounds_per_map_plot(data_df)
        result['multi_kills_plot'] = multi_kills_bar(data_df)
        result['timeframe'] = timeframe['timeframe']

        return result


# final abstraction method for ALL statistics to be displayed
# hsr, mean equip. value, md correlation, kdr/kda, kas, kpr FOR OVERALL, CT AND T SIDES.
def calculate_stats(data_df):
    ct_df = data_df[(data_df['Player Team'] == 'CT')].reset_index(drop=True)
    t_df = data_df[(data_df['Player Team'] == 'T')].reset_index(drop=True)

    if len(ct_df.index) == 0:
        ct_equip_value = 0
    else:
        ct_equip_value = int(ct_df['Current Equip. Value'].mean())

    if len(t_df.index) == 0:
        t_equip_value = 0
    else:
        t_equip_value = int(t_df['Current Equip. Value'].mean())

    pistol_results = pistol_stats(data_df)

    result = {'hsr': hsr(data_df), 'equip': int(data_df['Current Equip. Value'].mean()), 'correl': correl(data_df),
              'kdr_kda': kdr_kda(data_df), 'kas': kas(data_df), 'kpr': kpr(data_df),
              'ct_kpr': kpr(ct_df), 'ct_equip': ct_equip_value,
              'ct_hsr': hsr(ct_df), 'ct_correl': correl(ct_df), 't_kpr': kpr(t_df),
              't_equip': t_equip_value, 't_hsr': hsr(t_df), 't_correl': correl(t_df),
              'pistol_hsr': pistol_results['pistol_hsr'], 'pistol_kpr': pistol_results['pistol_kpr'],
              'pistol_k': pistol_results['pistol_k'], 'pistol_ct_hsr': pistol_results['pistol_ct_hsr'],
              'pistol_ct_kpr': pistol_results['pistol_ct_kpr'], 'pistol_ct_k': pistol_results['pistol_ct_k'],
              'pistol_t_hsr': pistol_results['pistol_t_hsr'], 'pistol_t_kpr': pistol_results['pistol_t_kpr'],
              'pistol_t_k': pistol_results['pistol_t_k']}

    return result


def calculate_empty():
    result = {'hsr': 0, 'equip': 0, 'correl': 0, 'kdr_kda': [0, 0], 'kas': 0, 'kpr': 0, 'ct_kpr': 0, 'ct_equip': 0,
              'ct_hsr': 0, 'ct_correl': 0, 't_kpr': 0, 't_equip': 0, 't_hsr': 0, 't_correl': 0, 'pistol_hsr': 0,
              'pistol_kpr': 0, 'pistol_k': 0, 'pistol_ct_hsr': 0, 'pistol_ct_kpr': 0, 'pistol_ct_k': 0,
              'pistol_t_hsr': 0, 'pistol_t_kpr': 0, 'pistol_t_k': 0}

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

    if total_kills == 0 or math.isnan(total_kills):
        return 0

    if total_hs == 0 or math.isnan(total_hs):
        return 0

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

    if total_deaths == 0 or math.isnan(total_deaths):
        return [0, 0]

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
                    if match_df.iloc[i]['Round Kills'] > 0 or match_df.iloc[i]['Kills'] > 0 or match_df.iloc[i]['Assists'] > 0 or match_df.iloc[i]['Deaths'] == 0:
                        kas_counter += 1
                    round_counter += 1
                else:
                    if match_df.iloc[i]['Round Kills'] > 0 or match_df.iloc[i]['Kills'] > match_df.iloc[i - 1]['Kills'] or match_df.iloc[i]['Assists'] > match_df.iloc[i - 1]['Assists'] or match_df.iloc[i]['Deaths'] == match_df.iloc[i - 1]['Deaths']:
                        kas_counter += 1
                    round_counter += 1

    if round_counter == 0 or math.isnan(round_counter):
        return 0

    kas_r = round((kas_counter / round_counter), 2)
    return kas_r * 100


def kpr(data_df):
    total_kills = data_df['Round Kills'].sum()
    count_df = data_df[(data_df['Player Name'].notnull()) & (data_df['Player Team'].notnull())]
    total_rounds = len(count_df.index)

    if total_rounds == 0 or math.isnan(total_rounds):
        return 0

    if total_kills == 0 or math.isnan(total_kills):
        return 0

    return round((total_kills / total_rounds), 2)


def pistol_stats(data_df):
    df_list = remove_empty(separate(data_df))

    pistol_df = pd.DataFrame()
    for df in df_list:
        df = df.reset_index(drop=True)
        try:
            temp_df = df.iloc[[0, 15]]
            pistol_df = pistol_df.append(temp_df, ignore_index=True)
        except:
            try:
                temp_df = df.iloc[0]
                pistol_df = pistol_df.append(temp_df, ignore_index=True)
            except:
                continue

    pistol_df = pistol_df[(pistol_df['Current Equip. Value'] <= 1000) & (pistol_df['Current Equip. Value'] > 0)]
    ct_pistol_df = pistol_df[(pistol_df['Player Team'] == 'CT')].reset_index(drop=True)
    t_pistol_df = pistol_df[(pistol_df['Player Team'] == 'T')].reset_index(drop=True)

    # TODO: Improve style for code below.

    pistol_results = {'pistol_hsr': hsr(pistol_df), 'pistol_kpr': kpr(pistol_df), 'pistol_k': pistol_k_ratio(pistol_df),
                      'pistol_ct_hsr': hsr(ct_pistol_df), 'pistol_ct_kpr': kpr(ct_pistol_df),
                      'pistol_ct_k': pistol_k_ratio(ct_pistol_df), 'pistol_t_hsr': hsr(t_pistol_df),
                      'pistol_t_kpr': kpr(t_pistol_df), 'pistol_t_k': pistol_k_ratio(t_pistol_df)}

    return pistol_results


def pistol_k_ratio(pistol_df):
    if len(pistol_df.index) == 0 or math.isnan(len(pistol_df.index)):
        return 0

    return round(len(pistol_df[pistol_df['Round Kills'] > 0].index) / len(pistol_df.index), 2)


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
    plt.suptitle('Rounds Played By Map')
    plt.xlabel('Map')
    plt.ylabel('Count')
    return mpld3.fig_to_html(fig, no_extras=True)


def money_scatter_plot(data_df):
    x = data_df['Current Equip. Value']
    y = data_df['Round Kills']

    fig = plt.figure()
    plt.scatter(x, y)
    plt.xlabel('Equipment Value ($)')
    plt.ylabel('# of Kills In Round')
    plt.yticks([0, 1, 2, 3, 4, 5])
    plt.suptitle('Kills/Round vs. Equipment Value')
    return mpld3.fig_to_html(fig, no_extras=True)


def multi_kills_bar(data_df):
    multi_list = [0, 1, 2, 3, 4, 5]

    multi_count_dict = {count: len(data_df[data_df['Round Kills'] == count]) for count in multi_list}

    fig = plt.figure()
    plt.bar(range(len(multi_count_dict)), list(multi_count_dict.values()), align='center')
    plt.xticks(range(len(multi_count_dict)), list(multi_count_dict.keys()))
    plt.suptitle('Multi-Kills')
    plt.xlabel('# of Kills In Round')
    plt.ylabel('Count')
    return mpld3.fig_to_html(fig, no_extras=True)


def blank_plot():
    fig = plt.figure()
    fig.suptitle('No Results To Graph')
    return mpld3.fig_to_html(fig, no_extras=True)
