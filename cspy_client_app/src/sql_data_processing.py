import requests
import time

import pandas as pd

from match_analysis import MatchAnalysis

# utility methods for processing in flask routes


def init_table_if_not_exists(sql_db):
    create_round_table_sql = '''CREATE TABLE IF NOT EXISTS per_round_data (Time INTEGER, SteamID INTEGER, Map TEXT, 
                                                                     'Map Status' TEXT, Round INTEGER, 'GS Code' INTEGER, 
                                                                     CT_Score INTEGER, T_Score INTEGER, 'Player Name' TEXT,
                                                                     'Player Team' TEXT, Kills INTEGER, Assists INTEGER,
                                                                     Deaths INTEGER, MVPs INTEGER, Score INTEGER,
                                                                     'Current Equip. Value' INTEGER, 'Round Kills' INTEGER,
                                                                     'Round HS Kills' INTEGER);'''

    sql_db.cursor().execute(create_round_table_sql)
    sql_db.commit()
    print("SQL Table Check Passed")


# checks previous entries in database to make sure there are no duplicates.
def check_prev_entries(game_data, round_db):

    # returns True if they are duplicates (except Time)
    def is_duplicate(last_entry_row, payload):
        match_stats = payload.player.match_stats
        player_state = payload.player.state

        if player_state.round_kills > 0 and last_entry_row['Kills'] == match_stats.kills:
            return True

        first_pass = last_entry_row['Player Team'] == payload.player.team and \
               last_entry_row['Kills'] == match_stats.kills and \
               last_entry_row['Assists'] == match_stats.assists and \
               last_entry_row['Deaths'] == match_stats.deaths and \
               last_entry_row['Round Kills'] == player_state.round_kills and \
               last_entry_row['Round HS Kills'] == player_state.round_killhs

        second_pass = last_entry_row['Player Team'] == payload.player.team and \
               last_entry_row['Kills'] == match_stats.kills and \
               last_entry_row['Deaths'] == match_stats.deaths and \
               last_entry_row['Round Kills'] == player_state.round_kills and \
               last_entry_row['Round HS Kills'] == player_state.round_killhs and \
               last_entry_row['CT_Score'] == payload.map.team_ct.score and \
               last_entry_row['T_Score'] == payload.map.team_t.score

        return True if first_pass or second_pass else False

    last_entry = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', round_db)

    if last_entry.shape[0] != 0:
        if abs(int(game_data.provider.timestamp - last_entry.iloc[0]['Time'])) <= 1:
            sql_delete = 'DELETE FROM per_round_data WHERE Time = (SELECT MAX(Time) FROM per_round_data);'
            round_db.cursor().execute(sql_delete)
            round_db.commit()
            print("Time Duplicate Replaced")
            return True

        if game_data.gamestate_code.value == 1:  # Checking for duplicate combo of midround death + endround payloads
            if last_entry.iloc[0]['GS Code'] == 2:
                if is_duplicate(last_entry.iloc[0], game_data):
                    print("Round Duplicate Not Inserted")
                    return False  # do not insert a duplicate.

    print("Not a Duplicate")
    return True


def insert_round_data(round_data, round_db):
    match_stats = round_data.player.match_stats
    player_state = round_data.player.state

    new_round_data = (
        round_data.provider.timestamp, round_data.provider.steamid, round_data.map.name, round_data.map.phase,
        round_data.map.round, round_data.gamestate_code.value, round_data.map.team_ct.score,
        round_data.map.team_t.score,
        round_data.player.name, round_data.player.team, match_stats.kills, match_stats.assists, match_stats.deaths,
        match_stats.mvps, match_stats.score, player_state.equip_value, player_state.round_kills,
        player_state.round_killhs)

    round_insert_sql = ''' INSERT INTO per_round_data(Time, SteamID, Map, "Map Status", Round, 'GS Code', CT_Score, T_Score, 
                                                      "Player Name", "Player Team", Kills, Assists, Deaths, MVPs, Score, 
                                                      "Current Equip. Value", "Round Kills", "Round HS Kills")
                                                      VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    round_db.cursor().execute(round_insert_sql, new_round_data)
    round_db.commit()


# clears per_round_data table to indicate end of game
def send_match_to_remote(round_db, api_address):
    # parse current per_round_data into dataframe
    data_for_match_df = pd.read_sql('SELECT * FROM per_round_data;', round_db)
    if data_for_match_df.empty or data_for_match_df.shape[0] == 0:
        return  # cancel if there's no data to analyze or send

    match_data = MatchAnalysis(data_for_match_df)
    del match_data.data_frame
    req_success = False

    for i in range(3):
        time.sleep(2)
        try:
            send_match_request = requests.post(api_address, json=match_data.__dict__, timeout=5)
            if send_match_request.status_code == 202:
                req_success = True
                break
        except requests.exceptions.RequestException as e:
            print("Requests Exception: ", e)

    # checking if request was successful
    if req_success:  # CS-Py's API should send 202: Accepted as response code upon success.
        # TODO: Temporarily removing auto-wipe of round_data table
        # clear per_round_data table
        # round_db.cursor().execute('DELETE FROM per_round_data;')
        # round_db.commit()
        print("Match Data Sent; Rounds Reset")
    else:
        print("API Request Failed. Not Clearing Round Data.")