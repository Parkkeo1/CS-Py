import sqlite3

from flask_api_server import cs_py_server
from sql_db_manager import server_sql_setup

# Standalone script for deploying on PythonAnywhere
server_sql_setup(sqlite3.connect(cs_py_server.config['DATABASE']))
