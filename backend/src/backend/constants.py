import os

CRDB_USER = os.getenv("CRDB_USER", "")
CRDB_PWD = os.getenv("CRDB_PWD", "")
CRDB_HOST = os.getenv("CRDB_HOST", "")
CRDB_CLUSTER = os.getenv("CRDB_CLUSTER", "")

local_db = os.getenv("LOCAL_DB", "")
if type(local_db) == str:
    local_db = local_db.lower() == "true"
LOCAL_DB: bool = local_db  # type: ignore

docker = os.getenv("DOCKER", "")
if type(docker) == str:
    docker = docker.lower() == "true"
DOCKER: bool = docker  # type: ignore

url = "postgresql://root@localhost:26257/statbotics2?sslmode=disable"

if DOCKER:
    # assuming LOCAL_DB, overwritten otherwise
    url = url.replace("localhost", "cockroachdb")

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

DJANGO_SECRET_KEY = os.getenv("SECRET_KEY", "EMPTY")
