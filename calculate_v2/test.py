from tba import read_tba

TBA = read_tba.ReadTBA()

data = TBA.getEvents(2009)
for match in data:
    print(match)
