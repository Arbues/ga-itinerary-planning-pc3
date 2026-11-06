import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _distance_matrix():
    # mat_dtype=True returns the MATLAB class (double), not the storage type
    return loadmat(os.path.join(_HERE, "distance_matrix.mat"), mat_dtype=True)["distance_matrix"]


def Distance(x):
    """Total distance of route x (MATLAB: Distance.m). x holds 1-based IDs."""
    distance_matrix = _distance_matrix()
    x = np.asarray(x, dtype=int)
    d = 0
    for i in range(x.size - 1):
        d = d + distance_matrix[x[i] - 1, x[i + 1] - 1]
        y = d
    return y
