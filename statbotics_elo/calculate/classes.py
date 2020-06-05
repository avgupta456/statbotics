import elo


class Match:
    def __init__(self, data):
        self.key = data["key"]

        self.red, self.blue = [], []
        for red in data["alliances"]["red"]["team_keys"]:
            self.red.append(int(red[3:]))
        for blue in data["alliances"]["blue"]["team_keys"]:
            self.blue.append(int(blue[3:]))

        self.time = data["actual_time"]
        self.winner = data["winning_alliance"]

        self.red_score = data["alliances"]["red"]["score"]
        self.blue_score = data["alliances"]["blue"]["score"]

        if(self.red_score > self.blue_score):
            self.winner = "red"
        elif(self.blue_score > self.red_score):
            self.winner = "blue"
        else:
            self.winner = ""

        self.playoff = (data["comp_level"] != "qm")

        self.red_ratings = []
        self.blue_ratings = []

        self.red_ratings_end = []
        self.blue_ratings_end = []

    def get_win_actual(self):
        if self.winner == "red":
            return 1
        elif self.winner == "blue":
            return 0
        else:
            return 0.5

    def set_ratings(self, red_ratings, blue_ratings):
        self.red_ratings = red_ratings
        self.blue_ratings = blue_ratings

    def set_ratings_end(self, red_ratings, blue_ratings):
        self.red_ratings_end = red_ratings
        self.blue_ratings_end = blue_ratings

    def get_ratings(self):
        return [self.red_ratings, self.blue_ratings]

    def get_ratings_end(self):
        return [self.red_ratings_end, self.blue_ratings_end]

    def get_win_prob(self):
        return elo.win_probability(self.red_ratings, self.blue_ratings)

    def correct_pred(self):
        if self.get_win_prob() > 0.5 and self.get_win_actual() > 0.5:
            return True
        elif self.get_win_prob() < 0.5 and self.get_win_actual() < 0.5:
            return True
        return False

    def __lt__(self, other):
        return self.time < other.time

    def __repr__(self):
        return "Match " + self.key + " at " + str(self.time)

    def __str__(self):
        return self.__repr__()


class Team:
    def __init__(self, number, rating):
        self.number = number

        self.rating = rating
        self.ratings = [rating]

    def get_rating(self):
        return self.rating

    def get_rating_max(self):
        return max(self.ratings[min(len(self.ratings)-1, 8):])

    def set_rating(self, rating):
        self.rating = rating
        self.ratings.append(rating)

    def __lt__(self, other):
        return self.get_rating_max() > other.get_rating_max()

    def __repr__(self):
        return "Team " + str(self.number) + ":\t" + str(self.get_rating())

    def __str__(self):
        return self.__repr__()
