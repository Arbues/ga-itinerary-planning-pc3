import os

import numpy as np
from scipy.io import savemat

_HERE = os.path.dirname(os.path.abspath(__file__))


def Burma_initial_pop(nRoute, nPlaces):
    """Create nRoute random routes starting at place 1 (MATLAB: Burma_initial_pop.m).

    WARNING: like the original, this overwrites burma_ind.mat, the shared
    initial population used by every scenario in GA.py.
    """
    # The Initialization Step defines initial individuals
    individual = []
    for _ in range(nRoute):
        # Producing Random Solutions
        range_of_numbers = np.arange(2, nPlaces + 1)
        random_indices = np.random.permutation(range_of_numbers.size)[: nPlaces - 1]
        A = range_of_numbers[random_indices]
        individual.append({"Plan": np.concatenate([[1], A]), "Fit": np.array([])})
    y = individual

    # Save as a MATLAB struct array (nRoute x 1) with fields Plan and Fit
    burma_ind = np.empty((nRoute, 1), dtype=[("Plan", "O"), ("Fit", "O")])
    for i, route in enumerate(y):
        burma_ind[i, 0]["Plan"] = route["Plan"].astype(float).reshape(1, -1)
        burma_ind[i, 0]["Fit"] = route["Fit"]
    savemat(os.path.join(_HERE, "burma_ind.mat"), {"burma_ind": burma_ind})

    return y
