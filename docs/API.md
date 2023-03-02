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

### Standardizing Year-Specific Data

Before diving into the tables, I want to clarify the data methodology for storing results from multiple years. Although the game changes year to year, since 2016 a consistent set of components have been used: Auto, Teleop, Endgame, Fouls, RP1, and RP2.

#### 2002-2015

Component and RP columns are left empty and data is stored in the `total` column.

#### 2016

The auto component represents points scored in the autonomous period. Teleop includes both crossing and boulder points. Endgame includes challenge and scale. RP1 is for breaching the outer works and RP2 is for capturing the tower.

#### 2017

The auto component represents points scored in the autonomous period. Teleop includes both rotor and fuel points. Endgame includes takeoff points. RP1 is for the rotor ranking point, and RP2 is for the kPa ranking point.

#### 2018

The auto component represents points scored in the autonomous period. Teleop includes switch and scale ownership and valut points. Endgame includes climb points. RP1 is for the auto quest ranking point, and RP2 is for the Face the Boss ranking point.

#### 2019

The auto component represents points scored in the autonomous period. Teleop includes hatch and cargo points on the rocket and cargo ship. Endgame includes HAB climb points. RP1 is for completing the rocket and RP2 is for the HAB docking ranking point.

#### 2020

The auto component represents points scored in the autonomous period. Teleop includes cell points in the lower, outer, and inner goals. Endgame includes climb points. RP1 is the Shield Energized ranking point and RP2 is the Shield Operational ranking point.

#### 2021

No data is stored for 2021.

#### 2022

The auto component represents points scored in the autonomous period. Teleop includes cargo in the upper and lower goals. Endgame includes climb points. RP1 is the Cargo Bonus ranking point and RP2 is the Hanger Bonus ranking point.

#### 2023

The auto component represents points scored in the autonomous period. Teleop includes game piece and link points. Endgame includes park and charge station points. RP1 is the Sustainability Bonus ranking point and RP2 is the Activation Bonus ranking point.

#### Future Years

I will update this section as new years are added. The breakdown is implemented in the `backend/src/tba/clean_data.py` file (`get_breakdown()` function).

### Year

