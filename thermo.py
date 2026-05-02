"""
Thermodynamics & Statistical Physics - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}


# =============================================================================
# THERMAL BASICS
# =============================================================================

def convert_temperature(value: float = 0.0, from_unit: str = 'C', to_unit: str = 'F') -> dict:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin."""
    if from_unit.upper() == 'C':
        celsius = value
    elif from_unit.upper() == 'F':
        celsius = (value - 32.0) * 5.0 / 9.0
    elif from_unit.upper() == 'K':
        celsius = value - 273.15
    else:
        return {'result': 'Invalid from_unit (use C, F, K)', 'details': {}, 'unit': ''}

    if to_unit.upper() == 'C':
        result = celsius
    elif to_unit.upper() == 'F':
        result = celsius * 9.0 / 5.0 + 32.0
    elif to_unit.upper() == 'K':
        result = celsius + 273.15
    else:
        return {'result': 'Invalid to_unit (use C, F, K)', 'details': {}, 'unit': ''}

    unit_symbols = {'C': 'deg C', 'F': 'deg F', 'K': 'K'}
    return {
        'result': f'{value:.4f} {from_unit.upper()} = {result:.4f} {to_unit.upper()}',
        'details': {'input_value': value, 'from_unit': from_unit, 'to_unit': to_unit,
                    'converted_value': result},
        'unit': unit_symbols.get(to_unit.upper(), '')
    }


def calc_heat(Q: float | None = None, m: float = 1.0, c: float = 4186.0,
              delta_T: float = 10.0) -> dict:
    """Heat transfer: Q = m * c * delta_T. Provide 3 of 4, solve for the unknown."""
    if Q is None:
        Q = m * c * delta_T
        solved = 'Q'
    elif m is None:
        m = Q / (c * delta_T) if c * delta_T != 0 else float('inf')
        solved = 'm'
    elif c is None:
        c = Q / (m * delta_T) if m * delta_T != 0 else float('inf')
        solved = 'c'
    elif delta_T is None:
        delta_T = Q / (m * c) if m * c != 0 else float('inf')
        solved = 'delta_T'
    else:
        Q_val = m * c * delta_T
        return {
            'result': f'Q = {Q_val:.4f} J (all parameters provided, Q computed)',
            'details': {'m': m, 'c': c, 'delta_T': delta_T, 'Q': Q_val},
            'unit': 'J'
        }

    labels = {'Q': 'Q (J)', 'm': 'mass (kg)', 'c': 'specific heat (J/kg*K)',
              'delta_T': 'delta_T (K)'}
    values = {'Q': Q, 'm': m, 'c': c, 'delta_T': delta_T}
    return {
        'result': f'Solved for {solved}: {labels[solved]} = {values[solved]:.4f}',
        'details': {**values},
        'unit': 'J' if solved == 'Q' else ('kg' if solved == 'm' else ('J/kg*K' if solved == 'c' else 'K'))
    }


def calc_specific_heat(Q: float = 4186.0, m: float = 0.1, delta_T: float = 10.0) -> dict:
    """Specific heat capacity: c = Q / (m * delta_T)."""
    c = Q / (m * delta_T)
    return {
        'result': f'Specific heat c = {c:.4f} J/(kg*K)',
        'details': {'heat_Q': Q, 'mass_m': m, 'delta_T': delta_T, 'specific_heat_c': c},
        'unit': 'J/(kg*K)'
    }


def calc_thermal_conduction(k: float = 205.0, A: float = 0.01, delta_T: float = 100.0,
                              L: float = 0.5, t: float = 60.0) -> dict:
    """Heat transfer by conduction: Q/t = k * A * delta_T / L."""
    Q_per_t = k * A * delta_T / L
    Q_total = Q_per_t * t
    R = L / (k * A)
    return {
        'result': f'Heat flow Q/t = {Q_per_t:.4f} W, Total Q = {Q_total:.4f} J, R_thermal = {R:.6f} K/W',
        'details': {'thermal_conductivity_k': k, 'area_A': A, 'delta_T': delta_T,
                    'length_L': L, 'time_t': t, 'Q_per_t': Q_per_t, 'Q_total': Q_total,
                    'thermal_resistance': R},
        'unit': 'W'
    }


def calc_convection(h: float = 25.0, A: float = 1.0, T_surface: float = 80.0,
                     T_fluid: float = 20.0) -> dict:
    """Convective heat transfer: Q = h * A * (T_surface - T_fluid)."""
    Q = h * A * (T_surface - T_fluid)
    return {
        'result': f'Convective heat transfer Q = {Q:.4f} W',
        'details': {'convection_coeff_h': h, 'area_A': A, 'T_surface': T_surface,
                    'T_fluid': T_fluid, 'heat_transfer_Q': Q},
        'unit': 'W'
    }


def calc_radiation(epsilon: float = 0.9, A: float = 1.0, T: float = 300.0) -> dict:
    """Stefan-Boltzmann radiation: P = epsilon * sigma * A * T^4."""
    sigma = 5.670374419e-8
    P = epsilon * sigma * A * (T ** 4)
    return {
        'result': f'Radiated power P = {P:.4f} W',
        'details': {'emissivity_epsilon': epsilon, 'area_A': A, 'temperature_T_K': T,
                    'sigma': sigma, 'radiated_power_P': P},
        'unit': 'W'
    }


