"""
Quantum Mechanics - Numerical Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_de_broglie_wavelength(mass_kg: float = 9.11e-31, velocity: float = 1e6) -> dict:
    """Compute de Broglie wavelength lambda = h/p."""
    h = 6.62607015e-34
    p = mass_kg * velocity
    wavelength = h / p
    wavelength_nm = wavelength * 1e9
    return {
        'result': f'lambda = {wavelength:.4e} m ({wavelength_nm:.4f} nm)',
        'details': {'mass_kg': mass_kg, 'velocity': velocity, 'momentum': p, 'wavelength_m': wavelength, 'wavelength_nm': wavelength_nm},
        'unit': 'm'
    }

def calc_probability_density(psi_real: float = 1.0, psi_imag: float = 0.0) -> dict:
    """Compute probability density |psi|^2 = |Re(psi)|^2 + |Im(psi)|^2."""
    prob = psi_real**2 + psi_imag**2
    return {
        'result': f'|psi|^2 = {prob:.6f}',
        'details': {'psi_real': psi_real, 'psi_imag': psi_imag, 'probability_density': prob},
        'unit': 'm^(-1) or dimensionless'
    }

def calc_normalization_constant(wavefunction_samples: list = None) -> dict:
    """Normalize a discretized wavefunction: N = 1/sqrt(sum(|psi_i|^2)*dx)."""
    if wavefunction_samples is None:
        wavefunction_samples = [1.0, 2.0, 1.0, 0.5]
    samples = np.array(wavefunction_samples, dtype=complex)
    dx = 1.0
    norm_sq = np.sum(np.abs(samples)**2) * dx
    N = 1.0 / np.sqrt(norm_sq)
    normalized = samples * N
    return {
        'result': f'N = {N:.6f}',
        'details': {'norm_sq': norm_sq, 'normalization_constant': N, 'normalized_wavefunction': normalized.tolist()},
        'unit': 'dimensionless'
    }

def calc_expectation_value(x_values: list = None, psi_values: list = None) -> dict:
    """Compute expectation value <A> = integral(psi* A psi) dx for operator A."""
    if x_values is None:
        x_values = np.linspace(0, 1, 100).tolist()
    if psi_values is None:
        psi_values = (np.sin(np.pi * np.linspace(0, 1, 100))).tolist()
    x_arr = np.array(x_values)
    psi_arr = np.array(psi_values, dtype=complex)
    dx = x_arr[1] - x_arr[0]
    prob_density = np.abs(psi_arr)**2
    exp_x = np.trapz(prob_density * x_arr, x_arr)
    exp_x2 = np.trapz(prob_density * x_arr**2, x_arr)
    var_x = exp_x2 - exp_x**2
    delta_x = np.sqrt(max(var_x, 0))
    return {
        'result': f'<x> = {exp_x:.6f}, Delta_x = {delta_x:.6f}',
        'details': {'expectation_x': exp_x, 'expectation_x2': exp_x2, 'variance': var_x, 'uncertainty_x': delta_x},
        'unit': 'm'
    }

def calc_uncertainty_principle(delta_x: float = 1e-10, delta_p: float = 1e-24) -> dict:
    """Check Heisenberg uncertainty principle: Delta_x * Delta_p >= hbar/2."""
    hbar = 1.054571817e-34
    product = delta_x * delta_p
    limit = hbar / 2.0
    satisfied = product >= limit
    ratio = product / limit
    return {
        'result': f'Dx*Dp = {product:.4e} >= hbar/2 = {limit:.4e} => {satisfied}',
        'details': {'delta_x': delta_x, 'delta_p': delta_p, 'product': product, 'hbar_over_2': limit, 'satisfied': satisfied, 'ratio': ratio},
        'unit': 'J*s'
    }

def calc_uncertainty_energy_time(delta_e: float = 1e-19, delta_t: float = 1e-15) -> dict:
    """Check energy-time uncertainty: Delta_E * Delta_t >= hbar/2."""
    hbar = 1.054571817e-34
    product = delta_e * delta_t
    limit = hbar / 2.0
    satisfied = product >= limit
    return {
        'result': f'DE*Dt = {product:.4e} >= hbar/2 = {limit:.4e} => {satisfied}',
        'details': {'delta_e': delta_e, 'delta_t': delta_t, 'product': product, 'hbar_over_2': limit, 'satisfied': satisfied},
        'unit': 'J*s'
    }

def calc_infinite_well_energy(n: int = 1, L: float = 1e-9, m: float = 9.11e-31) -> dict:
    """Energy levels of infinite square well: E_n = n^2 * pi^2 * hbar^2 / (2*m*L^2)."""
    hbar = 1.054571817e-34
    E_n = n**2 * np.pi**2 * hbar**2 / (2.0 * m * L**2)
    E_eV = E_n / 1.602176634e-19
    return {
        'result': f'E_{n} = {E_n:.4e} J = {E_eV:.6f} eV',
        'details': {'n': n, 'L_m': L, 'mass_kg': m, 'energy_J': E_n, 'energy_eV': E_eV},
        'unit': 'J'
    }

def calc_infinite_well_wavefunction(n: int = 1, L: float = 1e-9, x_points: int = 100) -> dict:
    """Wavefunction psi_n(x) = sqrt(2/L)*sin(n*pi*x/L) for infinite well."""
    x = np.linspace(0, L, x_points)
    psi = np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)
    integral = np.trapz(psi**2, x)
    return {
        'result': f'psi_{n}(x) computed on [{0}, {L}] with normalization integral = {integral:.6f}',
        'details': {'n': n, 'L': L, 'x_values': x.tolist(), 'psi_values': psi.tolist(), 'normalization_check': integral},
        'unit': 'm^(-1/2)'
    }

def calc_finite_well_transcendental(V0: float = 1e-18, L: float = 1e-9, m: float = 9.11e-31, n_states: int = 3) -> dict:
    """Find bound state energies for finite square well via graphical/Newton method."""
    hbar = 1.054571817e-34
    alpha0 = np.sqrt(2.0 * m * V0) * L / (2.0 * hbar)
    energies = []
    for n in range(1, n_states + 1):
        alpha_guess = n * np.pi / 2.0 - 0.1
        if alpha_guess < alpha0:
            for _ in range(50):
                f = alpha_guess * np.tan(alpha_guess) - np.sqrt(alpha0**2 - alpha_guess**2)
                fp = np.tan(alpha_guess) + alpha_guess / (np.cos(alpha_guess)**2) + alpha_guess / np.sqrt(alpha0**2 - alpha_guess**2)
                if abs(fp) > 1e-15:
                    alpha_guess = alpha_guess - f / fp
                if abs(f) < 1e-12:
                    break
            if alpha_guess < alpha0 and alpha_guess > 0:
                k = 2.0 * alpha_guess / L
                E = hbar**2 * k**2 / (2.0 * m)
                if E < V0:
                    energies.append(E)
    e_str = ', '.join([f'{e/1.602176634e-19:.4f} eV' for e in energies])
    return {
        'result': f'Bound state energies: {e_str}',
        'details': {'V0_J': V0, 'L_m': L, 'alpha0': alpha0, 'energies_J': energies, 'energies_eV': [e/1.602176634e-19 for e in energies], 'n_states_found': len(energies)},
        'unit': 'J'
    }

def calc_harmonic_oscillator_energy(n: int = 0, omega: float = 1e15) -> dict:
    """Energy levels of quantum harmonic oscillator: E_n = (n + 1/2)*hbar*omega."""
    hbar = 1.054571817e-34
    E_n = (n + 0.5) * hbar * omega
    E_eV = E_n / 1.602176634e-19
    E_0 = 0.5 * hbar * omega
    return {
        'result': f'E_{n} = {E_n:.4e} J = {E_eV:.6f} eV, zero-point = {E_0:.4e} J',
        'details': {'n': n, 'omega': omega, 'energy_J': E_n, 'energy_eV': E_eV, 'zero_point_energy': E_0},
        'unit': 'J'
    }

def calc_harmonic_oscillator_spacing(n_levels: int = 5, omega: float = 1e15) -> dict:
    """Compute energy spacing for harmonic oscillator levels."""
    hbar = 1.054571817e-34
    levels = [(n + 0.5) * hbar * omega for n in range(n_levels)]
    spacing = hbar * omega
    levels_eV = [e / 1.602176634e-19 for e in levels]
    return {
        'result': f'Levels: {[f"{e:.4f}" for e in levels_eV]} eV, spacing = {spacing/1.602176634e-19:.4f} eV',
        'details': {'n_levels': n_levels, 'omega': omega, 'energy_levels_J': levels, 'energy_levels_eV': levels_eV, 'spacing_J': spacing},
        'unit': 'J'
    }

def calc_potential_step_reflection(E: float = 1e-18, V0: float = 0.5e-18) -> dict:
    """Reflection coefficient for potential step: R = ((k1-k2)/(k1+k2))^2, E > V0."""
    hbar = 1.054571817e-34
    m = 9.11e-31
    if E <= V0:
        k1 = np.sqrt(2.0 * m * E) / hbar
        kappa = np.sqrt(2.0 * m * (V0 - E)) / hbar
        R = 1.0
        T = 0.0
        phase = 2.0 * np.arctan(kappa / k1)
        return {
            'result': f'E <= V0: R = {R:.6f}, T = {T:.6f} (total reflection)',
            'details': {'E_J': E, 'V0_J': V0, 'R': R, 'T': T, 'condition': 'E <= V0'},
            'unit': 'dimensionless'
        }
    k1 = np.sqrt(2.0 * m * E) / hbar
    k2 = np.sqrt(2.0 * m * (E - V0)) / hbar
    R = ((k1 - k2) / (k1 + k2))**2
    T = 4.0 * k1 * k2 / (k1 + k2)**2
    return {
        'result': f'R = {R:.6f}, T = {T:.6f}',
        'details': {'E_J': E, 'V0_J': V0, 'k1': k1, 'k2': k2, 'R': R, 'T': T, 'condition': 'E > V0'},
        'unit': 'dimensionless'
    }

def calc_tunneling_probability(E: float = 1e-18, V0: float = 2e-18, L: float = 1e-10) -> dict:
    """Transmission probability through rectangular barrier: T approx 16*(E/V0)*(1-E/V0)*exp(-2*kappa*L)."""
    hbar = 1.054571817e-34
    m = 9.11e-31
    if E >= V0:
        k1 = np.sqrt(2.0 * m * E) / hbar
        k2 = np.sqrt(2.0 * m * (E - V0)) / hbar
        T = 1.0 / (1.0 + (V0**2 * np.sin(k2 * L)**2) / (4.0 * E * (E - V0) + 1e-40))
        return {
            'result': f'T = {T:.6e} (above-barrier)',
            'details': {'E_J': E, 'V0_J': V0, 'barrier_width_m': L, 'T': T},
            'unit': 'dimensionless'
        }
    kappa = np.sqrt(2.0 * m * (V0 - E)) / hbar
    ratio = E / V0
    T_approx = 16.0 * ratio * (1.0 - ratio) * np.exp(-2.0 * kappa * L)
    k1 = np.sqrt(2.0 * m * E) / hbar
    T_exact_denom = 1.0 + (V0**2 * np.sinh(kappa * L)**2) / (4.0 * E * (V0 - E) + 1e-40)
    T_exact = 1.0 / T_exact_denom
    return {
        'result': f'T_approx = {T_approx:.6e}, T_exact = {T_exact:.6e}',
        'details': {'E_J': E, 'V0_J': V0, 'barrier_width_m': L, 'kappa': kappa, 'T_approx': T_approx, 'T_exact': T_exact},
        'unit': 'dimensionless'
    }

def calc_gamow_factor(Z1: float = 2.0, Z2: float = 2.0, E_MeV: float = 1.0, reduced_mass_amu: float = 2.0) -> dict:
    """Compute Gamow factor for nuclear tunneling: G = pi*alpha*Z1*Z2*sqrt(2*m*c^2/E)."""
    alpha = 1.0 / 137.036
    amu_to_kg = 1.660539066e-27
    c = 2.99792458e8
    e_charge = 1.602176634e-19
    reduced_mass = reduced_mass_amu * amu_to_kg
    rest_energy = reduced_mass * c**2 / e_charge
    E_joules = E_MeV * 1e6 * e_charge
    G = np.pi * alpha * Z1 * Z2 * np.sqrt(2.0 * rest_energy / (E_MeV))
    return {
        'result': f'Gamow factor G = {G:.4f}',
        'details': {'Z1': Z1, 'Z2': Z2, 'E_MeV': E_MeV, 'reduced_mass_amu': reduced_mass_amu, 'G': G, 'rest_energy_eV': rest_energy},
        'unit': 'dimensionless'
    }

def calc_wkb_energy_levels(potential_type: str = 'harmonic', quantum_number: int = 0, m: float = 9.11e-31) -> dict:
    """WKB quantization: integral(k(x)dx) = (n+1/2)*pi between turning points."""
    hbar = 1.054571817e-34
    omega = 1e15
    if potential_type == 'harmonic':
        E_n = (quantum_number + 0.5) * hbar * omega
        turning_point = np.sqrt(2.0 * E_n / (m * omega**2))
    elif potential_type == 'linear':
        F = 1e9
        turning_point = (3.0 * np.pi * (quantum_number + 0.75) * hbar / (2.0 * np.sqrt(2.0 * m * F)))**(2.0/3.0)
        E_n = F * turning_point
    else:
        turning_point = 1e-9
        E_n = (quantum_number + 0.5) * hbar * omega
    return {
        'result': f'WKB E_{quantum_number} = {E_n:.4e} J',
        'details': {'potential_type': potential_type, 'quantum_number': quantum_number, 'energy_J': E_n, 'turning_point_m': turning_point},
        'unit': 'J'
    }

def calc_pauli_matrices() -> dict:
    """Return Pauli matrices sigma_x, sigma_y, sigma_z."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    comm_xy = sx @ sy - sy @ sx
    check = np.allclose(comm_xy, 2j * sz)
    return {
        'result': f'Pauli matrices: sigma_i*sigma_j = i*epsilon_ijk*sigma_k (verified: {check})',
        'details': {'sigma_x': sx.tolist(), 'sigma_y': sy.tolist(), 'sigma_z': sz.tolist(), 'commutator_xy': comm_xy.tolist(), 'satisfies_algebra': check},
        'unit': 'dimensionless'
    }

