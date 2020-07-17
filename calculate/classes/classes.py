from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()  # all classes inherit from Base


class Team(Base):
    '''DECLARATION'''
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)

    team_years = relationship("TeamYear", back_populates="team")
    team_events = relationship("TeamEvent", back_populates="team")
    team_matches = relationship("TeamMatch", back_populates="team")

    '''GENERAL'''
    name = Column(String(100))
    state = Column(String(10))
    country = Column(String(30))
    district = Column(String(10))
    active = Column(Integer)

    '''ELO'''
    elo = Column(Float)
    elo_recent = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f'Team ({self.id})'

    def __str__(self):
        return self.__repr__()

    def isActive(self):
        return self.active == 1


class Year(Base):
    '''DECLARATION'''
    __tablename__ = 'years'
    id = Column(Integer, primary_key=True, index=True)

    events = relationship("Event", back_populates="year")
    matches = relationship("Match", back_populates="year")

    team_years = relationship("TeamYear", back_populates="year")
    team_events = relationship("TeamEvent", back_populates="year")
    team_matches = relationship("TeamMatch", back_populates="year")

    '''ELO'''
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

    '''OPR'''
    # stats are for team's max opr in given year, NOT EVENT
    opr_max = Column(Float)
    opr_1p = Column(Float)
    opr_5p = Column(Float)
    opr_10p = Column(Float)
    opr_25p = Column(Float)
    opr_median = Column(Float)
    opr_mean = Column(Float)
    opr_sd = Column(Float)
    opr_acc = Column(Float)
    opr_mse = Column(Float)

    ''''MIX'''
    mix_acc = Column(Float)
    mix_mse = Column(Float)

    '''ILS'''
    rp1_acc = Column(Float)
    rp1_mse = Column(Float)
    rp2_acc = Column(Float)
    rp2_mse = Column(Float)

    '''CONSTANTS'''
    score_mean = Column(Float)
    score_sd = Column(Float)
    auto_mean = Column(Float)
    teleop_mean = Column(Float)
    one_mean = Column(Float)
    two_mean = Column(Float)
    endgame_mean = Column(Float)
    foul_mean = Column(Float)
    no_foul_mean = Column(Float)
    rp_1_mean = Column(Float)
    rp_2_mean = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f'Year ({self.id})'

    def __str__(self):
        return self.__repr__()


class TeamYear(Base):
    '''DECLARATION'''
    __tablename__ = 'team_years'
    id = Column(Integer, primary_key=True, index=True)

    team_events = relationship("TeamEvent", back_populates="team_year")
    team_matches = relationship("TeamMatch", back_populates="team_year")

    year_id = Column(Integer, ForeignKey('years.id'), index=True)
    year = relationship('Year', back_populates="team_years")

    team_id = Column(Integer, ForeignKey('teams.id'), index=True)
    team = relationship('Team', back_populates="team_years")

    '''ELO'''
    elo_start = Column(Float)
    elo_pre_champs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

    '''OPR'''
    opr_start = Column(Float)
    opr_end = Column(Float)

    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_1 = Column(Float)
    opr_2 = Column(Float)
    opr_endgame = Column(Float)
    opr_fouls = Column(Float)
    opr_no_fouls = Column(Float)

    '''ILS'''
    ils_1 = Column(Float)
    ils_2 = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        if self.team_id == other.team_id:
            return self.year_id < other.year_id
        return self.team_id < other.team_id

    def __repr__(self):
        return f'TeamYear ({self.team_id} {self.year_id})'

    def __str__(self):
        return self.__repr__()


class Event(Base):
    '''DECLARATION'''
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)

    matches = relationship("Match", back_populates="event")
    team_events = relationship("TeamEvent", back_populates="event")
    team_matches = relationship("TeamMatch", back_populates="event")

    year_id = Column(Integer, ForeignKey('years.id'), index=True)
    year = relationship('Year', back_populates="events")

    '''GENERAL'''
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

    '''ELO'''
    elo_max = Column(Float)
    elo_top8 = Column(Float)
    elo_top24 = Column(Float)
    elo_mean = Column(Float)
    elo_sd = Column(Float)

    '''OPR'''
    opr_max = Column(Float)
    opr_top8 = Column(Float)
    opr_top24 = Column(Float)
    opr_mean = Column(Float)
    opr_sd = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "(Event " + str(self.key) + ")"

    def __str__(self):
        return self.__repr__()

    def getTeamEvent(self, team):
        for team_event in self.team_events:
            if team_event.team_id == team:
                return team_event
        return None