| Column             | Type  | Description                                                     |
| ------------------ | ----- | --------------------------------------------------------------- |
| year               | int   | Year of the season                                              |
| epa_max            | float | Maximum team end-of-season EPA for the year                     |
| epa_1p             | float | 1st percentile team end-of-season EPA                           |
| epa_5p             | float | 5th percentile team end-of-season EPA                           |
| epa_10p            | float | 10th percentile team end-of-season EPA                          |
| epa_25p            | float | 25th percentile team end-of-season EPA                          |
| epa_median         | float | Median team end-of-season EPA                                   |
| epa_75p            | float | 75th percentile team end-of-season EPA                          |
| epa_mean           | float | Mean team end-of-season EPA                                     |
| epa_sd             | float | Standard deviation of team end-of-season EPA                    |
| auto_epa_max       | float | Maximum team end-of-season auto EPA for the year                |
| auto_epa_1p        | float | 1st percentile team end-of-season auto EPA                      |
| auto_epa_5p        | float | 5th percentile team end-of-season auto EPA                      |
| auto_epa_10p       | float | 10th percentile team end-of-season auto EPA                     |
| auto_epa_25p       | float | 25th percentile team end-of-season auto EPA                     |
| auto_epa_median    | float | Median team end-of-season auto EPA                              |
| auto_epa_75p       | float | 75th percentile team end-of-season auto EPA                     |
| auto_epa_mean      | float | Mean team end-of-season auto EPA                                |
| auto_epa_sd        | float | Standard deviation of team end-of-season auto EPA               |
| teleop_epa_max     | float | Maximum team end-of-season teleop EPA for the year              |
| teleop_epa_1p      | float | 1st percentile team end-of-season teleop EPA                    |
| teleop_epa_5p      | float | 5th percentile team end-of-season teleop EPA                    |
| teleop_epa_10p     | float | 10th percentile team end-of-season teleop EPA                   |
| teleop_epa_25p     | float | 25th percentile team end-of-season teleop EPA                   |
| teleop_epa_median  | float | Median team end-of-season teleop EPA                            |
| teleop_epa_75p     | float | 75th percentile team end-of-season teleop EPA                   |
| teleop_epa_mean    | float | Mean team end-of-season teleop EPA                              |
| teleop_epa_sd      | float | Standard deviation of team end-of-season teleop EPA             |
| endgame_epa_max    | float | Maximum team end-of-season endgame EPA for the year             |
| endgame_epa_1p     | float | 1st percentile team end-of-season endgame EPA                   |
| endgame_epa_5p     | float | 5th percentile team end-of-season endgame EPA                   |
| endgame_epa_10p    | float | 10th percentile team end-of-season endgame EPA                  |
| endgame_epa_25p    | float | 25th percentile team end-of-season endgame EPA                  |
| endgame_epa_median | float | Median team end-of-season endgame EPA                           |
| endgame_epa_75p    | float | 75th percentile team end-of-season endgame EPA                  |
| endgame_epa_mean   | float | Mean team end-of-season endgame EPA                             |
| endgame_epa_sd     | float | Standard deviation of team end-of-season endgame EPA            |
| rp_1_epa_max       | float | Maximum team end-of-season RP1 EPA for the year                 |
| rp_1_epa_1p        | float | 1st percentile team end-of-season RP1 EPA                       |
| rp_1_epa_5p        | float | 5th percentile team end-of-season RP1 EPA                       |
| rp_1_epa_10p       | float | 10th percentile team end-of-season RP1 EPA                      |
| rp_1_epa_25p       | float | 25th percentile team end-of-season RP1 EPA                      |
| rp_1_epa_median    | float | Median team end-of-season RP1 EPA                               |
| rp_1_epa_75p       | float | 75th percentile team end-of-season RP1 EPA                      |
| rp_1_epa_mean      | float | Mean team end-of-season RP1 EPA                                 |
| rp_1_epa_sd        | float | Standard deviation of team end-of-season RP1 EPA                |
| rp_2_epa_max       | float | Maximum team end-of-season RP2 EPA for the year                 |
| rp_2_epa_1p        | float | 1st percentile team end-of-season RP2 EPA                       |
| rp_2_epa_5p        | float | 5th percentile team end-of-season RP2 EPA                       |
| rp_2_epa_10p       | float | 10th percentile team end-of-season RP2 EPA                      |
| rp_2_epa_25p       | float | 25th percentile team end-of-season RP2 EPA                      |
| rp_2_epa_median    | float | Median team end-of-season RP2 EPA                               |
| rp_2_epa_75p       | float | 75th percentile team end-of-season RP2 EPA                      |
| rp_2_epa_mean      | float | Mean team end-of-season RP2 EPA                                 |
| rp_2_epa_sd        | float | Standard deviation of team end-of-season RP2 EPA                |
| epa_quals_acc      | float | Accuracy of EPA model on all quals matches                      |
| epa_quals_mse      | float | Mean squared error of EPA model on all quals matches            |
| quals_count        | int   | Number of quals matches                                         |
| epa_elims_acc      | float | Accuracy of EPA model on all elims matches                      |
| epa_elims_mse      | float | Mean squared error of EPA model on all elims matches            |
| elims_count        | int   | Number of elims matches                                         |
| epa_champs_acc     | float | Accuracy of EPA model on all champs matches                     |
| epa_champs_mse     | float | Mean squared error of EPA model on all champs matches           |
| champs_count       | int   | Number of champs matches                                        |
| epa_acc            | float | Accuracy of EPA model on all matches                            |
| epa_mse            | float | Mean squared error of EPA model on all matches                  |
| count              | int   | Number of matches                                               |
| rp_1_acc           | float | Accuracy of RP1 model on qualification matches                  |
| rp_1_mse           | float | Mean squared error of RP1 model on qualification matches        |
| rp_1_champs_acc    | float | Accuracy of RP1 model on champs qualification matches           |
| rp_1_champs_mse    | float | Mean squared error of RP1 model on champs qualification matches |
| rp_2_acc           | float | Accuracy of RP2 model on qualification matches                  |
| rp_2_mse           | float | Mean squared error of RP2 model on qualification matches        |
| rp_2_champs_acc    | float | Accuracy of RP2 model on champs qualification matches           |
| rp_2_champs_mse    | float | Mean squared error of RP2 model on champs qualification matches |
| rp_champs_count    | int   | 2 \* number of champs qualification matches                     |
| rp_count           | int   | 2 \* number of qualification matches                            |
| score_mean         | float | Mean score of Week 1 matches                                    |
| score_sd           | float | Standard deviation of score of Week 1 matches                   |
| auto_mean          | float | Mean auto score of Week 1 matches                               |
| teleop_mean        | float | Mean teleop score of Week 1 matches                             |
| endgame_mean       | float | Mean endgame score of Week 1 matches                            |
| fouls_mean         | float | Mean fouls of Week 1 matches                                    |
| no_fouls_mean      | float | Mean no-fouls score of Week 1 matches                           |
| rp_1_mean          | float | Mean RP1 rate of Week 1 qualification matches                   |
| rp_2_mean          | float | Mean RP2 rate of Week 1 qualification matches                   |

