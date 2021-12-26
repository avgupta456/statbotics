import os

CRDB_USER = os.getenv("CRDB_USER", "")
CRDB_PWD = os.getenv("CRDB_PWD", "")
CRDB_HOST = os.getenv("CRDB_HOST", "")
CRDB_CLUSTER = os.getenv("CRDB_CLUSTER", "")
LOCAL_DB = os.getenv("LOCAL_DB", "True") == "True"

url = "postgresql://root@localhost:26257/statbotics2?sslmode=disable"
if not LOCAL_DB:
    url = (
        "postgresql://"
        + CRDB_USER
        + ":"
        + CRDB_PWD
        + "@"
        + CRDB_HOST
        + "/statbotics?sslmode=verify-full&sslrootcert=.\\root.crt&options=--cluster%3D"
        + CRDB_CLUSTER
    )

DATABASE_URL = url

print(DATABASE_URL)

DJANGO_SECRET_KEY = os.getenv("SECRET_KEY", "")
