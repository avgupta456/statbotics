import os
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

CRDB_USER = os.getenv("CRDB_USER", "")
CRDB_PWD = os.getenv("CRDB_PWD", "")
CRDB_HOST = os.getenv("CRDB_HOST", "")
CRDB_CLUSTER = os.getenv("CRDB_CLUSTER", "")
LOCAL_DB = os.getenv("LOCAL_DB", "True") == "True"

if LOCAL_DB:
    engine = create_engine(
        "cockroachdb://root@localhost:26257/statbotics?sslmode=disable"
    )
else:
    engine = create_engine(
        "cockroachdb://"
        + CRDB_USER
        + ":"
        + CRDB_PWD
        + "@"
        + CRDB_HOST
        + "/statbotics?sslmode=verify-full&sslrootcert=\\root.crt&options=--cluster%3D"
        + CRDB_CLUSTER,
    )

Session = sessionmaker(bind=engine)

Base: Any = declarative_base()  # type: ignore


def clean_db() -> None:
    Base.metadata.drop_all(bind=engine)  # type: ignore
    Base.metadata.create_all(engine)
