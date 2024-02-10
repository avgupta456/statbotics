# Statbotics Backend

The Statbotics backend is a Python FastAPI server that calculates, stores, and serves EPA data to the frontend and REST/Python API. The backend is deployed on a Google App Engine instance and uses a CockroachDB database.

## Setup

Requires Python 3.8+.

1. Install dependencies: `pip install -r requirements.txt` or `poetry install`
2. Create a `.env` file with the following environment variables:
   - PROD (bool): Whether to run in production mode
   - CRDB_USER (str): CockroachDB username
   - CRDB_PWD (str): CockroachDB password
   - CRDB_HOST (str): CockroachDB host
   - CRDB_CLUSTER (str): CockroachDB cluster name
3. Run the server: `yarn start` or `poetry run uvicorn main:app --reload --port=8000`

## Deployment

The `app.yaml` file is used to deploy the backend to Google App Engine. The `cloudbuild.yaml` file specifies the steps to deploy the backend, and Google Cloud Build automatically executes the pipeline upon pushing to the `master` branch.

## Structure

The backend is structured as follows:

- `main.py`: The main FastAPI app
- `api/`: The endpoints serving the REST API. Depends on `db/`.
- `data/`: The scripts to load matches and calculate EPA data. Depends on `db/` and `tba/`.
- `db/`: The database models and functions to interact with the database.
- `site/`: The endpoints serving the frontend. Depends on `db/`.
- `tba/`: The functions to interact with The Blue Alliance API.
- `utils/`: Utility functions.

## Contributing

Contributions are welcome! Please open an issue or pull request.
