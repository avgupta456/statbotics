from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from src.constants import CONN_STR, ASYNC_CONN_STR

engine = create_engine(CONN_STR)
async_engine = create_async_engine(ASYNC_CONN_STR)

Session = sessionmaker(bind=engine)
async_session = async_sessionmaker(bind=async_engine)


# Only for type hints, doesn't enable slots
# Mirror to avoid intermediate commits to DB
class Base(MappedAsDataclass, DeclarativeBase):
    pass


def clean_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