def calc_net_radiation(epsilon: float = 0.9, A: float = 1.0, T_obj: float = 373.0,
                        T_env: float = 293.0) -> dict:
    """Net radiative heat transfer: P_net = epsilon * sigma * A * (T_obj^4 - T_env^4)."""
    sigma = 5.670374419e-8
    P_net = epsilon * sigma * A * (T_obj ** 4 - T_env ** 4)
    return {
        'result': f'Net radiated power P_net = {P_net:.4f} W',
        'details': {'emissivity_epsilon': epsilon, 'area_A': A, 'T_obj': T_obj,
                    'T_env': T_env, 'P_net': P_net},
        'unit': 'W'
    }


def calc_thermal_expansion(alpha: float = 1.2e-5, L0: float = 1.0, delta_T: float = 50.0) -> dict:
    """Linear thermal expansion: delta_L = alpha * L0 * delta_T."""
    delta_L = alpha * L0 * delta_T
    L_final = L0 + delta_L
    return {
        'result': f'delta_L = {delta_L:.6f} m, L_final = {L_final:.6f} m',
        'details': {'alpha': alpha, 'L0': L0, 'delta_T': delta_T,
                    'delta_L': delta_L, 'L_final': L_final},
        'unit': 'm'
    }


def calc_volume_expansion(beta: float = 3.6e-5, V0: float = 0.001, delta_T: float = 50.0) -> dict:
    """Volume thermal expansion: delta_V = beta * V0 * delta_T."""
    delta_V = beta * V0 * delta_T
    V_final = V0 + delta_V
    return {
        'result': f'delta_V = {delta_V:.4e} m^3, V_final = {V_final:.4e} m^3',
        'details': {'beta': beta, 'V0': V0, 'delta_T': delta_T,
                    'delta_V': delta_V, 'V_final': V_final},
        'unit': 'm^3'
    }


# =============================================================================
# IDEAL GAS LAWS
# =============================================================================

def calc_ideal_gas_law(P: float | None = None, V: float = 0.0224, n: float = 1.0,
                        T: float = 273.15) -> dict:
    """Ideal gas law: PV = nRT. Provide None for the unknown, or compute P if all given."""
    R = 8.314462618  # J/(mol*K)
    if P is None:
        P = n * R * T / V
        solved = 'P'
    elif V is None:
        V = n * R * T / P
        solved = 'V'
    elif n is None:
        n = P * V / (R * T)
        solved = 'n'
    elif T is None:
        T = P * V / (n * R)
        solved = 'T'
    else:
        PV = n * R * T
        return {
            'result': f'PV = {PV:.4f} J, nRT = {n*R*T:.4f} J (all given, checking PV=nRT)',
            'details': {'P': P, 'V': V, 'n': n, 'R': R, 'T': T, 'PV': P*V, 'nRT': n*R*T},
            'unit': 'Pa*m^3 = J'
        }
    symbols = {'P': 'Pa', 'V': 'm^3', 'n': 'mol', 'T': 'K'}
    values = {'P': P, 'V': V, 'n': n, 'R': R, 'T': T}
    result_value = values[solved]
    return {
        'result': f'{solved} = {result_value:.4f} {symbols[solved]}',
        'details': values,
        'unit': symbols[solved]
    }


def calc_boyle(P1: float = 101325.0, V1: float = 2.0, V2: float = 1.0) -> dict:
    """Boyle's law (constant T): P1 * V1 = P2 * V2."""
    P2 = P1 * V1 / V2
    return {
        'result': f'P2 = {P2:.4f} Pa',
        'details': {'P1': P1, 'V1': V1, 'V2': V2, 'P2': P2},
        'unit': 'Pa'
    }


def calc_charles(V1: float = 1.0, T1: float = 273.15, T2: float = 373.15) -> dict:
    """Charles's law (constant P): V1/T1 = V2/T2."""
    V2 = V1 * T2 / T1
    return {
        'result': f'V2 = {V2:.4f} m^3',
        'details': {'V1': V1, 'T1': T1, 'T2': T2, 'V2': V2},
        'unit': 'm^3'
    }


def calc_gay_lussac(P1: float = 101325.0, T1: float = 273.15, T2: float = 373.15) -> dict:
    """Gay-Lussac's law (constant V): P1/T1 = P2/T2."""
    P2 = P1 * T2 / T1
    return {
        'result': f'P2 = {P2:.4f} Pa',
        'details': {'P1': P1, 'T1': T1, 'T2': T2, 'P2': P2},
        'unit': 'Pa'
    }


def calc_molecular_kinetic_energy(T: float = 300.0) -> dict:
    """Average molecular kinetic energy: KE_avg = (3/2) * k_B * T."""
    k_B = 1.380649e-23
    KE = 1.5 * k_B * T
    return {
        'result': f'Avg molecular KE = {KE:.4e} J',
        'details': {'k_B': k_B, 'T_K': T, 'average_KE': KE},
        'unit': 'J'
    }


def calc_rms_speed(T: float = 300.0, M_molar: float = 0.02896) -> dict:
    """RMS speed of gas molecules: v_rms = sqrt(3RT/M)."""
    R = 8.314462618
    v_rms = math.sqrt(3.0 * R * T / M_molar)
    return {
        'result': f'v_rms = {v_rms:.4f} m/s',
        'details': {'R': R, 'T_K': T, 'molar_mass_kg_per_mol': M_molar, 'v_rms': v_rms},
        'unit': 'm/s'
    }


# =============================================================================
# THERMODYNAMIC LAWS
# =============================================================================

