"""
Relativity - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}

# =============================================================================
# SPECIAL RELATIVITY
# =============================================================================

def calc_lorentz_factor(v: float = 2.5e8, c: float = 299792458.0) -> dict:
    """Lorentz factor: gamma = 1 / sqrt(1 - v^2/c^2)."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c (v/c = {v/c:.4f})', 'details': {'v': v, 'c': c}, 'unit': 'dimensionless'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    return {
        'result': f'gamma = {gamma:.6f}, beta = v/c = {beta:.6f}',
        'details': {'velocity_v': v, 'speed_of_light_c': c, 'beta': beta, 'gamma': gamma},
        'unit': 'dimensionless'
    }


def calc_beta_from_gamma(gamma: float = 2.0) -> dict:
    """Compute beta = v/c from Lorentz factor gamma."""
    if gamma < 1.0:
        return {'result': 'gamma must be >= 1', 'details': {'gamma': gamma}, 'unit': 'dimensionless'}
    beta = math.sqrt(1.0 - 1.0 / (gamma * gamma))
    return {
        'result': f'beta = v/c = {beta:.6f} ({beta*100:.2f}% of c)',
        'details': {'gamma': gamma, 'beta': beta},
        'unit': 'dimensionless'
    }


def calc_time_dilation(dt0: float = 1.0, v: float = 2.5e8, c: float = 299792458.0) -> dict:
    """Time dilation: delta_t = gamma * delta_t0."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 's'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    dt = gamma * dt0
    return {
        'result': f'delta_t = {dt:.6f} s (proper time delta_t0 = {dt0:.4f} s, gamma = {gamma:.4f})',
        'details': {'proper_time_dt0': dt0, 'v': v, 'c': c, 'beta': beta,
                    'gamma': gamma, 'dilated_time_dt': dt},
        'unit': 's'
    }


def calc_length_contraction(L0: float = 100.0, v: float = 2.5e8, c: float = 299792458.0) -> dict:
    """Length contraction: L = L0 / gamma."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 'm'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    L = L0 / gamma
    contraction = L0 - L
    return {
        'result': f'L = {L:.6f} m (rest length L0 = {L0:.4f} m, contracted by {contraction:.4f} m)',
        'details': {'rest_length_L0': L0, 'v': v, 'c': c, 'beta': beta,
                    'gamma': gamma, 'contracted_length_L': L, 'contraction_amount': contraction},
        'unit': 'm'
    }


def calc_velocity_addition(u: float = 2.0e8, v: float = 1.5e8, c: float = 299792458.0) -> dict:
    """Relativistic velocity addition: w = (u + v) / (1 + u*v/c^2)."""
    w = (u + v) / (1.0 + u * v / (c * c))
    return {
        'result': f'w = {w:.4e} m/s = {w/c:.6f}c',
        'details': {'u': u, 'v': v, 'c': c, 'w': w, 'w_over_c': w / c,
                    'newtonian_sum': u + v, 'newtonian_over_c': (u + v) / c},
        'unit': 'm/s'
    }


def calc_relativistic_mass(m0: float = 1.0, v: float = 2.5e8, c: float = 299792458.0) -> dict:
    """Relativistic mass: m = gamma * m0."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 'kg'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    m = gamma * m0
    return {
        'result': f'm = {m:.6f} kg (rest mass m0 = {m0:.4f} kg, gamma = {gamma:.4f})',
        'details': {'rest_mass_m0': m0, 'v': v, 'c': c, 'beta': beta,
                    'gamma': gamma, 'relativistic_mass_m': m},
        'unit': 'kg'
    }


def calc_rest_energy(m: float = 1.0, c: float = 299792458.0) -> dict:
    """Rest energy: E0 = m * c^2."""
    E0 = m * c * c
    return {
        'result': f'E0 = {E0:.4e} J = {E0/1.602176634e-13:.4f} MeV',
        'details': {'mass_m': m, 'c': c, 'rest_energy_E0_J': E0,
                    'rest_energy_MeV': E0 / 1.602176634e-13},
        'unit': 'J'
    }


def calc_total_energy(m0: float = 9.1093837e-31, v: float = 2.5e8, c: float = 299792458.0) -> dict:
    """Total relativistic energy: E = gamma * m0 * c^2."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 'J'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    E0 = m0 * c * c
    E = gamma * E0
    KE = E - E0
    return {
        'result': f'E = {E:.4e} J, KE = {KE:.4e} J, E0 = {E0:.4e} J',
        'details': {'rest_mass_m0': m0, 'v': v, 'c': c, 'beta': beta,
                    'gamma': gamma, 'rest_energy_E0': E0, 'total_energy_E': E,
                    'kinetic_energy_KE': KE, 'KE_MeV': KE / 1.602176634e-13},
        'unit': 'J'
    }


