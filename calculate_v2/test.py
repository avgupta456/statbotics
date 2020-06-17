from tba import read_tba

TBA = read_tba.ReadTBA()

events = TBA.getEvents('2006')
time = 0
total = 0
for event in events:
    print(event)
    total += len(TBA.getMatches(2006, event["key"], event["time"]))
print(total)