### Team

| Column          | Type  | Description                                                              |
| --------------- | ----- | ------------------------------------------------------------------------ |
| team            | int   | Team number                                                              |
| name            | str   | Team name                                                                |
| offseason       | bool  | Whether this team only competes in the offseason (ex. 99XX)              |
| state           | str   | State/province abbreviation of team's location. Valid for USA and Canada |
| country         | str   | Country of team's location                                               |
| district        | str   | District abbreviationteam competes in (if any)                           |
| rookie_year     | int   | Year team first competed                                                 |
| active          | bool  | Whether the team is competing in the current season                      |
| norm_epa        | float | Normalized EPA of the team in the last complete season                   |
| norm_epa_recent | float | Mean of normalized EPA of the team in the last 5 seasons                 |
| norm_epa_mean   | float | Mean of normalized EPA of the team in all seasons                        |
| norm_epa_max    | float | Maximum normalized EPA of the team in all seasons                        |
| wins            | int   | Number of wins across all official matches                               |
| losses          | int   | Number of losses across all official matches                             |
| ties            | int   | Number of ties across all official matches                               |
| count           | int   | Number of official matches played in                                     |
| winrate         | float | Win rate across all official matches                                     |
| full_wins       | int   | Number of wins across all official and offseason matches                 |
| full_losses     | int   | Number of losses across all official and offseason matches               |
| full_ties       | int   | Number of ties across all official and offseason matches                 |
| full_count      | int   | Number of official and offseason matches played in                       |
| full_winrate    | float | Win rate across all official and offseason matches                       |

### TeamYear

| Column                  | Type  | Description                                                                     |
| ----------------------- | ----- | ------------------------------------------------------------------------------- |
| year                    | int   | Year                                                                            |
| team                    | int   | Team number                                                                     |
| offseason               | bool  | Whether this team only competes in the offseason (ex. 99XX)                     |
| name                    | str   | Team name                                                                       |
| state                   | str   | State/province abbreviation of team's location. Valid for USA and Canada        |
| country                 | str   | Country of team's location                                                      |
| district                | str   | District abbreviationteam competes in (if any)                                  |
| epa_start               | float | EPA at the start of the season                                                  |
| epa_pre_champs          | float | EPA prior to the start of champs                                                |
| epa_end                 | float | EPA at the end of the season                                                    |
| epa_mean                | float | Mean EPA of the team in the season                                              |
| epa_max                 | float | Maximum EPA of the team in the season                                           |
| epa_diff                | float | Difference between the end and start of season EPA                              |
| auto_epa_start          | float | Auto EPA at the start of the season                                             |
| auto_epa_pre_champs     | float | Auto EPA prior to the start of champs                                           |
| auto_epa_end            | float | Auto EPA at the end of the season                                               |
| auto_epa_mean           | float | Mean auto EPA of the team in the season                                         |
| auto_epa_max            | float | Maximum auto EPA of the team in the season                                      |
| teleop_epa_start        | float | Teleop EPA at the start of the season                                           |
| teleop_epa_pre_champs   | float | Teleop EPA prior to the start of champs                                         |
| teleop_epa_end          | float | Teleop EPA at the end of the season                                             |
| teleop_epa_mean         | float | Mean teleop EPA of the team in the season                                       |
| teleop_epa_max          | float | Maximum teleop EPA of the team in the season                                    |
| endgame_epa_start       | float | Endgame EPA at the start of the season                                          |
| endgame_epa_pre_champs  | float | Endgame EPA prior to the start of champs                                        |
| endgame_epa_end         | float | Endgame EPA at the end of the season                                            |
| endgame_epa_mean        | float | Mean endgame EPA of the team in the season                                      |
| endgame_epa_max         | float | Maximum endgame EPA of the team in the season                                   |
| rp_1_epa_start          | float | RP1 EPA at the start of the season                                              |
| rp_1_epa_pre_champs     | float | RP1 EPA prior to the start of champs                                            |
| rp_1_epa_end            | float | RP1 EPA at the end of the season                                                |
| rp_1_epa_mean           | float | Mean RP1 EPA of the team in the season                                          |
| rp_1_epa_max            | float | Maximum RP1 EPA of the team in the season                                       |
| rp_2_epa_start          | float | RP2 EPA at the start of the season                                              |
| rp_2_epa_pre_champs     | float | RP2 EPA prior to the start of champs                                            |
| rp_2_epa_end            | float | RP2 EPA at the end of the season                                                |
| rp_2_epa_mean           | float | Mean RP2 EPA of the team in the season                                          |
| rp_2_epa_max            | float | Maximum RP2 EPA of the team in the season                                       |
| norm_epa_end            | float | Normalized EPA at the end of the season                                         |
| wins                    | int   | Number of wins across all official matches                                      |
| losses                  | int   | Number of losses across all official matches                                    |
| ties                    | int   | Number of ties across all official matches                                      |
| count                   | int   | Number of official matches played in                                            |
| winrate                 | float | Win rate across all official matches                                            |
| full_wins               | int   | Number of wins across all official and offseason matches                        |
| full_losses             | int   | Number of losses across all official and offseason matches                      |
| full_ties               | int   | Number of ties across all official and offseason matches                        |
| full_count              | int   | Number of official and offseason matches played in                              |
| full_winrate            | float | Win rate across all official and offseason matches                              |
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

