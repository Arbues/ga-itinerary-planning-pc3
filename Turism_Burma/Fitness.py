import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _distance_matrix():
    # Reading Distance Matrix (loaded once and cached instead of on every call)
    return loadmat(os.path.join(_HERE, "distance_matrix.mat"), mat_dtype=True)["distance_matrix"]


def Fitness(x):
    """Fitness = 1 / total distance (MATLAB: Fitness.m). x holds 1-based IDs."""
    distance_matrix = _distance_matrix()
    x = np.asarray(x, dtype=int)

    d = 0
    for i in range(x.size - 1):
        d = d + distance_matrix[x[i] - 1, x[i + 1] - 1]

    f = 1 / d
    return f
