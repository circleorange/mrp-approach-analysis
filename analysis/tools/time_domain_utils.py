import numpy as np
import scipy as sp
import pandas as pd

def moving_average(data, window=3, mode='reflect') -> np.ndarray:
        """
        Apply local mean over moving window and shift every sample by mean of local neighbourhood.
        """
        return sp.ndimage.uniform_filter(data, size=window, mode=mode)

def weighted_moving_average(type, data, window=5, sigma=1, pad_mode='reflect') -> np.ndarray:
    """
    Apply weighted moving average with user-specified weights.
    Returns an array of the same length as input, with padding at ends.

    Weight types:
        - Simple/Uniform MA Weights: Boxcar, Rolling Mean
        - Hann/Hamming Weights: Cosine-shaped, common in Signal Processing
        - Gaussian Weights: Bell-shaped
    """
    # >>>>> Padding to maintain same output size >>>>>

    pad = window // 2
    data_padded = np.pad(data, pad_width=pad, mode=pad_mode)

    # >>>>> Weight Types>>>>>

    if type == 'uniform':
        weights = np.ones(window) / window
    elif type == 'gaussian':
        weights = sp.signal.gaussian(window, std=sigma)
        weights /= weights.sum()  # Normalize weights
    elif type == 'hann':
        weights = np.hanning(window) # or np.hamming
        weights /= weights.sum()  # Normalize weights
    
    return np.convolve(data_padded, weights, mode='valid')

def block_mean(data, window: int) -> np.ndarray:
    """
    Apply block mean over size and set every sample to mean of the block.
    """
    trimmed_len = len(data) - (len(data) % window)
    data = data[:trimmed_len]
    reshaped = data.reshape(-1, window)
    means = reshaped.mean(axis=1)
    return np.repeat(means, window)

def moving_window_mean(data, window=5, center=True, axis=1) -> np.ndarray:
        """
        Apply moving window mean to smooth the signal.
        Returns np array with the same shape as the input.
        """
        if data.ndim == 1: axis = 0
        
        # Get moving windows
        windows = np.lib.stride_tricks.sliding_window_view(data, window_shape=window, axis=axis)
        means = np.mean(windows, axis=-1)
        
        # Pad to match the original shape
        if center:
            pad_left = window // 2
            pad_right = window - pad_left - 1
        else:
            pad_left = window - 1
            pad_right = 0
        
        # For 1D
        if data.ndim == 1:
            result = np.full_like(data, np.nan, dtype=float)
            result[pad_left:len(data)-pad_right] = means
        else:
            result = np.full_like(data, np.nan, dtype=float)
            slicer = [slice(None)] * data.ndim
            slicer[axis] = slice(pad_left, data.shape[axis] - pad_right)
            result[tuple(slicer)] = means
        return result

def density_distribution(array, n_bins=1000):
    density = sp.stats.gaussian_kde(array)
    x = np.linspace(array.min(), array.max(), n_bins)
    return x, density(x)

def moving_variance(arr, window=10, center=True):
    return pd.Series(arr).rolling(window, center=center).var().to_numpy()
