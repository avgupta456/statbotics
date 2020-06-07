import pickle


def dump(path, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


def saveMain(main):
    print("Started Pickling")
    dump("./data/main.p", main)
    print("Finished Pickling")


def loadMain():
    print("Started Fetching")
    data = load("./data/main.p")
    print("Finished Fetching")
    return data
