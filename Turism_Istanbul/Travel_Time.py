import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _travel_times():
    return loadmat(os.path.join(_HERE, "Travel_Times.mat"), mat_dtype=True)["Travel_Times"]


def Travel_Time(x):
    """Total travel time of route x (MATLAB: Travel_Time.m). x holds 1-based IDs."""
    Travel_Times = _travel_times()
    x = np.asarray(x, dtype=int)
    t = 0
    for i in range(x.size - 1):
        t = t + Travel_Times[x[i] - 1, x[i + 1] - 1]
        y = t
    return y