def calc_spin_operator(axis: str = 'z', spin: float = 0.5) -> dict:
    """Spin operator S_i = (hbar/2)*sigma_i for given axis."""
    hbar = 1.054571817e-34
    if axis == 'x':
        mat = (hbar / 2.0) * np.array([[0, 1], [1, 0]], dtype=complex)
    elif axis == 'y':
        mat = (hbar / 2.0) * np.array([[0, -1j], [1j, 0]], dtype=complex)
    elif axis == 'z':
        mat = (hbar / 2.0) * np.array([[1, 0], [0, -1]], dtype=complex)
    else:
        mat = np.zeros((2,2))
    eigenvalues = np.linalg.eigvalsh(mat)
    return {
        'result': f'S_{axis} eigenvalues: {[f"{v:.4e}" for v in eigenvalues]} J*s',
        'details': {'axis': axis, 'spin': spin, 'operator': mat.tolist(), 'eigenvalues': eigenvalues.tolist(), 'hbar': hbar},
        'unit': 'J*s'
    }

def calc_spin_half_state(theta: float = np.pi/4, phi: float = 0.0) -> dict:
    """Spin-1/2 state |psi> = cos(theta/2)|up> + e^(i*phi)*sin(theta/2)|down>."""
    up = np.cos(theta / 2.0)
    down = np.exp(1j * phi) * np.sin(theta / 2.0)
    state = np.array([up, down], dtype=complex)
    prob_up = np.abs(up)**2
    prob_down = np.abs(down)**2
    pauli_z = np.array([[1, 0], [0, -1]], dtype=complex)
    exp_sz = (1.054571817e-34 / 2.0) * np.conj(state).T @ pauli_z @ state
    return {
        'result': f'|up> prob = {prob_up:.4f}, |down> prob = {prob_down:.4f}',
        'details': {'theta': theta, 'phi': phi, 'state': state.tolist(), 'prob_up': prob_up, 'prob_down': prob_down, 'expectation_Sz': float(np.real(exp_sz))},
        'unit': 'dimensionless'
    }

