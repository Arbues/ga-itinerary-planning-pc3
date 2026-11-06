import math
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

from COX import COX
from Distance import Distance
from Mutation import Mutation
from SortPop import SortPop

_HERE = os.path.dirname(os.path.abspath(__file__))


def num2str(x):
    """Approximation of MATLAB num2str for scalars and integer vectors."""
    arr = np.atleast_1d(np.asarray(x))
    if arr.size > 1:
        items = [str(int(v)) for v in arr]
        width = max(len(s) for s in items)
        return "  ".join(s.rjust(width) for s in items).strip()
    v = float(arr[0])
    if math.isnan(v):
        return "NaN"
    if math.isinf(v):
        return "Inf" if v > 0 else "-Inf"
    if v == int(v):
        return str(int(v))
    digits = min(max(math.floor(math.log10(abs(v))) + 5, 5), 16)
    return f"{v:.{digits}g}"


def _load_initial_population():
    """Load burma_ind.mat (MATLAB struct array) as a list of dicts."""
    raw = loadmat(os.path.join(_HERE, "burma_ind.mat"), mat_dtype=True)["burma_ind"]
    return [
        {"Plan": np.asarray(r["Plan"]).ravel().astype(int), "Fit": None}
        for r in raw.flat
    ]


def GA(inputs, parameters):
    # User inputs
    ObjectFunction = inputs["ObjectFunction"]
    nPlaces = inputs["nPlaces"]
    data = inputs["data"]

    # GA parameters
    nGen = parameters["nGen"]
    nRoute = parameters["nRoute"]
    pOff = parameters["pOff"]
    nOff = round(pOff * nRoute / 2) * 2
    pMut = parameters["pMut"]

    # The best solution initial value
    bestsol = {"Plan": None, "Fit": 0}

    # The Initial population
    # All scenarios utilized the same initial population
    burma_ind = _load_initial_population()
    for i in range(nRoute):
        # Finding the Fitness of each Solution
        burma_ind[i]["Fit"] = ObjectFunction(burma_ind[i]["Plan"])
        # Finding the Best Solution in each generation
        if burma_ind[i]["Fit"] > bestsol["Fit"]:
            bestsol = dict(burma_ind[i])

    # Best Fitness of each generation
    bestfit = np.full(nGen, np.nan)
    bestdistance = np.full(nGen, np.nan)

    burma_ind = SortPop(burma_ind)

    # The Evolution Loop
    for g in range(nGen):
        # Initialize of Offspring Population.
        # MATLAB builds an (nOff/2 x 2) struct matrix and flattens it
        # column-major, so all first children come before all second children.
        off1 = []
        off2 = []

        # Crossover
        for k in range(nOff // 2):

            # Select Parents
            # # Random Selection Method
            # q = np.random.permutation(nRoute)
            # p1 = burma_ind[q[0]]
            # p2 = burma_ind[q[1]]

            # Tournament Selection Method
            tournamentSize = math.floor(nRoute * 0.2)
            tournament = np.random.permutation(nRoute)[:tournamentSize]
            c = [burma_ind[tournament[i]] for i in range(tournamentSize)]
            cand = SortPop(c)
            p1 = cand[0]
            p2 = cand[1]

            # Modifying Tournament Selection by adding this (16 lines) code to the last tournament selection code
            t = 2
            j = 1
            while np.array_equal(p1["Plan"], p2["Plan"]):
                t = t + 1
                if t <= tournamentSize:
                    p2 = cand[t - 1]
                else:
                    p2 = burma_ind[j - 1]
                    j = j + 1
                    if j > nOff:
                        # Copy first: MATLAB structs are values, never aliases
                        p2 = dict(p2)
                        p2["Plan"] = Mutation(p1["Plan"], 0.9)
                        pMut = 0.9
                        break

            # Perform Crossover
            y1, y2 = COX(p1["Plan"], p2["Plan"])
            off1.append({"Plan": y1, "Fit": None})
            off2.append({"Plan": y2, "Fit": None})

        # Convert the offsprings to Single-Column Matrix
        indoff = off1 + off2

        # Mutation
        for M in range(nOff):
            # Perform Mutation
            indoff[M]["Plan"] = Mutation(indoff[M]["Plan"], pMut)
            # Evaluation
            indoff[M]["Fit"] = ObjectFunction(indoff[M]["Plan"])
            # Compare Solution to Best Solution ever Found
            if indoff[M]["Fit"] > bestsol["Fit"]:
                bestsol = dict(indoff[M])

        # Update Best Fitness of each generation
        bestfit[g] = bestsol["Fit"]
        bestdistance[g] = Distance(bestsol["Plan"])

        # Merge and Sort Population
        burma_ind = SortPop(burma_ind + indoff)

        # Remove Extra routes
        burma_ind = burma_ind[:nRoute]

        # Display Iteration Information
        print(
            "Generation " + num2str(g + 1) + ": Best Fitness = " + num2str(bestfit[g])
            + "  & Total Distance = " + num2str(bestdistance[g])
        )

    # Plotting Data
    plt.figure()
    plt.plot(data[:, 1], data[:, 2], "ro", markerfacecolor="r")
    for row in data:
        plt.text(row[1], row[2], str(int(row[0])))
    plt.title("Places Locations")
    plt.grid(True)

    # The Best Route Figure
    for i in range(nPlaces - 1):
        x1 = data[bestsol["Plan"][i] - 1, 1]
        y1 = data[bestsol["Plan"][i] - 1, 2]
        x2 = data[bestsol["Plan"][i + 1] - 1, 1]
        y2 = data[bestsol["Plan"][i + 1] - 1, 2]
        plt.plot([x1, x2], [y1, y2], "k-")

    # Results
    output = {
        "burma_ind": burma_ind,
        "bestsol": bestsol,
        "bestfit": bestfit,
        "bestdistance": bestdistance,
    }
    print("The Optimal Route: " + num2str(output["bestsol"]["Plan"]))

    return output
