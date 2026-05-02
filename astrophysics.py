"""
Astrophysics & Cosmology - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

G = 6.67430e-11
M_sun = 1.9885e30
R_sun = 6.957e8
L_sun = 3.828e26
sigma_sb = 5.670374419e-8
c_light = 2.99792458e8

def calc_mass_luminosity(mass: float = 1.0, exponent: float = 3.5) -> dict:
    """Mass-luminosity relation: L/L_sun = (M/M_sun)^alpha for main sequence."""
    L_ratio = mass**exponent
    L = L_ratio * L_sun
    return {
        'result': f'L = {L:.4e} W = {L_ratio:.4f} L_sun for M = {mass} M_sun',
        'details': {'mass_Msun': mass, 'luminosity_ratio': L_ratio, 'luminosity_W': L, 'exponent': exponent},
        'unit': 'W'
    }

def calc_stefan_boltzmann_luminosity(radius: float = 1.0, temperature: float = 5778.0) -> dict:
    """Stellar luminosity: L = 4*pi*R^2*sigma*T^4."""
    R_m = radius * R_sun
    L = 4.0 * np.pi * R_m**2 * sigma_sb * temperature**4
    L_ratio = L / L_sun
    F = sigma_sb * temperature**4
    return {
        'result': f'L = {L:.4e} W = {L_ratio:.4f} L_sun',
        'details': {'radius_Rsun': radius, 'radius_m': R_m, 'temperature_K': temperature, 'luminosity_W': L, 'luminosity_Lsun': L_ratio, 'surface_flux': F},
        'unit': 'W'
    }

def calc_main_sequence_lifetime(mass: float = 1.0) -> dict:
    """Main sequence lifetime: t_MS = 10^10 * (M/M_sun)^(-2.5) years."""
    t_MS = 1e10 * mass**(-2.5)
    return {
        'result': f'Main sequence lifetime = {t_MS:.4e} years',
        'details': {'mass_Msun': mass, 'lifetime_years': t_MS, 'lifetime_seconds': t_MS * 365.25 * 86400},
        'unit': 'years'
    }

def calc_chandrasekhar_mass(mu_e: float = 2.0) -> dict:
    """Chandrasekhar mass limit: M_ch ~ (5.836/mu_e^2) * M_sun."""
    M_ch = 5.836 / mu_e**2
    return {
        'result': f'M_Ch = {M_ch:.4f} M_sun',
        'details': {'mu_e': mu_e, 'Chandrasekhar_mass_Msun': M_ch},
        'unit': 'M_sun'
    }

def calc_jeans_mass(temperature: float = 10.0, density: float = 1e-19) -> dict:
    """Jeans mass: M_J = (pi/(6*G))^(3/2) * c_s^3 * rho^(-1/2)."""
    k_B = 1.380649e-23
    m_p = 1.67262192369e-27
    mean_molecular_weight = 2.3
    c_s = np.sqrt(k_B * temperature / (mean_molecular_weight * m_p))
    M_J = (np.pi / (6.0 * G))**(1.5) * c_s**3 * density**(-0.5)
    M_J_Msun = M_J / M_sun
    lambda_J = c_s * np.sqrt(np.pi / (G * density))
    return {
        'result': f'M_J = {M_J:.4e} kg = {M_J_Msun:.4f} M_sun, lambda_J = {lambda_J:.4e} m',
        'details': {'temperature_K': temperature, 'density_kg_m3': density, 'sound_speed': c_s, 'Jeans_mass_kg': M_J, 'Jeans_mass_Msun': M_J_Msun, 'Jeans_length_m': lambda_J},
        'unit': 'kg'
    }

def calc_virial_theorem(kinetic_energy: float = 1e35, potential_energy: float = -2e35) -> dict:
    """Virial theorem: 2*<T> + <U> = 0 for gravitationally bound system."""
    total = 2.0 * kinetic_energy + potential_energy
    balanced = abs(total) < 1e-3 * abs(kinetic_energy)
    return {
        'result': f'2T + U = {total:.4e} J, virial satisfied: {balanced}',
        'details': {'T_J': kinetic_energy, 'U_J': potential_energy, 'total_2T_plus_U': total, 'virial_satisfied': balanced},
        'unit': 'J'
    }

def calc_kepler_equation(mean_anomaly: float = 1.0, eccentricity: float = 0.5, tolerance: float = 1e-12) -> dict:
    """Kepler's equation: M = E - e*sin(E), solve for E via Newton-Raphson."""
    E = mean_anomaly
    for _ in range(100):
        f = E - eccentricity * np.sin(E) - mean_anomaly
        fp = 1.0 - eccentricity * np.cos(E)
        E_new = E - f / fp
        if abs(E_new - E) < tolerance:
            E = E_new
            break
        E = E_new
    true_anomaly = 2.0 * np.arctan2(np.sqrt(1.0 + eccentricity) * np.sin(E / 2.0), np.sqrt(1.0 - eccentricity) * np.cos(E / 2.0))
    return {
        'result': f'E = {E:.8f} rad, true anomaly = {true_anomaly:.8f} rad',
        'details': {'mean_anomaly_rad': mean_anomaly, 'eccentricity': eccentricity, 'eccentric_anomaly_rad': E, 'true_anomaly_rad': true_anomaly},
        'unit': 'rad'
    }

