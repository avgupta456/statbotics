from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes.constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE
)

engine = create_engine('mysql+pymysql://' +
                       MYSQL_USERNAME + ":" +
                       MYSQL_PASSWORD + "@" +
                       MYSQL_HOST + ":" +
                       MYSQL_PORT + "/" +
                       MYSQL_DATABASE,
                       echo=False)  # make true to see sql queries

session = sessionmaker(bind=engine)()  # sessionmake returns function


def getEngine():
    return engine


def getSession():
    return session
