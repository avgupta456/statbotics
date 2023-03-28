import os

# GLOBAL

PROD = os.getenv("PROD", "False") == "True"

# DB

CRDB_USER = os.getenv("CRDB_USER", "")
CRDB_PWD = os.getenv("CRDB_PWD", "")
CRDB_HOST = os.getenv("CRDB_HOST", "")
CRDB_CLUSTER = os.getenv("CRDB_CLUSTER", "")
LOCAL_DB = os.getenv("LOCAL_DB", "True") == "True"

CONN_STR = (
    "cockroachdb://root@localhost:26257/statbotics2?sslmode=disable"
    if LOCAL_DB
    else (
        "cockroachdb://"
        + CRDB_USER
        + ":"
        + CRDB_PWD
        + "@"
        + CRDB_HOST
        + "/statbotics2?sslmode=verify-full&sslrootcert=root.crt&options=--cluster%3D"
        + CRDB_CLUSTER
    )
)

# CONFIG

CURR_YEAR = 2023
CURR_WEEK = 5
MAX_TEAM = 9316
