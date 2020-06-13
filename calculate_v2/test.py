from tba import read_tba

TBA = read_tba.ReadTBA()

data = TBA.getMatches('2005wat')
for match in data:
    print(match)
