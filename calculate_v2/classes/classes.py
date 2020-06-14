from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # all classes inherit from Base


class Team(Base):
    '''DECLARATION'''
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)

    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))
    active = Column(Integer)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.getNumber() < other.getNumber()

    def __repr__(self):
        return f'Team ({self.getNumber()})'

    def __str__(self):
        return self.__repr__()

    '''GET KEYS'''
    def getNumber(self):
        return self.id

    '''GETTERS'''
    def getName(self):
        return self.name

    def getDistrict(self):
        return self.district

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    def isActive(self):
        return self.active == 1


class Year(Base):
    '''DECLARATION'''
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.getYear() < other.getYear()

    def __repr__(self):
        return f'Year ({self.getYear()})'

    def __str__(self):
        return self.__repr__()

    '''GET KEYS'''
    def getYear(self):
        return self.id

    '''GETTERS'''


class TeamYear(Base):
    '''DECLARATION'''
    __tablename__ = 'team_years'
    id = Column(Integer, primary_key=True)

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year')

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team')

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        if self.getTeam() == other.getTeam():
            return self.getYear() < other.getYear()
        else:
            return self.getTeam() < other.getTeam()

    def __repr__(self):
        return f'TeamYear ({self.getTeam()} {self.getYear()})'

    def __str__(self):
        return self.__repr__()

    '''GET KEYS'''
    def getTeam(self):
        return self.team_id

    def getYear(self):
        return self.year_id

    def getId(self):
        return self.id

    '''GETTERS'''


class Event(Base):
    '''DECLARATION'''
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year')

    key = Column(String(20))
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Event " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    '''GET KEYS'''
    def getYear(self):
        return self.year_id

    def getId(self):
        return self.id

    '''GETTERS'''
    def getKey(self):
        return self.key

    def getName(self):
        return self.name

    def getState(self):
        return self.state

    def getCountry(self):
        return self.country

    def getDistrict(self):
        return self.district


class TeamEvent(Base):
    '''DECLARATIONS'''
    __tablename__ = 'team_events'
    id = Column(Integer, primary_key=True)

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team')

    team_year_id = Column(Integer, ForeignKey('team_years.id'))
    team_year = relationship('TeamYear')

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year')

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event')

    '''SUPER FUNCTIONS'''
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

    '''GET KEYS'''
    def getTeam(self):
        return self.team_id

    def getTeamYear(self):
        return self.team_year_id

    def getId(self):
        return self.id

    def getYear(self):
        return self.year_id

    def getEvent(self):
        return self.event_id

    '''GETTERS'''
    def getKey(self):
        return self.event.getKey()


class Match(Base):
    '''DECLARATION'''
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year')

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event')

    key = Column(String(20))
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    red = Column(String(20))
    blue = Column(String(20))

    winner = Column(String(10))

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Match " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    '''GET KEYS'''
    def getYear(self):
        return self.year_id

    def getEvent(self):
        return self.event_id

    def getId(self):
        return self.id

    '''GETTERS'''
    def getKey(self):
        return self.key

    def getCompLevel(self):
        return self.comp_level

    def getSetNumber(self):
        return self.set_number

    def getMatchNumber(self):
        return self.match_number

    def getRed(self):
        return [int(x) for x in self.red.split(',')]

    def getBlue(self):
        return [int(x) for x in self.blue.split(',')]

    def getWinner(self):
        return self.winner


class TeamMatch(Base):
    '''DECLARATION'''
    __tablename__ = 'team_matches'
    id = Column(Integer, primary_key=True)

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year')

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event')

    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match')

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team')

    team_year_id = Column(Integer, ForeignKey('team_years.id'))
    team_year = relationship('TeamYear')

    team_event_id = Column(Integer, ForeignKey('team_events.id'))
    team_event = relationship('TeamEvent')

    alliance = Column(String(10))

    '''SUPER FUNCTIONS'''
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

    '''GET KEYS'''
    def getTeam(self):
        return self.team_id

    def getTeamYear(self):
        return self.team_year_id

    def getTeamEvent(self):
        return self.team_event_id

    def getId(self):
        return self.id

    def getYear(self):
        return self.year_id

    def getEvent(self):
        return self.event_id

    def getMatch(self):
        return self.match_id

    '''GETTERS'''
    def getAlliance(self):
        return self.alliance


def createTables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