def calc_vis_viva(GM: float = 1.32712440018e20, r: float = 1.5e11, a: float = 1.5e11) -> dict:
    """Vis-viva equation: v^2 = GM*(2/r - 1/a)."""
    v_sq = GM * (2.0 / r - 1.0 / a)
    v = np.sqrt(max(v_sq, 0.0))
    if a > 0 and a < float('inf'):
        T = 2.0 * np.pi * np.sqrt(a**3 / GM)
    else:
        T = float('inf')
    return {
        'result': f'v = {v:.4e} m/s, period T = {T:.4e} s = {T/86400:.4f} days',
        'details': {'GM': GM, 'r_m': r, 'a_m': a, 'velocity_m_s': v, 'period_s': T},
        'unit': 'm/s'
    }

def calc_orbital_period(GM: float = 1.32712440018e20, a: float = 1.5e11) -> dict:
    """Orbital period from Kepler's third law: T^2 = 4*pi^2*a^3/GM."""
    T = 2.0 * np.pi * np.sqrt(a**3 / GM)
    n = 2.0 * np.pi / T
    return {
        'result': f'T = {T:.4e} s = {T/86400:.4f} days = {T/31557600:.4f} years',
        'details': {'GM': GM, 'semi_major_axis_m': a, 'period_s': T, 'mean_motion_rad_s': n},
        'unit': 's'
    }

def calc_hohmann_transfer(r1: float = 1.5e11, r2: float = 2.28e11, GM: float = 1.32712440018e20) -> dict:
    """Hohmann transfer orbit: delta_v = sqrt(GM/r1)*(sqrt(2*r2/(r1+r2)) - 1)."""
    a_t = (r1 + r2) / 2.0
    v1_initial = np.sqrt(GM / r1)
    v1_transfer = np.sqrt(GM * (2.0 / r1 - 1.0 / a_t))
    delta_v1 = v1_transfer - v1_initial
    v2_final = np.sqrt(GM / r2)
    v2_transfer = np.sqrt(GM * (2.0 / r2 - 1.0 / a_t))
    delta_v2 = v2_final - v2_transfer
    delta_v_total = abs(delta_v1) + abs(delta_v2)
    T_transfer = np.pi * np.sqrt(a_t**3 / GM)
    return {
        'result': f'Total delta_v = {delta_v_total:.4e} m/s, transfer time = {T_transfer/86400:.2f} days',
        'details': {'r1_m': r1, 'r2_m': r2, 'transfer_semi_axis': a_t, 'delta_v1': delta_v1, 'delta_v2': delta_v2, 'delta_v_total': delta_v_total, 'transfer_time_s': T_transfer},
        'unit': 'm/s'
    }

def calc_orbital_elements(position_velocity: dict = None) -> dict:
    """Compute orbital elements from position and velocity vectors."""
    if position_velocity is None:
        position_velocity = {'r': [1.5e11, 0, 0], 'v': [0, 29780, 0], 'GM': 1.32712440018e20}
    r_vec = np.array(position_velocity['r'])
    v_vec = np.array(position_velocity['v'])
    GM_val = position_velocity['GM']
    r = np.linalg.norm(r_vec)
    v = np.linalg.norm(v_vec)
    h_vec = np.cross(r_vec, v_vec)
    h = np.linalg.norm(h_vec)
    e_vec = np.cross(v_vec, h_vec) / GM_val - r_vec / r
    e = np.linalg.norm(e_vec)
    epsilon = 0.5 * v**2 - GM_val / r
    if abs(e - 1.0) > 1e-10:
        a = -GM_val / (2.0 * epsilon)
    else:
        a = float('inf')
    inclination = np.arccos(h_vec[2] / h) if h > 0 else 0.0
    return {
        'result': f'a = {a:.4e} m, e = {e:.6f}, i = {np.degrees(inclination):.4f} deg',
        'details': {'semi_major_axis_m': a, 'eccentricity': e, 'inclination_rad': inclination, 'inclination_deg': np.degrees(inclination), 'specific_energy': epsilon},
        'unit': 'm'
    }

