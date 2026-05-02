"""
Nuclear & Particle Physics - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_nuclear_binding_energy(Z: int = 26, N: int = 30) -> dict:
    """Binding energy: B = Z*m_p + N*m_n - M_nucleus (in amu*931.494 MeV/amu)."""
    m_p = 1.00727646688
    m_n = 1.00866491588
    atomic_masses = {
        (26, 30): 55.9349375, (26, 28): 53.9396105, (26, 31): 56.9353940,
        (92, 146): 238.0507882, (6, 6): 12.0, (8, 8): 15.9949146,
        (1, 0): 1.00782503223, (2, 1): 3.01604928199, (1, 1): 2.01410177811,
        (79, 118): 196.9665701, (82, 126): 207.9766528, (2, 2): 4.00260325413,
        (3, 4): 7.01600455, (4, 5): 9.0121822, (5, 5): 10.0129370,
    }
    m_atom = atomic_masses.get((Z, N), Z * m_p + N * m_n - 0.001 * (Z + N))
    m_nucleus = m_atom - Z * 0.00054857990907
    mass_defect = Z * m_p + N * m_n - m_nucleus
    B_MeV = mass_defect * 931.49410242
    B_per_nucleon = B_MeV / (Z + N) if (Z + N) > 0 else 0
    return {
        'result': f'B = {B_MeV:.4f} MeV, B/A = {B_per_nucleon:.4f} MeV/nucleon',
        'details': {'Z': Z, 'N': N, 'A': Z + N, 'mass_defect_amu': mass_defect, 'B_MeV': B_MeV, 'B_per_nucleon_MeV': B_per_nucleon},
        'unit': 'MeV'
    }

def calc_semi_empirical_mass(Z: int = 26, N: int = 30) -> dict:
    """Bethe-Weizsacker semi-empirical mass formula."""
    A = Z + N
    a_v = 15.75
    a_s = 17.8
    a_c = 0.711
    a_a = 23.7
    a_p = 11.18
    delta = 0.0
    if Z % 2 == 0 and N % 2 == 0:
        delta = a_p / A**0.5
    elif Z % 2 == 1 and N % 2 == 1:
        delta = -a_p / A**0.5
    B_vol = a_v * A
    B_surf = a_s * A**(2.0/3.0)
    B_coul = a_c * Z * (Z - 1) / A**(1.0/3.0)
    B_asym = a_a * (N - Z)**2 / A
    B_pair = delta
    B_total = B_vol - B_surf - B_coul - B_asym + B_pair
    B_per_A = B_total / A
    return {
        'result': f'B = {B_total:.4f} MeV, B/A = {B_per_A:.4f} MeV/nucleon',
        'details': {'Z': Z, 'N': N, 'A': A, 'volume_term': B_vol, 'surface_term': B_surf, 'coulomb_term': B_coul, 'asymmetry_term': B_asym, 'pairing_term': B_pair, 'B_total_MeV': B_total, 'B_per_A': B_per_A},
        'unit': 'MeV'
    }

def calc_nuclear_radius(A: int = 56, r0: float = 1.2e-15) -> dict:
    """Nuclear radius: R = r0 * A^(1/3)."""
    R = r0 * A**(1.0/3.0)
    V = (4.0/3.0) * np.pi * R**3
    density = A / V
    return {
        'result': f'R = {R:.4e} m = {R*1e15:.4f} fm',
        'details': {'A': A, 'r0_m': r0, 'radius_m': R, 'radius_fm': R * 1e15, 'volume_m3': V, 'nucleon_density': density},
        'unit': 'm'
    }

def calc_nuclear_density() -> dict:
    """Nuclear density (approximately constant): rho ~ 2.3e17 kg/m^3."""
    r0 = 1.2e-15
    m_nucleon = 1.660539066e-27
    V_A1 = (4.0/3.0) * np.pi * r0**3
    density = m_nucleon / V_A1
    return {
        'result': f'rho_nuclear = {density:.4e} kg/m^3',
        'details': {'r0_m': r0, 'nucleon_mass_kg': m_nucleon, 'density_kg_m3': density},
        'unit': 'kg/m^3'
    }

def calc_radioactive_decay(N0: float = 1e6, half_life: float = 3.0, time: float = 5.0, unit: str = 's') -> dict:
    """Radioactive decay: N(t) = N0 * exp(-lambda*t), lambda = ln(2)/t_1/2."""
    lam = np.log(2.0) / half_life
    N_t = N0 * np.exp(-lam * time)
    activity = lam * N_t
    return {
        'result': f'N({time} {unit}) = {N_t:.4e}, A = {activity:.4e} Bq',
        'details': {'N0': N0, 'half_life': half_life, 'time': time, 'lambda': lam, 'N_t': N_t, 'activity_Bq': activity, 'time_unit': unit},
        'unit': 'dimensionless'
    }

def calc_half_life_from_lambda(decay_constant: float = 0.1) -> dict:
    """Half-life from decay constant: t_1/2 = ln(2) / lambda."""
    t_half = np.log(2.0) / decay_constant
    mean_lifetime = 1.0 / decay_constant
    return {
        'result': f't_1/2 = {t_half:.6f}, tau_mean = {mean_lifetime:.6f}',
        'details': {'decay_constant': decay_constant, 'half_life': t_half, 'mean_lifetime': mean_lifetime},
        'unit': 's'
    }

def calc_activity(N: float = 1e20, half_life: float = 1.28e9) -> dict:
    """Activity: A = lambda * N, with half-life in years."""
    t_half_seconds = half_life * 365.25 * 24 * 3600
    lam = np.log(2.0) / t_half_seconds
    A = lam * N
    A_Ci = A / 3.7e10
    return {
        'result': f'A = {A:.4e} Bq = {A_Ci:.4e} Ci',
        'details': {'N': N, 'half_life_years': half_life, 'decay_constant': lam, 'activity_Bq': A, 'activity_Ci': A_Ci},
        'unit': 'Bq'
    }

def calc_decay_chain(lambda_chain: list = None, N0: float = 1e6, times: list = None) -> dict:
    """Bateman equations for serial decay chain N1 -> N2 -> N3 -> ..."""
    if lambda_chain is None:
        lambda_chain = [0.1, 0.05, 0.02]
    if times is None:
        times = [0, 5, 10, 15, 20]
    lam = np.array(lambda_chain)
    n_species = len(lam)
    results = []
    for t in times:
        N = np.zeros(n_species)
        prod = 1.0
        for i in range(n_species):
            if i == 0:
                N[i] = N0 * np.exp(-lam[i] * t)
            else:
                sum_terms = 0.0
                for j in range(i):
                    denominator = 1.0
                    for k in range(i + 1):
                        if k != j:
                            denominator *= (lam[k] - lam[j])
                    sum_terms += np.exp(-lam[j] * t) / (denominator + 1e-40)
                coeff_prod = 1.0
                for k in range(i):
                    coeff_prod *= lam[k]
                N[i] = N0 * coeff_prod * sum_terms
        results.append({'time': t, 'N': N.tolist()})
    final_N = results[-1]['N']
    return {
        'result': f'N at t={times[-1]}: {[f"{n:.2e}" for n in final_N]}',
        'details': {'lambda_chain': lambda_chain, 'N0': N0, 'times': times, 'populations': results},
        'unit': 'dimensionless'
    }

def calc_carbon_dating(c14_ratio: float = 0.5) -> dict:
    """Carbon-14 dating: t = (t_1/2/ln(2)) * ln(N0/N) with t_1/2 = 5730 yr."""
    t_half = 5730.0
    if c14_ratio <= 0 or c14_ratio >= 1:
        return {
            'result': 'Ratio must be 0 < N/N0 < 1',
            'details': {'c14_ratio': c14_ratio},
            'unit': 'years'
        }
    t_age = t_half * np.log(1.0 / c14_ratio) / np.log(2.0)
    return {
        'result': f'Age = {t_age:.2f} years',
        'details': {'c14_ratio': c14_ratio, 'half_life_years': t_half, 'age_years': t_age},
        'unit': 'years'
    }

def calc_q_value(m_initial: float = 238.0507882, m_final_sum: float = 234.043601 + 4.00260325413) -> dict:
    """Q-value for nuclear reaction: Q = (m_initial - m_final)*931.494 MeV."""
    mass_difference = m_initial - m_final_sum
    Q_MeV = mass_difference * 931.49410242
    reaction_type = 'exothermic' if Q_MeV > 0 else 'endothermic'
    return {
        'result': f'Q = {Q_MeV:.4f} MeV ({reaction_type})',
        'details': {'m_initial_amu': m_initial, 'm_final_amu': m_final_sum, 'mass_diff_amu': mass_difference, 'Q_MeV': Q_MeV, 'type': reaction_type},
        'unit': 'MeV'
    }

def calc_fission_energy(m_parent: float = 235.0439299, m_daughter1: float = 93.915361, m_daughter2: float = 137.905247, n_emitted: int = 2) -> dict:
    """Fission energy release from mass difference."""
    m_n = 1.00866491588
    m_products = m_daughter1 + m_daughter2 + n_emitted * m_n
    delta_m = m_parent - m_products
    E_MeV = delta_m * 931.49410242
    E_J = E_MeV * 1.602176634e-13
    return {
        'result': f'Fission energy = {E_MeV:.4f} MeV = {E_J:.4e} J',
        'details': {'parent_mass': m_parent, 'daughter1_mass': m_daughter1, 'daughter2_mass': m_daughter2, 'n_emitted': n_emitted, 'delta_m_amu': delta_m, 'energy_MeV': E_MeV, 'energy_J': E_J},
        'unit': 'MeV'
    }

def calc_fusion_energy(reaction: str = 'DT') -> dict:
    """Fusion energy release for common reactions."""
    reactions = {
        'DT': {'products': 'He-4 + n', 'Q_MeV': 17.59, 'cross_section_peak': 5.0},
        'DD_n': {'products': 'He-3 + n', 'Q_MeV': 3.27},
        'DD_p': {'products': 'T + p', 'Q_MeV': 4.03},
        'DHe3': {'products': 'He-4 + p', 'Q_MeV': 18.35},
        'pB11': {'products': '3 He-4', 'Q_MeV': 8.68},
        'TT': {'products': 'He-4 + 2n', 'Q_MeV': 11.33},
    }
    data = reactions.get(reaction, {'products': 'unknown', 'Q_MeV': 0.0})
    Q_J = data['Q_MeV'] * 1.602176634e-13
    return {
        'result': f'{reaction} -> {data["products"]}: Q = {data["Q_MeV"]:.2f} MeV',
        'details': {'reaction': reaction, 'products': data['products'], 'Q_MeV': data['Q_MeV'], 'Q_J': Q_J},
        'unit': 'MeV'
    }

def calc_lawson_criterion(T_keV: float = 20.0, efficiency: float = 0.33) -> dict:
    """Lawson criterion: n*tau_E*T >= 3e21 keV*s/m^3 (DT)."""
    required_triple = 3e21
    triple_product = required_triple / efficiency
    return {
        'result': f'n*tau_E >= {triple_product:.2e} m^(-3)*s for T_i = {T_keV} keV',
        'details': {'T_keV': T_keV, 'efficiency': efficiency, 'required_ntT': required_triple, 'required_n_tau': triple_product},
        'unit': 'm^(-3)*s'
    }

def calc_cross_section_from_radius(radius: float = 1.2e-15) -> dict:
    """Geometric cross section: sigma = pi * R^2."""
    sigma = np.pi * radius**2
    sigma_barn = sigma * 1e28
    return {
        'result': f'sigma = {sigma:.4e} m^2 = {sigma_barn:.4f} barn',
        'details': {'radius_m': radius, 'sigma_m2': sigma, 'sigma_barn': sigma_barn},
        'unit': 'm^2'
    }

def calc_reaction_rate(target_density: float = 1e28, beam_flux: float = 1e13, cross_section_barn: float = 1.0) -> dict:
    """Reaction rate: R = n_target * phi * sigma."""
    sigma_m2 = cross_section_barn * 1e-28
    R = target_density * beam_flux * sigma_m2
    return {
        'result': f'Reaction rate R = {R:.4e} s^(-1)*m^(-3)',
        'details': {'target_density': target_density, 'beam_flux': beam_flux, 'cross_section_barn': cross_section_barn, 'cross_section_m2': sigma_m2, 'rate': R},
        'unit': 's^(-1)*m^(-3)'
    }

def calc_relativistic_momentum(mass_kg: float = 1.6726e-27, velocity: float = 0.9 * 2.99792458e8) -> dict:
    """Relativistic momentum: p = gamma * m * v."""
    c = 2.99792458e8
    beta = velocity / c
    if beta >= 1.0:
        return {
            'result': f'beta = {beta:.4f} >= 1, invalid',
            'details': {},
            'unit': 'kg*m/s'
        }
    gamma = 1.0 / np.sqrt(1.0 - beta**2)
    p = gamma * mass_kg * velocity
    E_kin = (gamma - 1.0) * mass_kg * c**2
    E_kin_MeV = E_kin / 1.602176634e-13
    return {
        'result': f'p = {p:.4e} kg*m/s, E_kin = {E_kin_MeV:.4f} MeV',
        'details': {'mass_kg': mass_kg, 'beta': beta, 'gamma': gamma, 'momentum': p, 'kinetic_energy_MeV': E_kin_MeV},
        'unit': 'kg*m/s'
    }

def calc_relativistic_energy(mass_kg: float = 9.11e-31, momentum_kgms: float = 1e-21) -> dict:
    """Relativistic energy: E^2 = (pc)^2 + (mc^2)^2."""
    c = 2.99792458e8
    rest_energy = mass_kg * c**2
    E = np.sqrt((momentum_kgms * c)**2 + rest_energy**2)
    E_kin = E - rest_energy
    E_MeV = E / 1.602176634e-13
    E_kin_MeV = E_kin / 1.602176634e-13
    return {
        'result': f'E_total = {E_MeV:.4f} MeV, E_kin = {E_kin_MeV:.4f} MeV',
        'details': {'mass_kg': mass_kg, 'momentum': momentum_kgms, 'rest_energy_MeV': rest_energy / 1.602176634e-13, 'total_E_MeV': E_MeV, 'kinetic_E_MeV': E_kin_MeV},
        'unit': 'MeV'
    }

def calc_invariant_mass(particles: list = None) -> dict:
    """Invariant mass: M^2 = (sum(E_i))^2 - |sum(p_i)|^2."""
    if particles is None:
        particles = [
            {'E': 100.0, 'px': 50.0, 'py': 0.0, 'pz': 0.0},
            {'E': 100.0, 'px': -50.0, 'py': 0.0, 'pz': 0.0},
        ]
    total_E = sum(p['E'] for p in particles)
    total_px = sum(p['px'] for p in particles)
    total_py = sum(p['py'] for p in particles)
    total_pz = sum(p['pz'] for p in particles)
    M_sq = total_E**2 - (total_px**2 + total_py**2 + total_pz**2)
    if M_sq < 0:
        M = 0.0
    else:
        M = np.sqrt(M_sq)
    return {
        'result': f'Invariant mass M = {M:.4f} GeV/c^2',
        'details': {'particles': particles, 'total_E': total_E, 'total_P': [total_px, total_py, total_pz], 'M_sq': M_sq, 'invariant_mass': M},
        'unit': 'GeV/c^2'
    }

def calc_decay_width_from_lifetime(tau: float = 2.2e-6) -> dict:
    """Decay width: Gamma = hbar / tau."""
    hbar = 6.582119569e-16
    Gamma_eV = hbar / tau
    Gamma_MeV = Gamma_eV / 1e6
    return {
        'result': f'Gamma = {Gamma_MeV:.6e} MeV',
        'details': {'lifetime_s': tau, 'hbar_eVs': hbar, 'Gamma_eV': Gamma_eV, 'Gamma_MeV': Gamma_MeV},
        'unit': 'MeV'
    }

def calc_branching_ratio(partial_widths: list = None) -> dict:
    """Branching ratios from partial decay widths."""
    if partial_widths is None:
        partial_widths = [0.3, 0.5, 0.2]
    widths = np.array(partial_widths)
    total = np.sum(widths)
    ratios = widths / total if total > 0 else widths
    return {
        'result': f'BR = {[f"{r:.4f}" for r in ratios]}',
        'details': {'partial_widths': partial_widths, 'total_width': float(total), 'branching_ratios': ratios.tolist()},
        'unit': 'dimensionless'
    }

def calc_luminosity_integrated(n_events: float = 1000.0, cross_section_barn: float = 1.0) -> dict:
    """Integrated luminosity: L_int = N_events / sigma."""
    sigma_m2 = cross_section_barn * 1e-28
    L_int = n_events / sigma_m2
    L_int_inv_fb = L_int * 1e-43
    return {
        'result': f'L_int = {L_int:.4e} m^(-2) = {L_int_inv_fb:.4f} fb^(-1)',
        'details': {'n_events': n_events, 'cross_section_barn': cross_section_barn, 'L_int_m2': L_int, 'L_int_inv_fb': L_int_inv_fb},
        'unit': 'm^(-2)'
    }

def calc_luminosity_collider(n_bunches: float = 2808, n_particles: float = 1.15e11, f_rev: float = 11245, sigma_x: float = 16e-6, sigma_y: float = 16e-6) -> dict:
    """Luminosity: L = (n_b * N1 * N2 * f_rev) / (4*pi*sigma_x*sigma_y)."""
    L = n_bunches * n_particles**2 * f_rev / (4.0 * np.pi * sigma_x * sigma_y)
    L_cm2s = L * 1e-4
    return {
        'result': f'L = {L:.4e} m^(-2)*s^(-1) = {L_cm2s:.4e} cm^(-2)*s^(-1)',
        'details': {'n_bunches': n_bunches, 'n_particles_per_bunch': n_particles, 'f_rev_Hz': f_rev, 'sigma_x_m': sigma_x, 'sigma_y_m': sigma_y, 'luminosity': L},
        'unit': 'm^(-2)*s^(-1)'
    }

def calc_ckm_rotation(theta12: float = 0.226, theta23: float = 0.042, theta13: float = 0.0039, delta_cp: float = 1.14) -> dict:
    """CKM matrix from standard parametrization angles."""
    c12 = np.cos(theta12); s12 = np.sin(theta12)
    c23 = np.cos(theta23); s23 = np.sin(theta23)
    c13 = np.cos(theta13); s13 = np.sin(theta13)
    V = np.array([
        [c12*c13, s12*c13, s13*np.exp(-1j*delta_cp)],
        [-s12*c23 - c12*s23*s13*np.exp(1j*delta_cp), c12*c23 - s12*s23*s13*np.exp(1j*delta_cp), s23*c13],
        [s12*s23 - c12*c23*s13*np.exp(1j*delta_cp), -c12*s23 - s12*c23*s13*np.exp(1j*delta_cp), c23*c13]
    ])
    magnitudes = np.abs(V)
    unitarity_check = np.sum(np.abs(V @ np.conj(V).T - np.eye(3)))
    return {
        'result': f'|V_ud|={magnitudes[0,0]:.4f}, |V_us|={magnitudes[0,1]:.4f}, |V_ub|={magnitudes[0,2]:.4f}',
        'details': {'theta12': theta12, 'theta23': theta23, 'theta13': theta13, 'delta_cp': delta_cp, 'CKM_matrix': V.tolist(), 'magnitudes': magnitudes.tolist(), 'unitarity_deviation': unitarity_check},
        'unit': 'dimensionless'
    }

def calc_beta_decay_Q(parent_Z: int = 6, parent_N: int = 14, daughter_Z: int = 7, daughter_N: int = 13) -> dict:
    """Q-value for beta decay using approximate masses."""
    m_n = 1.00866491588
    m_p = 1.00727646688
    m_parent = parent_Z * m_p + parent_N * m_n - 0.008 * (parent_Z + parent_N) / 931.494
    m_daughter = daughter_Z * m_p + daughter_N * m_n - 0.008 * (daughter_Z + daughter_N) / 931.494
    if daughter_Z == parent_Z + 1:
        Q_MeV = (m_parent - m_daughter) * 931.49410242
    elif daughter_Z == parent_Z - 1:
        Q_MeV = (m_parent - m_daughter - 2 * 0.00054857990907) * 931.49410242
    else:
        Q_MeV = (m_parent - m_daughter) * 931.49410242
    return {
        'result': f'Q_beta = {Q_MeV:.4f} MeV',
        'details': {'parent_Z': parent_Z, 'parent_N': parent_N, 'daughter_Z': daughter_Z, 'daughter_N': daughter_N, 'm_parent_amu': m_parent, 'm_daughter_amu': m_daughter, 'Q_MeV': Q_MeV},
        'unit': 'MeV'
    }

def calc_alpha_decay_energy(parent_A: int = 238, parent_Z: int = 92) -> dict:
    """Alpha decay Q-value from semi-empirical masses."""
    daughter_A = parent_A - 4
    daughter_Z = parent_Z - 2
    m_parent = parent_Z * 1.00727646688 + (parent_A - parent_Z) * 1.00866491588
    m_parent -= 0.008 * parent_A / 931.494
    m_daughter = daughter_Z * 1.00727646688 + (daughter_A - daughter_Z) * 1.00866491588
    m_daughter -= 0.008 * daughter_A / 931.494
    m_alpha = 4.00260325413
    Q_MeV = (m_parent - m_daughter - m_alpha) * 931.49410242
    return {
        'result': f'Q_alpha = {Q_MeV:.4f} MeV',
        'details': {'parent_A': parent_A, 'parent_Z': parent_Z, 'daughter_A': daughter_A, 'daughter_Z': daughter_Z, 'Q_MeV': Q_MeV},
        'unit': 'MeV'
    }

def calc_neutron_proton_ratio(Z: int = 20, N: int = 20) -> dict:
    """N/Z ratio and comparison to valley of stability."""
    ratio = N / Z if Z > 0 else float('inf')
    A = Z + N
    stable_approx = 1.0 + 0.015 * A**(2.0/3.0)
    return {
        'result': f'N/Z = {ratio:.4f}, valley approx = {stable_approx:.4f}',
        'details': {'Z': Z, 'N': N, 'A': A, 'N_Z_ratio': ratio, 'valley_stability_N_Z': stable_approx},
        'unit': 'dimensionless'
    }

def calc_threshold_energy(projectile_mass: float = 1.00866491588, target_mass: float = 235.0439299, Q_MeV: float = -5.0) -> dict:
    """Threshold energy for endothermic reaction: E_th = -Q*(m_p+m_t)/m_t."""
    if Q_MeV >= 0:
        E_th = 0.0
    else:
        E_th = -Q_MeV * (projectile_mass + target_mass) / target_mass
    return {
        'result': f'E_threshold = {E_th:.4f} MeV',
        'details': {'projectile_mass_amu': projectile_mass, 'target_mass_amu': target_mass, 'Q_MeV': Q_MeV, 'threshold_MeV': E_th},
        'unit': 'MeV'
    }

def calc_rutherford_scattering(Z1: int = 2, Z2: int = 79, E_MeV: float = 5.0, theta_deg: float = 30.0) -> dict:
    """Rutherford differential cross section."""
    e = 1.602176634e-19
    epsilon_0 = 8.8541878128e-12
    E_J = E_MeV * 1e6 * e
    theta = np.radians(theta_deg)
    sin4 = np.sin(theta / 2.0)**4
    if sin4 < 1e-30:
        dsig_dOmega = float('inf')
    else:
        prefactor = (Z1 * Z2 * e**2 / (16.0 * np.pi * epsilon_0 * E_J))**2
        dsig_dOmega = prefactor / sin4
    dsig_barn = dsig_dOmega * 1e28
    return {
        'result': f'dsigma/dOmega = {dsig_dOmega:.4e} m^2/sr = {dsig_barn:.4f} barn/sr',
        'details': {'Z1': Z1, 'Z2': Z2, 'E_MeV': E_MeV, 'theta_deg': theta_deg, 'dSigma_dOmega_m2': dsig_dOmega, 'dSigma_dOmega_barn': dsig_barn},
        'unit': 'm^2/sr'
    }

def calc_breit_wigner(s: float = 1000.0, M: float = 91.2, Gamma: float = 2.5) -> dict:
    """Relativistic Breit-Wigner cross section: sigma ~ 1/((s-M^2)^2 + M^2*Gamma^2)."""
    denominator = (s - M**2)**2 + M**2 * Gamma**2
    if denominator < 1e-40:
        sigma_norm = 1.0
    else:
        sigma_norm = 1.0 / denominator
    return {
        'result': f'sigma(norm) at sqrt(s)={np.sqrt(s):.2f} GeV = {sigma_norm:.6e}',
        'details': {'s_GeV2': s, 'M_GeV': M, 'Gamma_GeV': Gamma, 'peak': 1.0/(M**2*Gamma**2), 'sigma_norm': sigma_norm},
        'unit': 'dimensionless'
    }

def calc_bethe_bloch(beta_gamma: float = 3.0, Z_incident: int = 1, Z_material: int = 14, A_material: float = 28.0, I_eV: float = 173.0, density: float = 2.33) -> dict:
    """Bethe-Bloch stopping power dE/dx (simplified)."""
    K = 0.307075
    beta = beta_gamma / np.sqrt(1.0 + beta_gamma**2)
    gamma = beta_gamma / beta if beta > 0 else 1.0
    W_max = 2.0 * 0.511 * beta**2 * gamma**2 / (1.0 + 2.0 * gamma * 0.511 / (0.511 * 938.0) + (0.511 / (0.511 * 938.0))**2)
    I_J = I_eV * 1.602176634e-19
    term1 = 0.5 * np.log(2.0 * 0.511e6 * beta**2 * gamma**2 * W_max / I_eV**2)
    term2 = beta**2
    dedx_MeV_cm2_g = K * Z_incident**2 * Z_material / A_material * (1.0 / beta**2) * (term1 - term2)
    dedx_MeV_cm = dedx_MeV_cm2_g * density
    return {
        'result': f'dE/dx = {dedx_MeV_cm2_g:.4f} MeV*cm^2/g = {dedx_MeV_cm:.4f} MeV/cm',
        'details': {'beta_gamma': beta_gamma, 'beta': beta, 'gamma': gamma, 'Z_incident': Z_incident, 'Z_material': Z_material, 'A_material': A_material, 'I_eV': I_eV, 'dEdx_mass': dedx_MeV_cm2_g, 'dEdx_linear': dedx_MeV_cm},
        'unit': 'MeV*cm^2/g'
    }

def calc_neutron_moderation(E_initial_eV: float = 2e6, A_target: float = 1.0, n_collisions: int = 18) -> dict:
    """Neutron moderation: E_n = E_0 * ((A^2+1)/(A+1)^2)^n."""
    alpha = ((A_target - 1.0) / (A_target + 1.0))**2
    xi = 1.0 + alpha * np.log(alpha) / (1.0 - alpha) if alpha > 0 else 1.0
    E_n = E_initial_eV * ((A_target**2 + 1.0) / (A_target + 1.0)**2)**n_collisions
    avg_collisions = np.log(E_initial_eV / 0.025) / xi
    return {
        'result': f'E after {n_collisions} collisions = {E_n:.4f} eV, ~{avg_collisions:.0f} collisions to thermal',
        'details': {'E_initial_eV': E_initial_eV, 'A_target': A_target, 'n_collisions': n_collisions, 'E_final_eV': E_n, 'avg_lethargy': xi, 'collisions_to_thermal': avg_collisions},
        'unit': 'eV'
    }

def calc_mass_parabolas(Z: int = 26, A_range: int = 5) -> dict:
    """Mass parabolas for isobars at fixed A."""
    A_center = Z + 30
    m_p = 1.00727646688
    m_n = 1.00866491588
    a_c = 0.711
    a_a = 23.7
    a_p = 11.18
    parabolas = []
    for A in range(A_center - A_range, A_center + A_range + 1):
        Z0 = A / (2.0 + 0.0154 * A**(2.0/3.0))
        parabolas.append({'A': A, 'Z_stable_approx': round(Z0, 2)})
    return {
        'result': f'Stable Z approx for A around {A_center}: {parabolas}',
        'details': {'input_Z': Z, 'A_center': A_center, 'parabolas': parabolas},
        'unit': 'dimensionless'
    }

def calc_pair_production_threshold() -> dict:
    """Pair production threshold: E_gamma >= 2*m_e*c^2 = 1.022 MeV."""
    m_e_c2 = 0.511
    threshold = 2.0 * m_e_c2
    return {
        'result': f'Pair production threshold = {threshold:.3f} MeV',
        'details': {'electron_rest_mass_MeV': m_e_c2, 'threshold_MeV': threshold},
        'unit': 'MeV'
    }

def calc_compton_edge(E_gamma_MeV: float = 0.662) -> dict:
    """Compton edge: E_e_max = E_gamma * (2*E_gamma/(m_e*c^2)) / (1 + 2*E_gamma/(m_e*c^2))."""
    m_c2 = 0.511
    x = E_gamma_MeV / m_c2
    E_edge = E_gamma_MeV * (2.0 * x) / (1.0 + 2.0 * x)
    E_backscatter = E_gamma_MeV / (1.0 + 2.0 * x)
    return {
        'result': f'Compton edge = {E_edge:.4f} MeV, backscatter peak = {E_backscatter:.4f} MeV',
        'details': {'E_gamma_MeV': E_gamma_MeV, 'E_electron_max_MeV': E_edge, 'E_backscatter_MeV': E_backscatter},
        'unit': 'MeV'
    }

def calc_photoelectric_cross_section(Z: int = 82, E_gamma_MeV: float = 0.1) -> dict:
    """Approximate photoelectric cross section: sigma_pe ~ Z^5 / E^(7/2)."""
    sigma_approx = Z**5 / (E_gamma_MeV**3.5 + 1e-30)
    return {
        'result': f'sigma_pe(approx) proportional to = {sigma_approx:.2e} (arbitrary units)',
        'details': {'Z': Z, 'E_gamma_MeV': E_gamma_MeV, 'sigma_approx': sigma_approx},
        'unit': 'arbitrary'
    }

def calc_shell_model_energy(j: float = 1.5, l: int = 1) -> dict:
    """Nuclear shell model spin-orbit: j = l +/- 1/2 energy splitting."""
    hbar = 1.054571817e-34
    s_dot_l = 0.5 * (j * (j + 1.0) - l * (l + 1.0) - 0.75)
    return {
        'result': f'j={j}, l={l}: <s*l> = {s_dot_l:.4f} hbar^2',
        'details': {'j': j, 'l': l, 's_dot_l': s_dot_l},
        'unit': 'dimensionless'
    }

def calc_magic_numbers() -> dict:
    """Nuclear magic numbers: 2, 8, 20, 28, 50, 82, 126."""
    magic = [2, 8, 20, 28, 50, 82, 126]
    return {
        'result': f'Nuclear magic numbers: {magic}',
        'details': {'magic_numbers': magic, 'count': len(magic)},
        'unit': 'dimensionless'
    }

COMMANDS = {
    'binding_energy': {'func': calc_nuclear_binding_energy, 'params': ['Z', 'N'], 'desc': 'Nuclear binding energy from mass defect'},
    'semi_empirical_mass': {'func': calc_semi_empirical_mass, 'params': ['Z', 'N'], 'desc': 'Bethe-Weizsacker semi-empirical mass formula'},
    'nuclear_radius': {'func': calc_nuclear_radius, 'params': ['A', 'r0'], 'desc': 'Nuclear radius R = r0*A^(1/3)'},
    'nuclear_density': {'func': calc_nuclear_density, 'params': [], 'desc': 'Constant nuclear matter density'},
    'radioactive_decay': {'func': calc_radioactive_decay, 'params': ['N0', 'half_life', 'time', 'unit'], 'desc': 'Radioactive decay N(t) = N0*e^(-lambda*t)'},
    'half_life': {'func': calc_half_life_from_lambda, 'params': ['decay_constant'], 'desc': 'Half-life from decay constant'},
    'activity': {'func': calc_activity, 'params': ['N', 'half_life'], 'desc': 'Radioactive activity A = lambda*N'},
    'decay_chain': {'func': calc_decay_chain, 'params': ['lambda_chain', 'N0', 'times'], 'desc': 'Bateman equations for serial decay chain'},
    'carbon_dating': {'func': calc_carbon_dating, 'params': ['c14_ratio'], 'desc': 'Carbon-14 dating age calculation'},
    'q_value': {'func': calc_q_value, 'params': ['m_initial', 'm_final_sum'], 'desc': 'Q-value for nuclear reaction'},
    'fission_energy': {'func': calc_fission_energy, 'params': ['m_parent', 'm_daughter1', 'm_daughter2', 'n_emitted'], 'desc': 'Nuclear fission energy release'},
    'fusion_energy': {'func': calc_fusion_energy, 'params': ['reaction'], 'desc': 'Fusion energy for common reactions'},
    'lawson_criterion': {'func': calc_lawson_criterion, 'params': ['T_keV', 'efficiency'], 'desc': 'Lawson criterion for fusion'},
    'cross_section': {'func': calc_cross_section_from_radius, 'params': ['radius'], 'desc': 'Geometric nuclear cross section'},
    'reaction_rate': {'func': calc_reaction_rate, 'params': ['target_density', 'beam_flux', 'cross_section_barn'], 'desc': 'Nuclear reaction rate'},
    'relativistic_momentum': {'func': calc_relativistic_momentum, 'params': ['mass_kg', 'velocity'], 'desc': 'Relativistic momentum p = gamma*m*v'},
    'relativistic_energy': {'func': calc_relativistic_energy, 'params': ['mass_kg', 'momentum_kgms'], 'desc': 'Relativistic energy E^2 = (pc)^2 + (mc^2)^2'},
    'invariant_mass': {'func': calc_invariant_mass, 'params': ['particles'], 'desc': 'Invariant mass of particle system'},
    'decay_width': {'func': calc_decay_width_from_lifetime, 'params': ['tau'], 'desc': 'Decay width Gamma = hbar/tau'},
    'branching_ratio': {'func': calc_branching_ratio, 'params': ['partial_widths'], 'desc': 'Branching ratios from partial widths'},
    'luminosity_integrated': {'func': calc_luminosity_integrated, 'params': ['n_events', 'cross_section_barn'], 'desc': 'Integrated luminosity from event count'},
    'luminosity_collider': {'func': calc_luminosity_collider, 'params': ['n_bunches', 'n_particles', 'f_rev', 'sigma_x', 'sigma_y'], 'desc': 'Collider luminosity from beam parameters'},
    'ckm_matrix': {'func': calc_ckm_rotation, 'params': ['theta12', 'theta23', 'theta13', 'delta_cp'], 'desc': 'CKM quark mixing matrix'},
    'beta_decay_Q': {'func': calc_beta_decay_Q, 'params': ['parent_Z', 'parent_N', 'daughter_Z', 'daughter_N'], 'desc': 'Beta decay Q-value'},
    'alpha_decay_Q': {'func': calc_alpha_decay_energy, 'params': ['parent_A', 'parent_Z'], 'desc': 'Alpha decay Q-value'},
    'nz_ratio': {'func': calc_neutron_proton_ratio, 'params': ['Z', 'N'], 'desc': 'N/Z stability ratio'},
    'threshold_energy': {'func': calc_threshold_energy, 'params': ['projectile_mass', 'target_mass', 'Q_MeV'], 'desc': 'Threshold energy for endothermic reaction'},
    'rutherford': {'func': calc_rutherford_scattering, 'params': ['Z1', 'Z2', 'E_MeV', 'theta_deg'], 'desc': 'Rutherford scattering differential cross section'},
    'breit_wigner': {'func': calc_breit_wigner, 'params': ['s', 'M', 'Gamma'], 'desc': 'Relativistic Breit-Wigner resonance'},
    'bethe_bloch': {'func': calc_bethe_bloch, 'params': ['beta_gamma', 'Z_incident', 'Z_material', 'A_material', 'I_eV', 'density'], 'desc': 'Bethe-Bloch stopping power'},
    'neutron_moderation': {'func': calc_neutron_moderation, 'params': ['E_initial_eV', 'A_target', 'n_collisions'], 'desc': 'Neutron moderation energy loss'},
    'mass_parabolas': {'func': calc_mass_parabolas, 'params': ['Z', 'A_range'], 'desc': 'Isobaric mass parabolas'},
    'pair_production': {'func': calc_pair_production_threshold, 'params': [], 'desc': 'Pair production threshold energy'},
    'compton_edge': {'func': calc_compton_edge, 'params': ['E_gamma_MeV'], 'desc': 'Compton edge energy'},
    'photoelectric': {'func': calc_photoelectric_cross_section, 'params': ['Z', 'E_gamma_MeV'], 'desc': 'Approximate photoelectric cross section'},
    'shell_model': {'func': calc_shell_model_energy, 'params': ['j', 'l'], 'desc': 'Nuclear shell model spin-orbit coupling'},
    'magic_numbers': {'func': calc_magic_numbers, 'params': [], 'desc': 'Nuclear magic numbers'}
}
