import numpy as np
from helper import constants


def computeOPR(input, output, year):
    MTM = np.matmul(input.T, input)
    MTs = np.matmul(input.T, output)
    try:
        out = np.matmul(np.linalg.inv(MTM), MTs)
    except np.linalg.LinAlgError:
        out = computeAverages(input, output)
    if np.min(out) < - constants.mean[year]/3:
        out = computeAverages(input, output)
    return out


def computeAverages(input, output):
    out = np.zeros(shape=(input.shape[1], 1))
    for i in range(input.shape[1]):
        scores = []
        for j in range(input.shape[0]):
            if input[j][i] == 1:
                scores.append(output[j])
        out[i] = sum(scores)/len(scores)
    return out


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
    matches, out = [], {}
    match_objs = sorted(event.getMatches(playoffs=False))
    for m in match_objs:
        if m.playoff == 0:
            match = m.getRed()
            match.extend(m.getBlue())
            match.extend([m.red_score, m.blue_score])
            matches.append(match)

    teams, input, output = formatMatches(matches)
    oprs = computeOPR(input, output, event.getYear())
    for i in range(len(teams)):
        out[teams[i]] = round(float(oprs[i][0]), 2)

    return out