def calc_stern_gerlach(s_z_state: float = 0.5) -> dict:
    """Stern-Gerlach measurement: spin projection m_s = +/- 1/2."""
    hbar = 1.054571817e-34
    ms_up = 0.5
    ms_down = -0.5
    prob_up = 0.5 * (1.0 + 2.0 * s_z_state)
    prob_down = 0.5 * (1.0 - 2.0 * s_z_state)
    prob_up = max(0.0, min(1.0, prob_up))
    prob_down = 1.0 - prob_up
    return {
        'result': f'P(up) = {prob_up:.4f}, P(down) = {prob_down:.4f}',
        'details': {'s_z_state': s_z_state, 'ms_up': ms_up, 'ms_down': ms_down, 'prob_up': prob_up, 'prob_down': prob_down},
        'unit': 'dimensionless'
    }

def calc_angular_momentum(l: int = 1, m: int = 0) -> dict:
    """Eigenvalues of L^2 and Lz: L^2 = l(l+1)hbar^2, Lz = m*hbar."""
    hbar = 1.054571817e-34
    L2 = l * (l + 1) * hbar**2
    Lz = m * hbar
    return {
        'result': f'L^2 = {L2:.4e} J^2*s^2, Lz = {Lz:.4e} J*s for (l={l}, m={m})',
        'details': {'l': l, 'm': m, 'L2': L2, 'Lz': Lz, 'hbar': hbar},
        'unit': 'J^2*s^2 / J*s'
    }

def calc_spherical_harmonic(l: int = 1, m: int = 0, theta: float = np.pi/4, phi: float = 0.0) -> dict:
    """Evaluate spherical harmonic Y_lm(theta, phi)."""
    if l == 0 and m == 0:
        Y = 1.0 / np.sqrt(4.0 * np.pi)
    elif l == 1 and m == 0:
        Y = np.sqrt(3.0 / (4.0 * np.pi)) * np.cos(theta)
    elif l == 1 and m == 1:
        Y = -np.sqrt(3.0 / (8.0 * np.pi)) * np.sin(theta) * np.exp(1j * phi)
    elif l == 1 and m == -1:
        Y = np.sqrt(3.0 / (8.0 * np.pi)) * np.sin(theta) * np.exp(-1j * phi)
    elif l == 2 and m == 0:
        Y = np.sqrt(5.0 / (16.0 * np.pi)) * (3.0 * np.cos(theta)**2 - 1.0)
    elif l == 2 and m == 1:
        Y = -np.sqrt(15.0 / (8.0 * np.pi)) * np.sin(theta) * np.cos(theta) * np.exp(1j * phi)
    elif l == 2 and m == 2:
        Y = np.sqrt(15.0 / (32.0 * np.pi)) * np.sin(theta)**2 * np.exp(2j * phi)
    else:
        Y = 1.0 / np.sqrt(4.0 * np.pi)
    return {
        'result': f'Y_{l}^{m}({theta:.3f}, {phi:.3f}) = {Y:.6f}',
        'details': {'l': l, 'm': m, 'theta': theta, 'phi': phi, 'Y_value': complex(Y) if isinstance(Y, complex) else float(Y)},
        'unit': 'dimensionless'
    }

def calc_hydrogen_energy(n: int = 1) -> dict:
    """Bohr model: E_n = -13.6 / n^2 eV."""
    E_eV = -13.605693122994 / n**2
    E_J = E_eV * 1.602176634e-19
    return {
        'result': f'E_{n} = {E_eV:.6f} eV = {E_J:.4e} J',
        'details': {'n': n, 'energy_eV': E_eV, 'energy_J': E_J, 'rydberg_eV': 13.605693122994},
        'unit': 'eV'
    }

def calc_bohr_radius(n: int = 1) -> dict:
    """Bohr radius: r_n = n^2 * a_0, a_0 = 0.529 Angstrom."""
    a0 = 5.29177210903e-11
    r_n = n**2 * a0
    return {
        'result': f'r_{n} = {r_n:.6e} m = {r_n*1e10:.4f} Angstrom',
        'details': {'n': n, 'bohr_radius_a0': a0, 'radius_m': r_n, 'radius_angstrom': r_n * 1e10},
        'unit': 'm'
    }

