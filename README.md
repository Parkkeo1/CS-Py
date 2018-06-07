# CS-Py
A Python Project that uses Valve's client-side [game state integration service](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) to augment the player experience in Counter-Strike: Global Offensive by analyzing in-game performance with data-driven metrics. By Isaac Park, CS Major @ UIUC.

**Project Status:** Planning to develop this project further during this summer: testing, finding & fixing bugs, optimizing code quality/speed, and working on new patches/releases. See [all issues so far (both opened and closed).](https://github.com/Parkkeo1/CS-Py/issues?utf8=%E2%9C%93&q=is%3Aissue)

### Why and How
For a game meant for competitive play, Counter-Strike: Global Offensive surprisingly lacks built-in options by which players can analyze their own performance. In standard match-making, the in-game scoreboard only displays simple statistics (kills, assists, deaths, score, and the number of round "MVPs") that, while useful for cursory glances during the game, are inadequate metrics to accurately gauge player skill. 

Existing third-party websites such as csgo-stats.com seem to mostly provide overly general (total kills, total games played, etc) and often outdated data about players. HLTV.org, while very solid in terms of data and analysis, only keeps track of professional players and matches. Other websites require users to manurally upload large match-replay files.

Thus, CS-Py's purpose, as a local/standalone application, is to expand the number of metrics available to normal players and provide more indicative and accurate analyses of their performance in CS:GO.

As a Flask web applications, CS-Py parses in-game user data directly from JSON payloads that are exposed by the CS:GO client when GSI is enabled. After storing this information in a SQL table, the app calculates performance metrics such as Headshot Ratio, KAS Percentage (impact and consistency rating), KDR/KDA, and Monetary Dependency rating that the user can then view in the web browser and filter his/her data by match and time (day, week, month, lifetime). More ideas for analysis are below.

#### Home Screen of CS-Py When Launched

![Example, Index Page](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/example2.png?raw=true)

#### Results Page

![Example, Results Page](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/example1.png?raw=true)

In the future, I hope to implement remote/cloud SQL DB storage and an in-game GUI transparent overlay that will display live performance statistics for the current match.

### v1.1 Released. Install CS-Py [Here](https://github.com/Parkkeo1/CS-Py/releases/tag/v1.1) For Windows.
- Current statistical features of CS-Py are explained [here.](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/statistics_documentation.md)
- Please report bugs by creating a new issue [here.](https://github.com/Parkkeo1/CS-Py/issues)

### Installation and Usage
- For developers and contributors: git clone the repository, then in terminal: $ python main.py
- For all other users: [See Releases](https://github.com/Parkkeo1/CS-Py/releases) and [README.txt.](https://github.com/Parkkeo1/CS-Py/blob/master/README.txt)

### Current Ideas For Player Statistics & Analysis
1. KDR and KDA
2. HSR
3. KAS Percentage
4. Correlation between # of kills and monetary value of player equipment by round.
5. Using all of the above statistics to determine how CT/T-sided a player tends to play (overall vs. depending on the map).
6. Specific: pistol round performance: Kills/Pistol Round, HSR, KAS, KDR, etc
7. Kills Per Round; KPR
