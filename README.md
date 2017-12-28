# CS-Py
A Python Project that uses Valve's client-side [game state integration service](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) to augment the player experience in Counter-Strike: Global Offensive by analyzing in-game performance with data-driven metrics. By Isaac Park, CS Major @ UIUC.

### Why and How
For a game meant for competitive play, Counter-Strike: Global Offensive surprisingly lacks built-in options by which players can analyze their own performance. In standard match-making, the in-game scoreboard only displays simple statistics (kills, assists, deaths, score, and the number of round "MVPs") that, while useful for cursory glances during the game, are inadequate metrics to accurately gauge player skill. 

Existing third-party websites such as csgo-stats.com seem to mostly provide overly general (total kills, total games played, etc) and often outdated data about players. HLTV.org, while very solid in terms of data and analysis, only keeps track of professional players and matches. 

Thus, CS-Py's purpose, as a local/standalone application, is to expand the number of metrics available to normal players and provide more indicative and accurate analyses of their performance in CS:GO.

As a flask app, CS-Py collects player data at the end of each in-game round from the POST JSON requests that are locally sent by the CS:GO client when GSI is enabled. After storing this information in a SQL table, the app calculates performance metrics such as Headshot Ratio, KAS Percentage, KDR/KDA, and Monetary Dependency that the user can then view in the web browser and filter his/her data by match and time (day, week, month, lifetime). More ideas for analysis are below.

My current end goal is to package this Python app into a Windows Executable so that any user can use it without having to install Python. In the future, I hope to implement remote/cloud SQL DB storage and an in-game GUI transparent overlay that will display live performance statistics for the current match.

### Installation and Usage (for testing and development purposes)
1. git clone this repository or download it as ZIP.
2. CS-Py has the following dependencies: Python3 (+ SQLite3), Flask, and Pandas.
3. The gamestate_integration_main.cfg file must be placed in the csgo/cfg directory. [More detailed instructions here.](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration#Locating_CS:GO_Install_Directory)
4. Run the flask server by navigating to the local directory where you copied the repository to and then running $ python main.py through terminal.
5. When a new browser tab/window opens up, click 'Start GS Data Collection' to start collecting in-game data for your CS:GO (competitive mode) matches. After playing for a while, you can choose to analyze your performance from the same index page.
6. Make sure to click 'Stop' after your match to prevent the app from collecting data about pseudo-competitive modes such as retakes, etc.

### Project Objectives (By Priority)
1. Implement by-round data storage for statistical analysis using Pandas dataframe.s *Completed 12/23/17*
2. Integrate SQL database functionality and store player data by individual rounds. *Completed 12/23/17*
4. Develop front-end GUI (probably an in-web-browser application) to display player statistics and graphs. *WIP*
4. Develop full-screen (transparent) overlay to be used on top of the CSGO app as a live statistics display in-game.

### Current Ideas For Player Statistics & Analysis
1. KDR and KDA
2. HSR
3. Modified KAST (based on HLTV, but changed to not take traded kills into account).
4. Correlation between # of kills and monetary value of player equipment by round.
5. Using all of the above statistics to determine how well a player overall plays on different maps.
6. Using all of the above statistics to determine how CT/T-sided a player tends to play (overall vs. depending on the map).
7. Graphing these statistics by time to see player's skill improvement. 
