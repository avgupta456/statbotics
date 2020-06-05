from google.cloud import datastore
import os


def getEnvVar(client, name):
    key = client.key("secret", name)
    entry = client.get(key)
    return entry["value"]


# accessed by settings.py
CLOUDSQL_CONNECTION = os.environ.get("CLOUDSQL_CONNECTION")
CLOUDSQL_DATABASE = os.environ.get("CLOUDSQL_DATABASE")
CLOUDSQL_PASSWORD = os.environ.get("CLOUDSQL_PASSWORD")
CLOUDSQL_USER = os.environ.get("CLOUDSQL_USER")
SECRET_KEY = os.environ.get("SECRET_KEY")

if CLOUDSQL_CONNECTION is None or \
        CLOUDSQL_DATABASE is None or \
        CLOUDSQL_PASSWORD is None or \
        CLOUDSQL_USER is None or \
        SECRET_KEY is None:

    client = datastore.Client()
    CLOUDSQL_CONNECTION = getEnvVar(client, "CLOUDSQL_CONNECTION")
    CLOUDSQL_DATABASE = getEnvVar(client, "CLOUDSQL_DATABASE")
    CLOUDSQL_PASSWORD = getEnvVar(client, "CLOUDSQL_PASSWORD")
    CLOUDSQL_USER = getEnvVar(client, "CLOUDSQL_USER")
    SECRET_KEY = getEnvVar(client, "SECRET_KEY")

# comment out to use the production database
# CLOUDSQL_DATABASE += "2"

print(CLOUDSQL_CONNECTION)
print(CLOUDSQL_DATABASE)
print(CLOUDSQL_PASSWORD)
print(CLOUDSQL_USER)
print(SECRET_KEY)
