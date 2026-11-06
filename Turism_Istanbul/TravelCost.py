import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _travel_costs():
    return loadmat(os.path.join(_HERE, "Travel_Costs.mat"), mat_dtype=True)["Travel_Costs"]


def TravelCost(x):
    """Total travel cost of route x (MATLAB: TravelCost.m). x holds 1-based IDs."""
    Travel_Costs = _travel_costs()
    x = np.asarray(x, dtype=int)
    d = 0
    for i in range(x.size - 1):
        d = d + Travel_Costs[x[i] - 1, x[i + 1] - 1]
    y = d
    return y
