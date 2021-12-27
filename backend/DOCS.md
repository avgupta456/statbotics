# Statbotics Backend

The Statbotics backend queries the CockroachDB database and exposes REST API endpoints for the frontend to consume.

## Installation

```bash
poetry install
```

## Usage

The local development environment can be started by running the Django Rest Framework application.

```bash
poetry run python manage.py runserver
```

Note, the backend requires a running CockroachDB instance. See `/data` for instructions on setting up the local DB, or connect to the production instance by changing the `LOCAL_DB` environment variable. The production database requires the `CRDB_PWD` environment variable to be set in the `.env` file.
