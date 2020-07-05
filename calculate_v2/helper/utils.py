import pickle
import os

import time
import datetime

import numpy as np


def dump(path, data):
    os.makedirs(path)
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def dump_cache(path, data):
    os.makedirs(path)
    with open(path+"/data.p", 'wb') as f:
        pickle.dump(data, f)


def load_cache(file):
    with open(file+"/data.p", 'rb') as f:
        return pickle.load(f)


def getTime(date):
    timestamp = int(time.mktime(datetime.datetime.
                                strptime(date, "%Y-%m-%d").timetuple()))
    return timestamp


def getTeamYearId(team, year):
    return int(str(year)+str(team))


def getTeamEventId(team, event):
    return int("1"+str(event).zfill(4)+str(team))


def clean(num):
    return round(float(num), 2)


# for ils
def logistic(n):
    return float(1/(1+np.e**(-4*(n-0.5))))


def logistic_inv(n):
    if n <= 0: return -1/3  # noqa 702
    return max(-1/3, float(-np.log((1-n)/np.e**2/n)/4))
