import os
from typing import List

# GLOBAL

PROD = os.getenv("PROD", "False") == "True"

# 8001 emulates the data server
BACKEND_URL = "https://api.statbotics.io" if PROD else "http://localhost:8001"

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
    else "cockroachdb://root@localhost:26257/statbotics3?sslmode=disable"
)

ASYNC_CONN_STR = CONN_STR.replace("cockroachdb://", "cockroachdb+asyncpg://").split(
    "?sslmode"
)[0]

# API

AUTH_KEY_BLACKLIST: List[str] = []

# CONFIG

CURR_YEAR = 2025
CURR_WEEK = 2

# MISC

EPS = 1e-6
