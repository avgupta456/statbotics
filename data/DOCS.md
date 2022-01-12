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
