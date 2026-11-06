def SortPop(ind):
    """Sort routes by fitness in descending order (MATLAB: SortPop.m).

    Python's sort is stable, like MATLAB's sort(..., 'descend'), so routes
    with equal fitness keep their original relative order.
    """
    return sorted(ind, key=lambda route: route["Fit"], reverse=True)
