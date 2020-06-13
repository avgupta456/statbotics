from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes import classes
from classes.constants import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE
)


class SQL:
    def __init__(self, clean=True):
        # set echo to true to see SQL queries in console
        self.engine = create_engine('mysql+pymysql://' +
                                    MYSQL_USERNAME + ":" +
                                    MYSQL_PASSWORD + "@" +
                                    MYSQL_HOST + ":" +
                                    MYSQL_PORT + "/" +
                                    MYSQL_DATABASE,
                                    echo=False)

        # sessionmake returns function
        self.session = sessionmaker(bind=self.engine)()

        # resets tables
        if clean:
            classes.createTables(self.engine)

    def getEngine(self):
        return self.engine

    def getSession(self):
        return self.session
