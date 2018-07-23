import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# ---------------------------

# Functions for handling POST requests


# makes sure required tables exist; if not, create them
def server_sql_setup(sql_db):
    create_users_table_sql = '''CREATE TABLE IF NOT EXISTS all_users (User_SteamID INTEGER, "Match Count" INTEGER)'''

    create_matches_table_sql = '''CREATE TABLE IF NOT EXISTS all_matches (Match_ID INTEGER PRIMARY KEY,
                                                                          User_SteamID INTEGER, Start INTEGER, End INTEGER,
                                                                          'Round Count' INTEGER, Map TEXT, Kills INTEGER, 
                                                                          Assists INTEGER, Deaths INTEGER, Score INTEGER, 
                                                                          Rating1 REAL, HSR REAL, MDC REAL, KPR REAL, KAS REAL,
                                                                          KDR REAL, KDA REAL, MEAN REAL,
                                                                          CT_HSR REAL, CT_MDC REAL,
                                                                          CT_KPR REAL, CT_KAS REAL, CT_KDR REAL,
                                                                          CT_KDA REAL, CT_MEAN REAL,
                                                                          T_HSR REAL, T_MDC REAL, T_KPR REAL, T_KAS REAL,
                                                                          T_KDR REAL, T_KDA REAL, T_MEAN REAL,
                                                                          FOREIGN KEY (User_SteamID)
                                                                          REFERENCES all_users(User_SteamID))'''

    db_cursor = sql_db.cursor()
    db_cursor.execute(create_users_table_sql)
    db_cursor.execute(create_matches_table_sql)
    sql_db.commit()
    print("SQL Table Check Passed")


# returns True if user already exists in database, False if user is not yet in DB.
def does_user_exist(payload_user_id, sql_db):
    all_users_cursor = sql_db.cursor()

    check_for_user_sql = '''SELECT EXISTS (SELECT 1 FROM all_users WHERE User_SteamID == ?)'''
    all_users_cursor.execute(check_for_user_sql, (payload_user_id,))

    if all_users_cursor.fetchone() == (0,):
        print("New User")
        return False
    else:
        print("Existing User")
        return True


# adds new user and initializes the match count to 1
def add_new_user(user_id, sql_db):
    all_users_cursor = sql_db.cursor()

    add_user_sql = '''INSERT INTO all_users(User_SteamID, "Match Count") VALUES (?, ?)'''
    all_users_cursor.execute(add_user_sql, (user_id, 1))
    sql_db.commit()
    print("New User: %s Added" % user_id)


# adds 1 to the match count of user in the all_users sql table
def update_existing_user(user_id, sql_db):
    all_users_cursor = sql_db.cursor()

    update_user_sql = '''UPDATE all_users SET "Match Count" = "Match Count" + 1 WHERE User_SteamID == ?'''
    all_users_cursor.execute(update_user_sql, (user_id,))
    sql_db.commit()
    print("Match Count of User: %s Updated" % user_id)


# checks for duplicate matches in the all_matches table with current payload, using user_id, start, and end times
# Returns True if duplicate exists. False if payload is unique, new entry.
def is_duplicate_match(payload, sql_db):
    all_matches_cursor = sql_db.cursor()

    # if there's at least one that matches the current payload, then duplicate exists.
    check_for_duplicate_sql = '''SELECT EXISTS (SELECT 1 from all_matches WHERE User_SteamID == ? AND Start == ? AND End == ?)'''
    all_matches_cursor.execute(check_for_duplicate_sql, (payload.steamid, payload.start, payload.end))

    if all_matches_cursor.fetchone() == (0,):
        print("Not A Duplicate, Inserting")
        return False
    else:
        print("Duplicate Found, Not Inserting")
        return True


# inserts user data into all_matches SQL table
def insert_match_data(payload, sql_db):
    all_matches_cursor = sql_db.cursor()

    insert_user_data_sql = '''INSERT INTO all_matches(User_SteamID, Start, End, 'Round Count', Map, Kills, Assists, 
                                                      Deaths, Score, Rating1, HSR, MDC,
                                                      KPR, KAS, KDR, KDA, MEAN, CT_HSR, CT_MDC, CT_KPR, CT_KAS, CT_KDR,
                                                      CT_KDA, CT_MEAN, T_HSR, T_MDC, T_KPR, T_KAS, T_KDR, T_KDA, T_MEAN)
                                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

    new_match_data = (
        payload.steamid, payload.start, payload.end, payload.round_count, payload.map_name, payload.kills,
        payload.assists, payload.deaths, payload.score, payload.rating1,
        payload.hsr, payload.mdc, payload.kpr, payload.kas, payload.kdr, payload.kda, payload.mean_equip, payload.ct_hsr,
        payload.ct_mdc, payload.ct_kpr, payload.ct_kas, payload.ct_kdr, payload.ct_kda, payload.ct_mean_equip, payload.t_hsr,
        payload.t_mdc, payload.t_kpr, payload.t_kas, payload.t_kdr, payload.t_kda, payload.t_mean_equip
    )

    all_matches_cursor.execute(insert_user_data_sql, new_match_data)
    sql_db.commit()
    print("New Match Data Inserted For User: %s" % payload.steamid)


# ---------------------------

# Functions for handling GET requests


# Gets matches of given user as SQL query, loads data into Pandas dataframe, then returns dataframe as list of dicts.
def load_matches_from_sql(user_steam_id, sql_db):
    get_user_matches_sql = '''SELECT * from all_matches WHERE User_SteamID == ?'''
    user_matches_df = pd.read_sql(get_user_matches_sql, sql_db, params=(user_steam_id,))
    user_matches_list = user_matches_df.to_dict(orient='records')
    return user_matches_list
