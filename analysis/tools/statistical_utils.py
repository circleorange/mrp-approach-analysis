import numpy as np

def linear_regression(y, x=None) -> np.ndarray:
    """
    trendline[0] = first fitted y-value (intercept)
    """
    if x is None: x = np.arange(len(y))
    m, b = np.polyfit(x, y, 1)
    trendline = m * x + b
    return trendline, m, b

def normalize(arr: np.ndarray, min_val: float = 0.0, max_val: float = 1.0) -> np.ndarray:
    """
    Normalize variable to a range between min_val and max_val.
    """
    return min_val + (arr - np.min(arr)) * (max_val - min_val) / (np.max(arr) - np.min(arr))