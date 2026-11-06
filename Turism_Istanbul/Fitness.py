import os
from functools import lru_cache

import numpy as np
from scipy.io import loadmat

from Norm import Norm
from TravelCost import TravelCost

_HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def _normalized_matrices():
    # Reading Distance and Time Matrices (loaded once and cached instead of on every call)
    Travel_Dis = loadmat(os.path.join(_HERE, "Travel_Dis.mat"), mat_dtype=True)["Travel_Dis"]
    Ndmat = Norm(Travel_Dis)

    Travel_Times = loadmat(os.path.join(_HERE, "Travel_Times.mat"), mat_dtype=True)["Travel_Times"]
    Ntmat = Norm(Travel_Times)
    return Ndmat, Ntmat


def Fitness(x, budget):
    """Fitness = normalized remaining budget / (normalized distance + time)
    (MATLAB: Fitness.m). x holds 1-based IDs."""
    Ndmat, Ntmat = _normalized_matrices()
    x = np.asarray(x, dtype=int)

    # Reading Travel Costs Matrix
    n = TravelCost(x)

    d = 0
    for i in range(x.size - 1):
        d = d + Ndmat[x[i] - 1, x[i + 1] - 1] + Ntmat[x[i] - 1, x[i + 1] - 1]
    Npayment = (budget - n) / budget
    f = Npayment / d

    return f