def calc_hydrogen_radial_probability(n: int = 2, l: int = 1, r_values: int = 200) -> dict:
    """Radial probability distribution P(r) = r^2|R_nl(r)|^2 for hydrogen."""
    a0 = 5.29177210903e-11
    r_max = 20.0 * a0
    r = np.linspace(1e-15, r_max, r_values)
    if n == 1 and l == 0:
        R = 2.0 * a0**(-1.5) * np.exp(-r / a0)
    elif n == 2 and l == 0:
        R = (1.0 / (2.0 * np.sqrt(2.0))) * a0**(-1.5) * (2.0 - r / a0) * np.exp(-r / (2.0 * a0))
    elif n == 2 and l == 1:
        R = (1.0 / (2.0 * np.sqrt(6.0))) * a0**(-1.5) * (r / a0) * np.exp(-r / (2.0 * a0))
    elif n == 3 and l == 0:
        rho = 2.0 * r / (3.0 * a0)
        R = (2.0 / (81.0 * np.sqrt(3.0))) * a0**(-1.5) * (27.0 - 18.0 * rho + 2.0 * rho**2) * np.exp(-r / (3.0 * a0))
    elif n == 3 and l == 1:
        rho = 2.0 * r / (3.0 * a0)
        R = (4.0 / (81.0 * np.sqrt(6.0))) * a0**(-1.5) * (6.0 * rho - rho**2) * np.exp(-r / (3.0 * a0))
    else:
        rho_val = r / a0
        R = np.exp(-rho_val / n)
    P = r**2 * R**2
    most_probable_r = r[np.argmax(P)]
    return {
        'result': f'Most probable r = {most_probable_r:.4e} m for n={n}, l={l}',
        'details': {'n': n, 'l': l, 'r_values': r.tolist(), 'probability': P.tolist(), 'most_probable_r': most_probable_r},
        'unit': 'm'
    }

def calc_rydberg_formula(n1: int = 2, n2: int = 3, Z: float = 1.0) -> dict:
    """Rydberg formula: 1/lambda = R_inf * Z^2 * (1/n1^2 - 1/n2^2)."""
    R_inf = 1.0973731568160e7
    inv_lambda = R_inf * Z**2 * (1.0 / n1**2 - 1.0 / n2**2)
    if inv_lambda <= 0:
        return {
            'result': 'n2 must be > n1 for emission',
            'details': {'n1': n1, 'n2': n2, 'Z': Z, 'inv_lambda': inv_lambda},
            'unit': 'm^(-1)'
        }
    wavelength = 1.0 / inv_lambda
    wavelength_nm = wavelength * 1e9
    E_eV = 1.23984198e-6 / wavelength
    return {
        'result': f'lambda = {wavelength_nm:.4f} nm, E = {E_eV:.4f} eV',
        'details': {'n1': n1, 'n2': n2, 'Z': Z, 'wavelength_m': wavelength, 'wavelength_nm': wavelength_nm, 'energy_eV': E_eV, 'R_inf': R_inf},
        'unit': 'm'
    }

def calc_fermi_dirac(energy: float = 0.0, E_F: float = 5.0, T: float = 300.0) -> dict:
    """Fermi-Dirac distribution: f(E) = 1/(exp((E-E_F)/(kT)) + 1)."""
    k_B = 1.380649e-23
    E_joules = energy * 1.602176634e-19
    E_F_joules = E_F * 1.602176634e-19
    exponent = (E_joules - E_F_joules) / (k_B * T)
    if exponent > 100:
        f = 0.0
    elif exponent < -100:
        f = 1.0
    else:
        f = 1.0 / (np.exp(exponent) + 1.0)
    return {
        'result': f'f(E={energy}eV) = {f:.6f} at T = {T} K',
        'details': {'energy_eV': energy, 'E_F_eV': E_F, 'T_K': T, 'occupation': f, 'k_B': k_B},
        'unit': 'dimensionless'
    }

def calc_bose_einstein(energy: float = 0.01, T: float = 300.0, mu: float = 0.0) -> dict:
    """Bose-Einstein distribution: n(E) = 1/(exp((E-mu)/(kT)) - 1)."""
    k_B = 1.380649e-23
    E_joules = energy * 1.602176634e-19
    mu_joules = mu * 1.602176634e-19
    if E_joules <= mu_joules:
        return {
            'result': f'E must be > mu for Bose-Einstein (got E={energy}, mu={mu})',
            'details': {'energy_eV': energy, 'mu_eV': mu, 'T_K': T, 'occupation': float('inf')},
            'unit': 'dimensionless'
        }
    exponent = (E_joules - mu_joules) / (k_B * T)
    if exponent < 1e-10:
        n = 1.0 / (exponent + 1e-40)
    else:
        n = 1.0 / (np.exp(exponent) - 1.0)
    return {
        'result': f'n(E={energy}eV) = {n:.6f} at T = {T} K',
        'details': {'energy_eV': energy, 'mu_eV': mu, 'T_K': T, 'occupation': n},
        'unit': 'dimensionless'
    }

def calc_bose_einstein_condensation_temperature(density: float = 1e28, m: float = 4.0 * 1.660539066e-27) -> dict:
    """BEC critical temperature: T_c = (2*pi*hbar^2/k_B*m)*(n/zeta(3/2))^(2/3)."""
    hbar = 1.054571817e-34
    k_B = 1.380649e-23
    zeta_32 = 2.612
    T_c = (2.0 * np.pi * hbar**2 / (k_B * m)) * (density / zeta_32)**(2.0/3.0)
    return {
        'result': f'T_c = {T_c:.6e} K = {T_c*1e9:.4f} nK',
        'details': {'density': density, 'mass_kg': m, 'T_c_K': T_c, 'zeta_3_2': zeta_32},
        'unit': 'K'
    }

def calc_coherent_state(alpha: complex = 1.0+0j, n_max: int = 20) -> dict:
    """Coherent state |alpha> = exp(-|alpha|^2/2)*sum(alpha^n/sqrt(n!)|n>)."""
    alpha_val = complex(alpha)
    norm_factor = np.exp(-np.abs(alpha_val)**2 / 2.0)
    coefficients = []
    for n in range(n_max + 1):
        coeff = norm_factor * alpha_val**n / np.sqrt(math.factorial(n))
        coefficients.append(coeff)
    amplitudes = np.abs(coefficients)**2
    mean_n = np.sum([n * amplitudes[n] for n in range(n_max + 1)])
    return {
        'result': f'|alpha={alpha_val}| coherent: <n> = {mean_n:.4f}',
        'details': {'alpha': alpha_val, 'n_max': n_max, 'mean_photon_number': mean_n, 'norm_factor': norm_factor, 'coefficient_moduli': [float(abs(c)) for c in coefficients[:10]]},
        'unit': 'dimensionless'
    }

def calc_fock_state(n: int = 3, n_max: int = 10) -> dict:
    """Fock state |n>: definite photon number state."""
    state = np.zeros(n_max + 1, dtype=complex)
    state[n] = 1.0
    number_op = np.diag(np.arange(n_max + 1))
    mean_n = np.conj(state).T @ number_op @ state
    var_n = np.conj(state).T @ number_op @ number_op @ state - mean_n**2
    return {
        'result': f'Fock state |{n}>: <n> = {float(np.real(mean_n)):.4f}, Delta_n = {float(np.real(np.sqrt(var_n))):.4f}',
        'details': {'n': n, 'n_max': n_max, 'mean_n': float(np.real(mean_n)), 'variance': float(np.real(var_n)), 'state': state.tolist()},
        'unit': 'dimensionless'
    }

