# Statbotics API

In addition to the website, Statbotics makes data available through both a REST API and Python API. These APIs interface with same the database that powers the website. In these docs, I will briefly describe the REST and Python APIs, and then provide a detailed schema of the database.

## REST API

The REST API is available at https://api.statbotics.io/v2/. The Swagger documentation for the API is available at https://www.statbotics.io/api/rest.

For example, to get data associated with 254's undefeated 2018 season, you can query the following URL: https://api.statbotics.io/v2/team_year/254/2018.

## Python API

The Python API is available at https://pypi.org/project/statbotics. The documentation for the API is available at https://www.statbotics.io/api/python.

To use the Python API, you can install it with pip:

```bash
pip install statbotics
```

Then, you can import it and use it to make the request:

```python
import statbotics

sb = statbotics.Statbotics()

print(sb.get_team_year(254, 2018))
```

## Database Schema

The Statbotics database includes the following tables:

- **Year**: Table summarizing EPA statistics and prediction accuracy for each year.
- **Team**: Table summarizing team normalized EPA and match statistics across all years.
- **TeamYear**: Table summarizing team's EPA and match statistics for a given year.
- **Event**: Table with event metadata, EPA statistics, and prediction accuracy for each event.
- **TeamEvent**: Table with team's EPA and match statistics during a given event.
- **Match**: Table with match metadata, EPA statistics, and prediction accuracy for each match.
- **TeamMatch**: Table with team's EPA and match statistics during a given match.

### Year

