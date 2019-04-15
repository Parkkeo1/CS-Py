## Understanding CS-Py's Statistics

As a program that tracks players' performance in CS:GO, CS-Py generates a variety of metrics about and for the user.
Thus, it is necessary to provide explanations on how these numbers are calculated so that players are able to better gauge their in-game skill. The statistics below are what CS-Py collects and stores into a remote database.

### The Statistics (* in More Details Section)

1. User's Unique Steam ID
2. Start/End UNIX Timestamps for Match
3. Number of Rounds in Match
4. Match Map
5. Kills, Assists, Deaths
6. Score (Same as In-game)
7. HLTV Rating v1.0

#### NOTE: Metrics 8-13 Are Recorded For Both, CT, and T Sides.

8. Headshot Ratio*- The ratio of your kills that end in a headshot (like the in-game killfeed)
9. Monetary Dependency Ratio*
10. Kills Per Round*
11. KAS Percentage*
12. Kill-Death Ratio (KDR), Kill-Assist-Death Ratio (KDA)*
13. Mean Equipment Value*

### More Details

#### Headshot Ratio (HSR)
The ratio of your kills that end in a headshot (like the in-game killfeed)


#### Monetary Dependency Correlation Coefficient (MD Correlation)
The correlation between how many kills you get in each round and your equipment value in that given round. 

This stat is useful for calculating whether a player tends to need better weapons/equipment to play much better (i.e. player relies on having an AWP or a full nadeset to be good) or do as well with all types of low and high tier equipment.


#### Kills Per Round (KPR)
How many kills you get per round, on average. Calculated with: total number of kills / total number of rounds played.


#### KAS Percentage 
Modified version of the KAST statistic by HLTV. CS-Py excludes traded deaths. From HLTV:
> You also may have noticed the addition of KAST (percentage of rounds with a kill, assist, survival or traded death) to our site last month, which is a stat that is best described as round-to-round consistency. It helps us notice players who might not put up the big numbers but often contribute to their team in some fashion.


#### Kill (+ Assist) / Death Ratio (KDR and KDA)
Self-explanatory. Calculated with: total number of kills (+ total number of assists) / total number of deaths. 

In a team game like CS:GO, KDA is more useful.


#### Mean Equipment Value
In dollars, your average equipment value (value of your guns, armor, etc) in the given timeframe (match, day, week, etc).

Shows whether you were able to comfortably full-buy for most of your game(s) or you were constantly eco-ing or force-buying.
