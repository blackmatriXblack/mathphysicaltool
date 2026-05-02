"""
Atomic, Molecular & Condensed Matter Physics - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_electron_configuration(Z: int = 26) -> dict:
    """Determine ground-state electron configuration by Aufbau principle."""
    subshell_order = [
        ('1s', 2), ('2s', 2), ('2p', 6), ('3s', 2), ('3p', 6),
        ('4s', 2), ('3d', 10), ('4p', 6), ('5s', 2), ('4d', 10),
        ('5p', 6), ('6s', 2), ('4f', 14), ('5d', 10), ('6p', 6),
        ('7s', 2), ('5f', 14), ('6d', 10), ('7p', 6)
    ]
    remaining = Z
    config = {}
    for orbital, capacity in subshell_order:
        if remaining <= 0:
            break
        electrons = min(remaining, capacity)
        config[orbital] = electrons
        remaining -= electrons
    config_str = ' '.join([f'{orb}{config[orb]}' for orb in config])
    return {
        'result': f'Z={Z}: {config_str}',
        'details': {'Z': Z, 'configuration': config, 'configuration_string': config_str, 'remaining_electrons': remaining},
        'unit': 'dimensionless'
    }

def calc_rydberg_spectral(n1: int = 2, n2: int = 3, Z: float = 1.0) -> dict:
    """Rydberg formula: 1/lambda = R_inf * Z^2 * (1/n1^2 - 1/n2^2)."""
    R_inf = 1.0973731568160e7
    delta = 1.0 / n1**2 - 1.0 / n2**2
    if delta <= 0:
        return {
            'result': 'n2 must be > n1 for emission lines',
            'details': {'n1': n1, 'n2': n2, 'Z': Z, 'delta': delta},
            'unit': 'm^(-1)'
        }
    inv_lambda = R_inf * Z**2 * delta
    wavelength = 1.0 / inv_lambda
    wavelength_nm = wavelength * 1e9
    E_eV = 1240.0 / wavelength_nm
    series = 'Lyman' if n1 == 1 else 'Balmer' if n1 == 2 else 'Paschen' if n1 == 3 else 'Brackett' if n1 == 4 else 'Pfund' if n1 == 5 else 'general'
    return {
        'result': f'{series} series: lambda = {wavelength_nm:.4f} nm, E = {E_eV:.4f} eV',
        'details': {'n1': n1, 'n2': n2, 'Z': Z, 'wavelength_m': wavelength, 'wavelength_nm': wavelength_nm, 'energy_eV': E_eV, 'series': series},
        'unit': 'm'
    }

def calc_ionization_energy(Z: int = 1, n: int = 1) -> dict:
    """Ionization energy: E_ion = 13.6 * Z^2 / n^2 eV (hydrogen-like)."""
    E_eV = 13.605693122994 * Z**2 / n**2
    E_J = E_eV * 1.602176634e-19
    return {
        'result': f'Ionization energy = {E_eV:.4f} eV = {E_J:.4e} J',
        'details': {'Z': Z, 'n': n, 'E_eV': E_eV, 'E_J': E_J},
        'unit': 'eV'
    }

def calc_electron_affinity(element: str = 'Cl') -> dict:
    """Electron affinity for selected elements (approximate values in eV)."""
    affinities = {
        'H': 0.754, 'He': -0.5, 'Li': 0.618, 'Be': -0.5, 'B': 0.277,
        'C': 1.263, 'N': -0.07, 'O': 1.461, 'F': 3.399, 'Ne': -1.2,
        'Na': 0.548, 'Mg': -0.4, 'Al': 0.433, 'Si': 1.385, 'P': 0.746,
        'S': 2.077, 'Cl': 3.613, 'Ar': -1.0, 'K': 0.501, 'Ca': 0.024,
        'Br': 3.364, 'I': 3.059
    }
    ea = affinities.get(element, None)
    if ea is None:
        ea = 0.0
    return {
        'result': f'Electron affinity of {element} = {ea:.3f} eV',
        'details': {'element': element, 'electron_affinity_eV': ea},
        'unit': 'eV'
    }

def calc_lennard_jones(r: float = 4.0e-10, epsilon: float = 1.65e-21, sigma: float = 3.4e-10) -> dict:
    """Lennard-Jones potential: V(r) = 4*epsilon*[(sigma/r)^12 - (sigma/r)^6]."""
    ratio = sigma / r
    V = 4.0 * epsilon * (ratio**12 - ratio**6)
    V_eV = V / 1.602176634e-19
    r_min = sigma * 2.0**(1.0/6.0)
    F = -24.0 * epsilon * (2.0 * ratio**12 - ratio**6) / r
    return {
        'result': f'V(r) = {V:.4e} J = {V_eV:.6f} eV, equilibrium at r_min = {r_min:.4e} m',
        'details': {'r_m': r, 'epsilon_J': epsilon, 'sigma_m': sigma, 'potential_J': V, 'potential_eV': V_eV, 'force_N': F, 'r_min_m': r_min},
        'unit': 'J'
    }

def calc_morse_potential(r: float = 1.5e-10, D_e: float = 7.0e-19, a: float = 2e10, r_e: float = 1.2e-10) -> dict:
    """Morse potential: V(r) = D_e * (1 - exp(-a*(r-r_e)))^2."""
    arg = np.exp(-a * (r - r_e))
    V = D_e * (1.0 - arg)**2
    V_eV = V / 1.602176634e-19
    harmonic_omega = a * np.sqrt(2.0 * D_e / 1.66e-27)
    return {
        'result': f'V(r) = {V:.4e} J = {V_eV:.6f} eV',
        'details': {'r_m': r, 'D_e_J': D_e, 'a': a, 'r_e_m': r_e, 'potential_J': V, 'potential_eV': V_eV, 'harmonic_freq_approx': harmonic_omega},
        'unit': 'J'
    }

def calc_rotational_spectra(J: int = 1, I_moment: float = 1.0e-46) -> dict:
    """Rotational energy: E_J = J*(J+1)*hbar^2 / (2*I)."""
    hbar = 1.054571817e-34
    E_J = J * (J + 1) * hbar**2 / (2.0 * I_moment)
    E_eV = E_J / 1.602176634e-19
    B_const = hbar**2 / (2.0 * I_moment)
    transition_J_to_Jp1 = 2.0 * B_const * (J + 1)
    return {
        'result': f'E_{J} = {E_J:.4e} J = {E_eV:.6f} eV, Delta_E(J->J+1) = {transition_J_to_Jp1:.4e} J',
        'details': {'J': J, 'I_kg_m2': I_moment, 'rotational_constant_B': B_const, 'E_J': E_J, 'E_eV': E_eV, 'transition_energy': transition_J_to_Jp1},
        'unit': 'J'
    }

def calc_vibrational_spectra(v: int = 1, omega: float = 3e14) -> dict:
    """Vibrational energy: E_v = (v + 1/2)*hbar*omega."""
    hbar = 1.054571817e-34
    E_v = (v + 0.5) * hbar * omega
    E_eV = E_v / 1.602176634e-19
    spacing = hbar * omega
    return {
        'result': f'E_{v} = {E_v:.4e} J = {E_eV:.6f} eV, spacing = {spacing:.4e} J',
        'details': {'v': v, 'omega': omega, 'energy_J': E_v, 'energy_eV': E_eV, 'spacing_J': spacing},
        'unit': 'J'
    }

def calc_franck_condon_overlap(v_ground: int = 0, v_excited: int = 2, delta_r: float = 0.1e-10, omega: float = 3e14, reduced_mass: float = 1.66e-27) -> dict:
    """Franck-Condon factor: overlap integral of vibrational wavefunctions."""
    hbar = 1.054571817e-34
    alpha = np.sqrt(reduced_mass * omega / hbar)
    hermite_vals_ground = _hermite_eval(v_ground, 0.0)
    hermite_vals_excited = _hermite_eval(v_excited, alpha * delta_r)
    overlap = np.exp(-alpha**2 * delta_r**2 / 4.0)
    for k in range(min(v_ground, v_excited) + 1):
        pass
    if v_ground == 0 and v_excited == 0:
        overlap = np.exp(-alpha**2 * delta_r**2 / 4.0)
    elif v_ground == 0 and v_excited == 1:
        overlap = alpha * delta_r / np.sqrt(2.0) * np.exp(-alpha**2 * delta_r**2 / 4.0)
    elif v_ground == 0 and v_excited == 2:
        overlap = (alpha**2 * delta_r**2 - 1.0) / (2.0 * np.sqrt(2.0)) * np.exp(-alpha**2 * delta_r**2 / 4.0)
    else:
        overlap = np.exp(-alpha**2 * delta_r**2 / 4.0) / (1.0 + abs(v_ground - v_excited))
    FC_factor = overlap**2
    return {
        'result': f'Franck-Condon factor |<{v_ground}|{v_excited}>|^2 = {FC_factor:.6e}',
        'details': {'v_ground': v_ground, 'v_excited': v_excited, 'delta_r_m': delta_r, 'overlap': overlap, 'FC_factor': FC_factor},
        'unit': 'dimensionless'
    }

def _hermite_eval(n: int, x: float) -> float:
    """Evaluate physicist's Hermite polynomial H_n(x) recursively."""
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0 * x
    h_nm2 = 1.0
    h_nm1 = 2.0 * x
    for i in range(2, n + 1):
        h_n = 2.0 * x * h_nm1 - 2.0 * (i - 1) * h_nm2
        h_nm2 = h_nm1
        h_nm1 = h_n
    return h_nm1

