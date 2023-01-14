# Statbotics

Statbotics is an open-source data analytics platform for the FIRST Robotics Competition (FRC). We have created the Expected Points Added (EPA) rating system, which predicts a team's average scoring contribution to a match. EPA builds upon the Elo rating system, but is directly in point units, separates into additional components, and has additional modifications that improve accuracy and calibration. Statbotics computes both historical and realtime EPA results, and exposes data through a CSV export, REST API, Python package, and website ([statbotics.io](https://www.statbotics.io)). The website includes interactive tables, visualizations, event simulation, and more. The major components are summarized below, with more detailed development documentation in each subdirectory.

<p width="100%" align="center">
  <img src="https://user-images.githubusercontent.com/16708871/212447884-68af251c-0813-4542-a81f-1a63c1388a69.png" width=400 />
</p>

## EPA Model

The Expected Points Added (EPA) model builds upon the Elo rating system, but transforms ratings to point units and makes several modifications. The EPA model was developed to replace both Elo and OPR (Offensive Power Rating) with a single unified system. At a high level, the EPA model converts Elo into point contributions, and then makes several modifications to improve accuracy and interpretability. More details are available on the [Statbotics blog](https://www.statbotics.io/blog/epa). The table below shows the prediction accuracy improvements of EPA compared to existing approaches.

<p width="100%" align="center">
  <img src="https://user-images.githubusercontent.com/16708871/212448401-676284d9-de76-4153-9532-05b9ba493a60.png" width=800 />
</p>

## Server

A FastAPI Python server integrates with The Blue Alliance (TBA) to compute, store, and serve EPA ratings. Seven SQL tables are created to aggregate results: `Teams`, `Years`, `TeamYears`, `Events`, `TeamEvents`, `Matches`, and `TeamMatches` (on CockroachDB). An internal API serves the frontend, while the REST API and Python API are made available for public use. The REST API docs is accessible [here](https://www.statbotics.io/api/rest).

## Python API

The Python API makes Expected Points Added (EPA) statistics just a few Python lines away! Currently we support queries on teams, years, events, and matches. Here's a short example demonstrating the package:

Install via

```bash
pip install statbotics==2.0.1
```

Then run

```python
import statbotics

sb = statbotics.Statbotics()
print(sb.get_team(254))

>> {'team': 254, 'name': 'The Cheesy Poofs', 'offseason': False, 'state': 'CA', 'country': 'USA', 'district': None, 'rookie_year': 1999, 'active': True, 'norm_epa': 1961.0, 'norm_epa_recent': 1956.0, 'norm_epa_mean': 1896.0, 'norm_epa_max': 2114.0, ... }
```

More details are available [here](https://www.statbotics.io/api/python).

## Website

The website is written in NextJS, TypeScript, and TailwindCSS and aims to make EPA statistics accessible and actionable. The website includes EPA tables (with location filters, sortable columns), figures (Bubble charts, line graphs, bar graphs, etc.), live event simulation (including ranking points and tiebreakers), match breakdowns (with component predictions), and so much more. Check it out at [statbotics.io](https://www.statbotics.io)!

## Other

Feedback is always appreciated, either through GitHub issues or the [Statbotics Canny](https://statbotics.canny.io/feature-requests).

If you are interested in contributing, please reach out to me directly through any platform (GitHub, Email, ChiefDelphi, etc.)

I (Abhijit Gupta) currently front the cloud hosting costs for Statbotics. If you are able and interested, feel free to pitch in using [this link](https://www.buymeacoffee.com/statbotics).

Thanks for your interest!
