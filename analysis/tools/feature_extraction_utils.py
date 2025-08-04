import numpy as np
import scipy as sp

def diff(arr: np.ndarray) -> np.ndarray:
    """
    Calculate difference between each consecutive value in a 1D array.
    Output length is (len(signal) - 1).
    """
    return np.diff(arr)

def envelope(mtx: np.ndarray, axis: int = 1) -> np.ndarray:
    """
    Hilbert transform measures the instantaneous amplitude (outline) of the analytic signal (Hilbert-transformed).
    Returns the envelope of the signal along the specified axis of same dimensions.
    """
    analytic_signal = sp.signal.hilbert(mtx, axis=axis)
    envelope = np.abs(analytic_signal)
    return envelope

def energy(mtx: np.ndarray, axis: int = 1) -> float:
    """
    Total power of the signal.
    """
    return np.sum(np.square(mtx), axis=axis)

def rms(mtx: np.ndarray, axis: int = 1) -> float:
    if mtx.ndim == 1: return np.sqrt(mtx**2)
    else: return np.sqrt(np.mean(mtx**2, axis=axis))

def variance(mtx: np.ndarray, axis: int = 1) -> float:
    if mtx.ndim == 1: return np.var(mtx)
    else: return np.var(mtx, axis=axis)

def mean(mtx: np.ndarray, axis: int = 1) -> float:
    if mtx.ndim == 1: return np.mean(mtx)
    else: return np.mean(mtx, axis=axis)