def calc_miller_indices_hkl(a: float = 4.0e-10, b: float = 4.0e-10, c: float = 4.0e-10, h: int = 1, k: int = 0, l: int = 0) -> dict:
    """Interplanar spacing for cubic: d_hkl = a / sqrt(h^2+k^2+l^2)."""
    d_spacing = a / np.sqrt(h**2 + k**2 + l**2 + 1e-30)
    volume = a * b * c
    return {
        'result': f'd_{{{h}{k}{l}}} = {d_spacing:.6e} m = {d_spacing*1e10:.4f} Angstrom',
        'details': {'a': a, 'b': b, 'c': c, 'h': h, 'k': k, 'l': l, 'd_spacing_m': d_spacing, 'd_spacing_angstrom': d_spacing * 1e10, 'cell_volume': volume},
        'unit': 'm'
    }

def calc_bragg_diffraction(d_spacing: float = 2.0e-10, wavelength: float = 1.54e-10, order: int = 1) -> dict:
    """Bragg diffraction: n*lambda = 2*d*sin(theta)."""
    arg = order * wavelength / (2.0 * d_spacing)
    if abs(arg) > 1.0:
        return {
            'result': f'No diffraction: n*lambda/(2d) = {arg:.4f} > 1',
            'details': {'d_spacing': d_spacing, 'wavelength': wavelength, 'order': order, 'sin_theta_arg': arg},
            'unit': 'rad'
        }
    theta = np.arcsin(arg)
    theta_deg = np.degrees(theta)
    return {
        'result': f'theta = {theta:.6f} rad = {theta_deg:.4f} deg',
        'details': {'d_spacing': d_spacing, 'wavelength': wavelength, 'order': order, 'theta_rad': theta, 'theta_deg': theta_deg},
        'unit': 'rad'
    }