| Column       | Type  | Description                                                                                                               |
| ------------ | ----- | ------------------------------------------------------------------------------------------------------------------------- |
| key          | str   | Event key                                                                                                                 |
| year         | int   | Year                                                                                                                      |
| name         | str   | Event name                                                                                                                |
| time         | int   | Timestamp of the event's start date                                                                                       |
| state        | str   | State/province abbreviation of event's location. Valid for USA and Canada                                                 |
| country      | str   | Country of event's location                                                                                               |
| district     | str   | District abbreviation event is in (if any)                                                                                |
| start_date   | str   | Event start date in yyyy-mm-dd format                                                                                     |
| end_date     | str   | Event end date in yyyy-mm-dd format                                                                                       |
| type         | str   | Event type (0=Regional, 1=District, 2=District Championship, 3=Champs Division, 4=Einsteins, 99=Offseason, 100=Preseason) |
| week         | int   | Week of the event (8 is champs)                                                                                           |
| offseason    | bool  | Whether the event is an offseason event                                                                                   |
| video        | str   | Link to the event's livestream                                                                                            |
| status       | str   | Status of the event ("Upcoming", "In Progress", "Completed")                                                              |
| qual_matches | int   | Number of qualification matches played at the event                                                                       |
| epa_max      | float | Maximum end-of-event EPA of any team at the event                                                                         |
| epa_top_8    | float | 8th highest end-of-event EPA of any team at the event                                                                     |
| epa_top_24   | float | 24th highest end-of-event EPA of any team at the event                                                                    |
| epa_mean     | float | Mean end-of-event EPA of all teams at the event                                                                           |
| epa_sd       | float | Standard deviation of end-of-event EPA of all teams at the event                                                          |
| epa_acc      | float | Accuracy of EPA model at predicting all matches at the event                                                              |
| epa_mse      | float | Mean squared error of EPA model at predicting all matches at the event                                                    |
| rp_1_acc     | float | Accuracy of EPA model at predicting RP1 of all alliances in qualification matches at the event                            |
| rp_1_mse     | float | Mean squared error of EPA model at predicting RP1 of all alliances in qualification matches at the event                  |
| rp_2_acc     | float | Accuracy of EPA model at predicting RP2 of all alliances in qualification matches at the event                            |
| rp_2_mse     | float | Mean squared error of EPA model at predicting RP2 of all alliances in qualification matches at the event                  |

### TeamEvent

