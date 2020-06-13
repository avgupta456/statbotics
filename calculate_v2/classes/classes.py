from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    String
)

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from constants import (
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
Base = declarative_base()  # all classes inherit from Base


class Team(Base):
    __tablename__ = 'teams'
    number = Column(Integer, primary_key=True)
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(10))
    '''district = Column(String(10)) TODO'''

    def __lt__(self, other):
        return self.getNumber() < other.getNumber()

    def __repr__(self):
        return f'Team ({self.getNumber()})'

    def __str__(self):
        return self.__repr__()

    def getNumber(self):
        return self.number

    def getName(self):
        return self.name

    ''' TODO
    def getDistrict(self):
        return self.district
    '''

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country


class Year(Base):
    __tablename__ = 'years'
    year = Column(Integer, primary_key=True)

    def __lt__(self, other):
        return self.getYear() < other.getYear()

    def __repr__(self):
        return f'Year ({self.getYear()})'

    def __str__(self):
        return self.__repr__()

    def getYear(self):
        return self.year


class TeamYear(Base):
    __tablename__ = 'team_years'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('years.year'))
    year = relationship('Year')

    team_id = Column(Integer, ForeignKey('teams.number'))
    team = relationship('Team')

    def __lt__(self, other):
        if self.getTeam() == other.getTeam():
            return self.getYear() < other.getYear()
        else:
            return self.getTeam() < other.getTeam()

    def __repr__(self):
        return f'TeamYear ({self.getTeam()} {self.getYear()})'

    def __str__(self):
        return self.__repr__()

    def getTeam(self):
        return self.team_id

    def getYear(self):
        return self.year_id


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('years.year'))
    year = relationship('Year')
    key = Column(String(10))
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Event " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getKey(self):
        return self.key

    def getName(self):
        return self.name

    def getYear(self):
        return self.year_id

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    def getDistrict(self):
        return self.district


Base.metadata.drop_all(engine)  # remove later
Base.metadata.create_all(engine)

team = Team(name="Cortechs Robotics",
            number=5511,
            state="NC",
            country="USA")

year = Year(year=2015)
team_year = TeamYear(team=team, year=year)
event = Event(year=year, key='2019abc', name='test2', state='test3', country='test4', district='test5')
session.add_all([team, year, team_year, event])
session.commit()

query = session.query(Team).filter_by(name='Cortechs Robotics').first()
print(query)

query = session.query(Year).filter_by(year=2015).first()
print(query)

query = session.query(TeamYear).filter_by(id=1).first()
print(query)

query = session.query(Event).filter_by(id=1).first()
print(query)
