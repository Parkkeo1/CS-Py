### Changelog
12/22/17: Switch to Flask successful (I think). Will be implementing SQLite3 DB functionality instead of using Flask-Session. TODO: put 
received data into pandas dataframe, then insert dataframe contents into sql table. Create DB file.

12/23/17: Previous day's goals accomplished; POST data is put into pandas dataframes and then inserted into SQLite DB tables accordingly: per_round_data and per_map_data. Also made some preliminary frontend changes to set up for the todo. TODO: Work on front-end; auto-refreshing display page for live match stats? Maybe also work on statistical analysis & visualizations using the ideas above.

12/24/17: Continued to work on front-end. Flask app now can receive 1 of 5 possible, different inputs from the user (last match, today, past 7 days, past month, lifetime). TODO: work on creating a query_db function that queries the database table differently depending on user request.

12/25/17: Today was more testing, gathering data, and refining collection methods. Fixed some data collection bugs by editing check_payload. Also edited DB structure and implemented a clean_db function to remove accidental duplicate data from the SQL table. Decided to delete the per_map_data SQL table; unnecessary. Same TODO as yesterday: work on creating a query_db function that queries the database table differently depending on user request.

12/26/17: Changed Data collection approach: changed 'Time' column back to the default UNIX Timestamps and added a 'gameover' event entry to make it easier to sort by individual matches. Tests for these changes were successful. Also worked on a simple HSR calculation function to call in the various query_db functions. Query_db functions return a 'result' dictionary back to the flask main.py. Basic test to display the calculated HSR for the past 24 hours onto the front-end was successful. TODO: keep working on the query_db functions.

12/26/17 (More): WIP start and end data collection functionality/options available to the user (to make sure the user can start collecting performance data for actual matches, not warmup or retake mode games). Using app.config because the default session module did not carry over to GSHandler. Updated front-end. TODO: work on query_db functions and create a helper function to determine entries where map status == 'gameover', in order to pinpoint individual match data.

12/27/17: Collected 2 matches worth of data, with the 'gameover' event entries to mark the end of matches. Finished and successfully tested query_db_match and query_db_time methods. Will be gathering more data later and testing further to make sure each timeframe analysis works. Also fixed some bugs where some flask variable strings/names were mismatched to those in the HTML templates. TODO: create helper function to separate matches and calculate KDR/KDA/KAS functions.

12/28/17: README.md overhaul. Fixed the clean_db() function to ignore the 'Time' column in the dataframe. Added 'Current Match' option and its function, query_db_current, for analyzing current, live match. TODO: work on separate() and kdr/kda/kas functions.

12/291/7: Finished separate() and worked on kdr_kda() in database.py. Separate() returns a list of dataframes (that are chunks of the original dataframe). Have to work on making sure that correct "original" dataframes are fed into the separate and kdr_kda functions when calculating statistics for the various time filters (i.e. make sure to not feed in the entire SQL table for all of them). TODO: Finish kdr_kda, test separate() and kdr_kda().
