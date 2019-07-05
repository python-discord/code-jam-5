def fit_to_range(val: float, a: float, b: float, a1: float, b1: float) -> float:
    """Fits a number with range a-b to a new range a1-b1."""
    new_value = ((val - a) / (b - a)) * (b1 - a1) + a1
    return new_value
