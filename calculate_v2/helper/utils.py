import pickle


def dump(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)
