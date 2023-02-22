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

- Year: Table summarizing EPA statistics and prediction accuracy for each year.
- Team: Table summarizing team normalized EPA and match statistics across all years.
- TeamYear: Table summarizing team's EPA and match statistics for a given year.
- Event: Table with event metadata, EPA statistics, and prediction accuracy for each event.
- TeamEvent: Table with team's EPA and match statistics during a given event.
- Match: Table with match metadata, EPA statistics, and prediction accuracy for each match.
- TeamMatch: Table with team's EPA and match statistics during a given match.

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

### TeamYear

### Event

### TeamEvent

### Match

### TeamMatch
