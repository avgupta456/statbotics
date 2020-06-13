from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # all classes inherit from Base


class Team(Base):
    __tablename__ = 'teams'
    number = Column(Integer, primary_key=True)
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
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
        return self.team.getNumber()

    def getYear(self):
        return self.year.getYear()


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
        return self.year.getYear()

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    def getDistrict(self):
        return self.district


class TeamEvent(Base):
    __tablename__ = 'team_events'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event')

    team_year_id = Column(Integer, ForeignKey('team_years.id'))
    team_year = relationship('TeamYear')

    def __lt__(self, other):
        if self.getTeam() == other.getTeam():
            return self.getKey() < other.getKey()
        else:
            return self.getTeam() < other.getTeam()

    def __repr__(self):
        return "(TeamEvent " + \
                str(self.getTeam()) + " " + \
                str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getTeam(self):
        return self.team_year.getTeam()

    def getKey(self):
        return self.event.getKey()


class Match(Base):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event')

    key = Column(String(10))
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    red1 = Column(Integer)
    red2 = Column(Integer)
    red3 = Column(Integer)

    blue1 = Column(Integer)
    blue2 = Column(Integer)
    blue3 = Column(Integer)

    winner = Column(String(10))

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Match " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getKey(self):
        return self.key

    def getCompLevel(self):
        return self.comp_level

    def getSetNumber(self):
        return self.set_number

    def getMatchNumber(self):
        return self.match_number

    def getRed(self):
        return [self.red1, self.red2, self.red3]

    def getBlue(self):
        return [self.blue1, self.blue2, self.blue3]

    def getWinner(self):
        return self.winner


class TeamMatch(Base):
    __tablename__ = 'team_matches'

    id = Column(Integer, primary_key=True)
    team_event_id = Column(Integer, ForeignKey('team_events.id'))
    team_event = relationship('TeamEvent')

    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match')

    alliance = Column(String(10))

    def __lt__(self, other):
        if self.getTeam() == other.getTeam():
            return self.getKey() < other.getKey()
        else:
            return self.getTeam() < other.getTeam()

    def __repr__(self):
        return "(TeamMatch " + \
                str(self.getTeam()) + " " + \
                str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getTeam(self):
        return self.team_event.getTeam()

    def getKey(self):
        return self.match.getKey()

    def getAlliance(self):
        return self.alliance


def createTables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
