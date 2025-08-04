import scipy as sp

def apply_gaussian_filter(data, axis=1, custom_kernel=None, sigma=1.0, mode="reflect"):
    """
    Apply Gaussian smoothing. Supports:
    - 1D: applies kernel on the data series (axis ignored).
    - 2D: applies column-wise, per trace (axis=0) or row-wise, per sample (axis=1) smoothing.

    Sigma controls the width of the Gaussian curve, i.e. "bluriness" of the Gaussian kernel,
        - Low sigma (0 to 1): Narrow and peaked curve, kernel mostly weights central value, less smoothing.
        - High sigma (> 1): Wider curve, more smoothing, kernel weights more neighboring values.
    """
    if data.ndim == 1: axis = 0
    if custom_kernel is not None: return sp.ndimage.convolve1d(data, custom_kernel, axis=axis, mode=mode)
    return sp.ndimage.gaussian_filter1d(data, sigma=sigma, axis=axis, mode=mode)

def apply_median_filter(mtx, window=3, mode='reflect'):
    """
    Apply median filter to remove outliers or smooth noise in the data.
    `window` can be either (int or tuple):
        - int: applies to both dimensions.
        - tuple: applies to each dimension separately (rows, columns).
    """
    return sp.ndimage.median_filter(mtx, size=window, mode=mode)