# Statbotics API

Statbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes historical Elo and OPR statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.

Visit https://statbotics.io for more content!

## Usage

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

Read below for more methods!

## API Reference

Visit https://statbotics.readthedocs.io/en/latest/

## Contribute

If you are interested in contributing, reach out to Abhijit Gupta (avgupta456@gmail.com)

## Support

If you are having issues, please let us know. We welcome issues and pull requests.

## License

The project is licensed under the MIT license.
