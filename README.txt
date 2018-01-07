CS-Py Installation/Usage Instructions:

      NOTE: CS-Py uses Valve's Game-State Integration (used by tournaments for custom HUDS and by Plays.tv for overlays),
            so using it is fine/legal (and ethical, since it doesn't give you an in-game advantage).
      
      1. Run install_cspy.exe. Follow the instructions on the installer.
      2. After installation, run CS-Py.exe as administrator.
      3. Check to make sure gamestate_integration_main.cfg is in your csgo/cfg directory.
         More detailed instructions: http://bit.ly/2D32JSu (Valve Developer Website/Wiki)
      
      NOTE: CS-Py automatically copies the cfg file into your csgo directory, but you should still check to make sure.
      
      4. When the browser opens:
          a. If this is your first time, then the player database must be created first.
              - Press the 'Start GS Collection' button and play a competitive game, preferably a standard matchmaking game.
              - During the game, you can examine your current stats for the match by choosing 'Current Match' to analyze.
              - After the game, you can examine your past game stats by choosing 'Past Match' to analyze.
              - Start collecting when you begin another game, stop afterwards, etc.
              
          b. If you have already recorded data previously with the program, you can immediately analyze your stats after starting CS-Py.              You can also choose to do the above and collect data while playing a match.
              
      NOTE: CS-Py only collects 'competitive' mode games/matches. Deathmatch and Casual, for example, are ignored.

      5. Important details:
          a. The 'Reset Match' button is for when you exit a match early (i.e. retake server) and want to start a new game (i.e. MM).
             Resetting the match makes sure your stats from different games/servers don't get accidentally combined/convoluted.

          b. Due to how CS:GO handles bot games, the pistol rounds statistics will be incorrect if data is collected for an bot match.
             However, other statistics will still be accurate.

          c. The statistics calculated and data collected by CS-Py has been verified to be correct for MM matches. 
             Due to how ESEA Pugs restart the match multiple times before going live, results may vary.
    
          d. This program can record and calculate your performance statistics for matches while GS is enabled. 
             Thus, it does not work for games that you played in the past without having this program running and enabled.

      6. Report bugs here: https://github.com/Parkkeo1/CS-Py/issues

      7. Further documentation for CS-Py can be found at: https://github.com/Parkkeo1/CS-Py

Created by Parkkeo1/LGIC