def calc_reciprocal_lattice(a: list = None, b: list = None, c: list = None) -> dict:
    """Reciprocal lattice vectors: a* = 2*pi*(b x c)/volume, etc."""
    if a is None:
        a = [4e-10, 0, 0]
    if b is None:
        b = [0, 4e-10, 0]
    if c is None:
        c = [0, 0, 4e-10]
    av = np.array(a)
    bv = np.array(b)
    cv = np.array(c)
    volume = np.abs(np.dot(av, np.cross(bv, cv)))
    a_star = 2.0 * np.pi * np.cross(bv, cv) / volume
    b_star = 2.0 * np.pi * np.cross(cv, av) / volume
    c_star = 2.0 * np.pi * np.cross(av, bv) / volume
    return {
        'result': f'a* = [{a_star[0]:.2e}, {a_star[1]:.2e}, {a_star[2]:.2e}] m^(-1)',
        'details': {'a': av.tolist(), 'b': bv.tolist(), 'c': cv.tolist(), 'volume': volume, 'a_star': a_star.tolist(), 'b_star': b_star.tolist(), 'c_star': c_star.tolist()},
        'unit': 'm^(-1)'
    }

def calc_structure_factor(h: int = 1, k: int = 0, l: int = 0, atom_positions: list = None, atomic_factors: list = None) -> dict:
    """Structure factor F_hkl = sum(f_j * exp(2*pi*i*(h*x_j + k*y_j + l*z_j)))."""
    if atom_positions is None:
        atom_positions = [[0, 0, 0], [0.5, 0.5, 0.5]]
    if atomic_factors is None:
        atomic_factors = [1.0, 1.0]
    F = 0.0
    for f, pos in zip(atomic_factors, atom_positions):
        phase = 2.0 * np.pi * (h * pos[0] + k * pos[1] + l * pos[2])
        F += f * (np.cos(phase) + 1j * np.sin(phase))
    intensity = np.abs(F)**2
    return {
        'result': f'|F|^2 = {intensity:.6f}, F = {F:.4f}',
        'details': {'h': h, 'k': k, 'l': l, 'F': complex(F), '|F|': abs(F), 'intensity': intensity},
        'unit': 'dimensionless'
    }

def calc_free_electron_dispersion(k: float = 1e10, m: float = 9.11e-31) -> dict:
    """Free electron energy: E = hbar^2 * k^2 / (2*m)."""
    hbar = 1.054571817e-34
    E = hbar**2 * k**2 / (2.0 * m)
    E_eV = E / 1.602176634e-19
    v_group = hbar * k / m
    return {
        'result': f'E(k) = {E:.4e} J = {E_eV:.6f} eV',
        'details': {'k': k, 'mass': m, 'energy_J': E, 'energy_eV': E_eV, 'group_velocity': v_group},
        'unit': 'J'
    }

def calc_fermi_energy(electron_density: float = 8.5e28) -> dict:
    """Fermi energy: E_F = (hbar^2/(2m))*(3*pi^2*n)^(2/3)."""
    hbar = 1.054571817e-34
    m_e = 9.1093837015e-31
    E_F = (hbar**2 / (2.0 * m_e)) * (3.0 * np.pi**2 * electron_density)**(2.0/3.0)
    E_F_eV = E_F / 1.602176634e-19
    k_F = (3.0 * np.pi**2 * electron_density)**(1.0/3.0)
    T_F = E_F / 1.380649e-23
    return {
        'result': f'Fermi energy = {E_F_eV:.4f} eV, k_F = {k_F:.4e} m^(-1), T_F = {T_F:.2e} K',
        'details': {'electron_density': electron_density, 'E_F_J': E_F, 'E_F_eV': E_F_eV, 'k_F': k_F, 'T_F': T_F},
        'unit': 'J'
    }

def calc_density_of_states_3d(energy: float = 1.0, effective_mass: float = 9.11e-31) -> dict:
    """3D density of states: g(E) = (1/(2*pi^2))*(2m/hbar^2)^(3/2)*sqrt(E)."""
    hbar = 1.054571817e-34
    e_joules = energy * 1.602176634e-19
    if e_joules <= 0:
        g = 0.0
    else:
        prefactor = 1.0 / (2.0 * np.pi**2)
        factor = (2.0 * effective_mass / hbar**2)**(1.5)
        g = prefactor * factor * np.sqrt(e_joules)
    return {
        'result': f'g({energy} eV) = {g:.4e} J^(-1)*m^(-3)',
        'details': {'energy_eV': energy, 'effective_mass': effective_mass, 'DOS_J_per_m3': g, 'DOS_eV_per_m3': g * 1.602176634e-19},
        'unit': 'J^(-1)*m^(-3)'
    }

def calc_band_gap_material(material: str = 'Si') -> dict:
    """Band gap values for common semiconductors at 300 K."""
    bandgaps = {
        'Si': 1.12, 'Ge': 0.67, 'GaAs': 1.43, 'GaN': 3.4, 'InP': 1.35,
        'InAs': 0.36, 'GaP': 2.26, 'SiC': 3.0, 'ZnO': 3.37, 'CdTe': 1.5,
        'AlAs': 2.16, 'InSb': 0.17, 'ZnS': 3.6, 'ZnSe': 2.7, 'C_diamond': 5.47,
        'AlN': 6.0, 'TiO2': 3.2, 'PbS': 0.41, 'PbTe': 0.32
    }
    Eg = bandgaps.get(material, 0.0)
    Eg_J = Eg * 1.602176634e-19
    wavelength_nm = 1240.0 / Eg if Eg > 0 else float('inf')
    return {
        'result': f'{material}: E_g = {Eg:.3f} eV, threshold wavelength = {wavelength_nm:.1f} nm',
        'details': {'material': material, 'band_gap_eV': Eg, 'band_gap_J': Eg_J, 'threshold_wavelength_nm': wavelength_nm},
        'unit': 'eV'
    }