| Column                   | Type  | Description                                                               |
| ------------------------ | ----- | ------------------------------------------------------------------------- |
| team                     | int   | Team number                                                               |
| year                     | int   | Year of event                                                             |
| event                    | str   | Event key                                                                 |
| offseason                | bool  | Whether the event is an offseason event                                   |
| team_name                | str   | Team name                                                                 |
| event_name               | str   | Event name                                                                |
| state                    | str   | State/province abbreviation of event's location. Valid for USA and Canada |
| country                  | str   | Country of event's location                                               |
| district                 | str   | District abbreviation event is in (if any)                                |
| type                     | str   | Event type (see Event table)                                              |
| week                     | int   | Week of the event (8 is champs)                                           |
| status                   | str   | Status of the event (see Event table)                                     |
| epa_start                | float | Team EPA at the start of the event                                        |
| epa_pre_playoffs         | float | Team EPA at the start of playoffs                                         |
| epa_end                  | float | Team EPA at the end of the event                                          |
| epa_mean                 | float | Mean team EPA across all matches at the event                             |
| epa_max                  | float | Maximum team EPA across all matches at the event                          |
| epa_diff                 | float | Difference between team EPA at the end and start of the event             |
| auto_epa_start           | float | Team auto EPA at the start of the event                                   |
| auto_epa_pre_playoffs    | float | Team auto EPA at the start of playoffs                                    |
| auto_epa_end             | float | Team auto EPA at the end of the event                                     |
| auto_epa_mean            | float | Mean team auto EPA across all matches at the event                        |
| auto_epa_max             | float | Maximum team auto EPA across all matches at the event                     |
| teleop_epa_start         | float | Team teleop EPA at the start of the event                                 |
| teleop_epa_pre_playoffs  | float | Team teleop EPA at the start of playoffs                                  |
| teleop_epa_end           | float | Team teleop EPA at the end of the event                                   |
| teleop_epa_mean          | float | Mean team teleop EPA across all matches at the event                      |
| teleop_epa_max           | float | Maximum team teleop EPA across all matches at the event                   |
| endgame_epa_start        | float | Team endgame EPA at the start of the event                                |
| endgame_epa_pre_playoffs | float | Team endgame EPA at the start of playoffs                                 |
| endgame_epa_end          | float | Team endgame EPA at the end of the event                                  |
| endgame_epa_mean         | float | Mean team endgame EPA across all matches at the event                     |
| endgame_epa_max          | float | Maximum team endgame EPA across all matches at the event                  |
| rp_1_epa_start           | float | Team RP1 EPA at the start of the event                                    |
| rp_1_epa_end             | float | Team RP1 EPA at the end of the event                                      |
| rp_1_epa_mean            | float | Mean team RP1 EPA across all matches at the event                         |
| rp_1_epa_max             | float | Maximum team RP1 EPA across all matches at the event                      |
| rp_2_epa_start           | float | Team RP2 EPA at the start of the event                                    |
| rp_2_epa_end             | float | Team RP2 EPA at the end of the event                                      |
| rp_2_epa_mean            | float | Mean team RP2 EPA across all matches at the event                         |
| rp_2_epa_max             | float | Maximum team RP2 EPA across all matches at the event                      |
| wins                     | int   | Number of wins at the event                                               |
| losses                   | int   | Number of losses at the event                                             |
| ties                     | int   | Number of ties at the event                                               |
| count                    | int   | Number of matches at the event                                            |
| winrate                  | float | Winrate at the event                                                      |
| qual_wins                | int   | Number of qualification wins at the event                                 |
| qual_losses              | int   | Number of qualification losses at the event                               |
| qual_ties                | int   | Number of qualification ties at the event                                 |
| qual_count               | int   | Number of qualification matches at the event                              |
| rps                      | int   | Number of RPs at the event                                                |
| rps_per_match            | float | RPs per match at the event                                                |
| rank                     | int   | Rank at the event                                                         |
| num_teams                | int   | Number of teams at the event                                              |

### Match

