# Statbotics Elo

Statbotics aims to create and distribute modern data analytics for the FIRST Robotics Competition. This folder includes models (ELO, OPR, ILS, etc) that calculate the datasets Statbotics uses.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

The project is broken into two subsections - /calculate fetches data from TBA and calculates Elo ratings, /api uses the backend to interpret Elo ratings and make data visualizations. In /calculate, main.py contains three functions. load_data() fetches match and location history from The Blue Alliance, calculate_elos() processes every match and stores Elo rankings in pickle files, and push() computes additional statistics and stores the data in a CloudSQL database. Additionally, test.py contains a simple command line interface for interacting with the processed data.
