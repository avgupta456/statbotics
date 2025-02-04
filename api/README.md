# Statbotics API

Statbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes Expected Points Added (EPA) statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.

Visit https://statbotics.io for more content!

## Usage

With Python>=3.8 and pip installed, run

```
pip install statbotics==3.0.0
```

Then in a Python file, create a Statbotics object and get started!

```
import statbotics

sb = statbotics.Statbotics()
print(sb.get_team(254))

>> {'team': 254, 'name': 'The Cheesy Poofs', 'country': 'USA', 'state': 'CA', 'district': None, 'rookie_year': 1999, 'active': True, 'record': {'wins': 808, 'losses': 160, 'ties': 8, 'count': 976, 'winrate': 0.832}, 'norm_epa': {'current': 1909.0, 'recent': 1904.0, 'mean': 1894.0, 'max': 2058.0}}
```

Read below for more methods!

## API Reference

Visit https://statbotics.readthedocs.io/en/latest/

## Contribute

If you are interested in contributing, reach out to Abhijit Gupta (avgupta456@gmail.com)

## Support

If you are having issues, please let us know. We welcome issues and pull requests.

## License

The project is licensed under the MIT license.
