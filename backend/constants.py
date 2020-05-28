# Imports the Google Cloud client library
from google.cloud import datastore

# Instantiates a client
client = datastore.Client()

def getEnvVar(name):
    key = client.key("secret", name)
    entry = client.get(key)
    return entry["value"]

CLOUDSQL_CONNECTION = getEnvVar("CLOUDSQL_CONNECTION")
CLOUDSQL_DATABASE = getEnvVar("CLOUDSQL_DATABASE")
CLOUDSQL_PASSWORD = getEnvVar("CLOUDSQL_PASSWORD")
CLOUDSQL_USER = getEnvVar("CLOUDSQL_USER")
SECRET_KEY = getEnvVar("SECRET_KEY")
