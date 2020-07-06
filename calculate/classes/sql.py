from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from classes import classes

from constants.cloud_db import (
    CLOUDSQL_USER,
    CLOUDSQL_PASSWORD,
    CLOUDSQL_DATABASE
)

from constants.local_db import (
    MYSQL_USERNAME,
    MYSQL_PASSWORD,
    MYSQL_HOST,
    MYSQL_PORT,
    MYSQL_DATABASE
)


class SQL:
    def __init__(self, clean=True, echo=False):

        self.local_engine = create_engine('mysql+pymysql://' +
                                          MYSQL_USERNAME + ":" +
                                          MYSQL_PASSWORD + "@" +
                                          MYSQL_HOST + ":" +
                                          MYSQL_PORT + "/" +
                                          MYSQL_DATABASE,
                                          echo=echo)

        # CLOUDSQL DB
        self.cloud_engine = create_engine('mysql+pymysql://' +
                                          CLOUDSQL_USER + ':' +
                                          CLOUDSQL_PASSWORD +
                                          '@127.0.0.1:3307/' +
                                          CLOUDSQL_DATABASE, echo=echo)

        # sessionmaker returns function
        self.local_session = sessionmaker(bind=self.local_engine)()
        self.cloud_session = sessionmaker(bind=self.cloud_engine)()

        # resets tables
        if clean: classes.createTables(self.local_engine)  # noqa 701

    def getLocalEngine(self):
        return self.local_engine

    def getCloudEngine(self):
        return self.cloud_engine

    def getLocalSession(self):
        return self.local_session

    def getCloudSession(self):
        return self.cloud_session
