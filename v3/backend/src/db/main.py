from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker

from src.constants import CONN_STR

engine = create_engine(CONN_STR)

Session = sessionmaker(bind=engine)


# Only for type hints, doesn't enable slots
# Mirror to avoid intermediate commits to DB
class Base(MappedAsDataclass, DeclarativeBase):
    pass


def clean_db() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