def calc_schwarzschild_radius(mass: float = 1.0) -> dict:
    """Schwarzschild radius: R_s = 2*G*M / c^2."""
    M_kg = mass * M_sun
    R_s = 2.0 * G * M_kg / c_light**2
    return {
        'result': f'R_s = {R_s:.4e} m = {R_s/1000:.4f} km',
        'details': {'mass_Msun': mass, 'mass_kg': M_kg, 'Schwarzschild_radius_m': R_s, 'Schwarzschild_radius_km': R_s / 1000},
        'unit': 'm'
    }

def calc_neutron_star_properties(mass: float = 1.4) -> dict:
    """Neutron star density: rho = 3M/(4*pi*R^3), R ~ 10 km."""
    M_kg = mass * M_sun
    R = 10000.0
    rho = 3.0 * M_kg / (4.0 * np.pi * R**3)
    surface_g = G * M_kg / R**2
    v_esc = np.sqrt(2.0 * G * M_kg / R)
    return {
        'result': f'rho = {rho:.4e} kg/m^3, g = {surface_g:.4e} m/s^2, v_esc = {v_esc/3e8:.4f}c',
        'details': {'mass_Msun': mass, 'radius_km': R/1000, 'density_kg_m3': rho, 'surface_gravity': surface_g, 'escape_velocity': v_esc},
        'unit': 'kg/m^3'
    }

def calc_white_dwarf_mass_radius(mass: float = 0.6) -> dict:
    """White dwarf mass-radius: R/R_sun ~ 0.011*(M/M_sun)^(-1/3)."""
    R_ratio = mass**(-1.0/3.0) * 0.011
    R_m = R_ratio * R_sun
    R_km = R_m / 1000.0
    rho_central = 3.0 * mass * M_sun / (4.0 * np.pi * R_m**3)
    return {
        'result': f'R = {R_km:.2f} km, rho_c = {rho_central:.4e} kg/m^3',
        'details': {'mass_Msun': mass, 'radius_ratio': R_ratio, 'radius_m': R_m, 'radius_km': R_km, 'central_density': rho_central},
        'unit': 'm'
    }

def calc_hubble_law(distance_Mpc: float = 100.0, H0: float = 70.0) -> dict:
    """Hubble's law: v = H0 * d."""
    v = H0 * distance_Mpc
    z_approx = v / (c_light / 1000.0)
    return {
        'result': f'v = {v:.2f} km/s, z_approx = {z_approx:.6f}',
        'details': {'distance_Mpc': distance_Mpc, 'H0_kms_Mpc': H0, 'recession_velocity_km_s': v, 'redshift_approx': z_approx},
        'unit': 'km/s'
    }

def calc_redshift(wavelength_observed: float = 656.3e-9, wavelength_emitted: float = 121.6e-9) -> dict:
    """Redshift: z = (lambda_obs - lambda_emit) / lambda_emit."""
    z = (wavelength_observed - wavelength_emitted) / wavelength_emitted
    v_approx = z * c_light
    return {
        'result': f'z = {z:.6f}, v_approx = {v_approx:.4e} m/s',
        'details': {'lambda_obs_m': wavelength_observed, 'lambda_emit_m': wavelength_emitted, 'z': z, 'velocity_approx_m_s': v_approx},
        'unit': 'dimensionless'
    }

def calc_cosmic_scale_factor(redshift: float = 1.0) -> dict:
    """Scale factor: a(t) = 1/(1+z)."""
    a = 1.0 / (1.0 + redshift)
    return {
        'result': f'a(z={redshift}) = {a:.6f}',
        'details': {'redshift': redshift, 'scale_factor': a},
        'unit': 'dimensionless'
    }

