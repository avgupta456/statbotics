# Statbotics API

Statbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes Expected Points Added (EPA) statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.

Visit https://statbotics.io for more content!

## Usage

With Python>=3.8 and pip installed, run

```
pip install statbotics==2.0.1
```

Then in a Python file, create a Statbotics object and get started!

```
import statbotics

sb = statbotics.Statbotics()
print(sb.get_team(254))

>> {'team': 254, 'name': 'The Cheesy Poofs', 'offseason': False, 'state': 'CA', 'country': 'USA', 'district': None, 'rookie_year': 1999, 'active': True, 'norm_epa': 1961.0, 'norm_epa_recent': 1956.0, 'norm_epa_mean': 1896.0, 'norm_epa_max': 2114.0, ... }
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