| Column             | Type  | Description                                                      |
| ------------------ | ----- | ---------------------------------------------------------------- |
| year               | int   | Year of the season.                                              |
| epa_max            | float | Maximum team end-of-season EPA for the year.                     |
| epa_1p             | float | 1st percentile team end-of-season EPA.                           |
| epa_5p             | float | 5th percentile team end-of-season EPA.                           |
| epa_10p            | float | 10th percentile team end-of-season EPA.                          |
| epa_25p            | float | 25th percentile team end-of-season EPA.                          |
| epa_median         | float | Median team end-of-season EPA.                                   |
| epa_75p            | float | 75th percentile team end-of-season EPA.                          |
| epa_mean           | float | Mean team end-of-season EPA.                                     |
| epa_sd             | float | Standard deviation of team end-of-season EPA.                    |
| auto_epa_max       | float | Maximum team end-of-season auto EPA for the year.                |
| auto_epa_1p        | float | 1st percentile team end-of-season auto EPA.                      |
| auto_epa_5p        | float | 5th percentile team end-of-season auto EPA.                      |
| auto_epa_10p       | float | 10th percentile team end-of-season auto EPA.                     |
| auto_epa_25p       | float | 25th percentile team end-of-season auto EPA.                     |
| auto_epa_median    | float | Median team end-of-season auto EPA.                              |
| auto_epa_75p       | float | 75th percentile team end-of-season auto EPA.                     |
| auto_epa_mean      | float | Mean team end-of-season auto EPA.                                |
| auto_epa_sd        | float | Standard deviation of team end-of-season auto EPA.               |
| teleop_epa_max     | float | Maximum team end-of-season teleop EPA for the year.              |
| teleop_epa_1p      | float | 1st percentile team end-of-season teleop EPA.                    |
| teleop_epa_5p      | float | 5th percentile team end-of-season teleop EPA.                    |
| teleop_epa_10p     | float | 10th percentile team end-of-season teleop EPA.                   |
| teleop_epa_25p     | float | 25th percentile team end-of-season teleop EPA.                   |
| teleop_epa_median  | float | Median team end-of-season teleop EPA.                            |
| teleop_epa_75p     | float | 75th percentile team end-of-season teleop EPA.                   |
| teleop_epa_mean    | float | Mean team end-of-season teleop EPA.                              |
| teleop_epa_sd      | float | Standard deviation of team end-of-season teleop EPA.             |
| endgame_epa_max    | float | Maximum team end-of-season endgame EPA for the year.             |
| endgame_epa_1p     | float | 1st percentile team end-of-season endgame EPA.                   |
| endgame_epa_5p     | float | 5th percentile team end-of-season endgame EPA.                   |
| endgame_epa_10p    | float | 10th percentile team end-of-season endgame EPA.                  |
| endgame_epa_25p    | float | 25th percentile team end-of-season endgame EPA.                  |
| endgame_epa_median | float | Median team end-of-season endgame EPA.                           |
| endgame_epa_75p    | float | 75th percentile team end-of-season endgame EPA.                  |
| endgame_epa_mean   | float | Mean team end-of-season endgame EPA.                             |
| endgame_epa_sd     | float | Standard deviation of team end-of-season endgame EPA.            |
| rp_1_epa_max       | float | Maximum team end-of-season RP1 EPA for the year.                 |
| rp_1_epa_1p        | float | 1st percentile team end-of-season RP1 EPA.                       |
| rp_1_epa_5p        | float | 5th percentile team end-of-season RP1 EPA.                       |
| rp_1_epa_10p       | float | 10th percentile team end-of-season RP1 EPA.                      |
| rp_1_epa_25p       | float | 25th percentile team end-of-season RP1 EPA.                      |
| rp_1_epa_median    | float | Median team end-of-season RP1 EPA.                               |
| rp_1_epa_75p       | float | 75th percentile team end-of-season RP1 EPA.                      |
| rp_1_epa_mean      | float | Mean team end-of-season RP1 EPA.                                 |
| rp_1_epa_sd        | float | Standard deviation of team end-of-season RP1 EPA.                |
| rp_2_epa_max       | float | Maximum team end-of-season RP2 EPA for the year.                 |
| rp_2_epa_1p        | float | 1st percentile team end-of-season RP2 EPA.                       |
| rp_2_epa_5p        | float | 5th percentile team end-of-season RP2 EPA.                       |
| rp_2_epa_10p       | float | 10th percentile team end-of-season RP2 EPA.                      |
| rp_2_epa_25p       | float | 25th percentile team end-of-season RP2 EPA.                      |
| rp_2_epa_median    | float | Median team end-of-season RP2 EPA.                               |
| rp_2_epa_75p       | float | 75th percentile team end-of-season RP2 EPA.                      |
| rp_2_epa_mean      | float | Mean team end-of-season RP2 EPA.                                 |
| rp_2_epa_sd        | float | Standard deviation of team end-of-season RP2 EPA.                |
| epa_quals_acc      | float | Accuracy of EPA model on all quals matches.                      |
| epa_quals_mse      | float | Mean squared error of EPA model on all quals matches.            |
| quals_count        | int   | Number of quals matches.                                         |
| epa_elims_acc      | float | Accuracy of EPA model on all elims matches.                      |
| epa_elims_mse      | float | Mean squared error of EPA model on all elims matches.            |
| elims_count        | int   | Number of elims matches.                                         |
| epa_champs_acc     | float | Accuracy of EPA model on all champs matches.                     |
| epa_champs_mse     | float | Mean squared error of EPA model on all champs matches.           |
| champs_count       | int   | Number of champs matches.                                        |
| epa_acc            | float | Accuracy of EPA model on all matches.                            |
| epa_mse            | float | Mean squared error of EPA model on all matches.                  |
| count              | int   | Number of matches.                                               |
| rp_1_acc           | float | Accuracy of RP1 model on qualification matches.                  |
| rp_1_mse           | float | Mean squared error of RP1 model on qualification matches.        |
| rp_1_champs_acc    | float | Accuracy of RP1 model on champs qualification matches.           |
| rp_1_champs_mse    | float | Mean squared error of RP1 model on champs qualification matches. |
| rp_2_acc           | float | Accuracy of RP2 model on qualification matches.                  |
| rp_2_mse           | float | Mean squared error of RP2 model on qualification matches.        |
| rp_2_champs_acc    | float | Accuracy of RP2 model on champs qualification matches.           |
| rp_2_champs_mse    | float | Mean squared error of RP2 model on champs qualification matches. |
| rp_champs_count    | int   | 2 \* number of champs qualification matches.                     |
| rp_count           | int   | 2 \* number of qualification matches.                            |
| score_mean         | float | Mean score of Week 1 matches.                                    |
| score_sd           | float | Standard deviation of score of Week 1 matches.                   |
| auto_mean          | float | Mean auto score of Week 1 matches.                               |
| teleop_mean        | float | Mean teleop score of Week 1 matches.                             |
| endgame_mean       | float | Mean endgame score of Week 1 matches.                            |
| fouls_mean         | float | Mean fouls of Week 1 matches.                                    |
| no_fouls_mean      | float | Mean no-fouls score of Week 1 matches.                           |
| rp_1_mean          | float | Mean RP1 rate of Week 1 qualification matches.                   |
| rp_2_mean          | float | Mean RP2 rate of Week 1 qualification matches.                   |

