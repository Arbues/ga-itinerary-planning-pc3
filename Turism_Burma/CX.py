import numpy as np


def CX(x1, x2):
    """Cycle crossover starting from place 1 (MATLAB: CX.m).

    Plans hold 1-based place IDs, so 0 is used as the "empty" marker exactly
    as in the original code.
    """
    x1 = np.asarray(x1)
    x2 = np.asarray(x2)
    s = x1.size
    y1 = np.zeros(s, dtype=x1.dtype)
    y2 = np.zeros(s, dtype=x2.dtype)

    t = np.flatnonzero(x1 == 1)[0]
    while y1[t] == 0:
        y1[t] = x1[t]
        t = np.flatnonzero(x1 == x2[t])[0]
    left = np.flatnonzero(y1 == 0)
    y1[left] = x2[left]

    t = np.flatnonzero(x2 == 1)[0]
    while y2[t] == 0:
        y2[t] = x2[t]
        t = np.flatnonzero(x2 == x1[t])[0]
    left = np.flatnonzero(y2 == 0)
    y2[left] = x1[left]

    return y1, y2
