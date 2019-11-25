"""List of fundamental constants"""
import numpy as np
import scipy.constants as constants

ELECTRON_CHARGE = constants.elementary_charge
AVOGADRO_NUMBER = constants.Avogadro
ELECTRIC_CONSTANT = constants.epsilon_0
BOLTZMANN_CONSTANT = constants.Boltzmann
GAS_CONSTANT = constants.gas_constant
FARADAY_CONSTANT = ELECTRON_CHARGE * AVOGADRO_NUMBER

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

def celsius_from_kelvin(temperature):
    return constants.convert_temperature(temperature, "Kelvin", "Celsius")

def kelvin_from_celsius(temperature):
    return constants.convert_temperature(temperature, "Celsius", "Kelvin")

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

def density_water(temperature=298.15):
    """
    Calculate the density of water saturated with air at 0.1 MPa in the range
    of5 °C to 40 °C.

    Returns density in g/cm^3

    Data from:
       Jones et al., J Res Natl Inst Stand Technol. 1992; 97(3): 335-340.
       DOI: 10.6028/jres.097.013.
    """

    temperature_celsius = celsius_from_kelvin(temperature)
    if (temperature_celsius < 5.0) or (temperature_celsius > 40.0):
        raise ValueError('Density of water is only valid in the range of '
                         '5 °C to 40 °C')
    rho = 999.84847 \
            + 6.337563e-2 * temperature_celsius \
            - 8.523829e-3 * temperature_celsius**2 \
            + 6.943248e-5 * temperature_celsius**3 \
            - 3.821216e-7 * temperature_celsius**4

    return rho/1000.0


def ionization_constant_water(temperature=298.15, density=None):
    """
    Calculate the ionizatoin constant (Kw) of water at the fiven temperature
    and 0.1 MPa pressure. If you pass a density, it will use this density
    indead of the 0.1 MPa pressure.

    Data from:
        Bandura etal., J. Phys. Chem. Ref. Data, Vol. 35, No. 1, 2006
        DOI: 10.1063/1.1928231
    """
    import numpy as np

    # using Model II from Bandura etal
    # model parameters
    n = 6
    alpha_0 = -0.864671
    alpha_1 = 8659.19
    alpha_2 = -22786.2
    beta_0 = 0.642044
    beta_1 = -56.8534
    beta_2 = -0.375754

    # Water parameters
    Mw = 18.01528

    # temperature
    T = temperature

    # density
    if density:
        D = density
    else:
        D = density_water(T)

    pKWG = 0.61415 \
            + 48251.33 / T \
            - 67707.93 / T**2.0 \
            + 10102100.0 / T**3.0

    Z = D * np.exp(alpha_0 \
                   + alpha_1/T \
                   + alpha_2/T**2 *np.power(D,2.0/3.0)
                  )

    pKw = -2*n*(
        np.log10(1 + Z) - (Z/(Z + 1)) * D * (
            beta_0 + beta_1/T + beta_2*D
        )
    ) + pKWG + 2 * np.log10(Mw/1000.0)

    return np.power(10, -pKw)