### Team

| Column          | Type  | Description                                                               |
| --------------- | ----- | ------------------------------------------------------------------------- |
| team            | int   | Team number.                                                              |
| name            | str   | Team name.                                                                |
| offseason       | bool  | Whether this team only competes in the offseason (ex. 99XX)               |
| state           | str   | State/province abbreviation of team's location. Valid for USA and Canada. |
| country         | str   | Country of team's location.                                               |
| district        | str   | District abbreviationteam competes in (if any).                           |
| rookie_year     | int   | Year team first competed.                                                 |
| active          | bool  | Whether the team is competing in the current season.                      |
| norm_epa        | float | Normalized EPA of the team in the last complete season.                   |
| norm_epa_recent | float | Mean of normalized EPA of the team in the last 5 seasons.                 |
| norm_epa_mean   | float | Mean of normalized EPA of the team in all seasons.                        |
| norm_epa_max    | float | Maximum normalized EPA of the team in all seasons.                        |
| wins            | int   | Number of wins across all official matches.                               |
| losses          | int   | Number of losses across all official matches.                             |
| ties            | int   | Number of ties across all official matches.                               |
| count           | int   | Number of official matches played in.                                     |
| winrate         | float | Win rate across all official matches.                                     |
| full_wins       | int   | Number of wins across all official and offseason matches.                 |
| full_losses     | int   | Number of losses across all official and offseason matches.               |
| full_ties       | int   | Number of ties across all official and offseason matches.                 |
| full_count      | int   | Number of official and offseason matches played in.                       |
| full_winrate    | float | Win rate across all official and offseason matches.                       |

### TeamYear

