import ts
import elo

class Match:
    def __init__(self, data):
        self.key = data["key"]

        self.red, self.blue = [], []
        for red in data["alliances"]["red"]["team_keys"]: self.red.append(int(red[3:]))
        for blue in data["alliances"]["blue"]["team_keys"]: self.blue.append(int(blue[3:]))

        self.time = data["actual_time"]
        if(self.time==None): print(self.key)
        self.winner = data["winning_alliance"]

        self.red_score = data["alliances"]["red"]["score"]
        self.blue_score = data["alliances"]["blue"]["score"]
        if(self.red_score>self.blue_score): self.winner="red"
        elif(self.blue_score>self.red_score): self.winner="blue"
        else: self.winner = ""

        self.playoff = (data["comp_level"]!="qm")

        self.red_ratings_ts = []
        self.blue_ratings_ts = []

        self.red_ratings_elo = []
        self.blue_ratings_elo = []

    def get_win_actual(self):
        if self.winner=="red": return 1
        elif self.winner=="blue": return 0
        else: return 0.5

    '''TRUESKILL SECTION'''
    def set_ratings_ts(self, red_ratings, blue_ratings):
        self.red_ratings_ts = red_ratings
        self.blue_ratings_ts = blue_ratings

    def get_ratings_ts(self):
        return [self.red_ratings_ts, self.blue_ratings_ts]

    def get_win_prob_ts(self):
        return ts.win_probability(self.red_ratings_ts, self.blue_ratings_ts)

    def correct_pred_ts(self):
        if self.get_win_prob_ts()>0.5 and self.get_win_actual()>0.5: return True
        elif self.get_win_prob_ts()<0.5 and self.get_win_actual()<0.5: return True
        return False

    '''ELO SECTION'''
    def set_ratings_elo(self, red_ratings, blue_ratings):
        self.red_ratings_elo = red_ratings
        self.blue_ratings_elo = blue_ratings

    def get_ratings_elo(self):
        return [self.red_ratings_elo, self.blue_ratings_elo]

    def get_win_prob_elo(self):
        return elo.win_probability(self.red_ratings_elo, self.blue_ratings_elo)

    def correct_pred_elo(self):
        if self.get_win_prob_elo()>0.5 and self.get_win_actual()>0.5: return True
        elif self.get_win_prob_elo()<0.5 and self.get_win_actual()<0.5: return True
        return False

    def __lt__(self, other):
         return self.time < other.time

    def __repr__(self):
        return "Match " + self.key + " at " + str(self.time)

    def __str__(self):
        return self.__repr__()

class Team:
    def __init__(self, number, rating_ts, rating_elo):
        self.number = number
        self.rating_ts = rating_ts
        self.ratings_ts = [rating_ts.mu]

        self.rating_elo = rating_elo
        self.ratings_elo = [rating_elo]

    def get_rating_ts(self):
        return self.rating_ts.mu

    def get_rating_max_ts(self):
        return max(self.ratings_ts[min(len(self.ratings_ts)-1,8):])

    def set_rating_ts(self, rating):
        self.rating_ts = rating
        self.ratings_ts.append(rating.mu)

    def get_rating_elo(self):
        return self.rating_elo

    def get_rating_max_elo(self):
        return max(self.ratings_elo[min(len(self.ratings_elo)-1,8):])

    def set_rating_elo(self, rating):
        self.rating_elo = rating
        self.ratings_elo.append(rating)

    def __lt__(self, other):
        return self.get_rating_max_elo() > other.get_rating_max_elo()

    def __repr__(self):
        return "Team " + str(self.number) + ": (" + str(self.get_rating_ts()) + ", " + str(self.get_rating_elo()) + ")"

    def __str__(self):
        return self.__repr__()
