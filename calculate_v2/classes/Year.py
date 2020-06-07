class Year:
    year = -1  # numeric year, ex: 2019

    TeamYear_c = None  # points to TeamYear children
    Event_c = None  # points to Event children

    def __init__(self, year):
        self.year = year