def calc_friedmann_density(Omega_m: float = 0.3, Omega_L: float = 0.7, Omega_k: float = 0.0, z: float = 0.0) -> dict:
    """Friedmann: H^2(z) = H0^2 * (Omega_m*(1+z)^3 + Omega_k*(1+z)^2 + Omega_L)."""
    H0 = 70.0
    E_sq = Omega_m * (1.0 + z)**3 + Omega_k * (1.0 + z)**2 + Omega_L
    H_z = H0 * np.sqrt(max(E_sq, 0.0))
    return {
        'result': f'H(z={z}) = {H_z:.4f} km/s/Mpc',
        'details': {'Omega_m': Omega_m, 'Omega_L': Omega_L, 'Omega_k': Omega_k, 'z': z, 'E_squared': E_sq, 'H_z': H_z},
        'unit': 'km/s/Mpc'
    }

def calc_critical_density(H0: float = 70.0) -> dict:
    """Critical density: rho_c = 3*H0^2/(8*pi*G)."""
    H0_SI = H0 * 1000.0 / 3.085677581e22
    rho_c = 3.0 * H0_SI**2 / (8.0 * np.pi * G)
    rho_c_GeV_cm3 = rho_c * 1.78266192e-9 * 1e-6
    return {
        'result': f'rho_c = {rho_c:.4e} kg/m^3',
        'details': {'H0_kms_Mpc': H0, 'H0_per_s': H0_SI, 'rho_c_kg_m3': rho_c, 'rho_c_GeV_cm3': rho_c_GeV_cm3},
        'unit': 'kg/m^3'
    }

def calc_age_of_universe(H0: float = 70.0) -> dict:
    """Age of universe (simple): t ~ 1/H0 for matter-dominated."""
    H0_SI = H0 * 1000.0 / 3.085677581e22
    t_age = 1.0 / H0_SI
    t_Gyr = t_age / (365.25 * 86400 * 1e9)
    return {
        'result': f't_age = {t_Gyr:.4f} Gyr',
        'details': {'H0': H0, 'H0_SI': H0_SI, 'age_s': t_age, 'age_Gyr': t_Gyr},
        'unit': 's'
    }

def calc_lookback_time(z: float = 1.0, H0: float = 70.0, Omega_m: float = 0.3, Omega_L: float = 0.7) -> dict:
    """Lookback time via numerical integration."""
    H0_SI = H0 * 1000.0 / 3.085677581e22
    n_steps = 1000
    z_array = np.linspace(0, z, n_steps)
    integrand = np.zeros(n_steps)
    for i, zi in enumerate(z_array):
        E = np.sqrt(Omega_m * (1.0 + zi)**3 + Omega_L)
        integrand[i] = 1.0 / ((1.0 + zi) * E)
    t_L = np.trapz(integrand, z_array) / H0_SI
    t_L_Gyr = t_L / (365.25 * 86400 * 1e9)
    return {
        'result': f'Lookback time to z={z} = {t_L_Gyr:.4f} Gyr',
        'details': {'z': z, 'H0': H0, 'Omega_m': Omega_m, 'Omega_L': Omega_L, 'lookback_time_s': t_L, 'lookback_time_Gyr': t_L_Gyr},
        'unit': 's'
    }

def calc_angular_diameter_distance(z: float = 1.0, H0: float = 70.0, Omega_m: float = 0.3, Omega_L: float = 0.7) -> dict:
    """Angular diameter distance: D_A = D_M / (1+z)."""
    c_kms = c_light / 1000.0
    n_steps = 500
    z_arr = np.linspace(0, z, n_steps)
    integrand = np.array([1.0 / np.sqrt(Omega_m * (1.0 + zi)**3 + Omega_L) for zi in z_arr])
    D_C = (c_kms / H0) * np.trapz(integrand, z_arr)
    D_A = D_C / (1.0 + z)
    return {
        'result': f'D_A = {D_A:.4f} Mpc',
        'details': {'z': z, 'H0': H0, 'comoving_distance_Mpc': D_C, 'angular_diameter_distance_Mpc': D_A},
        'unit': 'Mpc'
    }

