import pandas as pd
from datetime import datetime


def check_payload(payload):
    if 'map' in payload and 'provider' in payload and 'player' in payload:
        if 'activity' in payload['player'] and payload['player']['activity'] == 'playing':
            if 'mode' in payload['map'] and payload['map']['mode'] == 'competitive':
                if 'phase' in payload['map'] and (payload['map']['phase'] == 'live' or payload['map']['phase'] == 'intermission' or payload['map']['phase'] == 'gameover'):
                    if 'round' in payload['map'] and payload['map']['round'] != 0:
                        if 'round' in payload:
                            if 'phase' in payload['round'] and payload['round']['phase'] == 'over':
                                if 'previously' in payload:
                                    if 'round' in payload['previously']:
                                        if 'phase' in payload['previously']['round'] and payload['previously']['round']['phase'] == 'live':
                                            return True
                                    # if 'map' in payload['previously']:

    return False


def parse_payload(payload):
    time = datetime.utcfromtimestamp(payload['provider']['timestamp'])
    format_time = str(time.strftime('%b %d, %Y'))

    data_df = pd.DataFrame({
        'Time': format_time,
        'Map': payload['map']['name'],
        'Map Status': payload['map']['phase'],
        'Round #': payload['map']['round'],
        'Round Winner': payload['round']['win_team'],
        'Player Name': payload['player']['name'],
        'Player Team': payload['player']['team'],
        'Overall Kills': payload['player']['match_stats']['kills'],
        'Overall Assists': payload['player']['match_stats']['assists'],
        'Overall Deaths': payload['player']['match_stats']['deaths'],
        'Overall MVPs': payload['player']['match_stats']['mvps'],
        'Overall Score': payload['player']['match_stats']['score'],
        'Current Equip. Value': payload['player']['state']['equip_value'],
        'Round Kills': payload['player']['state']['round_kills'],
        'Round HS Kills': payload['player']['state']['round_killhs']
    })

    return data_df


    # if 'player' in payload and 'state' in payload['player']:
    #     if 'round_kills' in payload['player']['state'] and 'round_killhs' in payload['player']['state']:
    #         return [payload['player']['state']['round_kills'], payload['player']['state']['round_killhs']]