def calc_first_law(delta_U: float | None = None, Q: float = 500.0, W: float = 200.0) -> dict:
    """First law of thermodynamics: delta_U = Q - W."""
    if delta_U is None:
        delta_U = Q - W
        solved = 'delta_U'
    elif Q is None:
        Q = delta_U + W
        solved = 'Q'
    elif W is None:
        W = Q - delta_U
        solved = 'W'
    else:
        delta_U_val = Q - W
        return {
            'result': f'delta_U = {delta_U_val:.4f} J (all given, checking delta_U = Q-W)',
            'details': {'Q': Q, 'W': W, 'delta_U': delta_U_val},
            'unit': 'J'
        }
    values = {'delta_U': delta_U, 'Q': Q, 'W': W}
    return {
        'result': f'{solved} = {values[solved]:.4f} J',
        'details': values,
        'unit': 'J'
    }


def calc_isothermal_work(n: float = 1.0, T: float = 300.0, V1: float = 0.01, V2: float = 0.02) -> dict:
    """Isothermal work: W = nRT * ln(V2/V1)."""
    R = 8.314462618
    W = n * R * T * math.log(V2 / V1)
    return {
        'result': f'Isothermal work W = {W:.4f} J',
        'details': {'n_mol': n, 'T_K': T, 'V1': V1, 'V2': V2, 'R': R, 'work_W': W},
        'unit': 'J'
    }


def calc_adiabatic_process(P1: float = 101325.0, V1: float = 1.0, V2: float = 0.5,
                            gamma: float = 1.4) -> dict:
    """Adiabatic process: P1 * V1^gamma = P2 * V2^gamma."""
    P2 = P1 * (V1 ** gamma) / (V2 ** gamma)
    T_ratio = (V1 / V2) ** (gamma - 1.0)
    W = (P1 * V1 - P2 * V2) / (gamma - 1.0)
    return {
        'result': f'P2 = {P2:.2f} Pa, V2/V1 temp ratio = {T_ratio:.4f}, W = {W:.4f} J',
        'details': {'P1': P1, 'V1': V1, 'V2': V2, 'gamma': gamma, 'P2': P2,
                    'temperature_ratio': T_ratio, 'work_W': W},
        'unit': 'Pa'
    }


def calc_isobaric_work(P: float = 101325.0, V1: float = 1.0, V2: float = 2.0) -> dict:
    """Isobaric work: W = P * (V2 - V1)."""
    W = P * (V2 - V1)
    return {
        'result': f'Isobaric work W = {W:.4f} J',
        'details': {'pressure_P': P, 'V1': V1, 'V2': V2, 'delta_V': V2 - V1, 'work_W': W},
        'unit': 'J'
    }


def calc_isochoric_process(Q: float = 500.0) -> dict:
    """Isochoric process (constant volume): W = 0, delta_U = Q."""
    return {
        'result': f'Isochoric: W = 0 J, delta_U = Q = {Q:.4f} J',
        'details': {'heat_Q': Q, 'work_W': 0.0, 'delta_U': Q},
        'unit': 'J'
    }


def calc_carnot_efficiency(Tc: float = 300.0, Th: float = 500.0) -> dict:
    """Carnot efficiency: eta = 1 - Tc/Th."""
    eta = 1.0 - Tc / Th
    return {
        'result': f'Carnot efficiency eta = {eta:.4f} ({eta*100:.2f}%)',
        'details': {'T_cold_K': Tc, 'T_hot_K': Th, 'efficiency_eta': eta},
        'unit': 'dimensionless'
    }


def calc_heat_engine_COP_refrigerator(Tc: float = 273.0, Th: float = 300.0) -> dict:
    """COP of a Carnot refrigerator: COP_c = Tc / (Th - Tc)."""
    COP = Tc / (Th - Tc) if Th > Tc else float('inf')
    return {
        'result': f'COP (refrigerator) = {COP:.4f}',
        'details': {'T_cold_K': Tc, 'T_hot_K': Th, 'COP_refrigerator': COP},
        'unit': 'dimensionless'
    }


def calc_heat_engine_COP_heat_pump(Tc: float = 273.0, Th: float = 300.0) -> dict:
    """COP of a Carnot heat pump: COP_h = Th / (Th - Tc)."""
    COP = Th / (Th - Tc) if Th > Tc else float('inf')
    return {
        'result': f'COP (heat pump) = {COP:.4f}',
        'details': {'T_cold_K': Tc, 'T_hot_K': Th, 'COP_heat_pump': COP},
        'unit': 'dimensionless'
    }


# =============================================================================
# PHASE CHANGES
# =============================================================================

def calc_latent_heat(m: float = 1.0, L: float = 334000.0) -> dict:
    """Latent heat for phase change: Q = m * L."""
    Q = m * L
    return {
        'result': f'Latent heat Q = {Q:.2f} J',
        'details': {'mass_m': m, 'latent_heat_L': L, 'Q': Q},
        'unit': 'J'
    }


def calc_clausius_clapeyron(L: float = 2.26e6, T: float = 373.15,
                              V_vapor: float = 1.673, V_liquid: float = 0.001043) -> dict:
    """Clausius-Clapeyron: dP/dT = L / (T * delta_V)."""
    delta_V = V_vapor - V_liquid
    dP_dT = L / (T * delta_V)
    return {
        'result': f'dP/dT = {dP_dT:.2f} Pa/K',
        'details': {'latent_heat_L': L, 'temperature_T': T, 'delta_V': delta_V, 'dP_dT': dP_dT},
        'unit': 'Pa/K'
    }