class TeamEvent(Base):
    '''DECLARATIONS'''
    __tablename__ = 'team_events'
    id = Column(Integer, primary_key=True, index=True)

    team_matches = relationship("TeamMatch", back_populates="team_event")

    team_id = Column(Integer, ForeignKey('teams.id'), index=True)
    team = relationship('Team', back_populates="team_events")

    team_year_id = Column(Integer, ForeignKey('team_years.id'), index=True)
    team_year = relationship('TeamYear', back_populates="team_events")

    year_id = Column(Integer, ForeignKey('years.id'), index=True)
    year = relationship('Year', back_populates="team_events")

    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    event = relationship('Event', back_populates="team_events")

    '''GENERAL'''
    time = Column(Integer)

    '''ELO'''
    elo_start = Column(Float)
    elo_pre_playoffs = Column(Float)
    elo_end = Column(Float)
    elo_mean = Column(Float)
    elo_max = Column(Float)
    elo_diff = Column(Float)

    '''OPR'''
    opr_start = Column(Float)
    opr_end = Column(Float)

    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_1 = Column(Float)
    opr_2 = Column(Float)
    opr_endgame = Column(Float)
    opr_fouls = Column(Float)
    opr_no_fouls = Column(Float)

    '''ILS'''
    ils_1_start = Column(Float)
    ils_2_start = Column(Float)
    ils_1_end = Column(Float)
    ils_2_end = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        if self.team_id == other.team_id:
            return self.time < other.time
        return self.team_id < other.team_id

    def __repr__(self):
        return "(TeamEvent " + \
                str(self.team_id) + " " + \
                str(self.event.key) + ")"

    def __str__(self):
        return self.__repr__()


