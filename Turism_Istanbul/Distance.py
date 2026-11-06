import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _travel_dis():
    # mat_dtype=True returns the MATLAB class (double), not the storage type
    return loadmat(os.path.join(_HERE, "Travel_Dis.mat"), mat_dtype=True)["Travel_Dis"]


def Distance(x):
    """Total travel distance of route x (MATLAB: Distance.m). x holds 1-based IDs."""
    Travel_Dis = _travel_dis()
    x = np.asarray(x, dtype=int)
    d = 0
    for i in range(x.size - 1):
        d = d + Travel_Dis[x[i] - 1, x[i + 1] - 1]
        y = d
    return y
