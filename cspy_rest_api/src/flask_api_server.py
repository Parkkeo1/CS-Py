import os
import sqlite3

from flask import Flask, request
from flask_restful import Resource, Api

from sql_db_manager import check_for_user_id, add_new_user, update_existing_user, check_for_duplicate_matches, insert_match_data
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
                sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])
                print("Valid Payload Received")

                # insert into sql table(s) accordingly
                if check_for_user_id(payload.steamid, sql_db):  # user already exists
                    if check_for_duplicate_matches(payload, sql_db):
                        insert_match_data(payload, sql_db)
                        update_existing_user(payload.steamid, sql_db)
                    else:
                        print("Duplicate Found, Not Inserting")

                else:  # user does not exist
                    insert_match_data(payload, sql_db)
                    add_new_user(payload.steamid, sql_db)

                sql_db.close()
                return 'Data Accepted', 202

        return 'Invalid Data', 400


cs_py_rest_api.add_resource(ReceiveDataApi, '/api/data_receiver')
# cs_py_rest_api.add_resource(FrontEndDataApi, '/api/results/<string:user_steamid>')

# TODO For deployment, use PythonAnywhere.
if __name__ == '__main__':
    server_sql_setup()
    # cs_py_server.run(debug=False, port=5001)