def calc_bell_state(bell_index: int = 0) -> dict:
    """Return Bell states: 0=Phi+, 1=Phi-, 2=Psi+, 3=Psi-."""
    basis = np.zeros((4, 4), dtype=complex)
    if bell_index == 0:
        state = np.array([1.0, 0.0, 0.0, 1.0]) / np.sqrt(2.0)
        name = 'Phi+'
    elif bell_index == 1:
        state = np.array([1.0, 0.0, 0.0, -1.0]) / np.sqrt(2.0)
        name = 'Phi-'
    elif bell_index == 2:
        state = np.array([0.0, 1.0, 1.0, 0.0]) / np.sqrt(2.0)
        name = 'Psi+'
    elif bell_index == 3:
        state = np.array([0.0, 1.0, -1.0, 0.0]) / np.sqrt(2.0)
        name = 'Psi-'
    else:
        state = np.array([0, 0, 0, 0])
        name = 'invalid'
    rho = np.outer(state, np.conj(state))
    trace_rho2 = np.trace(rho @ rho)
    return {
        'result': f'Bell state |{name}>: Tr(rho^2) = {float(np.real(trace_rho2)):.4f} (pure)',
        'details': {'bell_index': bell_index, 'name': name, 'state': state.tolist(), 'density_matrix': rho.tolist(), 'purity': float(np.real(trace_rho2))},
        'unit': 'dimensionless'
    }

def calc_entanglement_entropy(state_vector: list = None) -> dict:
    """Von Neumann entropy S = -Tr(rho_A * log2(rho_A)) for bipartite state."""
    if state_vector is None:
        state_vector = [1.0/np.sqrt(2), 0, 0, 1.0/np.sqrt(2)]
    psi = np.array(state_vector, dtype=complex).reshape(4)
    psi_mat = psi.reshape(2, 2)
    rho_A = psi_mat @ np.conj(psi_mat).T
    eigenvalues = np.linalg.eigvalsh(rho_A)
    eigenvalues = np.clip(eigenvalues, 1e-15, 1.0)
    S = -np.sum(eigenvalues * np.log2(eigenvalues))
    return {
        'result': f'Von Neumann entropy S = {S:.6f} bits',
        'details': {'state': psi.tolist(), 'eigenvalues_rho_A': eigenvalues.tolist(), 'entropy': S, 'max_entropy': np.log2(2)},
        'unit': 'bits'
    }

def calc_time_evolution_schrodinger(initial_state: list = None, H_matrix: list = None, t: float = 1e-15) -> dict:
    """Evolve state via |psi(t)> = exp(-i*H*t/hbar)|psi(0)>."""
    hbar = 1.054571817e-34
    if initial_state is None:
        initial_state = [1.0, 0.0]
    if H_matrix is None:
        H_matrix = [[1e-19, 0], [0, 2e-19]]
    psi0 = np.array(initial_state, dtype=complex)
    H = np.array(H_matrix, dtype=complex)
    eigenvalues_H, eigenvectors_H = np.linalg.eigh(H)
    U_diag = np.exp(-1j * eigenvalues_H * t / hbar)
    U = eigenvectors_H @ np.diag(U_diag) @ np.conj(eigenvectors_H).T
    psi_t = U @ psi0
    probs = np.abs(psi_t)**2
    return {
        'result': f'Time-evolved state probabilities: {[f"{p:.4f}" for p in probs]}',
        'details': {'t_s': t, 'eigenvalues_H': eigenvalues_H.tolist(), 'evolved_state': psi_t.tolist(), 'probabilities': probs.tolist()},
        'unit': 'dimensionless'
    }

def calc_commutator(A: list = None, B: list = None) -> dict:
    """Compute commutator [A, B] = AB - BA."""
    if A is None:
        A = [[0, 1], [1, 0]]
    if B is None:
        B = [[1, 0], [0, -1]]
    a = np.array(A, dtype=complex)
    b = np.array(B, dtype=complex)
    comm = a @ b - b @ a
    return {
        'result': f'[A,B] computed, trace = {np.trace(comm):.6f}',
        'details': {'A': a.tolist(), 'B': b.tolist(), 'commutator': comm.tolist(), 'trace': float(np.real(np.trace(comm)))},
        'unit': 'dimensionless'
    }

def calc_ehrenfest_theorem(psi_values: list = None, x_values: list = None, V_func: str = 'harmonic') -> dict:
    """Ehrenfest: d<x>/dt = <p>/m, d<p>/dt = -<dV/dx> (numerical verification)."""
    if x_values is None:
        x_values = np.linspace(-5, 5, 100).tolist()
    if psi_values is None:
        psi_values = (np.exp(-np.linspace(-5, 5, 100)**2 / 2.0)).tolist()
    x_arr = np.array(x_values)
    psi_arr = np.array(psi_values, dtype=complex)
    dx = x_arr[1] - x_arr[0]
    prob = np.abs(psi_arr)**2
    exp_x = np.trapz(prob * x_arr, x_arr)
    dpsi = np.gradient(psi_arr, dx)
    p_op = -1j * 1.054571817e-34 * dpsi
    exp_p = np.trapz(np.conj(psi_arr) * p_op, x_arr)
    if V_func == 'harmonic':
        dV = x_arr
    elif V_func == 'linear':
        dV = np.ones_like(x_arr)
    else:
        dV = x_arr
    exp_dV = np.trapz(prob * dV, x_arr)
    return {
        'result': f'<x> = {exp_x:.4f}, <p> = {float(np.real(exp_p)):.4e}, <-dV/dx> = {exp_dV:.4f}',
        'details': {'expectation_x': float(exp_x), 'expectation_p': float(np.real(exp_p)), 'expectation_dVdx': float(exp_dV), 'V_type': V_func},
        'unit': 'mixed'
    }

def calc_density_matrix(pure_state: list = None, mixed_probs: list = None, mixed_states: list = None) -> dict:
    """Construct density matrix: rho = sum(p_i * |psi_i><psi_i|)."""
    if pure_state is None:
        pure_state = [1.0, 0.0]
    psi = np.array(pure_state, dtype=complex)
    rho_pure = np.outer(psi, np.conj(psi))
    purity = np.trace(rho_pure @ rho_pure)
    if mixed_probs is not None and mixed_states is not None:
        rho_mixed = np.zeros((len(psi), len(psi)), dtype=complex)
        for p, s in zip(mixed_probs, mixed_states):
            vec = np.array(s, dtype=complex)
            rho_mixed += p * np.outer(vec, np.conj(vec))
        purity_mixed = float(np.real(np.trace(rho_mixed @ rho_mixed)))
    else:
        rho_mixed = rho_pure
        purity_mixed = float(np.real(purity))
    return {
        'result': f'Pure state purity = {float(np.real(purity)):.4f}, Mixed purity = {purity_mixed:.4f}',
        'details': {'rho_pure': rho_pure.tolist(), 'rho_mixed': rho_mixed.tolist(), 'purity_pure': float(np.real(purity)), 'purity_mixed': purity_mixed},
        'unit': 'dimensionless'
    }

