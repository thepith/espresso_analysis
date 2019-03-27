"""Tools to work with units"""
import numpy as np

def c_SI_to_SIM(concentration_mol_L, sigma_in_meter, exponent=1.0):
    """ convert concentration from SI to simulation"""
    from simulation_tools import fundamental_constants
    # [sigma_per_meter] = sigma/m
    sigma_per_meter = 1.0 / sigma_in_meter
    # [sigmacubed_per_liter] =  sigma**3/L
    sigmacubed_per_liter = np.power(sigma_per_meter*0.1, 3.0)
    particles_per_mol = fundamental_constants.AVOGADRO_NUMBER
    conversion = np.power(particles_per_mol / sigmacubed_per_liter, exponent)
    concentration_N_per_sigma = concentration_mol_L * conversion
    return concentration_N_per_sigma

def c_SIM_to_SI(concentration_N_per_sigma_cubed,
                        sigma_in_meter,
                        exponent=1.0):
    """ convert concentration from SI to simulation"""
    from simulation_tools import fundamental_constants
    # [sigma_per_meter] = sigma/m
    sigma_per_meter = 1.0 / sigma_in_meter
    # [sigmacubed_per_liter] =  sigma**3/L
    sigmacubed_per_liter = np.power(sigma_per_meter*0.1, 3.0)
    particles_per_mol = fundamental_constants.AVOGADRO_NUMBER
    conversion = np.power(particles_per_mol / sigmacubed_per_liter, -exponent)
    concentration_mol_L = concentration_N_per_sigma_cubed * conversion
    return concentration_mol_L

def nernst_potential_in_V_to_reaction_constant(
    standard_potential,
    transfered_electrons = 1,
    temperature = 298.15,
    applied_potential = 0.0,
):
    """ convert the potential in V to a (dimensionless) reaction constant

Formula used:

    K = exp((E0 - E)*(nu * F)/(RT))

    where
    * nu is the number of transfered electrons
    * F, R, T are the faraday constants, the ideal gas constant and the temperature
    * E0 is the standard potential
    * E is the applied potential
    """
    from .fundamental_constants import FARADAY_CONSTANT, GAS_CONSTANT
    K = np.exp(
        (standard_potential - applied_potential) *
        (transfered_electrons * FARADAY_CONSTANT)/
        (GAS_CONSTANT * temperature)
    )
    return K
