import os
import sqlite3

from flask import Flask, request, g
from flask_restful import Resource, Api

from user_data_payload import UserDataPayload

cs_py_server = Flask(__name__)
cs_py_rest_api = Api(cs_py_server)
cs_py_server.config['DATABASE'] = os.path.join(cs_py_server.root_path, '..', 'users_and_matches.db')

# ---------------------------


# makes sure required tables exist; if not, create them
def server_sql_setup():
    sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])

    create_users_table_sql = '''CREATE TABLE IF NOT EXISTS all_users (User_SteamID INTEGER, "Match Count" INTEGER)'''

    create_matches_table_sql = '''CREATE TABLE IF NOT EXISTS all_matches (Match_ID INTEGER PRIMARY KEY, 
                                                                          User_SteamID INTEGER, Start INTEGER, End INTEGER, 
                                                                          'Round Count' INTEGER, Map TEXT, Rating1 REAL,
                                                                          HSR REAL, MDC REAL, KPR REAL, KAS REAL, 
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

# ---------------------------

# utility functions for payload validation and sql statements


def get_db():
    sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])
    return sql_db, sql_db.cursor()


# returns True if user already exists in database, False if user is not yet in DB.
def check_for_user_id(payload_user_id):
    sql_db, all_users_cursor = get_db()

    check_for_user_sql = '''SELECT EXISTS (SELECT 1 FROM all_users WHERE User_SteamID == ?)'''
    all_users_cursor.execute(check_for_user_sql, (payload_user_id,))
    return all_users_cursor.fetchone()


# adds new user and initializes the match count to 1
def add_new_user(user_id):
    sql_db, all_users_cursor = get_db()

    add_user_sql = '''INSERT INTO all_users(User_SteamID, "Match Count") VALUES (?, ?)'''
    all_users_cursor.execute(add_user_sql, (user_id, 1))
    sql_db.commit()
    sql_db.close()
    print("New User: %s Added" % user_id)


# adds 1 to the match count of user in the all_users sql table
def update_existing_user(user_id):
    sql_db, all_users_cursor = get_db()

    update_user_sql = '''UPDATE all_users SET "Match Count" = "Match Count" + 1 WHERE User_SteamID == ?'''
    all_users_cursor.execute(update_user_sql, (user_id,))
    sql_db.commit()
    sql_db.close()
    print("Match Count of User: %s Updated" % user_id)


# checks for duplicate matches in the all_matches table with current payload, using user_id, start, and end times
# Returns True if duplicate exists. False if payload is unique, new entry.
def check_for_duplicate_matches(payload):
    sql_db, all_matches_cursor = get_db()

    # if there's at least one that matches the current payload, then duplicate exists.
    check_for_duplicate_sql = '''SELECT EXISTS (SELECT 1 from all_matches WHERE User_SteamID == ? AND Start == ? AND End == ?)'''
    all_matches_cursor.execute(check_for_duplicate_sql, (payload.steamid, payload.start, payload.end))
    return all_matches_cursor.fetchone()


# inserts user data into all_matches SQL table
def insert_match_data(payload):
    sql_db, all_matches_cursor = get_db()

    insert_user_data_sql = '''INSERT INTO all_matches(User_SteamID, Start, End, 'Round Count', Map, Rating1, HSR, MDC, 
                                                      KPR, KAS, KDR, KDA, MEAN, CT_HSR, CT_MDC, CT_KPR, CT_KAS, CT_KDR, 
                                                      CT_KDA, CT_MEAN, T_HSR, T_MDC, T_KPR, T_KAS, T_KDR, T_KDA, T_MEAN)
                                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                      ?, ?, ?, ?, ?, ?, ?, ?)'''

    new_match_data = (
        payload.steamid, payload.start, payload.end, payload.round_count, payload.map_name, payload.rating1,
        payload.hsr, payload.mdc, payload.kpr, payload.kas, payload.kdr, payload.kda, payload.mean_equip, payload.ct_hsr,
        payload.ct_mdc, payload.ct_kpr, payload.ct_kas, payload.ct_kdr, payload.ct_kda, payload.ct_mean_equip, payload.t_hsr,
        payload.t_mdc, payload.t_kpr, payload.t_kas, payload.t_kdr, payload.t_kda, payload.t_mean_equip
    )

    all_matches_cursor.execute(insert_user_data_sql, new_match_data)
    sql_db.commit()
    sql_db.close()
    print("New Match Data Inserted For User: %s" % payload.steamid)

# ---------------------------

# API classes and functions


# for the future frontend website/webapp on EWS for CS-Py that will display to users their results
class FrontEndDataApi(Resource):
    def get(self, user_steamid):
        return user_steamid


# for receiving match data from user clients
class ReceiveDataApi(Resource):
    def post(self):
        if request.is_json:
            print(request.get_json())
            payload = UserDataPayload(request.get_json())

            if payload.is_valid:
                print("Valid Payload Received")
                # insert into sql table(s) accordingly
                if check_for_user_id(payload.steamid):  # user already exists
                    if check_for_duplicate_matches(payload):
                        insert_match_data(payload)
                        update_existing_user(payload.steamid)

                else:  # user does not exist
                    insert_match_data(payload)
                    add_new_user(payload.steamid)

                return 'Data Accepted', 202

        return 'Invalid Data', 400


cs_py_rest_api.add_resource(ReceiveDataApi, '/api/data_receiver')
# cs_py_rest_api.add_resource(FrontEndDataApi, '/api/results/<string:user_steamid>')

# TODO: Only for testing, remove for deployment. For deployment, use PythonAnywhere.
if __name__ == '__main__':
    server_sql_setup()
    cs_py_server.run(debug=False, port=5001)
