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
    from google.cloud import datastore
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
