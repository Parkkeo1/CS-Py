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
                                                                          User_SteamID INTEGER, Start INTEGER, End Integer, 
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


# returns True if user already exists in database, False if user is not yet in DB.
def check_for_user_id(payload_user_id):
    sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])
    all_users_cursor = sql_db.cursor()

    check_for_user_sql = '''SELECT EXISTS (SELECT 1 FROM all_users WHERE User_SteamID == ?)'''
    all_users_cursor.execute(check_for_user_sql, payload_user_id)
    return all_users_cursor.fetchone()


# adds new user and initializes the match count to 1
def add_new_user(user_id):
    sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])
    all_users_cursor = sql_db.cursor()

    add_user_sql = '''INSERT INTO all_users(User_SteamID, "Match Count") VALUES (?, ?)'''
    all_users_cursor.execute(add_user_sql, (user_id, 1))
    sql_db.commit()
    print("New User: %s Added" % user_id)


# adds 1 to the match count of user in the all_users sql table
def update_existing_user(user_id):
    sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])
    all_users_cursor = sql_db.cursor()

    update_user_sql = '''UPDATE all_users SET "Match Count" = "Match Count" + 1 WHERE User_SteamID == ?'''
    all_users_cursor.execute(update_user_sql, user_id)
    sql_db.commit()
    print("Match Count of User: %s Updated" % user_id)


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
                    # TODO: Handle duplicate match entries by comparing SteamID and Start/End Times.
                    pass
                else:  # user does not exist
                    pass

                return 'Data Accepted', 202

        return 'Invalid Data', 400


cs_py_rest_api.add_resource(ReceiveDataApi, '/api/data_receiver')
# cs_py_rest_api.add_resource(FrontEndDataApi, '/api/results/<string:user_steamid>')

# TODO: Only for testing, remove for deployment. For deployment, use PythonAnywhere.
if __name__ == '__main__':
    server_sql_setup()
    cs_py_server.run(debug=False, port=5001)
