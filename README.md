# [Statbotics.io](https://statbotics.io)

[![Downloads](https://pepy.tech/badge/statbotics)](https://pepy.tech/project/statbotics)
[![Frontend Build Status](https://travis-ci.com/avgupta456/statbotics_frontend.svg?branch=master)](https://travis-ci.com/avgupta456/statbotics_frontend)


Statbotics aims to create and distribute modern data analytics for the FIRST Robotics Competition. Due to the multiple distinct components to this project, the code is stored in multiple repositories, and this repository serves as overarching documentation. Details for specific subsections can be accessed via the links below.

Python Calculations: https://github.com/avgupta456/statbotics_calc

Django Backend: https://github.com/avgupta456/statbotics_backend

React Frontend: https://github.com/avgupta456/statbotics_frontend

Python API: https://github.com/avgupta456/statbotics_api

In the future, additional documentation, examples, and resources will be stored in this repository.

## Overview

Currently, we are focused on Elo Ratings, building upon Caleb Sykes' previous work. We're in the early stages, and hope to add content related to OPR, event prediction, and Zebra MotionWorks soon. Stay tuned!

Elo is a measure of a team's on-field strength, calculated using win margins from over 100,000 matches dating back to 2002. A Elo of 1500 is roughly average, and an Elo of 1800+ is in the top 1% worldwide. Head over to https://statbotics.io for tables and charts displaying Elo trends. Remember, this is just one method to rank teams, and shouldn't be taken too seriously ;)

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
print(sb.getTeam(254))

>> {'team':254, 'name': 'The Cheesy Poofs', 'state': 'CA', 'country': 'USA', 'district': 'None',
    'active': True, 'elo': 1860, 'elo_recent': 1972, 'elo_mean': 1898, 'elo_max': 2145}
```

Read the docs: https://statbotics.readthedocs.io/en/latest/

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Reach out to avgupta456@gmail.com for guidance.

## License
[MIT](https://choosealicense.com/licenses/mit/)