| Column                  | Type  | Description                                                                     |
| ----------------------- | ----- | ------------------------------------------------------------------------------- |
| year                    | int   | Year.                                                                           |
| team                    | int   | Team number                                                                     |
| offseason               | bool  | Whether this team only competes in the offseason (ex. 99XX)                     |
| name                    | str   | Team name.                                                                      |
| state                   | str   | State/province abbreviation of team's location. Valid for USA and Canada.       |
| country                 | str   | Country of team's location.                                                     |
| district                | str   | District abbreviationteam competes in (if any).                                 |
| epa_start               | float | EPA at the start of the season.                                                 |
| epa_pre_champs          | float | EPA prior to the start of champs.                                               |
| epa_end                 | float | EPA at the end of the season.                                                   |
| epa_mean                | float | Mean EPA of the team in the season.                                             |
| epa_max                 | float | Maximum EPA of the team in the season.                                          |
| epa_diff                | float | Difference between the start and end of season EPA.                             |
| auto_epa_start          | float | Auto EPA at the start of the season.                                            |
| auto_epa_pre_champs     | float | Auto EPA prior to the start of champs.                                          |
| auto_epa_end            | float | Auto EPA at the end of the season.                                              |
| auto_epa_mean           | float | Mean auto EPA of the team in the season.                                        |
| auto_epa_max            | float | Maximum auto EPA of the team in the season.                                     |
| teleop_epa_start        | float | Teleop EPA at the start of the season.                                          |
| teleop_epa_pre_champs   | float | Teleop EPA prior to the start of champs.                                        |
| teleop_epa_end          | float | Teleop EPA at the end of the season.                                            |
| teleop_epa_mean         | float | Mean teleop EPA of the team in the season.                                      |
| teleop_epa_max          | float | Maximum teleop EPA of the team in the season.                                   |
| endgame_epa_start       | float | Endgame EPA at the start of the season.                                         |
| endgame_epa_pre_champs  | float | Endgame EPA prior to the start of champs.                                       |
| endgame_epa_end         | float | Endgame EPA at the end of the season.                                           |
| endgame_epa_mean        | float | Mean endgame EPA of the team in the season.                                     |
| endgame_epa_max         | float | Maximum endgame EPA of the team in the season.                                  |
| rp_1_epa_start          | float | RP1 EPA at the start of the season.                                             |
| rp_1_epa_pre_champs     | float | RP1 EPA prior to the start of champs.                                           |
| rp_1_epa_end            | float | RP1 EPA at the end of the season.                                               |
| rp_1_epa_mean           | float | Mean RP1 EPA of the team in the season.                                         |
| rp_1_epa_max            | float | Maximum RP1 EPA of the team in the season.                                      |
| rp_2_epa_start          | float | RP2 EPA at the start of the season.                                             |
| rp_2_epa_pre_champs     | float | RP2 EPA prior to the start of champs.                                           |
| rp_2_epa_end            | float | RP2 EPA at the end of the season.                                               |
| rp_2_epa_mean           | float | Mean RP2 EPA of the team in the season.                                         |
| rp_2_epa_max            | float | Maximum RP2 EPA of the team in the season.                                      |
| norm_epa_end            | float | Normalized EPA at the end of the season.                                        |
| wins                    | int   | Number of wins across all official matches.                                     |
| losses                  | int   | Number of losses across all official matches.                                   |
| ties                    | int   | Number of ties across all official matches.                                     |
| count                   | int   | Number of official matches played in.                                           |
| winrate                 | float | Win rate across all official matches.                                           |
| full_wins               | int   | Number of wins across all official and offseason matches.                       |
| full_losses             | int   | Number of losses across all official and offseason matches.                     |
| full_ties               | int   | Number of ties across all official and offseason matches.                       |
| full_count              | int   | Number of official and offseason matches played in.                             |
| full_winrate            | float | Win rate across all official and offseason matches.                             |
| total_epa_rank          | int   | Rank of the team's end-of-season EPA among all teams                            |
| total_epa_percentile    | float | Percentile of the team's end-of-season EPA among all teams                      |
| total_team_count        | int   | Number of teams that played in the season                                       |
| country_epa_rank        | int   | Rank of the team's end-of-season EPA among all teams in the same country        |
| country_epa_percentile  | float | Percentile of the team's end-of-season EPA among all teams in the same country  |
| country_team_count      | int   | Number of teams that played in the season in the same country                   |
| state_epa_rank          | int   | Rank of the team's end-of-season EPA among all teams in the same state          |
| state_epa_percentile    | float | Percentile of the team's end-of-season EPA among all teams in the same state    |
| state_team_count        | int   | Number of teams that played in the season in the same state                     |
| district_epa_rank       | int   | Rank of the team's end-of-season EPA among all teams in the same district       |
| district_epa_percentile | float | Percentile of the team's end-of-season EPA among all teams in the same district |
| district_team_count     | int   | Number of teams that played in the season in the same district                  |

### Event

| Column | Type | Description |
| ------ | ---- | ----------- |

### TeamEvent

| Column | Type | Description |
| ------ | ---- | ----------- |

### Match

| Column | Type | Description |
| ------ | ---- | ----------- |

### TeamMatch

| Column | Type | Description |
| ------ | ---- | ----------- |
