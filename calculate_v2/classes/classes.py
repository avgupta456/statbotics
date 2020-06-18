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
    elo = Column(Float)
    elo_recent = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)

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
    elo_max = Column(Float)
    elo_1p = Column(Float)
    elo_5p = Column(Float)
    elo_10p = Column(Float)
    elo_25p = Column(Float)
    elo_median = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)
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
    elo_start = Column(Float)
    elo_pre_champs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

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

    # 0 is regional, 1 is district, 2 is district champ,
    # 3 is worlds division, 4 is einsteins/FOC
    type = Column(Integer)
    week = Column(Integer)

    '''NEW'''
    elo_max = Column(Float)
    elo_top8 = Column(Float)
    elo_top24 = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.time < other.time

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
    elo_start = Column(Float)
    elo_pre_playoffs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        if self.getTeam() == other.getTeam():
            return self.time < other.time
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
    red_elo_pre = Column(String(30))
    red_elo_post = Column(String(30))

    blue = Column(String(20))
    blue_elo_pre = Column(String(30))
    blue_elo_post = Column(String(30))

    red_score = Column(Integer)
    blue_score = Column(Integer)

    winner = Column(String(10))
    elo_winner = Column(String(10))
    elo_win_prob = Column(Float)

    playoff = Column(Integer)  # 0 is qual, 1 is playoff
    time = Column(Integer)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.time < other.time

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
        return [float(x) for x in self.red.split(',')]

    def getBlue(self):
        return [float(x) for x in self.blue.split(',')]

    def getTeams(self):
        return [self.getRed(), self.getBlue()]

    def getWinner(self):
        return self.winner

    '''ELO GETTERS'''
    def getRedEloPre(self):
        return [float(x) for x in self.red_elo_pre.split(',')]

    def getRedEloPost(self):
        return [float(x) for x in self.red_elo_post.split(',')]

    def getBlueEloPre(self):
        return [float(x) for x in self.blue_elo_pre.split(',')]

    def getBlueEloPost(self):
        return [float(x) for x in self.blue_elo_post.split(',')]

    def getTeamElo(self, team):
        red, blue = self.getTeams()
        for i in range(len(red)):
            if red[i] == team:
                return self.getRedEloPost()[i]
        for i in range(len(blue)):
            if blue[i] == team:
                return self.getBlueEloPost()[i]

    '''ELO SETTERS'''
    def setRedEloPre(self, elos):
        self.red_elo_pre = ','.join(map(str, elos))

    def setRedEloPost(self, elos):
        self.red_elo_post = ','.join(map(str, elos))

    def setBlueEloPre(self, elos):
        self.blue_elo_pre = ','.join(map(str, elos))

    def setBlueEloPost(self, elos):
        self.blue_elo_post = ','.join(map(str, elos))


def createTables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
