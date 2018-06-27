from server import *
import webbrowser

if __name__ == "__main__":
    # setup
    db_conn = sqlite3.connect(cs_py.config['DATABASE'])
    init_table_if_not_exists(db_conn)
    setup_gamestate_cfg()

    # auto-opens browser window to CS-Py frontend
    webbrowser.open_new('http://127.0.0.1:5000')
    cs_py.run(debug=False, threaded=True)
