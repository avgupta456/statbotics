# [Statbotics.io](https://statbotics.io)

[![Downloads](https://pepy.tech/badge/statbotics)](https://pepy.tech/project/statbotics)

## Overview

Welcome to Statbotics.io! Our mission is to develop and distribute FRC data analysis. Currently, we have calculated Elo Ratings, (component) OPRs, RP strengths, and win-loss records. These statistics are available through interactive tables, a REST API, and a Python library. Using these metrics, we have developed match predictions and a complete event simulator. We hope to continue adding new features, such as Zebra MotionWorks analysis and more predictive modeling.

### Elo

Elo is a measure of a team's on-field strength, calculated using win margins from over 100,000 matches dating back to 2002. An Elo of 1500 is roughly average, while an Elo of 1800+ is in the top 1% worldwide. At Statbotics, browse Elo ratings for teams, seasons, and events.

### OPR

OPR uses linear algebra to estimate a team's contribution to an alliance. Statbotics.io makes OPR and component OPR (Auto, Teleop, Endgame) data easily accessible for teams and events. For recent years, Ranking Point strengths are available as well.

### Insights

Combining Elo and OPR data from all prior matches, Statbotics.io allows users to quickly pull up and compare stats across teams. Find which teams performed the best this year, or the sleeper picks at your event.

### Predictions

Taking insights one step further, Statbotics.io leverages Elo and OPR statistics for accurate match prediction and event simulation. These tools can help your team make strategic decisions and win matches.

## API

This Python API makes historical Elo and OPR statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.

With Python>=3.6 and pip installed, run

```
pip install statbotics
```

Then in a Python file, create a Statbotics object and get started!

```
import statbotics

sb = statbotics.Statbotics()
print(sb.get_team(254))

>> {'team':254, 'name': 'The Cheesy Poofs', 'state': 'CA', 'country': 'USA', 'district': 'None',
    'active': True, 'elo': 1860, 'elo_recent': 1972, 'elo_mean': 1898, 'elo_max': 2145}
```

Read the docs: https://statbotics.readthedocs.io/en/latest/

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Reach out to avgupta456@gmail.com for guidance.

## License

[MIT](https://choosealicense.com/licenses/mit/)