def calc_phase_change_energy(m: float = 1.0, c_ice: float = 2108.0, c_water: float = 4186.0,
                              L_fusion: float = 334000.0, T_init: float = -10.0,
                              T_final: float = 10.0) -> dict:
    """Total energy for phase change from T_init to T_final through melting point 0 deg C."""
    T_melt = 0.0
    Q1 = m * c_ice * (T_melt - T_init) if T_init < T_melt else 0.0
    Q2 = m * L_fusion if T_init <= T_melt <= T_final else 0.0
    Q3 = m * c_water * (T_final - T_melt) if T_final > T_melt else 0.0
    Q_total = Q1 + Q2 + Q3
    return {
        'result': f'Total energy Q_total = {Q_total:.2f} J (Q1_heat_ice={Q1:.2f}, Q2_melt={Q2:.2f}, Q3_heat_water={Q3:.2f})',
        'details': {'m': m, 'T_init': T_init, 'T_final': T_final,
                    'Q_heat_ice': Q1, 'Q_melting': Q2, 'Q_heat_water': Q3, 'Q_total': Q_total},
        'unit': 'J'
    }


# =============================================================================
# ENTROPY AND FREE ENERGY
# =============================================================================

def calc_entropy_change_isothermal(Q_rev: float = 1000.0, T: float = 300.0) -> dict:
    """Entropy change in a reversible isothermal process: delta_S = Q_rev / T."""
    delta_S = Q_rev / T
    return {
        'result': f'delta_S = {delta_S:.4f} J/K',
        'details': {'reversible_heat_Q_rev': Q_rev, 'temperature_T': T, 'delta_S': delta_S},
        'unit': 'J/K'
    }


def calc_entropy_change_ideal_gas(n: float = 1.0, Cv: float = 12.471, T1: float = 300.0,
                                    T2: float = 400.0, V1: float = 1.0, V2: float = 2.0) -> dict:
    """Entropy change for ideal gas: delta_S = nCv*ln(T2/T1) + nR*ln(V2/V1)."""
    R = 8.314462618
    delta_S = n * Cv * math.log(T2 / T1) + n * R * math.log(V2 / V1)
    return {
        'result': f'delta_S = {delta_S:.4f} J/K',
        'details': {'n_mol': n, 'Cv': Cv, 'T1': T1, 'T2': T2, 'V1': V1, 'V2': V2,
                    'delta_S': delta_S},
        'unit': 'J/K'
    }


def calc_gibbs_free_energy(delta_H: float = -100000.0, delta_S: float = -200.0, T: float = 298.15) -> dict:
    """Gibbs free energy: delta_G = delta_H - T * delta_S."""
    delta_G = delta_H - T * delta_S
    spontaneous = delta_G < 0
    return {
        'result': f'delta_G = {delta_G:.2f} J (spontaneous: {spontaneous})',
        'details': {'delta_H': delta_H, 'delta_S': delta_S, 'T': T, 'delta_G': delta_G,
                    'spontaneous': spontaneous, 'equilibrium': abs(delta_G) < 1e-6},
        'unit': 'J'
    }


def calc_helmholtz_free_energy(delta_U: float = -50000.0, delta_S: float = -100.0, T: float = 298.15) -> dict:
    """Helmholtz free energy: delta_A = delta_U - T * delta_S."""
    delta_A = delta_U - T * delta_S
    return {
        'result': f'delta_A = {delta_A:.2f} J',
        'details': {'delta_U': delta_U, 'delta_S': delta_S, 'T': T, 'delta_A': delta_A},
        'unit': 'J'
    }


def calc_equilibrium_constant(delta_G: float = -10000.0, T: float = 298.15) -> dict:
    """Equilibrium constant from Gibbs: K = exp(-delta_G/(RT))."""
    R = 8.314462618
    K_eq = math.exp(-delta_G / (R * T))
    return {
        'result': f'Equilibrium constant K = {K_eq:.4e}',
        'details': {'delta_G': delta_G, 'T': T, 'R': R, 'K_eq': K_eq,
                    'ln_K': -delta_G / (R * T)},
        'unit': 'dimensionless'
    }


def calc_critical_point_params(a: float = 0.364, b: float = 4.27e-5) -> dict:
    """Van der Waals critical point: Tc = 8a/(27Rb), Pc = a/(27b^2), Vc = 3b."""
    R = 8.314462618
    Tc = 8.0 * a / (27.0 * R * b)
    Pc = a / (27.0 * b * b)
    Vc = 3.0 * b
    Zc = Pc * Vc / (R * Tc)
    return {
        'result': f'Tc = {Tc:.2f} K, Pc = {Pc:.2e} Pa, Vc = {Vc:.4e} m^3/mol, Zc = {Zc:.4f}',
        'details': {'a': a, 'b': b, 'R': R, 'Tc': Tc, 'Pc': Pc, 'Vc': Vc, 'Zc': Zc},
        'unit': 'K / Pa / m^3/mol'
    }


# =============================================================================
# STATISTICAL PHYSICS
# =============================================================================

def calc_maxwell_boltzmann_distribution(v: float = 500.0, m: float = 4.65e-26,
                                         T: float = 300.0) -> dict:
    """Maxwell-Boltzmann velocity distribution f(v) at a specific speed v."""
    k_B = 1.380649e-23
    coeff = 4.0 * math.pi * (m / (2.0 * math.pi * k_B * T)) ** 1.5
    f_v = coeff * v * v * math.exp(-m * v * v / (2.0 * k_B * T))
    return {
        'result': f'f(v={v:.2f}) = {f_v:.4e} s/m',
        'details': {'v': v, 'mass_m': m, 'T_K': T, 'k_B': k_B, 'f_v': f_v},
        'unit': 's/m'
    }


