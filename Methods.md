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