def calc_effective_mass_from_band(k_vals: list = None, E_vals: list = None) -> dict:
    """Effective mass: m* = hbar^2 / (d^2E/dk^2)."""
    if k_vals is None:
        k_vals = np.linspace(-1e9, 1e9, 101).tolist()
    if E_vals is None:
        E_vals = (1.054571817e-34**2 * np.linspace(-1e9, 1e9, 101)**2 / (2.0 * 9.11e-31)).tolist()
    k_arr = np.array(k_vals)
    E_arr = np.array(E_vals)
    dk = k_arr[1] - k_arr[0]
    d2E_dk2 = np.gradient(np.gradient(E_arr, dk), dk)
    idx_center = len(k_arr) // 2
    curvature = d2E_dk2[idx_center]
    hbar = 1.054571817e-34
    if abs(curvature) > 1e-40:
        m_eff = hbar**2 / curvature
    else:
        m_eff = float('inf')
    m_eff_ratio = m_eff / 9.1093837015e-31 if abs(m_eff) != float('inf') else float('inf')
    return {
        'result': f'm* = {m_eff:.4e} kg = {m_eff_ratio:.4f} m_e',
        'details': {'curvature': curvature, 'effective_mass': m_eff, 'm_eff_over_m_e': m_eff_ratio, 'hbar': hbar},
        'unit': 'kg'
    }

def calc_conductivity(carrier_density: float = 1e22, mobility: float = 0.14, charge_type: str = 'electron') -> dict:
    """Conductivity: sigma = n * e * mu."""
    e = 1.602176634e-19
    sigma = carrier_density * e * mobility
    resistivity = 1.0 / sigma if sigma > 0 else float('inf')
    return {
        'result': f'sigma = {sigma:.4e} S/m, rho = {resistivity:.4e} Ohm*m',
        'details': {'carrier_density': carrier_density, 'mobility': mobility, 'charge_type': charge_type, 'conductivity': sigma, 'resistivity': resistivity},
        'unit': 'S/m'
    }

def calc_stress_strain(force: float = 1000.0, area: float = 0.01, original_length: float = 1.0, delta_length: float = 0.001) -> dict:
    """Stress sigma = F/A, strain epsilon = Delta_L/L, Young's modulus E = sigma/epsilon."""
    stress = force / area
    strain = delta_length / original_length
    youngs_modulus = stress / strain if strain > 0 else float('inf')
    return {
        'result': f'sigma = {stress:.4e} Pa, epsilon = {strain:.6f}, E = {youngs_modulus:.4e} Pa',
        'details': {'force_N': force, 'area_m2': area, 'stress_Pa': stress, 'original_length_m': original_length, 'delta_length_m': delta_length, 'strain': strain, 'youngs_modulus_Pa': youngs_modulus},
        'unit': 'Pa'
    }

def calc_shear_modulus(youngs_modulus: float = 200e9, poisson_ratio: float = 0.3) -> dict:
    """Shear modulus: G = E / (2*(1+nu))."""
    G = youngs_modulus / (2.0 * (1.0 + poisson_ratio))
    return {
        'result': f'G = {G:.4e} Pa',
        'details': {'E_Pa': youngs_modulus, 'poisson_ratio': poisson_ratio, 'shear_modulus_Pa': G},
        'unit': 'Pa'
    }

def calc_bulk_modulus(youngs_modulus: float = 200e9, poisson_ratio: float = 0.3) -> dict:
    """Bulk modulus: K = E / (3*(1-2*nu))."""
    denominator = 3.0 * (1.0 - 2.0 * poisson_ratio)
    if abs(denominator) < 1e-15:
        K = float('inf')
    else:
        K = youngs_modulus / denominator
    return {
        'result': f'K = {K:.4e} Pa',
        'details': {'E_Pa': youngs_modulus, 'poisson_ratio': poisson_ratio, 'bulk_modulus_Pa': K},
        'unit': 'Pa'
    }

def calc_beam_bending(length: float = 1.0, load: float = 1000.0, E: float = 200e9, I_moment: float = 1e-6, support: str = 'simply_supported') -> dict:
    """Maximum beam deflection for various loading/support conditions."""
    if support == 'simply_supported':
        delta_max = load * length**3 / (48.0 * E * I_moment)
        max_moment = load * length / 4.0
    elif support == 'cantilever':
        delta_max = load * length**3 / (3.0 * E * I_moment)
        max_moment = load * length
    elif support == 'fixed_fixed':
        delta_max = load * length**3 / (192.0 * E * I_moment)
        max_moment = load * length / 8.0
    else:
        delta_max = load * length**3 / (48.0 * E * I_moment)
        max_moment = load * length / 4.0
    max_stress = max_moment * (I_moment**(1.0/4.0) * 0.5) / I_moment
    return {
        'result': f'delta_max = {delta_max:.6e} m = {delta_max*1e3:.4f} mm',
        'details': {'length_m': length, 'load_N': load, 'E_Pa': E, 'I_m4': I_moment, 'support': support, 'delta_max_m': delta_max, 'max_moment_Nm': max_moment, 'max_stress_Pa': max_stress},
        'unit': 'm'
    }

