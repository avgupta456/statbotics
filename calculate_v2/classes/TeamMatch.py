class TeamMatch:
    TeamEvent_p = None  # points to Team Event parent
    Matc_ph = None  # points to Match parent

    def __init__(self, TeamEvent, Match):
        self.TeamEvent = TeamEvent
        self.Match = Match
