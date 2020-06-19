import numpy as np

from helper import constants


def computeOPR(input, output):
    MTM = np.matmul(input.T, input)
    MTs = np.matmul(input.T, output)
    return np.matmul(np.linalg.inv(MTM), MTs)


# matches assumed to be list of [r1, r2, r3, b1, b2, b3, r_s, b_s]
def formatMatches(matches):
    TM = len(matches[0])//2-1  # number of teams per match
    M = len(matches)  # number of matches

    teams = set()
    for m in matches:
        # ignoring two score variables
        for i in range(len(m) - 2):
            teams.add(m[i])
    teams = list(teams)

    T = len(teams)  # number of teams
    input = np.zeros(shape=(2*M, T), dtype="float")
    output = np.zeros(shape=(2 * M, 1), dtype="float")

    for i in range(M):
        for j in range(2 * TM):
            input[2*i+j//TM][teams.index(matches[i][j])] = 1
        output[2*i][0] = matches[i][-2]
        output[2*i+1][0] = matches[i][-1]
    return teams, input, output


def getOPR(event):
    matches = []
    for m in event.matches:
        if m.playoff == 0:
            match = m.getRed()
            match.extend(m.getBlue())
            match.extend([m.red_score, m.blue_score])
            matches.append(match)
    teams, input, output = formatMatches(matches)
    oprs = computeOPR(input, output)
    return teams, oprs
