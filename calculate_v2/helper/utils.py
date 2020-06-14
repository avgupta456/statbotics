import pickle
import os


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