def calc_fracture_toughness(stress: float = 500e6, crack_length: float = 0.001, geometry_factor: float = 1.12) -> dict:
    """Stress intensity factor: K_I = Y * sigma * sqrt(pi*a)."""
    K_I = geometry_factor * stress * np.sqrt(np.pi * crack_length)
    K_I_MPa = K_I / 1e6
    return {
        'result': f'K_I = {K_I:.4e} Pa*sqrt(m) = {K_I_MPa:.4f} MPa*sqrt(m)',
        'details': {'stress_Pa': stress, 'crack_length_m': crack_length, 'Y': geometry_factor, 'K_I_Pa_sqrtm': K_I, 'K_I_MPa_sqrtm': K_I_MPa},
        'unit': 'Pa*sqrt(m)'
    }

def calc_intrinsic_carrier_conc(N_c: float = 2.8e25, N_v: float = 1.04e25, E_g: float = 1.12, T: float = 300.0) -> dict:
    """Intrinsic carrier concentration: n_i = sqrt(N_c * N_v) * exp(-E_g/(2*k*T))."""
    k_B = 1.380649e-23
    E_g_J = E_g * 1.602176634e-19
    n_i = np.sqrt(N_c * N_v) * np.exp(-E_g_J / (2.0 * k_B * T))
    return {
        'result': f'n_i = {n_i:.4e} m^(-3)',
        'details': {'N_c': N_c, 'N_v': N_v, 'E_g_eV': E_g, 'T_K': T, 'n_i': n_i},
        'unit': 'm^(-3)'
    }

def calc_pn_builtin_potential(N_a: float = 1e22, N_d: float = 1e22, n_i: float = 1.5e16, T: float = 300.0) -> dict:
    """Built-in potential: V_bi = (kT/q)*ln(N_a*N_d / n_i^2)."""
    k_B = 1.380649e-23
    q = 1.602176634e-19
    V_bi = (k_B * T / q) * np.log(N_a * N_d / (n_i**2))
    return {
        'result': f'V_bi = {V_bi:.6f} V',
        'details': {'N_a': N_a, 'N_d': N_d, 'n_i': n_i, 'T_K': T, 'V_bi_V': V_bi},
        'unit': 'V'
    }

def calc_depletion_width(V_bi: float = 0.7, V_applied: float = 0.0, N_a: float = 1e22, N_d: float = 1e22, epsilon_r: float = 11.9) -> dict:
    """Depletion width: W = sqrt(2*epsilon*(V_bi-V)*(N_a+N_d)/(q*N_a*N_d))."""
    epsilon_0 = 8.8541878128e-12
    epsilon_s = epsilon_0 * epsilon_r
    q = 1.602176634e-19
    V_total = V_bi - V_applied
    if V_total <= 0:
        return {
            'result': 'Forward bias exceeds built-in potential',
            'details': {'V_bi': V_bi, 'V_applied': V_applied, 'V_total': V_total},
            'unit': 'm'
        }
    W = np.sqrt(2.0 * epsilon_s * V_total * (N_a + N_d) / (q * N_a * N_d))
    x_n = W * N_a / (N_a + N_d)
    x_p = W * N_d / (N_a + N_d)
    return {
        'result': f'W = {W:.4e} m, x_n = {x_n:.4e} m, x_p = {x_p:.4e} m',
        'details': {'V_bi_V': V_bi, 'V_applied_V': V_applied, 'N_a': N_a, 'N_d': N_d, 'W_m': W, 'x_n_m': x_n, 'x_p_m': x_p},
        'unit': 'm'
    }

def calc_diode_current(V: float = 0.6, I0: float = 1e-12, T: float = 300.0, ideality: float = 1.0) -> dict:
    """Diode equation: I = I0 * (exp(q*V/(n*k*T)) - 1)."""
    k_B = 1.380649e-23
    q = 1.602176634e-19
    V_thermal = k_B * T / q
    arg = V / (ideality * V_thermal)
    if arg > 100:
        I = I0 * np.exp(arg)
    else:
        I = I0 * (np.exp(arg) - 1.0)
    return {
        'result': f'I = {I:.4e} A at V = {V} V',
        'details': {'V_V': V, 'I0_A': I0, 'T_K': T, 'ideality': ideality, 'thermal_voltage': V_thermal, 'I_A': I},
        'unit': 'A'
    }

def calc_doping_conductivity(dopant_conc: float = 1e22, mobility: float = 0.1, dopant_type: str = 'n') -> dict:
    """Doped semiconductor conductivity: sigma = n*e*mu or p*e*mu."""
    e = 1.602176634e-19
    sigma = dopant_conc * e * mobility
    rho = 1.0 / sigma if sigma > 0 else float('inf')
    return {
        'result': f'sigma = {sigma:.4e} S/m, rho = {rho:.4e} Ohm*m ({dopant_type}-type)',
        'details': {'dopant_conc': dopant_conc, 'mobility': mobility, 'type': dopant_type, 'conductivity': sigma, 'resistivity': rho},
        'unit': 'S/m'
    }

def calc_hall_effect(current_A: float = 1.0, B_T: float = 1.0, thickness_m: float = 0.001, n_carriers: float = 1e28) -> dict:
    """Hall voltage: V_H = I*B/(n*e*d)."""
    e = 1.602176634e-19
    V_H = current_A * B_T / (n_carriers * e * thickness_m)
    R_H = 1.0 / (n_carriers * e)
    return {
        'result': f'V_H = {V_H:.6e} V, R_H = {R_H:.4e} m^3/C',
        'details': {'current_A': current_A, 'B_T': B_T, 'thickness_m': thickness_m, 'n_carriers': n_carriers, 'V_H_V': V_H, 'Hall_coefficient': R_H},
        'unit': 'V'
    }

