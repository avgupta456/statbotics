import os

# GLOBAL

PROD = os.getenv("PROD", "False") == "True"

# DB

CRDB_USER = os.getenv("CRDB_USER", "")
CRDB_PWD = os.getenv("CRDB_PWD", "")
CRDB_HOST = os.getenv("CRDB_HOST", "")
CRDB_CLUSTER = os.getenv("CRDB_CLUSTER", "")

CONN_STR = (
    (
        "cockroachdb://"
        + CRDB_USER
        + ":"
        + CRDB_PWD
        + "@"
        + CRDB_HOST
        + "/statbotics3?sslmode=verify-full&sslrootcert=root.crt&options=--cluster%3D"
        + CRDB_CLUSTER
    )
    if PROD
    else "cockroachdb://root@localhost:26257/statbotics2?sslmode=disable"
)

# CONFIG

MAX_YEAR = 2024
CURR_YEAR = 2023
CURR_WEEK = 1

# MAX_TEAM = 9316   # (2023)
MAX_TEAM = 9650  # (2024)
