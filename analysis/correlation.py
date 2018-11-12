""" Collection of Functions to perform and analyse correlations"""

def integrated_correlation_time(corr_norm, correlation_width=5):
    """integrated_correlation_time
    A function to calculate the integratedCorrelationTime as a function of the
    number of integration steps M

    The correlation time hast to be normalized so that
    :math:`corr_norm = 1/(n - t)\\sum_n (f_i - <f>)(f_{i+t} - <f>)`

    it returnes the acf time defined as
    :math:`t_f = 0.5 * sum_{tau = -infty, infty} corr_norm(tau)`
    :math:`t_f = 0.5 + sum_{tau = 1, infty} corr_norm(tau)`

    to avoid including the error prone tail in the calculation, we sum up only to
    M (instead of infty) with
    :math:`M = C * t_f`
    where :math:`C` is defined by `correlation_width`.

    additonally it returns the estimate of the standard deviation on
    :math:`t_f` as well as :math:`M`

    See Sokal, A. "Monte Carlo Methods in Statistical Mechanics: Foundations and
    New Algorithms." In Functional Integration, edited by Cecile DeWitt-Morette,
    Pierre Cartier, and Antoine Folacci, 361:131-92. Boston, MA: Springer US, 1997.
    https://doi.org/10.1007/978-1-4899-0319-8_6.
    """
    import numpy as np
    assert corr_norm[0, 1] == 1.0, "Correlation is not normalized"
    assert corr_norm.ndim == 2, "Need an one-dimensional array as input"
    number_points = corr_norm[:, 1].size
    act = 0.0
    for tau in range(1, number_points):
        act += 0.5 * (corr_norm[tau - 1, 1] + corr_norm[tau, 1]) * \
                (corr_norm[tau, 0] - corr_norm[tau - 1, 0])

        if (corr_norm[tau, 0] > act*correlation_width):
            std_tau = np.sqrt((4*tau + 2)/number_points)*tau
            return act, std_tau, tau
    raise RuntimeError('Calculating the autocorrelation time failed')
