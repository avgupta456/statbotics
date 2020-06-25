import pickle
import os

import time
import datetime


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