def calc_quantum_zeno_effect(decay_rate: float = 0.1, n_measurements: int = 10, total_time: float = 1.0) -> dict:
    """Survival probability under frequent measurements: P_surv = cos(theta/N)^(2N)."""
    theta = decay_rate * total_time
    P_freq = np.cos(theta / n_measurements)**(2 * n_measurements)
    P_no_meas = np.cos(theta)**2
    return {
        'result': f'P_surv(no meas) = {P_no_meas:.6f}, P_surv({n_measurements} meas) = {P_freq:.6f}',
        'details': {'decay_rate': decay_rate, 'n_measurements': n_measurements, 'total_time': total_time, 'P_surv_free': P_no_meas, 'P_surv_measured': P_freq, 'Zeno_effect': P_freq > P_no_meas},
        'unit': 'dimensionless'
    }

def calc_rabi_oscillation(rabi_freq: float = 1e6, detuning: float = 0.0, time_s: float = 1e-6) -> dict:
    """Rabi oscillation: P_excited = (Omega_R/Omega_eff)^2 * sin^2(Omega_eff*t/2)."""
    Omega_eff = np.sqrt(rabi_freq**2 + detuning**2)
    P_excited = (rabi_freq / Omega_eff)**2 * np.sin(Omega_eff * time_s / 2.0)**2
    period = 2.0 * np.pi / Omega_eff
    return {
        'result': f'P_excited = {P_excited:.6f}, Rabi period = {period:.4e} s',
        'details': {'rabi_freq': rabi_freq, 'detuning': detuning, 'time': time_s, 'Omega_eff': Omega_eff, 'P_excited': P_excited, 'period': period},
        'unit': 'dimensionless'
    }

def calc_adiabatic_theorem(H_initial: list = None, H_final: list = None, sweep_time: float = 1e-9) -> dict:
    """Adiabatic condition: |<m|dH/dt|n>| / (E_m - E_n)^2 << 1."""
    if H_initial is None:
        H_initial = [[0, 1e-19], [1e-19, 0]]
    if H_final is None:
        H_final = [[1e-19, 0], [0, -1e-19]]
    Hi = np.array(H_initial, dtype=complex)
    Hf = np.array(H_final, dtype=complex)
    dH_dt = (Hf - Hi) / sweep_time
    ei, vi = np.linalg.eigh(Hi)
    ef, vf = np.linalg.eigh(Hf)
    gap = abs(ei[1] - ei[0])
    matrix_element = abs(np.conj(vi[:, 1]).T @ dH_dt @ vi[:, 0])
    adiabatic_parameter = matrix_element / (gap**2 + 1e-40)
    return {
        'result': f'Adiabatic parameter = {adiabatic_parameter:.6f} (<< 1 => adiabatic: {adiabatic_parameter < 0.1})',
        'details': {'gap': gap, 'matrix_element': matrix_element, 'adiabatic_parameter': adiabatic_parameter, 'sweep_time': sweep_time},
        'unit': 'dimensionless'
    }

def calc_landau_zener_probability(energy_gap: float = 1e-20, sweep_rate: float = 1e12) -> dict:
    """Landau-Zener transition probability: P = exp(-2*pi*Delta^2/(hbar*dE/dt))."""
    hbar = 1.054571817e-34
    P_transition = np.exp(-2.0 * np.pi * energy_gap**2 / (hbar * sweep_rate))
    return {
        'result': f'P_nonadiabatic transition = {P_transition:.6e}',
        'details': {'energy_gap': energy_gap, 'sweep_rate': sweep_rate, 'P_transition': P_transition, 'hbar': hbar},
        'unit': 'dimensionless'
    }

def calc_clebsch_gordan(j1: float = 0.5, j2: float = 0.5, m1: float = 0.5, m2: float = -0.5, J: float = 0.0, M: float = 0.0) -> dict:
    """Clebsch-Gordan coefficient <j1,m1;j2,m2|J,M> for simple cases."""
    if abs(m1 + m2 - M) > 1e-10:
        coeff = 0.0
    elif abs(j1 - 0.5) < 1e-10 and abs(j2 - 0.5) < 1e-10:
        if abs(J - 1.0) < 1e-10 and abs(M - 0.0) < 1e-10:
            if abs(m1 - 0.5) < 1e-10 and abs(m2 + 0.5) < 1e-10:
                coeff = 1.0 / np.sqrt(2.0)
            elif abs(m1 + 0.5) < 1e-10 and abs(m2 - 0.5) < 1e-10:
                coeff = 1.0 / np.sqrt(2.0)
            else:
                coeff = 0.0
        elif abs(J - 0.0) < 1e-10:
            if abs(m1 - 0.5) < 1e-10 and abs(m2 + 0.5) < 1e-10:
                coeff = 1.0 / np.sqrt(2.0)
            elif abs(m1 + 0.5) < 1e-10 and abs(m2 - 0.5) < 1e-10:
                coeff = -1.0 / np.sqrt(2.0)
            else:
                coeff = 0.0
        else:
            coeff = 0.0
    else:
        coeff = 1.0 if abs(J - (j1 + j2)) < 1e-10 and abs(M - (m1 + m2)) < 1e-10 else 0.0
    return {
        'result': f'<{j1},{m1};{j2},{m2}|{J},{M}> = {coeff:.6f}',
        'details': {'j1': j1, 'j2': j2, 'm1': m1, 'm2': m2, 'J': J, 'M': M, 'CG_coefficient': coeff},
        'unit': 'dimensionless'
    }

def calc_no_cloning_theorem(state_a: list = None, state_b: list = None) -> dict:
    """Numerical demonstration: inner product preserved before/after 'cloning'."""
    if state_a is None:
        state_a = [1.0, 0.0]
    if state_b is None:
        state_b = [1.0/np.sqrt(2), 1.0/np.sqrt(2)]
    a = np.array(state_a, dtype=complex)
    b = np.array(state_b, dtype=complex)
    inner = np.abs(np.dot(np.conj(a), b))**2
    return {
        'result': f'|<psi|phi>|^2 = {inner:.6f} (cloning would violate this)',
        'details': {'state_a': a.tolist(), 'state_b': b.tolist(), 'inner_product_squared': inner},
        'unit': 'dimensionless'
    }

def calc_ehrenfest_oscillator(x0: float = 1.0, p0: float = 0.0, omega: float = 1.0, t_span: list = None, n_steps: int = 100) -> dict:
    """Ehrenfest evolution of <x> and <p> for harmonic oscillator."""
    if t_span is None:
        t_span = [0, 2*np.pi]
    t = np.linspace(t_span[0], t_span[1], n_steps)
    x_exp = x0 * np.cos(omega * t) + p0 / omega * np.sin(omega * t)
    p_exp = -omega * x0 * np.sin(omega * t) + p0 * np.cos(omega * t)
    return {
        'result': f'<x> oscillates between {np.min(x_exp):.4f} and {np.max(x_exp):.4f}',
        'details': {'x0': x0, 'p0': p0, 'omega': omega, 't': t.tolist(), 'x_expectation': x_exp.tolist(), 'p_expectation': p_exp.tolist()},
        'unit': 'dimensionless'
    }

