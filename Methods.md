## Statbotics.io

This document will serve as documentation for the data, mathematics and programming behind Statbotics.io. This document, coupled with the open-source Github code, should explain all the results shown on the website and APIs.
If there are further questions, please do not hesitate to reach out to me on Chief Delphi (Strategos) or by email (avgupta456@gmail.com). Thank you!

## Overview

Our mission is to develop and distribute FRC data analysis. Currently, we have calculated Elo Ratings, (component) OPRs, RP strengths, and win-loss records. These statistics are available through interactive tables, a REST API, and a Python library. Using these metrics, we have developed match predictions and a complete event simulator. We hope to continue adding new features, such as Zebra MotionWorks analysis and more predictive modeling.

### Elo

Elo is a measure of a team's on-field strength, calculated using win margins from over 100,000 matches dating back to 2002. An Elo of 1500 is roughly average, while an Elo of 1800+ is in the top 1% worldwide. At Statbotics, browse Elo ratings for teams, seasons, and events.

### OPR

OPR uses linear algebra to estimate a team's contribution to an alliance. Statbotics.io makes OPR and component OPR (Auto, Teleop, Endgame) data easily accessible for teams and events. For recent years, Ranking Point strengths are available as well.

### Insights

Combining Elo and OPR data from all prior matches, Statbotics.io allows users to quickly pull up and compare stats across teams. Find which teams performed the best this year, or the sleeper picks at your event.

### Predictions

Taking insights one step further, Statbotics.io leverages Elo and OPR statistics for accurate match prediction and event simulation. These tools can help your team make strategic decisions and win matches.

## Data

Our database contains information on teams, events, and matches from 2002 onwards. We have stored the data in a relational database with seven tables, interconnected with one-to-one and many-to-one relationships.

### Years

This table has one entry for each year from 2002-Present, and contains information on mean scores (for normalization) and Elo and OPR percentiles (for health checks).

### Teams

This table contains an entry for each team that has played at least one match since 2002. As of 2020, there are some ~6500 rows in this table. For each team, the team name, location, district, active status, etc. are scraped from The Blue Alliance. Additionally, some Elo and win rate statistics are calculated and stored.

### Events

This table hosts all the events since 2002, roughly 1500 entries. For each event, the name and location are recorded (scraped from The Blue Alliance), as well as stats on the Elo and OPR distribution at the event.

### Matches

This table contains ~150,000 entries, one for each match played since 2002. For each match, a detailed score breakdown for both alliances is recorded, as well as the predicted and actual winner (for later tabulation).

### TeamYears

TeamYears is a cross between Teams and Year. As of 2020, there are ~37,000 entries. Each contains foreign keys to the team and year, Elo and OPR statistics from the given year, and win rates.

### TeamEvents

TeamEvents is a cross between Teams and Events. As of 2020, there are ~70,000 entries. Each contains foreign keys to the team and event, Elo and OPR statistics from the given event, the team's rank at the event, and win rates.

### TeamMatches

The largest table in the database, this contains all team-match pairs (nearly one million). Each row has foreign keys, and basic Elo and OPR statistics.

## Mathematics

The majority of the calculations are run in Python (statbotics_calc), and stored in the MySQL database described above.

### Elo

From Wikipedia, "the Elo[a] rating system is a method for calculating the relative skill levels of players in zero-sum games such as chess. It is named after its creator Arpad Elo, a Hungarian-American physics professor." Caleb Sykes modified Elo for use in alliance-based FRC, and my current implementation follows closely to his model. At its root, Elo assigns a rating to all players, and then after a match, updates the participant's rating based on the outcome.

All teams in 2002 were initialized with an Elo of 1500. From then on, new rookies were initialized with an Elo of 1450. After a match between the red alliance (with Elos r1, r2, r3) and the blue alliance (with Elos b1, b2, b3), the Elos are updated as follows:

```
red_sum = r1 + r2 + r3
blue_sum = b1 + b2 + b3

predicted_red_win_margin = 0.004 * (red_sum - blue_sum)
normalized_red_win_margin = red_win_margin / sd_score  # standard deviation
update = K * (normalized_red_win_margin - predicted_red_win_margin)

r1', r2', r3' = r1 + update, r2 + update, r3 + update
b1', b2', b3' = b1 - update, b2 - update, b3 - update
```

The constant K can be varied to tune the sensitivity of the model to new results. For best results, Caleb has found K=12 for qualification matches and K=4 for playoff matches works fairly well. This process is run on sequential matches for a given year to generate Elo ratings.

Between years, the predictive power of Elo is improved by applying mean reversion. Essentially, an above average team will generally be less above average the following year, and a below average team will generally be less below average the following year. Mean reversion with a two year history helps avoid sharp overreactions to one bad year.

```
elo_last_year, elo_this_year
elo_next_year = 0.2 * 1500 + 0.8 * (0.7 * elo_last_year + 0.3 * elo_this_year) 
              = 300 + 0.56 * elo_last_year + 0.24 * elo_this_year
```

These parameters were found by Caleb Sykes. Finally, given a set of Elos before a certain match, a logistic distribution can be used to predict the outcome between the red alliance (with Elos r1, r2, r3) and blue alliance (with Elos b1, b2, b3)

```
red_sum = r1 + r2 + r3
blue_sum = b1 + b2 + b3

red_win_prob = 1 / (1 + 10 ** ((blue_sum - red_sum) / 400))
```

And that's all! Some modifications are currently in the work to help prevent outliers and more quickly adjust to team performance at the beginning of each season.

### OPR and ILS

OPR stands for Offensive Power Rating, and uses linear algebra to estimate a team's actual contribution to an alliance. OPR is a fairly well understood metric in FRC, so I will be linking some resources that can do a much better job explaining than me. 

I believe Karthik from 1114 developed OPR as early as 2004: https://www.youtube.com/watch?v=l8syuYnXfJg&feature=youtu.be&t=6m49s

A TBA blog introducing the concept: https://blog.thebluealliance.com/2017/10/05/the-math-behind-opr-an-introduction/

How OPR can be used for strategy: https://blog.thebluealliance.com/2017/11/06/opr-you-basic-frc-strategy/

Deep dive into multiple OPR variants: https://brennonbrimhall.github.io/2020/06/18/predicting-matches-opr/

Hopefully after reading those (especially the first two links), you have a decent idea of what OPR is. As with most linear algebra, OPR can give crazy results with insufficient data. To make better predictions at the beginning of an event, where only a handful of matches have been played, we use ixOPR, which iteratively optimizes the OPR from a seed value. You can read about this method here (credit to Eugene Fang): https://github.com/the-blue-alliance/the-blue-alliance/pull/1478#issuecomment-210564302

Regarding the actual seed value, I follow Caleb Sykes methodology in using the most recent event's Max OPR. If the most recent event is from the previous season, the OPR is normalized to the new season's scoring using the mean week 1 score, and 10% mean reversion is applied. If the team has never played an event before, the mean OPR is used as the seed.

ILS stands for Iterative Logistic Strength, and aims to measure a team's contribution to ranking points (2016-Present) similar to how OPR measures contributions towards score. However, ILS follows an approach more like Elo in computing its values. I have imitated Caleb Sykes' algorithm verbatim, read about it here: https://blog.thebluealliance.com/2019/08/04/making-better-rp-predictions/

All constants for the Elo, OPR, and ILS models can be found in the Python code - statbotics_calc/models/*
