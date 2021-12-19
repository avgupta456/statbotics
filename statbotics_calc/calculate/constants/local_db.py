import os

from google.cloud import datastore


def getEnvVar(client, name):
    key = client.key("secret", name)
    entry = client.get(key)
    return entry["value"]


# accessed by settings.py
MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = os.environ.get("MYSQL_PORT")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")

if (
    MYSQL_USERNAME is None
    or MYSQL_PASSWORD is None
    or MYSQL_HOST is None
    or MYSQL_PORT is None
    or MYSQL_DATABASE is None
):

    client = datastore.Client()
    MYSQL_USERNAME = getEnvVar(client, "MYSQL_USERNAME")
    MYSQL_PASSWORD = getEnvVar(client, "MYSQL_PASSWORD")
    MYSQL_HOST = getEnvVar(client, "MYSQL_HOST")
    MYSQL_PORT = getEnvVar(client, "MYSQL_PORT")
    MYSQL_DATABASE = getEnvVar(client, "MYSQL_DATABASE")

"""
print(MYSQL_USERNAME)
print(MYSQL_PASSWORD)
print(MYSQL_HOST)
print(MYSQL_PORT)
print(MYSQL_DATABASE)
"""
