from classes import classes
from constants.cloud_db import CLOUDSQL_DATABASE, CLOUDSQL_PASSWORD, CLOUDSQL_USER
from constants.local_db import (
    MYSQL_DATABASE,
    MYSQL_HOST,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQL_USERNAME,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SQL:
    def __init__(self, clean=True, echo=False, local=True, cloud=True):

        if local:
            self.local_engine = create_engine(
                "mysql+pymysql://"
                + MYSQL_USERNAME
                + ":"
                + MYSQL_PASSWORD
                + "@"
                + MYSQL_HOST
                + ":"
                + MYSQL_PORT
                + "/"
                + MYSQL_DATABASE,
                echo=echo,
            )
            self.local_session = sessionmaker(bind=self.local_engine)()

        if cloud:
            self.cloud_engine = create_engine(
                "mysql+pymysql://"
                + CLOUDSQL_USER
                + ":"
                + CLOUDSQL_PASSWORD
                + "@127.0.0.1:3307/"
                + CLOUDSQL_DATABASE,
                echo=echo,
            )
            self.cloud_session = sessionmaker(bind=self.cloud_engine)()

        # resets tables
        if clean:
            classes.createTables(self.local_engine)

    def getLocalEngine(self):
        return self.local_engine

    def getCloudEngine(self):
        return self.cloud_engine

    def getLocalSession(self):
        return self.local_session

    def getCloudSession(self):
        return self.cloud_session