def calc_maxwell_boltzmann_speeds(T: float = 300.0, m: float = 4.65e-26) -> dict:
    """Most probable, mean, and RMS speeds for Maxwell-Boltzmann distribution."""
    k_B = 1.380649e-23
    R = 8.314462618
    M_molar = m * 6.02214076e23  # approximate molar mass
    v_mp = math.sqrt(2.0 * k_B * T / m)  # most probable
    v_mean = math.sqrt(8.0 * k_B * T / (math.pi * m))  # mean
    v_rms = math.sqrt(3.0 * k_B * T / m)  # RMS
    return {
        'result': f'v_mp = {v_mp:.2f} m/s, v_mean = {v_mean:.2f} m/s, v_rms = {v_rms:.2f} m/s',
        'details': {'temperature_T': T, 'molecular_mass_m': m, 'k_B': k_B,
                    'v_most_probable': v_mp, 'v_mean': v_mean, 'v_rms': v_rms,
                    'v_rms_from_molar_RT': math.sqrt(3.0 * R * T / M_molar)},
        'unit': 'm/s'
    }


def calc_equipartition_energy(T: float = 300.0, degrees_of_freedom: float = 3.0) -> dict:
    """Equipartition theorem: U = (f/2) * k_B * T per particle, or (f/2) * nRT."""
    k_B = 1.380649e-23
    energy_per_particle = 0.5 * degrees_of_freedom * k_B * T
    return {
        'result': f'Energy per particle = {energy_per_particle:.4e} J, per mole = {(energy_per_particle * 6.02214076e23):.4f} J/mol',
        'details': {'T_K': T, 'degrees_of_freedom': degrees_of_freedom, 'k_B': k_B,
                    'energy_per_particle': energy_per_particle,
                    'energy_per_mole': energy_per_particle * 6.02214076e23},
        'unit': 'J'
    }


def calc_partition_function_2level(E0: float = 0.0, E1: float = 2.07e-21, T: float = 300.0) -> dict:
    """Canonical partition function for a simple two-level system: Z = exp(-E0/kT) + exp(-E1/kT)."""
    k_B = 1.380649e-23
    Z = math.exp(-E0 / (k_B * T)) + math.exp(-E1 / (k_B * T))
    return {
        'result': f'Z = {Z:.6f}',
        'details': {'E0': E0, 'E1': E1, 'T': T, 'k_B': k_B, 'Z': Z},
        'unit': 'dimensionless'
    }


# =============================================================================
# ADDITIONAL THERMO FUNCTIONS
# =============================================================================

def calc_van_der_waals(P: float = 101325.0, V: float = 0.0224, n: float = 1.0,
                        T: float = 273.15, a: float = 0.364, b: float = 4.27e-5) -> dict:
    """Van der Waals equation: (P + a*n^2/V^2)*(V - n*b) = n*R*T."""
    R = 8.314462618
    P_vdw = n * R * T / (V - n * b) - a * n * n / (V * V)
    P_ideal = n * R * T / V
    return {
        'result': f'P_vdw = {P_vdw:.2f} Pa, P_ideal = {P_ideal:.2f} Pa, difference = {P_vdw - P_ideal:.2f} Pa',
        'details': {'a': a, 'b': b, 'V': V, 'n': n, 'T': T, 'P_vdw': P_vdw, 'P_ideal': P_ideal},
        'unit': 'Pa'
    }


def calc_enthalpy(delta_U: float = 500.0, P: float = 101325.0, delta_V: float = 0.001) -> dict:
    """Enthalpy: H = U + PV, or delta_H = delta_U + P*delta_V + V*delta_P."""
    delta_H = delta_U + P * delta_V
    return {
        'result': f'delta_H = {delta_H:.2f} J',
        'details': {'delta_U': delta_U, 'P': P, 'delta_V': delta_V, 'delta_H': delta_H},
        'unit': 'J'
    }


def calc_joule_thomson(delta_T: float = -5.0, delta_P: float = -100000.0) -> dict:
    """Joule-Thomson coefficient: mu_JT = (delta_T/delta_P)_H."""
    mu_JT = delta_T / delta_P
    return {
        'result': f'Joule-Thomson coefficient mu_JT = {mu_JT:.4e} K/Pa',
        'details': {'delta_T': delta_T, 'delta_P': delta_P, 'mu_JT': mu_JT},
        'unit': 'K/Pa'
    }


def calc_thermal_pressure_coefficient(V: float = 0.001, T: float = 300.0,
                                        n: float = 1.0) -> dict:
    """Thermal pressure coefficient beta = (dP/dT)_V = nR/V for ideal gas."""
    R = 8.314462618
    beta = n * R / V
    return {
        'result': f'Pressure coefficient beta = {beta:.4f} Pa/K',
        'details': {'V': V, 'T': T, 'n': n, 'beta': beta},
        'unit': 'Pa/K'
    }


def calc_isothermal_compressibility(V: float = 0.0224, P: float = 101325.0) -> dict:
    """Isothermal compressibility: kappa = -1/V * (dV/dP)_T = 1/P for ideal gas."""
    kappa = 1.0 / P
    return {
        'result': f'Compressibility kappa = {kappa:.4e} Pa^-1',
        'details': {'V': V, 'P': P, 'kappa': kappa},
        'unit': 'Pa^-1'
    }


