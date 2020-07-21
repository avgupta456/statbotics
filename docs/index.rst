Statbotics
==========

Statbotics.io aims to modernize FRC data analytics through developing and distributing cutting-edge metrics and analysis. This Python API makes historical Elo and OPR statistics just a few Python lines away!
Currently we support queries on teams, years, events, and matches. Read below for usage and documentation.

Visit https://statbotics.io for more content!

Usage
-----

With Python>=3.6 and pip installed, run

.. code-block:: python

    pip install statbotics

Then in a Python file, create a Statbotics object and get started!

.. code-block:: python

  import statbotics

  sb = statbotics.Statbotics()
  print(sb.getTeam(254))

  >> {'team':254, 'name': 'The Cheesy Poofs', 'state': 'CA', 'country': 'USA', 'district': 'None',
      'active': True, 'elo': 1860, 'elo_recent': 1972, 'elo_mean': 1898, 'elo_max': 2145}

Read below for more methods!

API Reference
-------------
.. autoclass:: statbotics.main.Statbotics
   :members: getTeam, getTeams, getYear, getYears, getTeamYear, getTeamYears, getEvent, getEvents, getTeamEvent, getTeamEvents, getMatch, getMatches, getTeamMatch, getTeamMatches

Contribute
----------

If you are interested in contributing, reach out to Abhijit Gupta (avgupta456@gmail.com)
Source code is available at github.com/avgupta456/statbotics_api

Support
-------

If you are having issues, please let us know.
We welcome issues and pull requests at github.com/avgupta456/statbotics_api

License
-------

The project is licensed under the MIT license.