def calc_luminosity_distance(z: float = 1.0, H0: float = 70.0, Omega_m: float = 0.3, Omega_L: float = 0.7) -> dict:
    """Luminosity distance: D_L = (1+z)^2 * D_A = (1+z) * D_C."""
    c_kms = c_light / 1000.0
    n_steps = 500
    z_arr = np.linspace(0, z, n_steps)
    integrand = np.array([1.0 / np.sqrt(Omega_m * (1.0 + zi)**3 + Omega_L) for zi in z_arr])
    D_C = (c_kms / H0) * np.trapz(integrand, z_arr)
    D_L = D_C * (1.0 + z)
    return {
        'result': f'D_L = {D_L:.4f} Mpc',
        'details': {'z': z, 'H0': H0, 'comoving_distance_Mpc': D_C, 'luminosity_distance_Mpc': D_L},
        'unit': 'Mpc'
    }

def calc_distance_modulus(z: float = 0.1, H0: float = 70.0, Omega_m: float = 0.3, Omega_L: float = 0.7) -> dict:
    """Distance modulus: mu = 5 * log10(D_L / 10 pc)."""
    c_kms = c_light / 1000.0
    n_steps = 500
    z_arr = np.linspace(0, z, n_steps)
    integrand = np.array([1.0 / np.sqrt(Omega_m * (1.0 + zi)**3 + Omega_L) for zi in z_arr])
    D_C = (c_kms / H0) * np.trapz(integrand, z_arr)
    D_L = D_C * (1.0 + z)
    D_L_pc = D_L * 1e6
    mu = 5.0 * np.log10(D_L_pc / 10.0)
    return {
        'result': f'mu = {mu:.4f} mag, D_L = {D_L:.2f} Mpc',
        'details': {'z': z, 'D_L_Mpc': D_L, 'mu_mag': mu},
        'unit': 'mag'
    }

def calc_virial_mass(velocity_dispersion: float = 200e3, radius: float = 1e21) -> dict:
    """Virial mass estimate: M_vir = 3*sigma_v^2*R / G."""
    M_vir = 3.0 * velocity_dispersion**2 * radius / G
    M_vir_Msun = M_vir / M_sun
    return {
        'result': f'M_vir = {M_vir:.4e} kg = {M_vir_Msun:.4e} M_sun',
        'details': {'velocity_dispersion_m_s': velocity_dispersion, 'radius_m': radius, 'M_vir_kg': M_vir, 'M_vir_Msun': M_vir_Msun},
        'unit': 'kg'
    }

def calc_rotation_curve(mass_interior: float = 1e40, radius: float = 1e20) -> dict:
    """Circular velocity: v_c = sqrt(G * M(r) / r)."""
    v_c = np.sqrt(G * mass_interior / radius)
    v_c_kms = v_c / 1000.0
    return {
        'result': f'v_c = {v_c_kms:.4f} km/s at r = {radius/3.086e19:.2f} kpc',
        'details': {'M_interior_kg': mass_interior, 'radius_m': radius, 'circular_velocity_m_s': v_c, 'circular_velocity_km_s': v_c_kms},
        'unit': 'm/s'
    }

def calc_nfw_profile(radius: float = 1e20, rho_0: float = 1e-17, r_s: float = 2e20) -> dict:
    """NFW dark matter density: rho(r) = rho_0 / ((r/r_s)*(1+r/r_s)^2)."""
    x = radius / r_s
    if x > 0:
        rho = rho_0 / (x * (1.0 + x)**2)
    else:
        rho = float('inf')
    M_enc = 4.0 * np.pi * rho_0 * r_s**3 * (np.log(1.0 + x) - x / (1.0 + x))
    return {
        'result': f'rho(r) = {rho:.4e} kg/m^3, M(<r) = {M_enc/M_sun:.4e} M_sun',
        'details': {'radius_m': radius, 'rho_0': rho_0, 'r_s_m': r_s, 'density': rho, 'enclosed_mass_kg': M_enc, 'enclosed_mass_Msun': M_enc / M_sun},
        'unit': 'kg/m^3'
    }

def calc_eddington_luminosity(mass: float = 10.0, electron_scattering_opacity: float = 0.034) -> dict:
    """Eddington luminosity: L_Edd = 4*pi*G*M*c / kappa."""
    M_kg = mass * M_sun
    L_Edd = 4.0 * np.pi * G * M_kg * c_light / electron_scattering_opacity
    L_Edd_solar = L_Edd / L_sun
    return {
        'result': f'L_Edd = {L_Edd:.4e} W = {L_Edd_solar:.4e} L_sun',
        'details': {'mass_Msun': mass, 'kappa': electron_scattering_opacity, 'L_Edd_W': L_Edd, 'L_Edd_Lsun': L_Edd_solar},
        'unit': 'W'
    }