def calc_debye_length_doping(T: float = 300.0, doping_conc: float = 1e22, epsilon_r: float = 11.9) -> dict:
    """Debye screening length in semiconductor: L_D = sqrt(epsilon*kT/(q^2*n))."""
    epsilon_0 = 8.8541878128e-12
    k_B = 1.380649e-23
    q = 1.602176634e-19
    L_D = np.sqrt(epsilon_0 * epsilon_r * k_B * T / (q**2 * doping_conc))
    return {
        'result': f'L_D = {L_D:.4e} m = {L_D*1e9:.4f} nm',
        'details': {'T_K': T, 'doping_conc': doping_conc, 'epsilon_r': epsilon_r, 'Debye_length_m': L_D},
        'unit': 'm'
    }

def calc_junction_capacitance(V_bi: float = 0.7, V_R: float = -1.0, N_a: float = 1e22, N_d: float = 1e22, area: float = 1e-6, epsilon_r: float = 11.9) -> dict:
    """Junction capacitance: C_j = epsilon*A / W."""
    epsilon_0 = 8.8541878128e-12
    epsilon_s = epsilon_0 * epsilon_r
    q = 1.602176634e-19
    V_total = V_bi - V_R
    if V_total <= 0:
        return {
            'result': 'Invalid: V_bi - V_R must be positive',
            'details': {},
            'unit': 'F'
        }
    W = np.sqrt(2.0 * epsilon_s * V_total * (N_a + N_d) / (q * N_a * N_d))
    C_j = epsilon_s * area / W
    return {
        'result': f'C_j = {C_j:.4e} F = {C_j*1e12:.4f} pF',
        'details': {'V_bi_V': V_bi, 'V_R_V': V_R, 'depletion_width': W, 'C_j_F': C_j, 'area_m2': area},
        'unit': 'F'
    }

def calc_elastic_energy_density(stress: float = 100e6, strain: float = 0.001) -> dict:
    """Elastic energy density: u = (1/2)*sigma*epsilon."""
    u = 0.5 * stress * strain
    return {
        'result': f'U = {u:.4e} J/m^3',
        'details': {'stress_Pa': stress, 'strain': strain, 'energy_density': u},
        'unit': 'J/m^3'
    }

def calc_thermal_expansion(length: float = 1.0, alpha: float = 2.3e-5, delta_T: float = 100.0) -> dict:
    """Thermal expansion: Delta_L = alpha * L_0 * Delta_T."""
    delta_L = alpha * length * delta_T
    new_length = length + delta_L
    return {
        'result': f'Delta_L = {delta_L:.6e} m, new L = {new_length:.6e} m',
        'details': {'original_length_m': length, 'alpha': alpha, 'delta_T_K': delta_T, 'delta_L_m': delta_L, 'new_length_m': new_length},
        'unit': 'm'
    }

def calc_composite_youngs_modulus(E_fiber: float = 70e9, E_matrix: float = 3e9, V_fiber: float = 0.6, orientation: str = 'longitudinal') -> dict:
    """Rule of mixtures for composite modulus."""
    V_matrix = 1.0 - V_fiber
    if orientation == 'longitudinal':
        E_composite = E_fiber * V_fiber + E_matrix * V_matrix
    elif orientation == 'transverse':
        if E_fiber > 0 and E_matrix > 0:
            E_composite = 1.0 / (V_fiber / E_fiber + V_matrix / E_matrix)
        else:
            E_composite = 0.0
    else:
        E_composite = E_fiber * V_fiber + E_matrix * V_matrix
    return {
        'result': f'E_{orientation} = {E_composite:.4e} Pa = {E_composite/1e9:.4f} GPa',
        'details': {'E_fiber_Pa': E_fiber, 'E_matrix_Pa': E_matrix, 'V_fiber': V_fiber, 'V_matrix': V_matrix, 'orientation': orientation, 'E_composite_Pa': E_composite},
        'unit': 'Pa'
    }

def calc_bragg_wavelength_fiber(period: float = 535e-9, n_eff: float = 1.45) -> dict:
    """Fiber Bragg grating: lambda_B = 2 * n_eff * Lambda."""
    lambda_B = 2.0 * n_eff * period
    return {
        'result': f'lambda_B = {lambda_B:.4e} m = {lambda_B*1e9:.4f} nm',
        'details': {'period_m': period, 'n_eff': n_eff, 'bragg_wavelength_m': lambda_B, 'bragg_wavelength_nm': lambda_B * 1e9},
        'unit': 'm'
    }

def calc_piezoelectric_strain(d_33: float = 300e-12, E_field: float = 1e6) -> dict:
    """Piezoelectric strain: S = d * E."""
    S = d_33 * E_field
    return {
        'result': f'S = {S:.4e} (strain)',
        'details': {'d_33_C_N': d_33, 'E_field_V_m': E_field, 'strain': S},
        'unit': 'dimensionless'
    }

def calc_dielectric_polarization(E_field: float = 1e5, chi: float = 5.0) -> dict:
    """Polarization: P = epsilon_0 * chi * E."""
    epsilon_0 = 8.8541878128e-12
    P = epsilon_0 * chi * E_field
    D = epsilon_0 * E_field + P
    epsilon_r = 1.0 + chi
    return {
        'result': f'P = {P:.4e} C/m^2, epsilon_r = {epsilon_r:.4f}',
        'details': {'E_field': E_field, 'chi': chi, 'polarization': P, 'D_field': D, 'epsilon_r': epsilon_r},
        'unit': 'C/m^2'
    }