def calc_perturbation_theory_1st_order(unperturbed_energies: list = None, perturbation_matrix: list = None) -> dict:
    """First-order nondegenerate perturbation: E_n^(1) = <n|H'|n>."""
    if unperturbed_energies is None:
        unperturbed_energies = [1.0, 2.0, 3.0]
    if perturbation_matrix is None:
        perturbation_matrix = [[0.1, 0.05, 0], [0.05, 0.2, 0.03], [0, 0.03, 0.15]]
    E0 = np.array(unperturbed_energies)
    Hp = np.array(perturbation_matrix)
    E1 = np.diag(Hp)
    E_total = E0 + E1
    return {
        'result': f'Corrected energies: {[f"{e:.4f}" for e in E_total]}',
        'details': {'E0': E0.tolist(), 'E1': E1.tolist(), 'E_total': E_total.tolist(), 'H_prime': Hp.tolist()},
        'unit': 'dimensionless'
    }

def calc_variational_principle(trial_params: list = None) -> dict:
    """Variational principle: <H> >= E_0, optimize trial parameter."""
    if trial_params is None:
        trial_params = [0.5, 1.0, 1.5, 2.0, 2.5]
    energies = []
    for alpha in trial_params:
        KE = alpha**2 / 2.0
        PE = -alpha
        E = KE + PE
        energies.append(E)
    idx_min = np.argmin(energies)
    return {
        'result': f'Optimal alpha = {trial_params[idx_min]:.4f}, E_min = {energies[idx_min]:.4f}',
        'details': {'alpha_values': trial_params, 'energies': energies, 'optimal_alpha': trial_params[idx_min], 'min_energy': energies[idx_min]},
        'unit': 'dimensionless'
    }

def calc_quantum_fourier_transform(state: list = None) -> dict:
    """Quantum Fourier Transform on n-qubit state."""
    if state is None:
        state = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    N = len(state)
    qft_matrix = np.zeros((N, N), dtype=complex)
    for j in range(N):
        for k in range(N):
            qft_matrix[j, k] = np.exp(2j * np.pi * j * k / N) / np.sqrt(N)
    state_vec = np.array(state, dtype=complex)
    transformed = qft_matrix @ state_vec
    return {
        'result': f'QFT applied, amplitude[0] = {abs(transformed[0]):.4f}',
        'details': {'input_state': state, 'transformed_state': transformed.tolist(), 'N': N},
        'unit': 'dimensionless'
    }

def calc_grover_iteration(target_index: int = 3, n_qubits: int = 3) -> dict:
    """Grover search: optimal iterations = floor(pi/4*sqrt(N))."""
    N = 2**n_qubits
    optimal_iterations = int(np.floor(np.pi / 4.0 * np.sqrt(N)))
    return {
        'result': f'N={N}, optimal Grover iterations = {optimal_iterations}',
        'details': {'n_qubits': n_qubits, 'N': N, 'target_index': target_index, 'optimal_iterations': optimal_iterations},
        'unit': 'dimensionless'
    }

def calc_decoherence_off_diagonal(t: float = 1e-9, gamma: float = 1e9) -> dict:
    """Decoherence: off-diagonal elements decay as exp(-gamma*t)."""
    decay = np.exp(-gamma * t)
    coherence_time = 1.0 / gamma
    return {
        'result': f'Off-diagonal decay = {decay:.6e}, coherence time = {coherence_time:.4e} s',
        'details': {'time_s': t, 'gamma': gamma, 'decay_factor': decay, 'coherence_time': coherence_time},
        'unit': 's'
    }

def calc_semiclassical_tunneling(mass_kg: float = 9.11e-31, barrier_func: str = 'parabolic', E: float = 1e-19, params: dict = None) -> dict:
    """Semiclassical tunneling integral for general 1D barrier."""
    hbar = 1.054571817e-34
    if params is None:
        params = {'V0': 2e-19, 'L': 1e-10}
    V0 = params.get('V0', 2e-19)
    L = params.get('L', 1e-10)
    if barrier_func == 'parabolic':
        kappa_max = np.sqrt(2.0 * mass_kg * (V0 - E)) / hbar
        integral = kappa_max * L * np.pi / 4.0
    elif barrier_func == 'triangular':
        kappa_max = np.sqrt(2.0 * mass_kg * (V0 - E)) / hbar
        integral = 2.0 * kappa_max * L / 3.0
    else:
        kappa_avg = np.sqrt(2.0 * mass_kg * (V0 - E)) / hbar
        integral = kappa_avg * L
    T = np.exp(-2.0 * integral)
    return {
        'result': f'Tunneling probability T = {T:.6e}',
        'details': {'barrier_type': barrier_func, 'mass_kg': mass_kg, 'E_J': E, 'V0_J': V0, 'L_m': L, 'integral': integral, 'T': T},
        'unit': 'dimensionless'
    }

def calc_number_phase_uncertainty(n_mean: float = 10.0) -> dict:
    """Number-phase uncertainty: Delta_n * Delta_phi >= 1/2."""
    Delta_n = np.sqrt(n_mean)
    Delta_phi = 1.0 / (2.0 * Delta_n)
    product = Delta_n * Delta_phi
    return {
        'result': f'Delta_n = {Delta_n:.4f}, Delta_phi = {Delta_phi:.4f}, product = {product:.4f} >= 0.5',
        'details': {'n_mean': n_mean, 'Delta_n': Delta_n, 'Delta_phi': Delta_phi, 'product': product, 'satisfies_inequality': product >= 0.5},
        'unit': 'dimensionless'
    }

