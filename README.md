# CS-Py
A Python Project that uses Valve's client-side [game state integration service](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration) to augment the player experience in Counter-Strike: Global Offensive by analyzing in-game performance with data-driven metrics. By Isaac Park, CS Major @ UIUC.

**Project Status:** v2 is WIP; it will feature a local Flask client and a remote Flask RESTful API Server. I also plan to develop a React.js frontend website to display the match results to the user. The RESTful API server will provide the website with the data.

### Why and How
For a game meant for competitive play, Counter-Strike: Global Offensive surprisingly lacks built-in options by which players can analyze their own performance. In standard match-making, the in-game scoreboard only displays simple statistics (kills, assists, deaths, score, and the number of round "MVPs") that, while useful for cursory glances during the game, are inadequate metrics to accurately gauge player skill. 

Existing third-party websites such as csgo-stats.com seem to mostly provide overly general (total kills, total games played, etc) and often outdated data about players. HLTV.org, while very solid in terms of data and analysis, only keeps track of professional players and matches. 

Thus, CS-Py's purpose, as a local/standalone application, is to expand the number of metrics available to normal players and provide more indicative and accurate analyses of their performance in CS:GO.

As a flask app, CS-Py collects player data at the end of each in-game round from the POST JSON requests that are locally sent by the CS:GO client when GSI is enabled. After storing this information in a SQL table, the app calculates performance metrics such as Headshot Ratio, KAS Percentage, KDR/KDA, and Monetary Dependency that the user can then view in the web browser and filter his/her data by match and time (day, week, month, lifetime). More ideas for analysis are below.

### Project Objectives for v2
1. Overhaul client Flask user application to be object-oriented, efficient, and cleaner in terms of code design. Improved SQL design.
2. Implement new Flask RESTful API server and deploy on PythonAnywhere. This server will store match analysis results for all users.
3. Implement new React.js frontend website that will use the RESTful API to get analysis results and display to the user.

#### --- Below information is only relevant to v1 ---

#### Home Screen of CS-Py When Launched

![Example, Index Page](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/example2.png?raw=true)

#### Results Page

![Example, Results Page](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/example1.png?raw=true)

In the future, I hope to implement remote/cloud SQL DB storage and an in-game GUI transparent overlay that will display live performance statistics for the current match.

### v1.1 Released. Install CS-Py [Here](https://github.com/Parkkeo1/CS-Py/releases/tag/v1.1) For Windows.
- Current statistical features of CS-Py are explained [here.](https://github.com/Parkkeo1/CS-Py/blob/master/documentation/statistics_documentation.md)
- Please report bugs by creating a new issue [here.](https://github.com/Parkkeo1/CS-Py/issues)
