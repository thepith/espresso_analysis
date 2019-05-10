""" Collection of Functions to perform and analyse correlations"""

def mean_std_err(data_array, root = 1.0):
    """caculate the mean and the error of a quantity"""
    import numpy as np
    mean = np.mean(data_array)
    error = np.std(data_array, ddof = 1) / np.sqrt(len(data_array))
    mean_root = np.power(mean, 1.0/root)
    error_root = 1.0/root * error * np.power(mean, 1.0/root - 1.0)
    return mean_root, error_root
