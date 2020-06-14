from tba import read_tba

TBA = read_tba.ReadTBA()

events = TBA.getEvents('2002')
time = 0
for event in events:
    if event["key"] == "2002ca":
        time = event["time"]
data = TBA.getMatches('2002ca', time)
for match in data:
    print(match["time"])
