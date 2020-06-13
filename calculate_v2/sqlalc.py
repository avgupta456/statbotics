from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String

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

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Team(Base):
    __tablename__ = 'teams'
    number = Column(Integer, primary_key=True)
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(10))
    # district = Column(String(10))

    def __repr__(self):
        return f'Team ({self.number})'


class Year(Base):
    __tablename__ = 'years'
    year = Column(Integer, primary_key=True)

    def __repr__(self):
        return f'Year ({self.year})'


class TeamYear(Base):
    __tablename__ = 'team_years'
    id = Column(Integer, primary_key=True)
    year_id = Column(Integer, ForeignKey('years.year'))
    year = relationship('Year')

    team_id = Column(Integer, ForeignKey('teams.number'))
    team = relationship('Team')

    def __repr__(self):
        return f'TeamYear ({self.team_id} {self.year_id})'


Base.metadata.drop_all(engine)  # remove later
Base.metadata.create_all(engine)

team = Team(name="Cortechs Robotics", number=5511, state="NC", country="USA")
year = Year(year=2015)
team_year = TeamYear(team=team, year=year)
session.add_all([team, year, team_year])
session.commit()

query = session.query(Team).filter_by(name='Cortechs Robotics').first()
print(query)

query = session.query(Year).filter_by(year=2015).first()
print(query)

query = session.query(TeamYear).filter_by(id=1).first()
print(query)
