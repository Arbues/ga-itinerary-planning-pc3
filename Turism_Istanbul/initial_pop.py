import os

import numpy as np
from scipy.io import savemat

_HERE = os.path.dirname(os.path.abspath(__file__))


def initial_pop(nRoute, nPlaces):
    """Create nRoute random routes starting at place 6 (MATLAB: initial_pop.m).

    Faithful to the original: the candidates are drawn from 1:nPlaces (which
    includes 6), so place 6 may appear twice and another place may be
    missing. The shipped ind.mat has no such duplicates.

    WARNING: like the original, this overwrites ind.mat, the shared initial
    population used by every scenario in GA.py. The original saves only the
    Plan field, and so does this function.
    """
    # The Initialization Step defines initial individuals
    individual = []
    for _ in range(nRoute):
        # Producing Random Solutions
        range_of_numbers = np.arange(1, nPlaces + 1)
        random_indices = np.random.permutation(range_of_numbers.size)[: nPlaces - 1]
        A = range_of_numbers[random_indices]
        individual.append({"Plan": np.concatenate([[6], A]), "Fit": None})
    y = individual

    # Save as a MATLAB struct array (nRoute x 1) with field Plan
    ind = np.empty((nRoute, 1), dtype=[("Plan", "O")])
    for i, route in enumerate(y):
        ind[i, 0]["Plan"] = route["Plan"].astype(float).reshape(1, -1)
    savemat(os.path.join(_HERE, "ind.mat"), {"ind": ind})

    return y
