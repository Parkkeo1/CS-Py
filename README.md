# CS-Py
A Python Project that uses Valve's game state integration service to augment the player experience in Counter-Strike: Global Offensive. By Isaac Park, CS Major @ UIUC.

### Project Objectives (By Priority)
1. Implement by-round data storage for statistical analysis using Pandas dataframe.s *Completed 12/23/17*
2. Integrate SQL database functionality and store player data by individual rounds. *Completed 12/23/17*
3. Integrate Logitech's RGB SDK for its gaming mice to trigger colors depending on in-game events.
4. Develop front-end GUI for the program (probably an in-web-browser application) to display player statistics and graphs.
5. Develop full-screen (transparent) overlay to be used on top of the CSGO application as a live statistics display for the player.

### Current Ideas For Player Statistics & Analysis
1. KDR and KDA
2. HSR
3. Modified KAST (based on HLTV, but changed to not take traded kills into account).
4. Correlation between # of kills and monetary value of primary + secondary weapon in each round
5. Using all of the above statistics to determine how well a player overall plays on different maps.
6. Using all of the above statistics to determine how CT/T-sided a player tends to play (overall vs. depending on the map).
7. Graphing these statistics by time to see player's skill improvement. 

### Changelog
12/22/17: Switch to Flask successful (I think). Will be implementing SQLite3 DB functionality instead of using Flask-Session. TODO: put 
received data into pandas dataframe, then insert dataframe contents into sql table. Create DB file.

12/23/17: Previous day's goals accomplished; POST data is put into pandas dataframes and then inserted into SQLite DB tables accordingly: per_round_data and per_map_data. Also made some preliminary frontend changes to set up for the todo. TODO: Work on front-end; auto-refreshing display page for live match stats? Maybe also work on statistical analysis & visualizations using the ideas above.

12/24/17: Continued to work on front-end. Flask app now can receive 1 of 5 possible, different inputs from the user (last match, today, past 7 days, past month, lifetime). TODO: work on creating a query_db function that queries the database table differently depending on user request.
