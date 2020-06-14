from sqlalchemy import Table, Column, ForeignKey, Integer, Float, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()  # all classes inherit from Base

'''For Many-to-Many relationships'''

team_match_table = Table(
    'association1',
    Base.metadata,
    Column('left_id', Integer, ForeignKey('teams.id')),
    Column('right_id', Integer, ForeignKey('matches.id'))
)

teamYear_match_table = Table(
    'association2',
    Base.metadata,
    Column('left_id', Integer, ForeignKey('team_years.id')),
    Column('right_id', Integer, ForeignKey('matches.id'))
)

teamEvent_match_table = Table(
    'association3',
    Base.metadata,
    Column('left_id', Integer, ForeignKey('team_events.id')),
    Column('right_id', Integer, ForeignKey('matches.id'))
)


class Team(Base):
    '''DECLARATION'''
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)

    team_years = relationship("TeamYear", back_populates="team")
    team_events = relationship("TeamEvent", back_populates="team")
    matches = relationship(
        "Match",
        secondary=team_match_table,
        back_populates="teams"
    )

    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))
    active = Column(Integer)

    '''NEW'''
    elo = Column(Integer)
    elo_recent = Column(Integer)
    elo_mean = Column(Integer)
    elo_max = Column(Integer)

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

    events = relationship("Event", back_populates="year")
    matches = relationship("Match", back_populates="year")

    team_years = relationship("TeamYear", back_populates="year")
    team_events = relationship("TeamEvent", back_populates="year")

    '''NEW'''
    elo_max = Column(Integer)
    elo_1p = Column(Integer)
    elo_5p = Column(Integer)
    elo_10p = Column(Integer)
    elo_25p = Column(Integer)
    elo_median = Column(Integer)
    elo_mean = Column(Integer)
    elo_sd = Column(Integer)
    elo_acc = Column(Float)
    elo_mse = Column(Float)

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

    team_events = relationship("TeamEvent", back_populates="team_year")
    matches = relationship(
        "Match",
        secondary=teamYear_match_table,
        back_populates="team_years"
    )

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year', back_populates="team_years")

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates="team_years")

    '''NEW'''
    elo_start = Column(Integer)
    elo_pre_champs = Column(Integer)
    elo_end = Column(Integer)
    elo_mean = Column(Integer)
    elo_max = Column(Integer)
    elo_diff = Column(Integer)

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

    matches = relationship("Match", back_populates="event")
    team_events = relationship("TeamEvent", back_populates="event")

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year', back_populates="events")

    key = Column(String(20))
    name = Column(String(100))
    time = Column(Integer)
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))

    '''NEW'''
    # regional, district, district championship,
    #   elims_only, worlds division, einstein
    type = Column(Integer)
    elo_max = Column(Integer)
    elo_top8 = Column(Integer)
    elo_top24 = Column(Integer)
    elo_mean = Column(Integer)
    elo_sd = Column(Integer)

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

    def getTime(self):
        return self.time


class TeamEvent(Base):
    '''DECLARATIONS'''
    __tablename__ = 'team_events'
    id = Column(Integer, primary_key=True)

    matches = relationship(
        "Match",
        secondary=teamEvent_match_table,
        back_populates="team_events"
    )

    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates="team_events")

    team_year_id = Column(Integer, ForeignKey('team_years.id'))
    team_year = relationship('TeamYear', back_populates="team_events")

    year_id = Column(Integer, ForeignKey('years.id'))
    year = relationship('Year', back_populates="team_events")

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', back_populates="team_events")

    time = Column(Integer)

    '''NEW'''
    elo_start = Column(Integer)
    elo_pre_playoffs = Column(Integer)
    elo_end = Column(Integer)
    elo_mean = Column(Integer)
    elo_max = Column(Integer)
    elo_diff = Column(Integer)

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
    year = relationship('Year', back_populates="matches")

    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship('Event', back_populates="matches")

    teams = relationship(
        "Team",
        secondary=team_match_table,
        back_populates="matches"
    )

    team_years = relationship(
        "TeamYear",
        secondary=teamYear_match_table,
        back_populates="matches"
    )

    team_events = relationship(
        "TeamEvent",
        secondary=teamEvent_match_table,
        back_populates="matches"
    )

    key = Column(String(20))
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    red = Column(String(20))
    blue = Column(String(20))

    red_score = Column(Integer)
    blue_score = Column(Integer)

    winner = Column(String(10))

    time = Column(Integer)

    '''NEW'''
    elo_red = Column(Integer)
    elo_blue = Column(Integer)
    elo_diff = Column(Integer)  # abs value
    elo_prob = Column(Float)

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


def createTables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
