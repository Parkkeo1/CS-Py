# CS-Py (WIP v2)
A performance analytics tool for CS:GO that analyzes players' data to provide deep insights into their skill through detailed metrics such as consistency, accuracy, and impact per game (ex. HLTV Rating, KAS %, HSR). Features a Python-Flask & SQL local client and remote RESTful API server. By Isaac Park, CS Major @ UIUC.

**Project Status:** v2 is WIP; it will feature a local Flask client and a remote Flask RESTful API Server. I also plan to develop a React.js frontend website to display the match results to the user. The RESTful API server will provide the website with the data.

### Why and How
For a game meant for competitive play, Counter-Strike: Global Offensive surprisingly lacks built-in options by which players can analyze their own performance. In standard match-making, the in-game scoreboard only displays simple statistics (kills, assists, deaths, score, and the number of round "MVPs") that, while useful for cursory glances during the game, are inadequate metrics to accurately gauge player skill. **Edit**: Even after the new Panorama update, certain detailed statistics are missing in the default game.

Existing third-party websites such as csgo-stats.com seem to mostly provide overly general (total kills, total games played, etc) and often outdated data about players. Most of these website services require users to manually download their demo replay files from the CS:GO client and upload them. Along with this inconvenience, demo files are known to often be corrupted. HLTV.org, while very solid in terms of data and analysis, only keeps track of professional players and matches. 

Thus, CS-Py's purpose, as an user & web application, is to expand the number of metrics available to normal players and provide more indicative and accurate analyses of their performance in CS:GO.

CS-Py is made possible by CS:GO's developer feature: [Game-State Integration](https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration). JSON payloads containing real-time game data are rapidly sent (every 1-2 seconds) by the CS:GO client and are processed/analyzed for player performance. The calculated metrics and results are stored in a SQLite database and then sent to the remote REST API. I plan to implement a separate front-end web app, probably with React.js and Express.js, that will use the data from the API to display the analysis results to users. 

### Project Objectives for v2
1. Overhaul client Flask user application to be object-oriented, efficient, and cleaner in terms of code design. Improved SQL design.
2. Implement new Flask RESTful API server and deploy on PythonAnywhere. This server will store match analysis results for all users.
3. Implement new React.js frontend website that will use the RESTful API to get analysis results and display to the user.

### v1.1 Released. Install CS-Py [Here](https://github.com/Parkkeo1/CS-Py/releases/tag/v1.1) For Windows.
- **Note**: v1 is the old release; CS-Py is a standalone, local Flask application and not a client-server web app.
- Current statistical features of CS-Py are explained [here.](https://github.com/Parkkeo1/CS-Py/blob/master/docs/stats.md)
- Please report bugs by creating a new issue [here.](https://github.com/Parkkeo1/CS-Py/issues)