def calc_tidal_force(mass_primary: float = 1.0, separation: float = 1.5e11) -> dict:
    """Tidal force across Earth: F_tidal = 2*G*M*d/r^3 (per unit mass)."""
    M_kg = mass_primary * M_sun
    d = 2.0 * 6.371e6
    F_tidal_per_kg = 2.0 * G * M_kg * d / separation**3
    return {
        'result': f'F_tidal per kg = {F_tidal_per_kg:.4e} m/s^2',
        'details': {'M_primary_Msun': mass_primary, 'separation_m': separation, 'object_size_m': d, 'tidal_acceleration': F_tidal_per_kg},
        'unit': 'm/s^2'
    }

def calc_escape_velocity(mass: float = 1.0, radius: float = 1.0) -> dict:
    """Escape velocity: v_esc = sqrt(2*G*M/R)."""
    M_kg = mass * M_sun
    R_m = radius * R_sun
    v_esc = np.sqrt(2.0 * G * M_kg / R_m)
    return {
        'result': f'v_esc = {v_esc:.4e} m/s = {v_esc/1000:.4f} km/s',
        'details': {'mass_Msun': mass, 'radius_Rsun': radius, 'v_esc_m_s': v_esc, 'v_esc_km_s': v_esc / 1000},
        'unit': 'm/s'
    }

def calc_hill_radius(mass_planet: float = 5.97e24, mass_star: float = 1.989e30, semi_major_axis: float = 1.5e11) -> dict:
    """Hill radius: R_H = a * (m_p / (3*M_star))^(1/3)."""
    R_H = semi_major_axis * (mass_planet / (3.0 * mass_star))**(1.0/3.0)
    return {
        'result': f'R_Hill = {R_H:.4e} m = {R_H/1e9:.4f} million km',
        'details': {'planet_mass_kg': mass_planet, 'star_mass_kg': mass_star, 'semi_major_axis_m': semi_major_axis, 'hill_radius_m': R_H},
        'unit': 'm'
    }

def calc_free_fall_time(density: float = 1e-19) -> dict:
    """Free-fall time: t_ff = sqrt(3*pi/(32*G*rho))."""
    t_ff = np.sqrt(3.0 * np.pi / (32.0 * G * density))
    t_ff_yr = t_ff / (365.25 * 86400)
    return {
        'result': f't_ff = {t_ff:.4e} s = {t_ff_yr:.4e} years',
        'details': {'density_kg_m3': density, 'free_fall_time_s': t_ff, 'free_fall_time_yr': t_ff_yr},
        'unit': 's'
    }

def calc_keplerian_velocity(mass: float = 1.0, radius: float = 1.5e11) -> dict:
    """Keplerian orbital velocity: v_k = sqrt(G*M/r)."""
    M_kg = mass * M_sun
    v_k = np.sqrt(G * M_kg / radius)
    return {
        'result': f'v_k = {v_k:.4e} m/s = {v_k/1000:.4f} km/s',
        'details': {'mass_Msun': mass, 'radius_m': radius, 'keplerian_velocity_m_s': v_k, 'keplerian_velocity_km_s': v_k / 1000},
        'unit': 'm/s'
    }

def calc_habitable_zone(luminosity: float = 1.0) -> dict:
    """Habitable zone boundaries: r_inner = sqrt(L/L_sun/1.1), r_outer = sqrt(L/L_sun/0.53) in AU."""
    r_inner_AU = np.sqrt(luminosity / 1.1)
    r_outer_AU = np.sqrt(luminosity / 0.53)
    return {
        'result': f'HZ: {r_inner_AU:.4f} - {r_outer_AU:.4f} AU',
        'details': {'luminosity_Lsun': luminosity, 'inner_boundary_AU': r_inner_AU, 'outer_boundary_AU': r_outer_AU},
        'unit': 'AU'
    }

def calc_surface_gravity(mass: float = 1.0, radius: float = 1.0) -> dict:
    """Surface gravity: g = G*M/R^2."""
    M_kg = mass * M_sun
    R_m = radius * R_sun
    g = G * M_kg / R_m**2
    log_g = np.log10(g * 100.0)
    return {
        'result': f'g = {g:.4e} m/s^2, log(g[cm/s^2]) = {log_g:.4f}',
        'details': {'mass_Msun': mass, 'radius_Rsun': radius, 'surface_gravity_m_s2': g, 'log_g_cgs': log_g},
        'unit': 'm/s^2'
    }

