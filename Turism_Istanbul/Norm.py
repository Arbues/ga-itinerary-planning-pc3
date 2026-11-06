import numpy as np


def Norm(A):
    """Min-max normalization over all elements of A (MATLAB: Norm.m)."""
    A = np.asarray(A, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        M = (A - np.min(A)) / (np.max(A) - np.min(A))
    return M