def calc_superconductor_critical_field(T: float = 4.2, T_c: float = 9.2, H_0: float = 0.2) -> dict:
    """Critical magnetic field: H_c(T) = H_0 * (1 - (T/T_c)^2)."""
    if T > T_c:
        H_c = 0.0
        state = 'normal'
    else:
        H_c = H_0 * (1.0 - (T / T_c)**2)
        state = 'superconducting'
    return {
        'result': f'H_c(T={T} K) = {H_c:.6f} T, state: {state}',
        'details': {'T_K': T, 'T_c_K': T_c, 'H_0_T': H_0, 'H_c_T': H_c, 'state': state},
        'unit': 'T'
    }

def calc_london_penetration_depth(n_s: float = 1e28, m: float = 9.11e-31) -> dict:
    """London penetration depth: lambda_L = sqrt(m/(mu_0 * n_s * e^2))."""
    mu_0 = 4.0 * np.pi * 1e-7
    e = 1.602176634e-19
    lambda_L = np.sqrt(m / (mu_0 * n_s * e**2))
    return {
        'result': f'lambda_L = {lambda_L:.4e} m = {lambda_L*1e9:.4f} nm',
        'details': {'n_s': n_s, 'mass': m, 'penetration_depth_m': lambda_L, 'mu_0': mu_0},
        'unit': 'm'
    }

def calc_fermi_velocity(electron_density: float = 8.5e28) -> dict:
    """Fermi velocity: v_F = hbar * k_F / m."""
    hbar = 1.054571817e-34
    m_e = 9.1093837015e-31
    k_F = (3.0 * np.pi**2 * electron_density)**(1.0/3.0)
    v_F = hbar * k_F / m_e
    return {
        'result': f'v_F = {v_F:.4e} m/s',
        'details': {'electron_density': electron_density, 'k_F': k_F, 'v_F': v_F},
        'unit': 'm/s'
    }

def calc_resistivity_temperature(rho_0: float = 1.68e-8, alpha_T: float = 3.9e-3, T: float = 373.0, T_ref: float = 293.0) -> dict:
    """Temperature-dependent resistivity: rho(T) = rho_0 * (1 + alpha*(T-T_ref))."""
    rho_T = rho_0 * (1.0 + alpha_T * (T - T_ref))
    return {
        'result': f'rho({T} K) = {rho_T:.4e} Ohm*m',
        'details': {'rho_0': rho_0, 'alpha': alpha_T, 'T_K': T, 'T_ref_K': T_ref, 'rho_T': rho_T},
        'unit': 'Ohm*m'
    }

def calc_drude_conductivity(n: float = 8.5e28, tau: float = 2.5e-14, m: float = 9.11e-31) -> dict:
    """Drude conductivity: sigma = n*e^2*tau/m."""
    e = 1.602176634e-19
    sigma = n * e**2 * tau / m
    rho = 1.0 / sigma
    return {
        'result': f'sigma = {sigma:.4e} S/m, rho = {rho:.4e} Ohm*m',
        'details': {'carrier_density': n, 'relaxation_time': tau, 'mass': m, 'conductivity': sigma, 'resistivity': rho},
        'unit': 'S/m'
    }

def calc_plasmon_frequency(n: float = 8.5e28, m: float = 9.11e-31, epsilon_inf: float = 1.0) -> dict:
    """Bulk plasmon frequency: omega_p = sqrt(n*e^2/(epsilon_0*epsilon_inf*m))."""
    epsilon_0 = 8.8541878128e-12
    e = 1.602176634e-19
    omega_p = np.sqrt(n * e**2 / (epsilon_0 * epsilon_inf * m))
    f_p = omega_p / (2.0 * np.pi)
    E_plasmon = 1.054571817e-34 * omega_p / 1.602176634e-19
    return {
        'result': f'omega_p = {omega_p:.4e} rad/s, f_p = {f_p:.4e} Hz, E = {E_plasmon:.4f} eV',
        'details': {'carrier_density': n, 'effective_mass': m, 'omega_p': omega_p, 'f_p': f_p, 'plasmon_energy_eV': E_plasmon},
        'unit': 'rad/s'
    }

