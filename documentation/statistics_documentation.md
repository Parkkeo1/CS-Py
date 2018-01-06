## Understanding CS-Py's Statistics

As a program that tracks players' performance in CS:GO, CS-Py generates a variety of metrics about and for the user.
Thus, it is necessary to provide explanations on how these numbers are calculated so that players are able to better gauge their in-game skill.

### The Statistics

#### Headshot Ratio (HSR)
The ratio of your kills that end in a headshot (like the in-game killfeed). Calculated with: total number of headshot kills / total number of kills.

Useful for gauging your aim.

#### Kills Per Round (KPR)
How many kills you get per round, on average. Calculated with: total number of kills / total number of rounds played.

How deadly are you?

#### KAS Percentage 
Modified version of the KAST statistic by HLTV. CS-Py excludes traded deaths. From HLTV:
> You also may have noticed the addition of KAST (percentage of rounds with a kill, assist, survival or traded death) to our site last month, which is a stat that is best described as round-to-round consistency. It helps us notice players who might not put up the big numbers but often contribute to their team in some fashion.

#### Kill (+ Assist) / Death Ratio (KDR and KDA)
Self-explanatory. Calculated with: total number of kills (+ total number of assists) / total number of deaths. 

In a team game like CS:GO, KDA is more useful.

#### Mean Equipment Value
In dollars, your average equipment value (value of your guns, armor, etc) in the given timeframe (match, day, week, etc).

Shows whether you were able to comfortably full-buy for most of your game(s) or you were constantly eco-ing or force-buying.

#### Monetary Dependency Correlation Coefficient (MD Correlation)
The correlation between how many kills you get in each round and your equipment value in that given round. 

This stat is useful for calculating whether a player tends to need better weapons/equipment to play much better (i.e. player relies on having an AWP or a full nadeset to be good) or do as well with all types of low and high tier equipment.

#### WIP, to be added.

### The Graphs

#### Rounds Player By Map
Self-explanatory. Shows how much you play many different maps or just a handful.

#### Kill/Round vs. Equipment Value
The MD correlation in graph form. The regression slope would be the correlation coefficient.

#### WIP, to be added.