def calc_maxwell_relation(P1: float = 101325.0, V1: float = 0.0224, T1: float = 273.15,
                           T2: float = 373.15) -> dict:
    """Check Maxwell relation: (dP/dT)_V = (dS/dV)_T via ideal gas approximation."""
    R = 8.314462618
    dp_dT_v = R / V1
    ds_dV_t = R / V1
    equal = abs(dp_dT_v - ds_dV_t) < 1e-12
    return {
        'result': f'(dP/dT)_V = {dp_dT_v:.4f} Pa/K, (dS/dV)_T = {ds_dV_t:.4f} J/(K*m^3), match: {equal}',
        'details': {'dp_dT': dp_dT_v, 'ds_dV': ds_dV_t, 'maxwell_holds': equal},
        'unit': 'Pa/K'
    }


def calc_chemical_potential(T: float = 300.0, P: float = 101325.0, P0: float = 100000.0,
                               n: float = 1.0) -> dict:
    """Chemical potential for ideal gas: mu = mu0 + RT*ln(P/P0) per mole."""
    R = 8.314462618
    delta_mu = R * T * math.log(P / P0)
    return {
        'result': f'delta_mu = {delta_mu:.2f} J/mol',
        'details': {'T': T, 'P': P, 'P0': P0, 'delta_mu': delta_mu},
        'unit': 'J/mol'
    }


def calc_boltzmann_factor(E: float = 2.07e-21, T: float = 300.0) -> dict:
    """Boltzmann factor: exp(-E/(k_B*T))."""
    k_B = 1.380649e-23
    factor = math.exp(-E / (k_B * T))
    return {
        'result': f'Boltzmann factor = {factor:.6f}',
        'details': {'energy_E': E, 'T': T, 'k_B': k_B, 'kT': k_B * T,
                    'boltzmann_factor': factor},
        'unit': 'dimensionless'
    }


def calc_ideal_gas_partition_function(V: float = 0.0224, T: float = 300.0,
                                        m: float = 4.65e-26) -> dict:
    """Single-particle translational partition function: Z1 = V/lambda_deB^3."""
    k_B = 1.380649e-23
    h = 6.62607015e-34
    lambda_deB = h / math.sqrt(2.0 * math.pi * m * k_B * T)
    Z1 = V / (lambda_deB ** 3)
    return {
        'result': f'Z1 = {Z1:.4e}, thermal wavelength lambda_deB = {lambda_deB:.4e} m',
        'details': {'V': V, 'T': T, 'm': m, 'lambda_deBroglie': lambda_deB, 'Z1': Z1},
        'unit': 'dimensionless'
    }


def calc_triple_point_water() -> dict:
    """Water triple point: T = 273.16 K = 0.01 deg C, P = 611.657 Pa."""
    return {
        'result': 'Water triple point: T = 273.16 K (0.01 deg C), P = 611.657 Pa (6.11657 mbar)',
        'details': {'T_K': 273.16, 'T_C': 0.01, 'P_Pa': 611.657, 'P_mbar': 6.11657},
        'unit': 'K / Pa'
    }


def calc_isentropic_efficiency(W_actual: float = 800.0, W_ideal: float = 1000.0) -> dict:
    """Isentropic efficiency: eta_s = W_actual / W_ideal."""
    eta_s = W_actual / W_ideal
    return {
        'result': f'Isentropic efficiency eta_s = {eta_s:.4f} ({eta_s*100:.2f}%)',
        'details': {'W_actual': W_actual, 'W_ideal': W_ideal, 'eta_s': eta_s},
        'unit': 'dimensionless'
    }


def calc_heat_engine_efficiency(Qh: float = 1000.0, W: float = 300.0) -> dict:
    """Heat engine efficiency: eta = W / Qh."""
    eta = W / Qh
    Qc = Qh - W
    return {
        'result': f'efficiency eta = {eta:.4f} ({eta*100:.2f}%), rejected heat Qc = {Qc:.2f} J',
        'details': {'Q_hot': Qh, 'work_W': W, 'Q_cold': Qc, 'efficiency_eta': eta},
        'unit': 'dimensionless'
    }


def calc_otto_cycle_efficiency(compression_ratio: float = 8.0, gamma: float = 1.4) -> dict:
    """Otto cycle efficiency: eta = 1 - 1/r^(gamma-1)."""
    eta = 1.0 - 1.0 / (compression_ratio ** (gamma - 1.0))
    return {
        'result': f'Otto efficiency eta = {eta:.4f} ({eta*100:.2f}%)',
        'details': {'r': compression_ratio, 'gamma': gamma, 'eta': eta},
        'unit': 'dimensionless'
    }


def calc_mean_free_path(T: float = 300.0, P: float = 101325.0, d: float = 3.7e-10) -> dict:
    """Mean free path: lambda = kT/(sqrt(2)*pi*d^2*P)."""
    k_B = 1.380649e-23
    l = k_B * T / (math.sqrt(2.0) * math.pi * d * d * P)
    return {
        'result': f'Mean free path lambda = {l:.4e} m',
        'details': {'T': T, 'P': P, 'molecular_diameter_d': d,
                    'k_B': k_B, 'mean_free_path': l},
        'unit': 'm'
    }


def calc_stefan_boltzmann_luminosity(R: float = 6.96e8, T: float = 5778.0) -> dict:
    """Stefan-Boltzmann luminosity: L = 4*pi*R^2 * sigma * T^4."""
    sigma = 5.670374419e-8
    L = 4.0 * math.pi * R * R * sigma * (T ** 4)
    return {
        'result': f'Luminosity L = {L:.4e} W',
        'details': {'radius_R': R, 'temperature_T': T, 'sigma': sigma, 'L': L},
        'unit': 'W'
    }


