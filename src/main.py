# # backend POST request handler
# @app.route('/GS', methods=['POST'])
# def GSHandler():
#     if request.is_json and app.config['STARTER']:
#         payload = request.get_json()
#         conn = get_db()
#         counter = check_payload(payload)
#         if counter == 1 or counter == 2:
#             if counter == 1:
#                 stats_df = parse_payload(payload)
#             else:
#                 stats_df = endgame_payload(payload)
#             print(stats_df)
#             last_df = pd.read_sql('SELECT * FROM per_round_data ORDER BY Time DESC LIMIT 1;', conn)
#             if counter == 2:
#                 # makes sure that, if we are attempting to enter in an endgame-stats_df,
#                 # check that the current last entry in the table is not also a 'gameover' entry.
#                 # This prevents having two 'gameover' events in a row, where the latter is a None/NaN entry.
#                 if len(last_df.index) == 0 or last_df.iloc[0]['Map Status'] != 'gameover':
#                     stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
#                     print('successful 2')
#             else:  # if counter == 1; parse payload
#                 if len(last_df.index) == 0 or abs(int(stats_df.iloc[0]['Time']) - int(last_df.iloc[0]['Time'])) > 1:
#                     stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
#                     print('successful 1')
#                 else:  # time difference is 1 second or less
#                     total_df = pd.read_sql('SELECT * FROM per_round_data', conn)
#                     new_df = total_df.iloc[:-1]  # excluding last entry AKA last_df
#                     new_df.to_sql("per_round_data", conn, if_exists="replace", index=False)
#
#                     # Inserting new entry, stats_df
#                     stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
#                     print('successful, last_df replaced')
#
#                     # To prevent cases such as this:
#                     #
#                     # 52  1515805253  de_cache       live   dumby  T  23.0  3.0  17.0  3.0  56.0  5000.0  1.0  0.0
#                     # 53  1515805254  de_cache   gameover   dumby  T  23.0  4.0  17.0  3.0  57.0  5000.0  1.0  0.0
#     return 'JSON Posted'

from server import *
import webbrowser

if __name__ == "__main__":
    # setup
    db_connection = sqlite3.connect(cs_py.config['DATABASE'])
    init_table_if_not_exists(db_connection)
    setup_gamestate_cfg()

    # auto-opens browser window to CS-Py frontend
    webbrowser.open_new('http://127.0.0.1:5000')
    cs_py.run(debug=False)