def calc_relativistic_kinetic_energy(m0: float = 9.1093837e-31, v: float = 2.5e8,
                                       c: float = 299792458.0) -> dict:
    """Relativistic kinetic energy: KE = (gamma - 1) * m0 * c^2."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 'J'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    KE = (gamma - 1.0) * m0 * c * c
    KE_classical = 0.5 * m0 * v * v
    return {
        'result': f'KE_rel = {KE:.4e} J = {KE/1.602176634e-13:.4f} MeV (classical = {KE_classical:.4e} J)',
        'details': {'m0': m0, 'v': v, 'c': c, 'beta': beta, 'gamma': gamma,
                    'KE_relativistic': KE, 'KE_classical': KE_classical,
                    'ratio': KE / KE_classical if KE_classical > 0 else float('inf')},
        'unit': 'J'
    }


def calc_relativistic_momentum(m0: float = 9.1093837e-31, v: float = 2.5e8,
                                  c: float = 299792458.0) -> dict:
    """Relativistic momentum: p = gamma * m0 * v."""
    if abs(v) >= c:
        return {'result': f'Error: v >= c', 'details': {}, 'unit': 'kg*m/s'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    p = gamma * m0 * v
    p_classical = m0 * v
    return {
        'result': f'p = {p:.4e} kg*m/s (classical = {p_classical:.4e} kg*m/s)',
        'details': {'m0': m0, 'v': v, 'c': c, 'beta': beta, 'gamma': gamma,
                    'momentum_relativistic': p, 'momentum_classical': p_classical,
                    'ratio': p / p_classical},
        'unit': 'kg*m/s'
    }


def calc_energy_momentum_relation(p: float = 1.0e-22, m0: float = 9.1093837e-31,
                                     c: float = 299792458.0) -> dict:
    """Energy-momentum relation: E^2 = (p*c)^2 + (m0*c^2)^2."""
    E0 = m0 * c * c
    pc = p * c
    E = math.sqrt(pc * pc + E0 * E0)
    KE = E - E0
    return {
        'result': f'E = {E:.4e} J, KE = {KE:.4e} J, pc = {pc:.4e} J, E0 = {E0:.4e} J',
        'details': {'momentum_p': p, 'rest_mass_m0': m0, 'c': c,
                    'rest_energy_E0': E0, 'pc_term': pc, 'total_energy_E': E,
                    'KE': KE},
        'unit': 'J'
    }


# =============================================================================
# GENERAL RELATIVITY
# =============================================================================

def calc_schwarzschild_radius(M: float = 5.972e24, G: float = 6.67430e-11,
                                c: float = 299792458.0) -> dict:
    """Schwarzschild radius: r_s = 2 * G * M / c^2."""
    r_s = 2.0 * G * M / (c * c)
    return {
        'result': f'r_s = {r_s:.4f} m = {r_s/1000:.4f} km',
        'details': {'mass_M_kg': M, 'G': G, 'c': c, 'schwarzschild_radius_r_s': r_s,
                    'M_solar_masses': M / 1.989e30},
        'unit': 'm'
    }


def calc_gravitational_time_dilation(dt0: float = 1.0, M: float = 5.972e24,
                                       r: float = 6.371e6, G: float = 6.67430e-11,
                                       c: float = 299792458.0) -> dict:
    """Gravitational time dilation: delta_t = delta_t0 / sqrt(1 - r_s/r)."""
    r_s = 2.0 * G * M / (c * c)
    if r <= r_s:
        return {'result': f'Error: r <= r_s ({r:.4f} <= {r_s:.4f}), inside event horizon',
                'details': {'r_s': r_s, 'r': r}, 'unit': 's'}
    dt_obs = dt0 / math.sqrt(1.0 - r_s / r)
    return {
        'result': f'delta_t_obs = {dt_obs:.10f} s (proper time = {dt0:.4f} s, dilated by {dt_obs/dt0:.4e}x)',
        'details': {'proper_time_dt0': dt0, 'mass_M': M, 'distance_r': r,
                    'r_s': r_s, 'dilated_time_dt_obs': dt_obs, 'dilation_factor': dt_obs / dt0},
        'unit': 's'
    }


def calc_gravitational_redshift(M: float = 5.972e24, r_emit: float = 6.371e6,
                                   r_obs: float = float('inf'),
                                   G: float = 6.67430e-11, c: float = 299792458.0) -> dict:
    """Gravitational redshift: z = sqrt((1 - r_s/r_obs)/(1 - r_s/r_emit)) - 1."""
    r_s = 2.0 * G * M / (c * c)
    if r_emit <= r_s:
        return {'result': f'Error: r_emit <= r_s (emission inside event horizon)', 'details': {}, 'unit': 'dimensionless'}
    if r_obs == float('inf'):
        z = 1.0 / math.sqrt(1.0 - r_s / r_emit) - 1.0
    else:
        if r_obs <= r_s:
            return {'result': f'Error: r_obs <= r_s', 'details': {}, 'unit': 'dimensionless'}
        z = math.sqrt((1.0 - r_s / r_obs) / (1.0 - r_s / r_emit)) - 1.0
    z_weak = G * M / (r_emit * c * c)
    return {
        'result': f'z = {z:.4e} (weak field approx: {z_weak:.4e})',
        'details': {'mass_M': M, 'r_emit': r_emit, 'r_obs': r_obs,
                    'r_s': r_s, 'redshift_z': z, 'weak_field_z': z_weak},
        'unit': 'dimensionless'
    }


def calc_orbital_velocity_GR(M: float = 1.989e30, r: float = 1.0e11,
                                G: float = 6.67430e-11, c: float = 299792458.0) -> dict:
    """Circular orbital velocity in Schwarzschild metric: v = sqrt(GM/(r - 3GM/c^2))."""
    r_s = 2.0 * G * M / (c * c)
    rg = G * M / (c * c)
    denominator = r - 1.5 * r_s
    if denominator <= 0:
        return {'result': f'No stable circular orbit at this radius (r < 3GM/c^2)', 'details': {
            'r': r, 'r_s': r_s, 'three_GM_c2': 3.0 * rg}, 'unit': 'm/s'}
    v = math.sqrt(G * M / denominator)
    v_newton = math.sqrt(G * M / r)
    return {
        'result': f'v_GR = {v:.2f} m/s = {v/1000:.2f} km/s (Newton: {v_newton/1000:.2f} km/s)',
        'details': {'M': M, 'r': r, 'G': G, 'r_s': r_s,
                    'orbital_velocity_GR': v, 'orbital_velocity_Newton': v_newton,
                    'ratio': v / v_newton},
        'unit': 'm/s'
    }


def calc_isco_radius(M: float = 10.0 * 1.989e30, G: float = 6.67430e-11,
                       c: float = 299792458.0) -> dict:
    """Innermost stable circular orbit (non-rotating BH): r_ISCO = 6GM/c^2 = 3r_s."""
    r_s = 2.0 * G * M / (c * c)
    r_isco = 6.0 * G * M / (c * c)
    return {
        'result': f'r_ISCO = {r_isco/1000:.1f} km = {r_isco/r_s:.1f} * r_s',
        'details': {'mass_M': M, 'M_solar': M / 1.989e30,
                    'r_s_km': r_s / 1000.0, 'r_isco_km': r_isco / 1000.0},
        'unit': 'km'
    }


def calc_photon_sphere(M: float = 1.989e30, G: float = 6.67430e-11,
                         c: float = 299792458.0) -> dict:
    """Photon sphere radius: r_ph = 3GM/c^2 = 1.5 * r_s."""
    r_s = 2.0 * G * M / (c * c)
    r_ph = 1.5 * r_s
    return {
        'result': f'r_photon = {r_ph/1000:.2f} km = 1.5 * r_s',
        'details': {'mass_M': M, 'r_s_km': r_s / 1000.0, 'r_photon_km': r_ph / 1000.0},
        'unit': 'km'
    }


def calc_gravitational_wave_strain(M: float = 1.989e30 * 30.0, R: float = 1.496e11,
                                      f: float = 100.0, G: float = 6.67430e-11,
                                      c: float = 299792458.0) -> dict:
    """Estimate gravitational wave strain: h ~ (G/c^4) * (M*c^2/R) * (v/c)^2."""
    v = 2.0 * math.pi * f * R
    if v >= c:
        v = 0.5 * c
    quadrupole_term = G * M / (R * c * c)
    h_est = quadrupole_term * (v / c) ** 2
    return {
        'result': f'GW strain h ~ {h_est:.4e} (at frequency {f:.1f} Hz)',
        'details': {'mass_M': M, 'orbital_separation_R': R, 'freq_f': f,
                    'orbital_velocity_v': v, 'v_over_c': v / c,
                    'quadrupole_factor': quadrupole_term, 'strain_estimate_h': h_est,
                    'note': 'order-of-magnitude estimate'},
        'unit': 'dimensionless'
    }


# =============================================================================
# ADDITIONAL RELATIVITY FUNCTIONS
# =============================================================================

def calc_spacetime_interval(x: float = 3.0e8, y: float = 0.0, z: float = 0.0, t: float = 1.0,
                              c: float = 299792458.0) -> dict:
    """Spacetime interval: s^2 = c^2*t^2 - x^2 - y^2 - z^2."""
    s_squared = (c * t) ** 2 - x * x - y * y - z * z
    if s_squared > 0:
        nature = 'timelike'
    elif abs(s_squared) < 1e-12:
        nature = 'lightlike'
    else:
        nature = 'spacelike'
    s = math.sqrt(abs(s_squared))
    return {
        'result': f's^2 = {s_squared:.4e} m^2 ({nature}), |s| = {s:.4e} m',
        'details': {'x': x, 't': t, 's_squared': s_squared, 's': s, 'nature': nature},
        'unit': 'm^2'
    }


def calc_lorentz_transform_position(x: float = 0.0, t: float = 0.0, v: float = 2.0e8,
                                       c: float = 299792458.0) -> dict:
    """Lorentz transformation of position: x' = gamma*(x - vt), t' = gamma*(t - vx/c^2)."""
    if abs(v) >= c:
        return {'result': 'Error: v >= c', 'details': {}, 'unit': 'm'}
    beta = v / c
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    x_prime = gamma * (x - v * t)
    t_prime = gamma * (t - v * x / (c * c))
    return {
        'result': f"x' = {x_prime:.4e} m, t' = {t_prime:.4e} s",
        'details': {'x': x, 't': t, 'v': v, 'c': c, 'beta': beta,
                    'gamma': gamma, 'x_prime': x_prime, 't_prime': t_prime},
        'unit': 'm / s'
    }


def calc_relativistic_doppler(f0: float = 5.0e14, v: float = 3.0e7, c: float = 299792458.0,
                                approaching: bool = True) -> dict:
    """Relativistic Doppler shift: f = f0*sqrt((1+beta)/(1-beta)) for approaching."""
    beta = v / c
    if approaching:
        if beta >= 1.0:
            return {'result': 'Error: v >= c', 'details': {}, 'unit': 'Hz'}
        f = f0 * math.sqrt((1.0 + beta) / (1.0 - beta))
    else:
        if beta >= 1.0:
            return {'result': 'Error: v >= c', 'details': {}, 'unit': 'Hz'}
        f = f0 * math.sqrt((1.0 - beta) / (1.0 + beta))
    z = f0 / f - 1.0
    return {
        'result': f'f = {f:.4e} Hz, redshift z = {z:.6f}',
        'details': {'f0': f0, 'v': v, 'c': c, 'beta': beta,
                    'approaching': approaching, 'frequency_f': f, 'z': z},
        'unit': 'Hz'
    }


def calc_compton_scattering(wavelength: float = 0.07e-9, theta_deg: float = 90.0) -> dict:
    """Compton scattering wavelength shift: delta_lambda = (h/(m_e*c))*(1 - cos(theta))."""
    h = 6.62607015e-34
    m_e = 9.1093837e-31
    c = 299792458.0
    lambda_c = h / (m_e * c)
    theta = math.radians(theta_deg)
    delta_lambda = lambda_c * (1.0 - math.cos(theta))
    lambda_prime = wavelength + delta_lambda
    return {
        'result': f"delta_lambda = {delta_lambda:.4e} m, lambda' = {lambda_prime:.4e} m, Compton lambda_c = {lambda_c:.4e} m",
        'details': {'wavelength': wavelength, 'theta_deg': theta_deg,
                    'compton_wavelength': lambda_c, 'delta_lambda': delta_lambda,
                    'lambda_prime': lambda_prime},
        'unit': 'm'
    }


def calc_tidal_force_Gm_over_R3(M: float = 5.97e24, r: float = 6.37e6, m: float = 1.0,
                                  delta_r: float = 1.0, G: float = 6.67430e-11) -> dict:
    """Tidal force: F_tidal = 2*G*M*m*delta_r / r^3."""
    F_tidal = 2.0 * G * M * m * delta_r / (r * r * r)
    return {
        'result': f'Tidal force F_tidal = {F_tidal:.4e} N across delta_r = {delta_r:.4f} m',
        'details': {'M': M, 'r': r, 'm': m, 'delta_r': delta_r,
                    'F_tidal': F_tidal},
        'unit': 'N'
    }


def calc_gravitational_lensing_angle(M: float = 1.989e30, b: float = 7.0e8,
                                       G: float = 6.67430e-11,
                                       c: float = 299792458.0) -> dict:
    """Einstein deflection angle: alpha = 4*G*M/(b*c^2)."""
    alpha = 4.0 * G * M / (b * c * c)
    alpha_arcsec = alpha * 206265.0
    return {
        'result': f'Deflection angle alpha = {alpha:.4e} rad = {alpha_arcsec:.4f} arcsec',
        'details': {'M': M, 'impact_parameter_b': b, 'alpha_rad': alpha,
                    'alpha_arcsec': alpha_arcsec},
        'unit': 'rad'
    }


def calc_einstein_ring_radius(M: float = 1.989e30, D_l: float = 1.0e21,
                                 D_s: float = 2.0e21, G: float = 6.67430e-11,
                                 c: float = 299792458.0) -> dict:
    """Einstein ring angular radius: theta_E = sqrt(4*G*M*(D_s-D_l)/(c^2*D_l*D_s))."""
    D_ls = D_s - D_l
    if D_ls <= 0:
        return {'result': 'Invalid geometry (D_l >= D_s)', 'details': {}, 'unit': 'arcsec'}
    theta_E = math.sqrt(4.0 * G * M * D_ls / (c * c * D_l * D_s))
    theta_E_arcsec = theta_E * 206265.0
    return {
        'result': f'Einstein ring radius theta_E = {theta_E:.4e} rad = {theta_E_arcsec:.4f} arcsec',
        'details': {'M': M, 'D_l': D_l, 'D_s': D_s, 'D_ls': D_ls,
                    'theta_E_rad': theta_E, 'theta_E_arcsec': theta_E_arcsec},
        'unit': 'arcsec'
    }


def calc_orbital_precession(M: float = 1.989e30, a: float = 5.79e10,
                               e: float = 0.2056, G: float = 6.67430e-11,
                               c: float = 299792458.0) -> dict:
    """GR perihelion precession per orbit: delta_phi = 6*pi*G*M/(a*(1-e^2)*c^2)."""
    delta_phi = 6.0 * math.pi * G * M / (a * (1.0 - e * e) * c * c)
    delta_phi_arcsec = delta_phi * 206265.0
    T = 2.0 * math.pi * math.sqrt(a * a * a / (G * M))
    precession_per_century = delta_phi_arcsec * (365.25 * 86400.0 * 100.0 / T)
    return {
        'result': f'Precession = {delta_phi:.4e} rad/orbit = {delta_phi_arcsec:.4f} arcsec/orbit = {precession_per_century:.4f} arcsec/century',
        'details': {'M': M, 'a': a, 'e': e, 'delta_phi_rad': delta_phi,
                    'delta_phi_arcsec': delta_phi_arcsec,
                    'orbital_period_T': T, 'precession_per_century': precession_per_century},
        'unit': 'rad'
    }


def calc_kerr_ergosphere(M: float = 10.0 * 1.989e30, a_spin: float = 0.5,
                           G: float = 6.67430e-11, c: float = 299792458.0) -> dict:
    """Kerr ergosphere radius: r_erg = GM/c^2 + sqrt((GM/c^2)^2 - a^2*cos^2(theta))."""
    rg = G * M / (c * c)
    a_param = a_spin * rg
    r_erg_equator = rg + math.sqrt(rg * rg - a_param * a_param * 0.0)  # cos(90deg) = 0
    r_erg_eq = rg + rg  # at equator, cos(theta)=0, so r_erg = 2rg = r_s
    r_s = 2.0 * rg
    r_erg = r_s  # at equator
    r_horizon = rg + math.sqrt(rg * rg - a_param * a_param)
    return {
        'result': f'Ergosphere (equator): r_erg = {r_erg/1000:.1f} km, Horizon: r_H = {r_horizon/1000:.1f} km',
        'details': {'M': M, 'spin_a': a_spin, 'rg_km': rg / 1000.0,
                    'r_ergosphere_km': r_erg / 1000.0, 'r_horizon_km': r_horizon / 1000.0},
        'unit': 'km'
    }


def calc_hawking_temperature(M: float = 1.989e30, G: float = 6.67430e-11,
                                c: float = 299792458.0,
                                h_bar: float = 1.054571817e-34) -> dict:
    """Hawking temperature: T_H = h_bar*c^3/(8*pi*G*k_B*M)."""
    k_B = 1.380649e-23
    T_H = h_bar * (c ** 3) / (8.0 * math.pi * G * k_B * M)
    return {
        'result': f'Hawking temperature T_H = {T_H:.4e} K',
        'details': {'M': M, 'G': G, 'c': c, 'h_bar': h_bar, 'k_B': k_B,
                    'T_H': T_H},
        'unit': 'K'
    }


def calc_hawking_evaporation_time(M: float = 1.989e30,
                                     G: float = 6.67430e-11,
                                     c: float = 299792458.0,
                                     h_bar: float = 1.054571817e-34) -> dict:
    """Hawking evaporation time: t_evap ~ (5120*pi*G^2*M^3)/(h_bar*c^4)."""
    t_evap = 5120.0 * math.pi * G * G * (M ** 3) / (h_bar * (c ** 4))
    return {
        'result': f'Evaporation time t_evap = {t_evap:.4e} s = {t_evap/(365.25*86400):.4e} years',
        'details': {'M': M, 't_evap_s': t_evap, 't_evap_years': t_evap / (365.25 * 86400.0)},
        'unit': 's'
    }


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Special Relativity
    'lorentz_factor': {'func': calc_lorentz_factor, 'params': ['v', 'c'],
                       'desc': 'Lorentz factor gamma = 1/sqrt(1 - v^2/c^2)'},
    'beta_from_gamma': {'func': calc_beta_from_gamma, 'params': ['gamma'],
                         'desc': 'Compute beta = v/c from Lorentz factor'},
    'time_dilation': {'func': calc_time_dilation, 'params': ['dt0', 'v', 'c'],
                      'desc': 'Time dilation delta_t = gamma * delta_t0'},
    'length_contraction': {'func': calc_length_contraction, 'params': ['L0', 'v', 'c'],
                            'desc': 'Length contraction L = L0/gamma'},
    'velocity_addition': {'func': calc_velocity_addition, 'params': ['u', 'v', 'c'],
                           'desc': "Relativistic velocity addition w = (u+v)/(1+uv/c^2)"},
    'relativistic_mass': {'func': calc_relativistic_mass, 'params': ['m0', 'v', 'c'],
                           'desc': 'Relativistic mass m = gamma*m0'},
    'rest_energy': {'func': calc_rest_energy, 'params': ['m', 'c'],
                    'desc': 'Rest energy E0 = m*c^2'},
    'total_energy': {'func': calc_total_energy, 'params': ['m0', 'v', 'c'],
                      'desc': 'Total energy E = gamma*m0*c^2 including KE'},
    'relativistic_kinetic_energy': {'func': calc_relativistic_kinetic_energy,
                                      'params': ['m0', 'v', 'c'],
                                      'desc': 'KE = (gamma - 1)*m0*c^2 vs classical'},
    'relativistic_momentum': {'func': calc_relativistic_momentum, 'params': ['m0', 'v', 'c'],
                                'desc': 'Relativistic momentum p = gamma*m0*v'},
    'energy_momentum_relation': {'func': calc_energy_momentum_relation,
                                   'params': ['p', 'm0', 'c'],
                                   'desc': 'E^2 = (pc)^2 + (m0c^2)^2'},
    # General Relativity
    'schwarzschild_radius': {'func': calc_schwarzschild_radius, 'params': ['M', 'G', 'c'],
                              'desc': 'Schwarzschild radius r_s = 2GM/c^2'},
    'gravitational_time_dilation': {'func': calc_gravitational_time_dilation,
                                      'params': ['dt0', 'M', 'r', 'G', 'c'],
                                      'desc': 'Gravitational time dilation near massive body'},
    'gravitational_redshift': {'func': calc_gravitational_redshift,
                                 'params': ['M', 'r_emit', 'r_obs', 'G', 'c'],
                                 'desc': 'Gravitational redshift from Schwarzschild metric'},
    'orbital_velocity_GR': {'func': calc_orbital_velocity_GR, 'params': ['M', 'r', 'G', 'c'],
                              'desc': 'GR-corrected circular orbital velocity'},
    'isco_radius': {'func': calc_isco_radius, 'params': ['M', 'G', 'c'],
                     'desc': 'ISCO radius for non-rotating BH: 6GM/c^2'},
    'photon_sphere': {'func': calc_photon_sphere, 'params': ['M', 'G', 'c'],
                       'desc': 'Photon sphere r = 3GM/c^2 = 1.5*r_s'},
    'gravitational_wave_strain': {'func': calc_gravitational_wave_strain,
                                    'params': ['M', 'R', 'f', 'G', 'c'],
                                    'desc': 'Estimate gravitational wave strain amplitude'},
    # Additional
    'spacetime_interval': {'func': calc_spacetime_interval, 'params': ['x', 'y', 'z', 't', 'c'],
                            'desc': 'Spacetime interval s^2 = (ct)^2 - x^2 - y^2 - z^2'},
    'lorentz_transform_position': {'func': calc_lorentz_transform_position,
                                     'params': ['x', 't', 'v', 'c'],
                                     'desc': "Lorentz transformation x' = gamma*(x-vt)"},
    'relativistic_doppler': {'func': calc_relativistic_doppler,
                              'params': ['f0', 'v', 'c', 'approaching'],
                              'desc': 'Relativistic Doppler shift for light'},
    'compton_scattering': {'func': calc_compton_scattering,
                            'params': ['wavelength', 'theta_deg'],
                            'desc': 'Compton wavelength shift delta_lambda = lambda_C*(1-cos(theta))'},
    'tidal_force': {'func': calc_tidal_force_Gm_over_R3,
                     'params': ['M', 'r', 'm', 'delta_r', 'G'],
                     'desc': 'Tidal force F = 2*G*M*m*delta_r/r^3'},
    'gravitational_lensing_angle': {'func': calc_gravitational_lensing_angle,
                                      'params': ['M', 'b', 'G', 'c'],
                                      'desc': 'Einstein lensing deflection alpha = 4GM/(bc^2)'},
    'einstein_ring_radius': {'func': calc_einstein_ring_radius,
                              'params': ['M', 'D_l', 'D_s', 'G', 'c'],
                              'desc': 'Einstein ring angular radius'},
    'orbital_precession': {'func': calc_orbital_precession,
                            'params': ['M', 'a', 'e', 'G', 'c'],
                            'desc': 'GR perihelion precession per orbit'},
    'kerr_ergosphere': {'func': calc_kerr_ergosphere,
                         'params': ['M', 'a_spin', 'G', 'c'],
                         'desc': 'Kerr BH ergosphere radius'},
    'hawking_temperature': {'func': calc_hawking_temperature,
                             'params': ['M', 'G', 'c', 'h_bar'],
                             'desc': 'Hawking black hole temperature'},
    'hawking_evaporation_time': {'func': calc_hawking_evaporation_time,
                                  'params': ['M', 'G', 'c', 'h_bar'],
                                  'desc': 'Hawking evaporation time for a black hole'},
}
