from typing import Any

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from src.constants import CONN_STR

engine = create_engine(CONN_STR)  # type: ignore

Session = sessionmaker(bind=engine)

Base: Any = declarative_base()


def clean_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