COMMANDS = {
    'electron_config': {'func': calc_electron_configuration, 'params': ['Z'], 'desc': 'Electron configuration by Aufbau principle'},
    'rydberg_spectral': {'func': calc_rydberg_spectral, 'params': ['n1', 'n2', 'Z'], 'desc': 'Rydberg formula spectral line wavelength'},
    'ionization_energy': {'func': calc_ionization_energy, 'params': ['Z', 'n'], 'desc': 'Hydrogen-like ionization energy'},
    'electron_affinity': {'func': calc_electron_affinity, 'params': ['element'], 'desc': 'Electron affinity for selected elements'},
    'lennard_jones': {'func': calc_lennard_jones, 'params': ['r', 'epsilon', 'sigma'], 'desc': 'Lennard-Jones potential'},
    'morse_potential': {'func': calc_morse_potential, 'params': ['r', 'D_e', 'a', 'r_e'], 'desc': 'Morse potential for diatomic molecules'},
    'rotational_spectra': {'func': calc_rotational_spectra, 'params': ['J', 'I_moment'], 'desc': 'Rotational energy levels E_J'},
    'vibrational_spectra': {'func': calc_vibrational_spectra, 'params': ['v', 'omega'], 'desc': 'Vibrational energy levels E_v'},
    'franck_condon': {'func': calc_franck_condon_overlap, 'params': ['v_ground', 'v_excited', 'delta_r', 'omega', 'reduced_mass'], 'desc': 'Franck-Condon factor'},
    'miller_indices': {'func': calc_miller_indices_hkl, 'params': ['a', 'b', 'c', 'h', 'k', 'l'], 'desc': 'Interplanar spacing from Miller indices'},
    'bragg_diffraction': {'func': calc_bragg_diffraction, 'params': ['d_spacing', 'wavelength', 'order'], 'desc': 'Bragg diffraction angle'},
    'reciprocal_lattice': {'func': calc_reciprocal_lattice, 'params': ['a', 'b', 'c'], 'desc': 'Reciprocal lattice vectors'},
    'structure_factor': {'func': calc_structure_factor, 'params': ['h', 'k', 'l', 'atom_positions', 'atomic_factors'], 'desc': 'Crystal structure factor F_hkl'},
    'free_electron': {'func': calc_free_electron_dispersion, 'params': ['k', 'm'], 'desc': 'Free electron dispersion E(k)'},
    'fermi_energy': {'func': calc_fermi_energy, 'params': ['electron_density'], 'desc': 'Fermi energy and wave vector'},
    'density_of_states': {'func': calc_density_of_states_3d, 'params': ['energy', 'effective_mass'], 'desc': '3D density of states g(E)'},
    'band_gap': {'func': calc_band_gap_material, 'params': ['material'], 'desc': 'Band gap of common semiconductors'},
    'effective_mass': {'func': calc_effective_mass_from_band, 'params': ['k_vals', 'E_vals'], 'desc': 'Effective mass from band curvature'},
    'conductivity': {'func': calc_conductivity, 'params': ['carrier_density', 'mobility', 'charge_type'], 'desc': 'Electrical conductivity sigma = n*e*mu'},
    'stress_strain': {'func': calc_stress_strain, 'params': ['force', 'area', 'original_length', 'delta_length'], 'desc': 'Stress, strain, Youngs modulus'},
    'shear_modulus': {'func': calc_shear_modulus, 'params': ['youngs_modulus', 'poisson_ratio'], 'desc': 'Shear modulus G from E and nu'},
    'bulk_modulus': {'func': calc_bulk_modulus, 'params': ['youngs_modulus', 'poisson_ratio'], 'desc': 'Bulk modulus K from E and nu'},
    'beam_bending': {'func': calc_beam_bending, 'params': ['length', 'load', 'E', 'I_moment', 'support'], 'desc': 'Beam deflection for various supports'},
    'fracture_toughness': {'func': calc_fracture_toughness, 'params': ['stress', 'crack_length', 'geometry_factor'], 'desc': 'Stress intensity factor K_I'},
    'intrinsic_carrier': {'func': calc_intrinsic_carrier_conc, 'params': ['N_c', 'N_v', 'E_g', 'T'], 'desc': 'Intrinsic carrier concentration n_i'},
    'pn_builtin': {'func': calc_pn_builtin_potential, 'params': ['N_a', 'N_d', 'n_i', 'T'], 'desc': 'PN junction built-in potential'},
    'depletion_width': {'func': calc_depletion_width, 'params': ['V_bi', 'V_applied', 'N_a', 'N_d', 'epsilon_r'], 'desc': 'PN junction depletion width'},
    'diode_current': {'func': calc_diode_current, 'params': ['V', 'I0', 'T', 'ideality'], 'desc': 'Diode I-V characteristic'},
    'doping_conductivity': {'func': calc_doping_conductivity, 'params': ['dopant_conc', 'mobility', 'dopant_type'], 'desc': 'Doped semiconductor conductivity'},
    'hall_effect': {'func': calc_hall_effect, 'params': ['current_A', 'B_T', 'thickness_m', 'n_carriers'], 'desc': 'Hall effect voltage'},
    'debye_screening': {'func': calc_debye_length_doping, 'params': ['T', 'doping_conc', 'epsilon_r'], 'desc': 'Debye screening length'},
    'junction_capacitance': {'func': calc_junction_capacitance, 'params': ['V_bi', 'V_R', 'N_a', 'N_d', 'area', 'epsilon_r'], 'desc': 'PN junction capacitance'},
    'elastic_energy': {'func': calc_elastic_energy_density, 'params': ['stress', 'strain'], 'desc': 'Elastic energy density'},
    'thermal_expansion': {'func': calc_thermal_expansion, 'params': ['length', 'alpha', 'delta_T'], 'desc': 'Linear thermal expansion'},
    'composite_modulus': {'func': calc_composite_youngs_modulus, 'params': ['E_fiber', 'E_matrix', 'V_fiber', 'orientation'], 'desc': 'Composite modulus (rule of mixtures)'},
    'bragg_fiber': {'func': calc_bragg_wavelength_fiber, 'params': ['period', 'n_eff'], 'desc': 'Fiber Bragg grating wavelength'},
    'piezoelectric': {'func': calc_piezoelectric_strain, 'params': ['d_33', 'E_field'], 'desc': 'Piezoelectric strain'},
    'polarization': {'func': calc_dielectric_polarization, 'params': ['E_field', 'chi'], 'desc': 'Dielectric polarization P'},
    'critical_field': {'func': calc_superconductor_critical_field, 'params': ['T', 'T_c', 'H_0'], 'desc': 'Superconductor critical magnetic field'},
    'london_depth': {'func': calc_london_penetration_depth, 'params': ['n_s', 'm'], 'desc': 'London penetration depth'},
    'fermi_velocity': {'func': calc_fermi_velocity, 'params': ['electron_density'], 'desc': 'Fermi velocity v_F'},
    'resistivity_T': {'func': calc_resistivity_temperature, 'params': ['rho_0', 'alpha_T', 'T', 'T_ref'], 'desc': 'Temperature-dependent resistivity'},
    'drude': {'func': calc_drude_conductivity, 'params': ['n', 'tau', 'm'], 'desc': 'Drude model conductivity'},
    'plasmon': {'func': calc_plasmon_frequency, 'params': ['n', 'm', 'epsilon_inf'], 'desc': 'Bulk plasmon frequency'}
}
