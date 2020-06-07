class Event:
    name = ""
    key = ""

    start_timestamp = -1

    Year_p = None  # points to year parent
    TeamEvent_c = None  # poitns to Team Match children
    Match_c = None  # poitns to Match children

    def __init__(self, Year):
        self.Year = Year