def calc_synchrotron_frequency(B_T: float = 1e-9, gamma: float = 1e4) -> dict:
    """Synchrotron critical frequency: nu_c = (3/(4*pi))*gamma^2*(e*B/(m_e*c))."""
    e = 1.602176634e-19
    m_e = 9.1093837015e-31
    omega_c = 3.0 * e * B_T * gamma**2 / (2.0 * m_e)
    nu_c = omega_c / (2.0 * np.pi)
    return {
        'result': f'nu_c = {nu_c:.4e} Hz',
        'details': {'B_T': B_T, 'gamma': gamma, 'critical_frequency_Hz': nu_c},
        'unit': 'Hz'
    }

def calc_roche_lobe(mass_primary: float = 1.0, mass_secondary: float = 0.6, separation: float = 5.0e9) -> dict:
    """Roche lobe radius: R_L/a = 0.49*q^(2/3)/(0.6*q^(2/3) + ln(1+q^(1/3)))."""
    q = mass_primary / mass_secondary
    R_L_over_a = 0.49 * q**(2.0/3.0) / (0.6 * q**(2.0/3.0) + np.log(1.0 + q**(1.0/3.0)))
    R_L = R_L_over_a * separation
    return {
        'result': f'R_L = {R_L:.4e} m = {R_L/R_sun:.4f} R_sun',
        'details': {'q': q, 'R_L_over_a': R_L_over_a, 'Roche_lobe_radius_m': R_L},
        'unit': 'm'
    }

def calc_doppler_shift(rest_wavelength: float = 656.3e-9, velocity: float = 100e3) -> dict:
    """Doppler shift: lambda_obs = lambda_rest * (1 + v/c)."""
    wl_obs = rest_wavelength * (1.0 + velocity / c_light)
    delta_lambda = wl_obs - rest_wavelength
    return {
        'result': f'lambda_obs = {wl_obs*1e9:.4f} nm, Delta_lambda = {delta_lambda*1e9:.4f} nm',
        'details': {'rest_wavelength_m': rest_wavelength, 'velocity_m_s': velocity, 'observed_wavelength_m': wl_obs, 'delta_wavelength_m': delta_lambda},
        'unit': 'm'
    }

