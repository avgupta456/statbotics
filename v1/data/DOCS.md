# Statbotics Data

Statbotics Data queries the TBA API for data, performs calculations, and stores the results in a CockroachDB Database.

## Installation

```bash
poetry install
```

## Usage

After downloading CockroachDB and installing it, you can run the following command to start the database:

```bash
cockroach start-single-node --insecure
```

Then, on a separate terminal, run:

```bash
poetry run python src/clean.py
```

Edit the environment variable `LOCAL_DB` to connect to either the local instance of CockroachDB or the production database. The production database requires the `CRDB_PWD` environment variable to be set in the `.env` file.

## Cron Job

A simple App Engine instance is deployed using FastAPI to expose an HTTP endpoint triggering the database refresh. A Google Cloud Scheduler cron job is created to run the refresh in a given time interval (anticipated to be once every three hours). The following script was used to increase the attempt deadline from 1 minute to 30 minutes:

```
gcloud beta scheduler jobs update http data_refresh --attempt-deadline=1800s --project=statbotics-io-276522
```

Currently the refresh takes approximately 2-3 minutes to requery the 2022 season. This might increase as the season progresses.
