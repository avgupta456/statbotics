from google.cloud import datastore

def getEnvVar(client, name):
    key = client.key("secret", name)
    entry = client.get(key)
    return entry["value"]

#accessed by settings.py
CLOUDSQL_CONNECTION = ""
CLOUDSQL_DATABASE = ""
CLOUDSQL_PASSWORD = ""
CLOUDSQL_USER = ""
SECRET_KEY = ""

try:
    import os

    CLOUDSQL_CONNECTION = os.environ.get("CLOUDSQL_CONNECTION")
    CLOUDSQL_DATABASE = os.environ.get("CLOUDSQL_DATABASE")
    CLOUDSQL_PASSWORD = os.environ.get("CLOUDSQL_PASSWORD")
    CLOUDSQL_USER = os.environ.get("CLOUDSQL_USER")
    SECRET_KEY = os.environ.get("SECRET_KEY")
except Exception as e:
    client = datastore.Client()
    CLOUDSQL_CONNECTION = getEnvVar(client, "CLOUDSQL_CONNECTION")
    CLOUDSQL_DATABASE = getEnvVar(client, "CLOUDSQL_DATABASE")
    CLOUDSQL_PASSWORD = getEnvVar(client, "CLOUDSQL_PASSWORD")
    CLOUDSQL_USER = getEnvVar(client, "CLOUDSQL_USER")
    SECRET_KEY = getEnvVar(client, "SECRET_KEY")

if (CLOUDSQL_CONNECTION==None or
    CLOUDSQL_DATABASE==None or
    CLOUDSQL_PASSWORD==None or
    CLOUDSQL_USER==None or
    SECRET_KEY==None):

    client = datastore.Client()
    CLOUDSQL_CONNECTION = getEnvVar(client, "CLOUDSQL_CONNECTION")
    CLOUDSQL_DATABASE = getEnvVar(client, "CLOUDSQL_DATABASE")
    CLOUDSQL_PASSWORD = getEnvVar(client, "CLOUDSQL_PASSWORD")
    CLOUDSQL_USER = getEnvVar(client, "CLOUDSQL_USER")
    SECRET_KEY = getEnvVar(client, "SECRET_KEY")
