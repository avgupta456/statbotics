from tba import read_tba

TBA = read_tba.ReadTBA()

year = 2020
event = TBA.getEvents(str(year))[10]
time = 0
total = 0
TBA.getMatches(year, event["key"], event["time"])
