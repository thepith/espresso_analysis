""" Collection of Functions to perform and analyse correlations"""

def mean_std_err(data_array):
    """caculate the mean and the error of a quantity"""
    import numpy as np
    mean = np.mean(data_array)
    error = np.std(data_array, ddof = 1) / np.sqrt(len(data_array))
    return mean, error
