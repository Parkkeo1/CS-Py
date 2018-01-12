# CS-Py
A Python Project that uses Valve's client-side [game state integration service](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) to augment the player experience in Counter-Strike: Global Offensive by analyzing in-game performance with data-driven metrics. By Isaac Park, CS Major @ UIUC.

### Why and How
For a game meant for competitive play, Counter-Strike: Global Offensive surprisingly lacks built-in options by which players can analyze their own performance. In standard match-making, the in-game scoreboard only displays simple statistics (kills, assists, deaths, score, and the number of round "MVPs") that, while useful for cursory glances during the game, are inadequate metrics to accurately gauge player skill. 

Existing third-party websites such as csgo-stats.com seem to mostly provide overly general (total kills, total games played, etc) and often outdated data about players. HLTV.org, while very solid in terms of data and analysis, only keeps track of professional players and matches. 

Thus, CS-Py's purpose, as a local/standalone application, is to expand the number of metrics available to normal players and provide more indicative and accurate analyses of their performance in CS:GO.

As a flask app, CS-Py collects player data at the end of each in-game round from the POST JSON requests that are locally sent by the CS:GO client when GSI is enabled. After storing this information in a SQL table, the app calculates performance metrics such as Headshot Ratio, KAS Percentage, KDR/KDA, and Monetary Dependency that the user can then view in the web browser and filter his/her data by match and time (day, week, month, lifetime). More ideas for analysis are below.

In the future, I hope to implement remote/cloud SQL DB storage and an in-game GUI transparent overlay that will display live performance statistics for the current match.

### v1.0 Released. Install CS-Py [Here](https://github.com/Parkkeo1/CS-Py/releases/tag/v1.0) As A Windows program.
- Current statistical features of CS-Py are explained [here.](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/statistics_documentation.md)
- Please report bugs by creating a new issue [here.](https://github.com/Parkkeo1/CS-Py/issues)

### Installation and Usage
- For developers and contributors: git clone the repository, then in terminal: $ python main.py
- For all other users: [See Releases](https://github.com/Parkkeo1/CS-Py/releases) and [README.txt.](https://github.com/Parkkeo1/CS-Py/blob/master/README.txt)

### Project Objectives (By Priority)
1. Implement by-round data storage for statistical analysis using Pandas dataframe.s *Completed 12/23/17*
2. Integrate SQL database functionality and store player data by individual rounds. *Completed 12/23/17*
4. Develop front-end GUI (i.e. web application) to display player statistics and graphs. *Completed 1/10/18*
4. Develop transparent screen overlay to be used on top of the CSGO app as a live statistics display.

### Current Ideas For Player Statistics & Analysis
1. KDR and KDA
2. HSR
3. KAS Percentage
4. Correlation between # of kills and monetary value of player equipment by round.
5. Using all of the above statistics to determine how CT/T-sided a player tends to play (overall vs. depending on the map).
6. Specific: pistol round performance: Kills/Pistol Round, HSR, KAS, KDR, etc
7. Kills Per Round; KPR