class Match(Base):
    '''DECLARATION'''
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True, index=True)

    team_matches = relationship("TeamMatch", back_populates="match")

    year_id = Column(Integer, ForeignKey('years.id'), index=True)
    year = relationship('Year', back_populates="matches")

    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    event = relationship('Event', back_populates="matches")

    '''GENERAL'''
    key = Column(String(20))
    comp_level = Column(String(10))
    set_number = Column(Integer)
    match_number = Column(Integer)

    red = Column(String(20))
    red_elo_sum = Column(Float)
    red_opr_sum = Column(Float)
    red_ils_1_sum = Column(Float)
    red_ils_2_sum = Column(Float)

    blue = Column(String(20))
    blue_elo_sum = Column(Float)
    blue_opr_sum = Column(Float)
    blue_ils_1_sum = Column(Float)
    blue_ils_2_sum = Column(Float)

    winner = Column(String(10))
    elo_winner = Column(String(10))
    elo_win_prob = Column(Float)
    opr_winner = Column(String(10))
    opr_win_prob = Column(Float)
    mix_winner = Column(String(10))
    mix_win_prob = Column(Float)
    red_rp_1_prob = Column(Float)
    red_rp_2_prob = Column(Float)
    blue_rp_1_prob = Column(Float)
    blue_rp_2_prob = Column(Float)

    playoff = Column(Integer)  # 0 is qual, 1 is playoff
    time = Column(Integer)

    red_score = Column(Integer)
    blue_score = Column(Integer)

    red_auto = Column(Integer)
    red_auto_movement = Column(Integer)
    red_auto_1 = Column(Integer)
    red_auto_2 = Column(Integer)
    red_auto_2_1 = Column(Integer)
    red_auto_2_2 = Column(Integer)
    red_auto_2_3 = Column(Integer)
    red_teleop_1 = Column(Integer)
    red_teleop_2 = Column(Integer)
    red_teleop_2_1 = Column(Integer)
    red_teleop_2_2 = Column(Integer)
    red_teleop_2_3 = Column(Integer)
    red_1 = Column(Integer)
    red_2 = Column(Integer)
    red_teleop = Column(Integer)
    red_endgame = Column(Integer)
    red_no_fouls = Column(Integer)
    red_fouls = Column(Integer)
    red_rp_1 = Column(Integer)
    red_rp_2 = Column(Integer)

    blue_auto = Column(Integer)
    blue_auto_movement = Column(Integer)
    blue_auto_1 = Column(Integer)
    blue_auto_2 = Column(Integer)
    blue_auto_2_1 = Column(Integer)
    blue_auto_2_2 = Column(Integer)
    blue_auto_2_3 = Column(Integer)
    blue_teleop_1 = Column(Integer)
    blue_teleop_2 = Column(Integer)
    blue_teleop_2_1 = Column(Integer)
    blue_teleop_2_2 = Column(Integer)
    blue_teleop_2_3 = Column(Integer)
    blue_1 = Column(Integer)
    blue_2 = Column(Integer)
    blue_teleop = Column(Integer)
    blue_endgame = Column(Integer)
    blue_no_fouls = Column(Integer)
    blue_fouls = Column(Integer)
    blue_rp_1 = Column(Integer)
    blue_rp_2 = Column(Integer)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "(Match " + str(self.key) + ")"

    def __str__(self):
        return self.__repr__()

    def getRed(self):
        return [int(x) for x in self.red.split(',')]

    def getBlue(self):
        return [int(x) for x in self.blue.split(',')]

    def getTeams(self):
        return [self.getRed(), self.getBlue()]

    def getRedTeamMatches(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "red":
                out.append(team_match)
        return out

    def getBlueTeamMatches(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "blue":
                out.append(team_match)
        return out

    def getTeamMatches(self):
        red, blue = [], []
        for team_match in self.team_matches:
            if team_match.alliance == "red":
                red.append(team_match)
            else:
                blue.append(team_match)
        return [red, blue]

    '''ELO/OPR GETTERS'''
    def getRedElo(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "red":
                out.append(team_match.elo)
        return out

    def getBlueElo(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "blue":
                out.append(team_match.elo)
        return out

    def getTeamElo(self, team):
        for team_match in self.team_matches:
            if team_match.team_id == team:
                return team_match.elo

    def getRedOpr(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "red":
                out.append(team_match.opr_start)
        return out

    def getBlueOpr(self):
        out = []
        for team_match in self.team_matches:
            if team_match.alliance == "blue":
                out.append(team_match.opr_start)
        return out

    def getTeamOpr(self, team):
        for team_match in self.team_matches:
            if team_match.team_id == team:
                return team_match.opr_score

    '''ELO/OPR SETTERS'''

    def setTeams(self, red, blue):
        self.red_teams = ",".join(red)
        self.blue_teams = ",".join(blue)


class TeamMatch(Base):
    '''DECLARATION'''
    __tablename__ = 'team_matches'
    id = Column(Integer, primary_key=True, index=True)

    team_id = Column(Integer, ForeignKey('teams.id'), index=True)
    team = relationship('Team', back_populates="team_matches")

    team_year_id = Column(Integer, ForeignKey('team_years.id'), index=True)
    team_year = relationship('TeamYear', back_populates="team_matches")

    team_event_id = Column(Integer, ForeignKey('team_events.id'), index=True)
    team_event = relationship('TeamEvent', back_populates="team_matches")

    year_id = Column(Integer, ForeignKey('years.id'), index=True)
    year = relationship('Year', back_populates="team_matches")

    event_id = Column(Integer, ForeignKey('events.id'), index=True)
    event = relationship('Event', back_populates="team_matches")

    match_id = Column(Integer, ForeignKey('matches.id'), index=True)
    match = relationship('Match', back_populates="team_matches")

    time = Column(Integer)
    alliance = Column(String(30))

    '''GENERAL'''

    elo = Column(Float)
    opr_score = Column(Float)
    opr_auto = Column(Float)
    opr_teleop = Column(Float)
    opr_one = Column(Float)
    opr_two = Column(Float)
    opr_endgame = Column(Float)
    opr_no_fouls = Column(Float)
    opr_fouls = Column(Float)

    ils_1 = Column(Float)
    ils_2 = Column(Float)

    '''SUPER FUNCTIONS'''
    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "(Match " + \
                str(self.team_id) + " " + \
                str(self.match.key) + ")"

    def __str__(self):
        return self.__repr__()


def createTables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
