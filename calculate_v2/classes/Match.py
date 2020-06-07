class Match:
    def __init__(self, Event, dict):
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