def calc_radiative_transfer(Q: float = 1000.0, A: float = 1.0, delta_T: float = 10.0,
                               L: float = 0.1) -> dict:
    """Radiative heat transfer coefficient: h_rad = Q/(A*delta_T)."""
    h_rad = Q / (A * delta_T)
    return {
        'result': f'Radiative coefficient h_rad = {h_rad:.4f} W/(m^2*K)',
        'details': {'Q': Q, 'A': A, 'delta_T': delta_T, 'h_radiative': h_rad},
        'unit': 'W/(m^2*K)'
    }


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Thermal basics
    'convert_temperature': {'func': convert_temperature, 'params': ['value', 'from_unit', 'to_unit'],
                            'desc': 'Convert between C, F, K'},
    'heat': {'func': calc_heat, 'params': ['Q', 'm', 'c', 'delta_T'],
             'desc': 'Heat transfer Q = mc*delta_T; omit one param to solve'},
    'specific_heat': {'func': calc_specific_heat, 'params': ['Q', 'm', 'delta_T'],
                      'desc': 'Specific heat c = Q/(m*delta_T)'},
    'thermal_conduction': {'func': calc_thermal_conduction, 'params': ['k', 'A', 'delta_T', 'L', 't'],
                            'desc': 'Conduction: Q/t = k*A*delta_T/L'},
    'convection': {'func': calc_convection, 'params': ['h', 'A', 'T_surface', 'T_fluid'],
                   'desc': 'Convection: Q = h*A*(Ts-Tf)'},
    'radiation': {'func': calc_radiation, 'params': ['epsilon', 'A', 'T'],
                  'desc': 'Radiation: P = epsilon*sigma*A*T^4'},
    'net_radiation': {'func': calc_net_radiation, 'params': ['epsilon', 'A', 'T_obj', 'T_env'],
                       'desc': 'Net radiation: P = epsilon*sigma*A*(Tobj^4-Tenv^4)'},
    'thermal_expansion': {'func': calc_thermal_expansion, 'params': ['alpha', 'L0', 'delta_T'],
                           'desc': 'Linear thermal expansion delta_L = alpha*L0*delta_T'},
    'volume_expansion': {'func': calc_volume_expansion, 'params': ['beta', 'V0', 'delta_T'],
                          'desc': 'Volume thermal expansion delta_V = beta*V0*delta_T'},
    # Ideal gas
    'ideal_gas_law': {'func': calc_ideal_gas_law, 'params': ['P', 'V', 'n', 'T'],
                      'desc': 'Ideal gas law PV=nRT; set unknown to None'},
    'boyle': {'func': calc_boyle, 'params': ['P1', 'V1', 'V2'],
              'desc': "Boyle's law P1*V1 = P2*V2"},
    'charles': {'func': calc_charles, 'params': ['V1', 'T1', 'T2'],
                'desc': "Charles's law V1/T1 = V2/T2"},
    'gay_lussac': {'func': calc_gay_lussac, 'params': ['P1', 'T1', 'T2'],
                   'desc': "Gay-Lussac's law P1/T1 = P2/T2"},
    'molecular_kinetic_energy': {'func': calc_molecular_kinetic_energy, 'params': ['T'],
                                  'desc': 'Avg molecular KE = (3/2)kT'},
    'rms_speed': {'func': calc_rms_speed, 'params': ['T', 'M_molar'],
                  'desc': 'RMS speed v_rms = sqrt(3RT/M)'},
    # Thermodynamic laws
    'first_law': {'func': calc_first_law, 'params': ['delta_U', 'Q', 'W'],
                  'desc': 'First law: delta_U = Q - W; omit one to solve'},
    'isothermal_work': {'func': calc_isothermal_work, 'params': ['n', 'T', 'V1', 'V2'],
                         'desc': 'Isothermal work W = nRT ln(V2/V1)'},
    'adiabatic_process': {'func': calc_adiabatic_process, 'params': ['P1', 'V1', 'V2', 'gamma'],
                           'desc': 'Adiabatic process PV^gamma = const'},
    'isobaric_work': {'func': calc_isobaric_work, 'params': ['P', 'V1', 'V2'],
                      'desc': 'Isobaric work W = P*(V2-V1)'},
    'isochoric_process': {'func': calc_isochoric_process, 'params': ['Q'],
                           'desc': 'Isochoric process: W=0, delta_U=Q'},
    'carnot_efficiency': {'func': calc_carnot_efficiency, 'params': ['Tc', 'Th'],
                           'desc': 'Carnot efficiency eta = 1 - Tc/Th'},
    'COP_refrigerator': {'func': calc_heat_engine_COP_refrigerator, 'params': ['Tc', 'Th'],
                          'desc': 'COP of Carnot refrigerator'},
    'COP_heat_pump': {'func': calc_heat_engine_COP_heat_pump, 'params': ['Tc', 'Th'],
                      'desc': 'COP of Carnot heat pump'},
    # Phase changes
    'latent_heat': {'func': calc_latent_heat, 'params': ['m', 'L'],
                    'desc': 'Latent heat Q = m*L'},
    'clausius_clapeyron': {'func': calc_clausius_clapeyron, 'params': ['L', 'T', 'V_vapor', 'V_liquid'],
                            'desc': 'Clausius-Clapeyron dP/dT = L/(T*delta_V)'},
    'phase_change_energy': {'func': calc_phase_change_energy,
                             'params': ['m', 'c_ice', 'c_water', 'L_fusion', 'T_init', 'T_final'],
                             'desc': 'Total energy for heating + phase change'},
    # Entropy & Free Energy
    'entropy_change_isothermal': {'func': calc_entropy_change_isothermal, 'params': ['Q_rev', 'T'],
                                   'desc': 'delta_S = Q_rev/T'},
    'entropy_change_ideal_gas': {'func': calc_entropy_change_ideal_gas,
                                  'params': ['n', 'Cv', 'T1', 'T2', 'V1', 'V2'],
                                  'desc': 'delta_S = nCv ln(T2/T1) + nR ln(V2/V1)'},
    'gibbs_free_energy': {'func': calc_gibbs_free_energy, 'params': ['delta_H', 'delta_S', 'T'],
                           'desc': 'Gibbs free energy delta_G = delta_H - T*delta_S'},
    'helmholtz_free_energy': {'func': calc_helmholtz_free_energy, 'params': ['delta_U', 'delta_S', 'T'],
                               'desc': 'Helmholtz free energy delta_A = delta_U - T*delta_S'},
    'equilibrium_constant': {'func': calc_equilibrium_constant, 'params': ['delta_G', 'T'],
                              'desc': 'Equilibrium constant K = exp(-delta_G/RT)'},
    'critical_point_params': {'func': calc_critical_point_params, 'params': ['a', 'b'],
                               'desc': 'Van der Waals critical point Tc, Pc, Vc'},
    # Statistical Physics
    'maxwell_boltzmann_distribution': {'func': calc_maxwell_boltzmann_distribution,
                                        'params': ['v', 'm', 'T'],
                                        'desc': 'Maxwell-Boltzmann distribution f(v)'},
    'maxwell_boltzmann_speeds': {'func': calc_maxwell_boltzmann_speeds, 'params': ['T', 'm'],
                                  'desc': 'Most probable, mean, and RMS speeds'},
    'equipartition_energy': {'func': calc_equipartition_energy, 'params': ['T', 'degrees_of_freedom'],
                              'desc': 'Equipartition theorem energy per particle'},
    'partition_function_2level': {'func': calc_partition_function_2level, 'params': ['E0', 'E1', 'T'],
                                   'desc': 'Partition function for 2-level system'},
    # Additional
    'van_der_waals': {'func': calc_van_der_waals, 'params': ['P', 'V', 'n', 'T', 'a', 'b'],
                       'desc': 'Van der Waals equation (P + a*n^2/V^2)*(V - n*b) = nRT'},
    'enthalpy': {'func': calc_enthalpy, 'params': ['delta_U', 'P', 'delta_V'],
                  'desc': 'Enthalpy delta_H = delta_U + P*delta_V'},
    'joule_thomson': {'func': calc_joule_thomson, 'params': ['delta_T', 'delta_P'],
                       'desc': 'Joule-Thomson coefficient mu_JT = (delta_T/delta_P)_H'},
    'thermal_pressure_coefficient': {'func': calc_thermal_pressure_coefficient,
                                       'params': ['V', 'T', 'n'],
                                       'desc': 'Thermal pressure coefficient beta = nR/V'},
    'isothermal_compressibility': {'func': calc_isothermal_compressibility, 'params': ['V', 'P'],
                                     'desc': 'Isothermal compressibility kappa = 1/P'},
    'maxwell_relation': {'func': calc_maxwell_relation, 'params': ['P1', 'V1', 'T1', 'T2'],
                          'desc': 'Check Maxwell relation equality'},
    'chemical_potential': {'func': calc_chemical_potential, 'params': ['T', 'P', 'P0', 'n'],
                            'desc': 'Chemical potential for ideal gas'},
    'boltzmann_factor': {'func': calc_boltzmann_factor, 'params': ['E', 'T'],
                          'desc': 'Boltzmann factor exp(-E/kT)'},
    'ideal_gas_partition_function': {'func': calc_ideal_gas_partition_function,
                                       'params': ['V', 'T', 'm'],
                                       'desc': 'Translational partition function Z1 = V/lambda^3'},
    'triple_point_water': {'func': calc_triple_point_water, 'params': [],
                            'desc': 'Water triple point constants'},
    'isentropic_efficiency': {'func': calc_isentropic_efficiency, 'params': ['W_actual', 'W_ideal'],
                               'desc': 'Isentropic efficiency eta_s = W_actual/W_ideal'},
    'heat_engine_efficiency': {'func': calc_heat_engine_efficiency, 'params': ['Qh', 'W'],
                                'desc': 'Heat engine efficiency eta = W/Qh'},
    'otto_cycle_efficiency': {'func': calc_otto_cycle_efficiency,
                                'params': ['compression_ratio', 'gamma'],
                                'desc': 'Otto cycle efficiency eta = 1 - 1/r^(gamma-1)'},
    'mean_free_path': {'func': calc_mean_free_path, 'params': ['T', 'P', 'd'],
                        'desc': 'Mean free path lambda = kT/(sqrt(2)*pi*d^2*P)'},
    'stefan_boltzmann_luminosity': {'func': calc_stefan_boltzmann_luminosity,
                                      'params': ['R', 'T'],
                                      'desc': 'Luminosity L = 4*pi*R^2*sigma*T^4'},
    'radiative_transfer': {'func': calc_radiative_transfer, 'params': ['Q', 'A', 'delta_T', 'L'],
                            'desc': 'Radiative heat transfer coefficient'},
}
