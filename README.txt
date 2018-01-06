CS-Py Installation/Usage Instructions:

1. Place the gamestate_integration_main.cfg file into your csgo/cfg directory. More detailed instructions: https://developer.valvesoftware.com/wiki/Counter-Strike:_Global_Offensive_Game_State_Integration#Locating_CS:GO_Install_Directory

2. Run CS-Py.exe as administrator.

3. When the browser opens:
    a. If this is your first time, then the player database must be created first.
        1. Press the 'Start GS Collection' button and play a competitive game, preferably a standard matchmaking game.
        2. During the game, you can examine your current stats for the match by choosing 'Current Match' to analyze on the browser page.
        3. After the game, you can examine your past game stats by choosing 'Past Match' to analyze on the browser page.
        4. Start collecting when you begin another game, stop afterwards, etc.

    b. If you have already recorded data previously with the program, you can immediately choose to analyze your stats once you start CS-Py.

4. Important notes:
    a. The 'Reset Match' button is meant to be used when you exit a match/game early (say a retake server for example) and want to start another one (like a new MM game).
       Resetting the match makes sure your stats from different games/servers don't get accidentally combined/convoluted.

    b. Due to how CS:GO handles offline bot games, the pistol rounds statistics will be incorrect if data is collected for an offline bot match.

    c. The statistics calculated and data collected by CS-Py has been verified to be correct for MM games and other competitive mode matches. Due to how ESEA Pugs restart the match multiple times before going live, results may vary.
    
    d. This program can record and calculate your performance statistics for matches while the program is running and GS is enabled. Thus, it does not work for games that you have played in the past without having this program running and enabled.

5. Report bugs here: https://github.com/Parkkeo1/CS-Py/issues

6. Further documentation for CS-Py can be found at: https://github.com/Parkkeo1/CS-Py

Created by Parkkeo1: https://github.com/Parkkeo1