COMMANDS = {
    'mass_luminosity': {'func': calc_mass_luminosity, 'params': ['mass', 'exponent'], 'desc': 'Mass-luminosity relation L ~ M^alpha'},
    'stefan_boltzmann': {'func': calc_stefan_boltzmann_luminosity, 'params': ['radius', 'temperature'], 'desc': 'Stellar luminosity from Stefan-Boltzmann'},
    'main_sequence_lifetime': {'func': calc_main_sequence_lifetime, 'params': ['mass'], 'desc': 'Main sequence stellar lifetime'},
    'chandrasekhar_mass': {'func': calc_chandrasekhar_mass, 'params': ['mu_e'], 'desc': 'Chandrasekhar mass limit'},
    'jeans_mass': {'func': calc_jeans_mass, 'params': ['temperature', 'density'], 'desc': 'Jeans mass for gravitational collapse'},
    'virial_theorem': {'func': calc_virial_theorem, 'params': ['kinetic_energy', 'potential_energy'], 'desc': 'Virial theorem check 2T+U=0'},
    'kepler_equation': {'func': calc_kepler_equation, 'params': ['mean_anomaly', 'eccentricity', 'tolerance'], 'desc': 'Kepler equation M = E - e*sin(E)'},
    'vis_viva': {'func': calc_vis_viva, 'params': ['GM', 'r', 'a'], 'desc': 'Vis-viva equation for orbital velocity'},
    'orbital_period': {'func': calc_orbital_period, 'params': ['GM', 'a'], 'desc': 'Orbital period from Kepler third law'},
    'hohmann_transfer': {'func': calc_hohmann_transfer, 'params': ['r1', 'r2', 'GM'], 'desc': 'Hohmann transfer delta-v'},
    'orbital_elements': {'func': calc_orbital_elements, 'params': ['position_velocity'], 'desc': 'Orbital elements from position and velocity vectors'},
    'schwarzschild_radius': {'func': calc_schwarzschild_radius, 'params': ['mass'], 'desc': 'Schwarzschild radius R_s = 2GM/c^2'},
    'neutron_star': {'func': calc_neutron_star_properties, 'params': ['mass'], 'desc': 'Neutron star density and properties'},
    'white_dwarf_mr': {'func': calc_white_dwarf_mass_radius, 'params': ['mass'], 'desc': 'White dwarf mass-radius relation'},
    'hubble_law': {'func': calc_hubble_law, 'params': ['distance_Mpc', 'H0'], 'desc': 'Hubble law v = H0*d'},
    'redshift': {'func': calc_redshift, 'params': ['wavelength_observed', 'wavelength_emitted'], 'desc': 'Redshift z from wavelength shift'},
    'scale_factor': {'func': calc_cosmic_scale_factor, 'params': ['redshift'], 'desc': 'Cosmic scale factor a = 1/(1+z)'},
    'friedmann': {'func': calc_friedmann_density, 'params': ['Omega_m', 'Omega_L', 'Omega_k', 'z'], 'desc': 'Friedmann equation expansion rate H(z)'},
    'critical_density': {'func': calc_critical_density, 'params': ['H0'], 'desc': 'Critical density rho_c = 3H0^2/(8*pi*G)'},
    'age_of_universe': {'func': calc_age_of_universe, 'params': ['H0'], 'desc': 'Age of the universe 1/H0 approximation'},
    'lookback_time': {'func': calc_lookback_time, 'params': ['z', 'H0', 'Omega_m', 'Omega_L'], 'desc': 'Lookback time to redshift z'},
    'angular_diameter_distance': {'func': calc_angular_diameter_distance, 'params': ['z', 'H0', 'Omega_m', 'Omega_L'], 'desc': 'Angular diameter distance D_A'},
    'luminosity_distance': {'func': calc_luminosity_distance, 'params': ['z', 'H0', 'Omega_m', 'Omega_L'], 'desc': 'Luminosity distance D_L'},
    'distance_modulus': {'func': calc_distance_modulus, 'params': ['z', 'H0', 'Omega_m', 'Omega_L'], 'desc': 'Distance modulus mu = 5*log10(D_L/10pc)'},
    'virial_mass': {'func': calc_virial_mass, 'params': ['velocity_dispersion', 'radius'], 'desc': 'Virial mass estimate from velocity dispersion'},
    'rotation_curve': {'func': calc_rotation_curve, 'params': ['mass_interior', 'radius'], 'desc': 'Circular velocity from enclosed mass'},
    'nfw_profile': {'func': calc_nfw_profile, 'params': ['radius', 'rho_0', 'r_s'], 'desc': 'NFW dark matter density profile'},
    'eddington_luminosity': {'func': calc_eddington_luminosity, 'params': ['mass', 'electron_scattering_opacity'], 'desc': 'Eddington luminosity limit'},
    'tidal_force': {'func': calc_tidal_force, 'params': ['mass_primary', 'separation'], 'desc': 'Tidal force per unit mass'},
    'escape_velocity': {'func': calc_escape_velocity, 'params': ['mass', 'radius'], 'desc': 'Escape velocity from stellar surface'},
    'hill_radius': {'func': calc_hill_radius, 'params': ['mass_planet', 'mass_star', 'semi_major_axis'], 'desc': 'Hill radius of a planet'},
    'free_fall_time': {'func': calc_free_fall_time, 'params': ['density'], 'desc': 'Free-fall time t_ff = sqrt(3*pi/(32*G*rho))'},
    'keplerian_velocity': {'func': calc_keplerian_velocity, 'params': ['mass', 'radius'], 'desc': 'Keplerian orbital velocity'},
    'habitable_zone': {'func': calc_habitable_zone, 'params': ['luminosity'], 'desc': 'Circumstellar habitable zone boundaries'},
    'surface_gravity': {'func': calc_surface_gravity, 'params': ['mass', 'radius'], 'desc': 'Stellar surface gravity g = GM/R^2'},
    'synchrotron': {'func': calc_synchrotron_frequency, 'params': ['B_T', 'gamma'], 'desc': 'Synchrotron critical frequency'},
    'roche_lobe': {'func': calc_roche_lobe, 'params': ['mass_primary', 'mass_secondary', 'separation'], 'desc': 'Roche lobe radius'},
    'doppler_shift': {'func': calc_doppler_shift, 'params': ['rest_wavelength', 'velocity'], 'desc': 'Doppler shift from radial velocity'}
}
