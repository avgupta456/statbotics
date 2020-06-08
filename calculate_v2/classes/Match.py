class Match:
    def __init__(self, Event, dict):
        self.Event_p = Event
        self.TeamMatch_c = {}

        self.key = dict["key"]
        self.comp_level = dict["comp_level"]
        self.set_number = dict["set_number"]
        self.match_number = dict["match_number"]
        self.red = dict["red"]
        self.blue = dict["blue"]
        self.winner = dict["winner"]
        self.time = dict["time"]
        self.score_breakdown = dict["score_breakdown"]

    def __lt__(self, other):
        return self.getKey() < other.getKey()

    def __repr__(self):
        return "(Match " + str(self.getKey()) + ")"

    def __str__(self):
        return self.__repr__()

    def getKey(self):
        return self.key

    def getParentEvent(self):
        return self.Event_p

    def addTeamMatches(self):
        for t in self.red:
            self.addTeamMatch({"num": t,
                               "alliance": "red",
                               "key": self.getKey()})
        for t in self.blue:
            self.addTeamMatch({"num": t,
                               "alliance": "blue",
                               "key": self.getKey()})

    def addTeamMatch(self, dict):
        self.getParentEvent().addTeamMatch(dict["num"], self.getKey(), dict)

    def setTeamMatch(self, team, TeamMatch):
        self.TeamMatch_c[team] = TeamMatch

    def getTeamMatch(self, team):
        return self.TeamMatch_c[team]

    def getTeamMatches(self):
        return self.TeamMatch_c

    def getCompLevel(self):
        return self.comp_level

    def getSetNumber(self):
        return self.set_number

    def getMatchNumber(self):
        return self.match_number

    def getRed(self):
        return self.red

    def getBlue(self):
        return self.blue

    def getWinner(self):
        return self.winner

    def getTime(self):
        return self.time

    def getScoreBreakdown(self):
        return self.score_breakdown
