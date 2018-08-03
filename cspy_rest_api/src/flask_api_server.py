import os
import sqlite3

from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS

from sql_db_manager import does_user_exist, add_new_user, update_existing_user, is_duplicate_match, insert_match_data, \
                           server_sql_setup, load_matches_from_sql
from user_data_payload import UserDataPayload

cs_py_server = Flask(__name__, template_folder='../templates', static_folder='../static')
cors = CORS(cs_py_server, resources={r'/api/user_data/*': {'origins': '*'}})

cs_py_rest_api = Api(cs_py_server)
cs_py_server.config['DATABASE'] = os.path.join(cs_py_server.root_path, '..', 'users_and_matches.db')

# ---------------------------


# Frontend routes

@cs_py_server.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@cs_py_server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# ---------------------------

# API classes and functions


# for the future frontend website/web app on EWS for CS-Py that will display to users their results
class FrontEndDataApi(Resource):
    def get(self, user_steamid):
        sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])

        if does_user_exist(user_steamid, sql_db):
            # format is a list of dictionaries
            all_user_matches = load_matches_from_sql(int(user_steamid), sql_db)
            sql_db.close()
            return all_user_matches
        else:
            sql_db.close()
            return 'User Has No Saved Matches', 404


# for receiving match data from user clients
class ReceiveDataApi(Resource):
    def post(self):
        if request.is_json:
            print(request.get_json())
            payload = UserDataPayload(request.get_json())

            if payload.is_valid:
                sql_db = sqlite3.connect(cs_py_server.config['DATABASE'])

                if does_user_exist(payload.steamid, sql_db):  # user already exists
                    if not is_duplicate_match(payload, sql_db):
                        insert_match_data(payload, sql_db)
                        update_existing_user(payload.steamid, sql_db)

                else:  # user does not exist
                    insert_match_data(payload, sql_db)
                    add_new_user(payload.steamid, sql_db)

                sql_db.close()
                return 'Data Accepted', 202

        return 'Invalid Data', 400


cs_py_rest_api.add_resource(ReceiveDataApi, '/api/data_receiver')
cs_py_rest_api.add_resource(FrontEndDataApi, '/api/user_data/<string:user_steamid>')

# TODO For deployment, use PythonAnywhere.
if __name__ == '__main__':
    server_sql_setup(sqlite3.connect(cs_py_server.config['DATABASE']))
    # cs_py_server.run(debug=False, port=5001)
