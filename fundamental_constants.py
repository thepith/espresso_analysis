"""List of fundamental constants"""
import numpy as np

ELECTRON_CHARGE = 1.602176634 * np.power(10.0, -19.0) # C  # exact
AVOGADRO_NUMBER = 6.02214076 * np.power(10.0, 23.0) # mol^{-1} # exact
ELECTRIC_CONSTANT = 8.854187817 * np.power(10.0, -12.0) # F m^{-1}
BOLTZMANN_CONSTANT = 1.380649 * np.power(10.0, -23.0) # J K^{-1} # exact
GAS_CONSTANT = 8.3144598 # J mol{-1} K{-1}

def dielectric_constant_water(temperature=298.15):
    """
    Return the tabulated dielectric constant of water at a given temperature
    at a pressure of 0.1 MPa

    Uses tabulated data taken from:
    Archer, Donald G., and Peiming Wang. "The Dielectric Constant of Water and
    Debye-Hueckel Limiting Law Slopes." Journal of Physical and Chemical
    Reference Data 19, no. 2 (March 1, 1990): 371-411.
    https://doi.org/10.1063/1.555853.

    Works in the Temperature range of 263.15 to 373.15 K.

    parameters:
        temperature: Temperature in Kelvin
    """
    tabulated_data = np.array([[263.15, 92.10],
                               [268.15, 89.96],
                               [273.15, 87.90],
                               [278.15, 85.90],
                               [283.15, 83.96],
                               [288.15, 82.06],
                               [293.15, 80.20],
                               [298.15, 78.38],
                               [303.15, 76.60],
                               [308.15, 74.86],
                               [313.15, 73.17],
                               [318.15, 71.50],
                               [323.15, 69.88],
                               [328.15, 68.29],
                               [333.15, 66.74],
                               [338.15, 65.22],
                               [343.15, 63.73],
                               [348.15, 62.28],
                               [353.15, 60.87],
                               [358.15, 59.48],
                               [363.15, 58.13],
                               [368.15, 56.81],
                               [373.15, 55.51]])
    polynomal_degree = 5
    fitdata = np.polyfit(tabulated_data[:, 0], tabulated_data[:, 1],
                         polynomal_degree)
    fitfunction = np.poly1d(fitdata)
    return fitfunction(temperature)

def bjerrum_length_water(temperature=298.15):
    """
    Return the bjerrum length of water at a given temperature. The Bjerrum
    length is defined as
    :math:`\\lambda_b = e^2 / (4 \\pi \\epsilon_0 \\epsilon_r k_B T)`

    parameters:
        temperature: Temperature in Kelvin (default 298.15)
    """
    bjerrum = np.power(ELECTRON_CHARGE, 2.0) / \
            (4.0 * np.pi *
             ELECTRIC_CONSTANT *
             dielectric_constant_water(temperature) *
             BOLTZMANN_CONSTANT *
             temperature
            )
    return bjerrum