COMMANDS = {
    'debroglie': {'func': calc_de_broglie_wavelength, 'params': ['mass_kg', 'velocity'], 'desc': 'de Broglie wavelength lambda = h/p'},
    'probability_density': {'func': calc_probability_density, 'params': ['psi_real', 'psi_imag'], 'desc': 'Probability density |psi|^2'},
    'normalization': {'func': calc_normalization_constant, 'params': ['wavefunction_samples'], 'desc': 'Normalization constant for discretized wavefunction'},
    'expectation': {'func': calc_expectation_value, 'params': ['x_values', 'psi_values'], 'desc': 'Expectation value <x> and uncertainty Delta_x'},
    'uncertainty': {'func': calc_uncertainty_principle, 'params': ['delta_x', 'delta_p'], 'desc': 'Heisenberg uncertainty principle check'},
    'energy_time_uncertainty': {'func': calc_uncertainty_energy_time, 'params': ['delta_e', 'delta_t'], 'desc': 'Energy-time uncertainty principle'},
    'infinite_well_energy': {'func': calc_infinite_well_energy, 'params': ['n', 'L', 'm'], 'desc': 'Infinite square well energy levels E_n'},
    'infinite_well_wf': {'func': calc_infinite_well_wavefunction, 'params': ['n', 'L', 'x_points'], 'desc': 'Infinite square well wavefunction psi_n(x)'},
    'finite_well': {'func': calc_finite_well_transcendental, 'params': ['V0', 'L', 'm', 'n_states'], 'desc': 'Finite square well bound states (transcendental eqn)'},
    'harmonic_energy': {'func': calc_harmonic_oscillator_energy, 'params': ['n', 'omega'], 'desc': 'Quantum harmonic oscillator energy E_n = (n+1/2)hbar*omega'},
    'harmonic_spacing': {'func': calc_harmonic_oscillator_spacing, 'params': ['n_levels', 'omega'], 'desc': 'Harmonic oscillator energy level spacing'},
    'potential_step': {'func': calc_potential_step_reflection, 'params': ['E', 'V0'], 'desc': 'Reflection/transmission at 1D potential step'},
    'tunneling': {'func': calc_tunneling_probability, 'params': ['E', 'V0', 'L'], 'desc': 'Quantum tunneling probability through rectangular barrier'},
    'gamow': {'func': calc_gamow_factor, 'params': ['Z1', 'Z2', 'E_MeV', 'reduced_mass_amu'], 'desc': 'Gamow factor for nuclear fusion tunneling'},
    'wkb': {'func': calc_wkb_energy_levels, 'params': ['potential_type', 'quantum_number', 'm'], 'desc': 'WKB approximation energy levels'},
    'pauli': {'func': calc_pauli_matrices, 'params': [], 'desc': 'Pauli spin matrices and commutation relations'},
    'spin_op': {'func': calc_spin_operator, 'params': ['axis', 'spin'], 'desc': 'Spin operator S_i with eigenvalues'},
    'spin_state': {'func': calc_spin_half_state, 'params': ['theta', 'phi'], 'desc': 'Spin-1/2 state on Bloch sphere'},
    'stern_gerlach': {'func': calc_stern_gerlach, 'params': ['s_z_state'], 'desc': 'Stern-Gerlach measurement probabilities'},
    'angular_momentum': {'func': calc_angular_momentum, 'params': ['l', 'm'], 'desc': 'L^2 and Lz eigenvalues'},
    'spherical_harmonic': {'func': calc_spherical_harmonic, 'params': ['l', 'm', 'theta', 'phi'], 'desc': 'Spherical harmonic Y_lm evaluation'},
    'hydrogen_energy': {'func': calc_hydrogen_energy, 'params': ['n'], 'desc': 'Hydrogen atom energy levels (Bohr model)'},
    'bohr_radius': {'func': calc_bohr_radius, 'params': ['n'], 'desc': 'Bohr radius r_n = n^2 * a_0'},
    'radial_probability': {'func': calc_hydrogen_radial_probability, 'params': ['n', 'l', 'r_values'], 'desc': 'Radial probability distribution P(r) for hydrogen'},
    'rydberg': {'func': calc_rydberg_formula, 'params': ['n1', 'n2', 'Z'], 'desc': 'Rydberg formula for spectral line wavelengths'},
    'fermi_dirac': {'func': calc_fermi_dirac, 'params': ['energy', 'E_F', 'T'], 'desc': 'Fermi-Dirac distribution f(E)'},
    'bose_einstein': {'func': calc_bose_einstein, 'params': ['energy', 'T', 'mu'], 'desc': 'Bose-Einstein distribution n(E)'},
    'bec_temperature': {'func': calc_bose_einstein_condensation_temperature, 'params': ['density', 'm'], 'desc': 'Bose-Einstein condensation critical temperature'},
    'coherent_state': {'func': calc_coherent_state, 'params': ['alpha', 'n_max'], 'desc': 'Coherent state construction and properties'},
    'fock_state': {'func': calc_fock_state, 'params': ['n', 'n_max'], 'desc': 'Fock (number) state properties'},
    'bell_state': {'func': calc_bell_state, 'params': ['bell_index'], 'desc': 'Bell entangled states'},
    'entanglement_entropy': {'func': calc_entanglement_entropy, 'params': ['state_vector'], 'desc': 'Von Neumann entanglement entropy'},
    'time_evolution': {'func': calc_time_evolution_schrodinger, 'params': ['initial_state', 'H_matrix', 't'], 'desc': 'Schrodinger time evolution U=exp(-iHt/hbar)'},
    'commutator': {'func': calc_commutator, 'params': ['A', 'B'], 'desc': 'Commutator [A,B] = AB - BA'},
    'ehrenfest': {'func': calc_ehrenfest_theorem, 'params': ['psi_values', 'x_values', 'V_func'], 'desc': 'Ehrenfest theorem numerical verification'},
    'density_matrix': {'func': calc_density_matrix, 'params': ['pure_state', 'mixed_probs', 'mixed_states'], 'desc': 'Density matrix construction and purity'},
    'zeno_effect': {'func': calc_quantum_zeno_effect, 'params': ['decay_rate', 'n_measurements', 'total_time'], 'desc': 'Quantum Zeno effect survival probability'},
    'rabi': {'func': calc_rabi_oscillation, 'params': ['rabi_freq', 'detuning', 'time_s'], 'desc': 'Rabi oscillation probability'},
    'adiabatic': {'func': calc_adiabatic_theorem, 'params': ['H_initial', 'H_final', 'sweep_time'], 'desc': 'Adiabatic theorem condition check'},
    'landau_zener': {'func': calc_landau_zener_probability, 'params': ['energy_gap', 'sweep_rate'], 'desc': 'Landau-Zener nonadiabatic transition probability'},
    'clebsch_gordan': {'func': calc_clebsch_gordan, 'params': ['j1', 'j2', 'm1', 'm2', 'J', 'M'], 'desc': 'Clebsch-Gordan coefficient for angular momentum coupling'},
    'no_cloning': {'func': calc_no_cloning_theorem, 'params': ['state_a', 'state_b'], 'desc': 'No-cloning theorem numerical demonstration'},
    'ehrenfest_oscillator': {'func': calc_ehrenfest_oscillator, 'params': ['x0', 'p0', 'omega', 't_span', 'n_steps'], 'desc': 'Ehrenfest expectation evolution for oscillator'},
    'perturbation': {'func': calc_perturbation_theory_1st_order, 'params': ['unperturbed_energies', 'perturbation_matrix'], 'desc': 'First-order perturbation theory correction'},
    'variational': {'func': calc_variational_principle, 'params': ['trial_params'], 'desc': 'Variational principle energy minimization'},
    'qft': {'func': calc_quantum_fourier_transform, 'params': ['state'], 'desc': 'Quantum Fourier Transform on computational basis'},
    'grover': {'func': calc_grover_iteration, 'params': ['target_index', 'n_qubits'], 'desc': 'Grover search optimal iterations count'},
    'decoherence': {'func': calc_decoherence_off_diagonal, 'params': ['t', 'gamma'], 'desc': 'Decoherence off-diagonal element decay'},
    'semiclassical_tunneling': {'func': calc_semiclassical_tunneling, 'params': ['mass_kg', 'barrier_func', 'E', 'params'], 'desc': 'Semiclassical tunneling via WKB exponent'},
    'number_phase': {'func': calc_number_phase_uncertainty, 'params': ['n_mean'], 'desc': 'Number-phase uncertainty relation'}
}
