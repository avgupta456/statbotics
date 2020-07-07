import numpy as np


def clean(num):
    return round(float(num), 2)


# for ils
def logistic(n):
    return float(1/(1+np.e**(-4*(n-0.5))))