| Column               | Type  | Description                                              |
| -------------------- | ----- | -------------------------------------------------------- |
| key                  | str   | Match key                                                |
| year                 | int   | Year of event                                            |
| event                | str   | Event key                                                |
| comp_level           | str   | Competition level (qm, ef, qf, sf, f)                    |
| set_number           | int   | Set number in a series of matches (1 for qualifications) |
| match_number         | int   | Match number in a series of matches                      |
| offseason            | bool  | Whether the event is an offseason event                  |
| status               | str   | Status of the match (see Event table)                    |
| video                | str   | Youtube video key for the match video                    |
| red_1                | int   | Red alliance team 1                                      |
| red_2                | int   | Red alliance team 2                                      |
| red_3                | int   | Red alliance team 3                                      |
| red_dq               | str   | Comma-separated list of red alliance DQ'd teams          |
| red_surrogate        | str   | Comma-separated list of red alliance surrogate teams     |
| red_epa_sum          | float | Sum of red alliance EPA                                  |
| red_auto_epa_sum     | float | Sum of red alliance auto EPA                             |
| red_teleop_epa_sum   | float | Sum of red alliance teleop EPA                           |
| red_endgame_epa_sum  | float | Sum of red alliance endgame EPA                          |
| red_rp_1_epa_sum     | float | Sum of red alliance RP1 EPA                              |
| red_rp_2_epa_sum     | float | Sum of red alliance RP2 EPA                              |
| blue_1               | int   | Blue alliance team 1                                     |
| blue_2               | int   | Blue alliance team 2                                     |
| blue_3               | int   | Blue alliance team 3                                     |
| blue_dq              | str   | Comma-separated list of blue alliance DQ'd teams         |
| blue_surrogate       | str   | Comma-separated list of blue alliance surrogate teams    |
| blue_epa_sum         | float | Sum of blue alliance EPA                                 |
| blue_auto_epa_sum    | float | Sum of blue alliance auto EPA                            |
| blue_teleop_epa_sum  | float | Sum of blue alliance teleop EPA                          |
| blue_endgame_epa_sum | float | Sum of blue alliance endgame EPA                         |
| blue_rp_1_epa_sum    | float | Sum of blue alliance RP1 EPA                             |
| blue_rp_2_epa_sum    | float | Sum of blue alliance RP2 EPA                             |
| winner               | str   | Winner of the match (red, blue, draw)                    |
| epa_winner           | str   | Predicted winner of the match (red, blue, draw)          |
| epa_win_prob         | float | Predicted probability of the match winner                |
| red_rp_1_prob        | float | Predicted probability of red alliance earning RP1        |
| red_rp_2_prob        | float | Predicted probability of red alliance earning RP2        |
| blue_rp_1_prob       | float | Predicted probability of blue alliance earning RP1       |
| blue_rp_2_prob       | float | Predicted probability of blue alliance earning RP2       |
| playoff              | bool  | Whether the match is a playoff match                     |
| time                 | int   | Match time in seconds                                    |
| predicted_time       | int   | Predicted match time in seconds (from TBA)               |
| red_score            | int   | Actual red score                                         |
| blue_score           | int   | Actual blue score                                        |
| red_auto             | int   | Red auto score                                           |
| red_auto_movement    | int   | Red auto movement score                                  |
| red_teleop           | int   | Red teleop score (excluding endgame)                     |
| red_endgame          | int   | Red endgame score                                        |
| red_no_fouls         | int   | Red no fouls score (auto + teleop + endgame)             |
| red_fouls            | int   | Red fouls score                                          |
| red_rp_1             | int   | 1 if red earned RP1, 0 otherwise                         |
| red_rp_2             | int   | 1 if red earned RP2, 0 otherwise                         |
| blue_auto            | int   | Blue auto score                                          |
| blue_auto_movement   | int   | Blue auto movement score                                 |
| blue_teleop          | int   | Blue teleop score (excluding endgame)                    |
| blue_endgame         | int   | Blue endgame score                                       |
| blue_no_fouls        | int   | Blue no fouls score (auto + teleop + endgame)            |
| blue_fouls           | int   | Blue fouls score                                         |
| blue_rp_1            | int   | 1 if blue earned RP1, 0 otherwise                        |
| blue_rp_2            | int   | 1 if blue earned RP2, 0 otherwise                        |

### TeamMatch

| Column      | Type  | Description                                       |
| ----------- | ----- | ------------------------------------------------- |
| team        | int   | Team number                                       |
| year        | int   | Year of event                                     |
| event       | str   | Event key                                         |
| match       | str   | Match key                                         |
| time        | int   | Match time in seconds (NOTE: currently incorrect) |
| offseason   | bool  | Whether the event is an offseason event           |
| playoff     | bool  | Whether the match is a playoff match              |
| alliance    | str   | Alliance color (red, blue) of team in match       |
| status      | str   | Status of the match (see Event table)             |
| dq          | bool  | Whether the team was disqualified in the match    |
| surrogate   | bool  | Whether the team was a surrogate in the match     |
| epa         | float | EPA of the team prior to the match                |
| auto_epa    | float | Auto EPA of the team prior to the match           |
| teleop_epa  | float | Teleop EPA of the team prior to the match         |
| endgame_epa | float | Endgame EPA of the team prior to the match        |
| rp_1_epa    | float | RP1 EPA of the team prior to the match            |
| rp_2_epa    | float | RP2 EPA of the team prior to the match            |
| post_epa    | float | EPA of the team after the match                   |
