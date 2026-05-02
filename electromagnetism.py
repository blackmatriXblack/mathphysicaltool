"""
Electromagnetism - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}

# =============================================================================
# ELECTROSTATICS
# =============================================================================

def calc_coulomb_force(q1: float = 1e-6, q2: float = 2e-6, r: float = 0.1) -> dict:
    """Coulomb's law: F = k * q1 * q2 / r^2."""
    k = 8.9875517923e9  # 1/(4*pi*epsilon0)
    F = k * q1 * q2 / (r * r)
    return {
        'result': f'Force F = {F:.4f} N (attractive if negative, repulsive if positive)',
        'details': {'k': k, 'q1': q1, 'q2': q2, 'distance_r': r, 'force_F': F},
        'unit': 'N'
    }


def calc_electric_field(q: float = 1e-6, r: float = 0.1) -> dict:
    """Electric field from a point charge: E = k * q / r^2."""
    k = 8.9875517923e9
    E = k * q / (r * r)
    return {
        'result': f'Electric field E = {E:.2f} N/C = {E:.2f} V/m',
        'details': {'k': k, 'source_charge_q': q, 'distance_r': r, 'electric_field_E': E},
        'unit': 'N/C'
    }


def calc_electric_field_force(q: float = 1e-6, E: float = 1e5) -> dict:
    """Force on a charge in an electric field: F = q * E."""
    F = q * E
    return {
        'result': f'Force F = {F:.4e} N',
        'details': {'charge_q': q, 'electric_field_E': E, 'force_F': F},
        'unit': 'N'
    }


def calc_electric_potential(q: float = 1e-6, r: float = 0.1) -> dict:
    """Electric potential from a point charge: V = k * q / r."""
    k = 8.9875517923e9
    V = k * q / r
    return {
        'result': f'Potential V = {V:.2f} V',
        'details': {'k': k, 'charge_q': q, 'distance_r': r, 'potential_V': V},
        'unit': 'V'
    }


def calc_potential_energy(q1: float = 1e-6, q2: float = 2e-6, r: float = 0.1) -> dict:
    """Electrostatic potential energy: U = k * q1 * q2 / r."""
    k = 8.9875517923e9
    U = k * q1 * q2 / r
    return {
        'result': f'Potential energy U = {U:.4e} J',
        'details': {'k': k, 'q1': q1, 'q2': q2, 'distance_r': r, 'potential_energy_U': U},
        'unit': 'J'
    }


def calc_electric_field_superposition(q1: float = 1e-6, x1: float = -0.5, y1: float = 0.0,
                                        q2: float = 2e-6, x2: float = 0.5, y2: float = 0.0,
                                        xP: float = 0.0, yP: float = 1.0) -> dict:
    """Superposition of electric fields from two point charges at point P."""
    k = 8.9875517923e9
    dx1, dy1 = xP - x1, yP - y1
    r1 = math.sqrt(dx1 * dx1 + dy1 * dy1)
    dx2, dy2 = xP - x2, yP - y2
    r2 = math.sqrt(dx2 * dx2 + dy2 * dy2)
    if r1 < 1e-15 or r2 < 1e-15:
        return {'result': 'Point P coincides with a charge', 'details': {}, 'unit': 'N/C'}
    Ex = k * q1 * dx1 / (r1 ** 3) + k * q2 * dx2 / (r2 ** 3)
    Ey = k * q1 * dy1 / (r1 ** 3) + k * q2 * dy2 / (r2 ** 3)
    E_mag = math.sqrt(Ex * Ex + Ey * Ey)
    E_dir = math.degrees(math.atan2(Ey, Ex))
    return {
        'result': f'E = {E_mag:.2f} N/C at angle {E_dir:.2f} deg',
        'details': {'Ex': Ex, 'Ey': Ey, 'E_magnitude': E_mag, 'E_direction_deg': E_dir},
        'unit': 'N/C'
    }


def calc_gauss_law_charge(flux: float = 1.0e5, epsilon0: float = 8.8541878128e-12) -> dict:
    """Gauss's law: Q_enc = epsilon0 * flux_E."""
    Q_enc = epsilon0 * flux
    return {
        'result': f'Enclosed charge Q_enc = {Q_enc:.4e} C',
        'details': {'electric_flux': flux, 'epsilon0': epsilon0, 'Q_enclosed': Q_enc},
        'unit': 'C'
    }


def calc_capacitance_parallel_plate(A: float = 0.01, d: float = 0.001,
                                      epsilon0: float = 8.8541878128e-12,
                                      kappa: float = 1.0) -> dict:
    """Parallel plate capacitance: C = kappa * epsilon0 * A / d."""
    epsilon = kappa * epsilon0
    C = epsilon * A / d
    return {
        'result': f'Capacitance C = {C:.4e} F = {C*1e6:.4f} uF = {C*1e12:.4f} pF',
        'details': {'area_A': A, 'separation_d': d, 'dielectric_constant_kappa': kappa,
                    'epsilon': epsilon, 'capacitance_C': C},
        'unit': 'F'
    }


def calc_capacitance_series(C_list: list = None) -> dict:
    """Equivalent capacitance for capacitors in series: 1/C_eq = sum(1/C_i)."""
    if C_list is None:
        C_list = [1e-6, 2e-6, 3e-6]
    reciprocal_sum = sum(1.0 / c for c in C_list)
    C_eq = 1.0 / reciprocal_sum
    return {
        'result': f'Series equivalent C_eq = {C_eq:.4e} F',
        'details': {'individual_C': C_list, 'C_eq': C_eq},
        'unit': 'F'
    }


def calc_capacitance_parallel(C_list: list = None) -> dict:
    """Equivalent capacitance for capacitors in parallel: C_eq = sum(C_i)."""
    if C_list is None:
        C_list = [1e-6, 2e-6, 3e-6]
    C_eq = sum(C_list)
    return {
        'result': f'Parallel equivalent C_eq = {C_eq:.4e} F',
        'details': {'individual_C': C_list, 'C_eq': C_eq},
        'unit': 'F'
    }


def calc_capacitor_energy(C: float = 1e-6, V: float = 100.0) -> dict:
    """Energy stored in a capacitor: U = 0.5 * C * V^2."""
    U = 0.5 * C * V * V
    Q = C * V
    return {
        'result': f'Stored energy U = {U:.4e} J, Charge Q = {Q:.4e} C',
        'details': {'capacitance_C': C, 'voltage_V': V, 'energy_U': U, 'charge_Q': Q},
        'unit': 'J'
    }


# =============================================================================
# DC CIRCUITS
# =============================================================================

def calc_ohms_law(V: float | None = None, I: float = 2.0, R: float = 50.0) -> dict:
    """Ohm's law: V = I * R. Set unknown parameter to None."""
    if V is None:
        V = I * R
        solved = 'V'
    elif I is None:
        I = V / R if R != 0 else float('inf')
        solved = 'I'
    elif R is None:
        R = V / I if I != 0 else float('inf')
        solved = 'R'
    else:
        V_val = I * R
        return {'result': f'V = {V_val:.4f} V (all given)', 'details': {'V': V_val, 'I': I, 'R': R}, 'unit': 'V'}
    values = {'V': V, 'I': I, 'R': R}
    units = {'V': 'V', 'I': 'A', 'R': 'Ohm'}
    return {
        'result': f'{solved} = {values[solved]:.4f} {units[solved]}',
        'details': values,
        'unit': units[solved]
    }


def calc_resistance(rho: float = 1.68e-8, L: float = 1.0, A: float = 3.14e-6) -> dict:
    """Resistance of a wire: R = rho * L / A."""
    R = rho * L / A
    return {
        'result': f'Resistance R = {R:.4f} Ohm',
        'details': {'resistivity_rho': rho, 'length_L': L, 'cross_section_A': A, 'resistance_R': R},
        'unit': 'Ohm'
    }


def calc_resistance_series(R_list: list = None) -> dict:
    """Equivalent resistance for series: R_eq = sum(R_i)."""
    if R_list is None:
        R_list = [100.0, 200.0, 300.0]
    R_eq = sum(R_list)
    return {
        'result': f'Series equivalent R_eq = {R_eq:.2f} Ohm',
        'details': {'individual_R': R_list, 'R_eq': R_eq},
        'unit': 'Ohm'
    }


def calc_resistance_parallel(R_list: list = None) -> dict:
    """Equivalent resistance for parallel: 1/R_eq = sum(1/R_i)."""
    if R_list is None:
        R_list = [100.0, 200.0]
    reciprocal_sum = sum(1.0 / r for r in R_list)
    R_eq = 1.0 / reciprocal_sum
    return {
        'result': f'Parallel equivalent R_eq = {R_eq:.4f} Ohm',
        'details': {'individual_R': R_list, 'R_eq': R_eq},
        'unit': 'Ohm'
    }


def calc_electric_power_VI(V: float = 120.0, I: float = 5.0) -> dict:
    """Electric power: P = V * I."""
    P = V * I
    R = V / I if I != 0 else float('inf')
    return {
        'result': f'Power P = {P:.2f} W',
        'details': {'voltage_V': V, 'current_I': I, 'power_P': P, 'equivalent_R': R},
        'unit': 'W'
    }


def calc_electric_power_IR(I: float = 5.0, R: float = 24.0) -> dict:
    """Electric power from Joule heating: P = I^2 * R."""
    P = I * I * R
    V = I * R
    return {
        'result': f'Power P = {P:.2f} W',
        'details': {'current_I': I, 'resistance_R': R, 'power_P': P, 'voltage_V': V},
        'unit': 'W'
    }


def calc_kirchhoff_voltage(V_supply: float = 12.0, R_list: list = None) -> dict:
    """Kirchhoff's voltage law for a series circuit: sum(V) = 0. Returns voltage drops."""
    if R_list is None:
        R_list = [100.0, 200.0, 300.0]
    R_total = sum(R_list)
    I = V_supply / R_total
    voltage_drops = [I * r for r in R_list]
    V_sum = sum(voltage_drops)
    return {
        'result': f'Current I = {I:.6f} A, Individual voltage drops: {[f"{v:.4f}V" for v in voltage_drops]}',
        'details': {'V_supply': V_supply, 'R_list': R_list, 'R_total': R_total,
                    'current_I': I, 'voltage_drops': voltage_drops,
                    'sum_voltage_drops': V_sum, 'KVL_satisfied': abs(V_sum - V_supply) < 1e-9},
        'unit': 'V'
    }


def calc_kirchhoff_current(I_in_list: list = None, I_out_list: list = None) -> dict:
    """Kirchhoff's current law: sum of currents in = sum of currents out."""
    if I_in_list is None:
        I_in_list = [2.0, 3.0, 1.0]
    if I_out_list is None:
        I_out_list = [4.0, 2.0]
    sum_in = sum(I_in_list)
    sum_out = sum(I_out_list)
    net = sum_in - sum_out
    return {
        'result': f'sum(I_in) = {sum_in:.4f} A, sum(I_out) = {sum_out:.4f} A, net = {net:.4e} A, KCL: {abs(net) < 1e-9}',
        'details': {'I_in': I_in_list, 'I_out': I_out_list, 'sum_in': sum_in,
                    'sum_out': sum_out, 'net': net, 'KCL_satisfied': abs(net) < 1e-9},
        'unit': 'A'
    }


def calc_rc_charging(V0: float = 10.0, R: float = 1000.0, C: float = 1e-6, t: float = 0.001) -> dict:
    """RC circuit charging: Vc(t) = V0*(1 - e^(-t/RC)), I(t) = (V0/R)*e^(-t/RC)."""
    tau = R * C
    Vc = V0 * (1.0 - math.exp(-t / tau))
    I = (V0 / R) * math.exp(-t / tau)
    Q = C * Vc
    return {
        'result': f'At t={t:.6f}s: Vc = {Vc:.4f} V, I = {I:.6f} A, tau = {tau:.6f} s',
        'details': {'V0': V0, 'R': R, 'C': C, 't': t, 'tau': tau,
                    'Vc': Vc, 'I': I, 'charge_Q': Q},
        'unit': 'V'
    }


def calc_rc_discharging(V0: float = 10.0, R: float = 1000.0, C: float = 1e-6, t: float = 0.001) -> dict:
    """RC circuit discharging: Vc(t) = V0 * e^(-t/RC)."""
    tau = R * C
    Vc = V0 * math.exp(-t / tau)
    I = -(V0 / R) * math.exp(-t / tau)
    return {
        'result': f'At t={t:.6f}s: Vc = {Vc:.4f} V, tau = {tau:.6f} s',
        'details': {'V0': V0, 'R': R, 'C': C, 't': t, 'tau': tau, 'Vc': Vc, 'I': I},
        'unit': 'V'
    }


# =============================================================================
# MAGNETOSTATICS
# =============================================================================

def calc_magnetic_field_wire(I: float = 10.0, r: float = 0.01) -> dict:
    """Magnetic field around a long straight wire: B = mu0 * I / (2*pi*r)."""
    mu0 = 1.25663706212e-6
    B = mu0 * I / (2.0 * math.pi * r)
    return {
        'result': f'B = {B:.4e} T = {B*1e4:.4f} Gauss',
        'details': {'mu0': mu0, 'current_I': I, 'distance_r': r, 'B': B},
        'unit': 'T'
    }


def calc_magnetic_field_solenoid(n: float = 1000.0, I: float = 1.0) -> dict:
    """Magnetic field inside an ideal solenoid: B = mu0 * n * I (n = turns/m)."""
    mu0 = 1.25663706212e-6
    B = mu0 * n * I
    return {
        'result': f'B = {B:.4e} T = {B*1e4:.4f} Gauss',
        'details': {'mu0': mu0, 'turns_per_meter_n': n, 'current_I': I, 'B': B},
        'unit': 'T'
    }


def calc_amperes_law(I_enclosed: float = 5.0, r: float = 0.05) -> dict:
    """Ampere's law for a circular path: B * (2*pi*r) = mu0 * I_enc."""
    mu0 = 1.25663706212e-6
    B = mu0 * I_enclosed / (2.0 * math.pi * r)
    return {
        'result': f'B = {B:.4e} T',
        'details': {'mu0': mu0, 'I_enclosed': I_enclosed, 'path_radius_r': r, 'B': B},
        'unit': 'T'
    }


def calc_force_on_current_wire(I: float = 5.0, L: float = 0.1, B: float = 0.5, angle_deg: float = 90.0) -> dict:
    """Force on a current-carrying wire: F = I * L * B * sin(theta)."""
    theta = math.radians(angle_deg)
    F = I * L * B * math.sin(theta)
    return {
        'result': f'Force F = {F:.4f} N',
        'details': {'current_I': I, 'length_L': L, 'B_field': B,
                    'angle_deg': angle_deg, 'theta_rad': theta, 'force_F': F},
        'unit': 'N'
    }


def calc_lorentz_force(q: float = 1.6e-19, v: float = 1e6, B: float = 0.5, angle_deg: float = 90.0) -> dict:
    """Lorentz force: F = q * v * B * sin(theta)."""
    theta = math.radians(angle_deg)
    F = abs(q) * v * B * math.sin(theta)
    return {
        'result': f'Lorentz force F = {F:.4e} N',
        'details': {'charge_q': q, 'velocity_v': v, 'B_field': B,
                    'angle_deg': angle_deg, 'theta_rad': theta, 'force_F': F},
        'unit': 'N'
    }


def calc_torque_on_loop(N: float = 100.0, I: float = 1.0, A: float = 0.01, B: float = 0.5,
                         angle_deg: float = 90.0) -> dict:
    """Torque on a current loop: tau = N * I * A * B * sin(theta)."""
    theta = math.radians(angle_deg)
    magnetic_moment = N * I * A
    tau = magnetic_moment * B * math.sin(theta)
    return {
        'result': f'Torque tau = {tau:.4e} N*m, magnetic moment mu = {magnetic_moment:.4e} A*m^2',
        'details': {'turns_N': N, 'current_I': I, 'area_A': A, 'B': B,
                    'angle_deg': angle_deg, 'magnetic_moment': magnetic_moment, 'torque_tau': tau},
        'unit': 'N*m'
    }


# =============================================================================
# ELECTROMAGNETIC INDUCTION
# =============================================================================

def calc_faraday_emf(N: float = 100.0, delta_flux: float = 0.001, delta_t: float = 0.01) -> dict:
    """Faraday's law: emf = -N * delta_flux / delta_t."""
    emf = -N * delta_flux / delta_t
    return {
        'result': f'Induced EMF epsilon = {emf:.4f} V',
        'details': {'turns_N': N, 'flux_change': delta_flux,
                    'time_interval': delta_t, 'induced_emf': emf},
        'unit': 'V'
    }


def calc_motional_emf(B: float = 0.5, L: float = 1.0, v: float = 10.0) -> dict:
    """Motional EMF: epsilon = B * L * v (perpendicular B, L, v)."""
    emf = B * L * v
    return {
        'result': f'Motional EMF epsilon = {emf:.4f} V',
        'details': {'B_field': B, 'conductor_length_L': L, 'velocity_v': v,
                    'emf': emf},
        'unit': 'V'
    }


def calc_self_inductance_emf(L: float = 0.01, delta_I: float = 2.0, delta_t: float = 0.001) -> dict:
    """Self-induced EMF: epsilon = -L * delta_I / delta_t."""
    emf = -L * delta_I / delta_t
    return {
        'result': f'Self-induced EMF epsilon = {emf:.4f} V',
        'details': {'inductance_L': L, 'current_change': delta_I,
                    'time_interval': delta_t, 'induced_emf': emf},
        'unit': 'V'
    }


def calc_mutual_inductance_emf(M: float = 0.005, delta_I1: float = 3.0, delta_t: float = 0.01) -> dict:
    """Mutually induced EMF: epsilon2 = -M * delta_I1 / delta_t."""
    emf2 = -M * delta_I1 / delta_t
    return {
        'result': f'Mutually induced EMF epsilon2 = {emf2:.4f} V',
        'details': {'mutual_inductance_M': M, 'current_change_coil1': delta_I1,
                    'time_interval': delta_t, 'emf2': emf2},
        'unit': 'V'
    }


def calc_lr_circuit_current(V0: float = 12.0, R: float = 100.0, L: float = 0.01, t: float = 0.0001) -> dict:
    """LR circuit current rise: I(t) = (V0/R)*(1 - e^(-R*t/L))."""
    tau = L / R
    I = (V0 / R) * (1.0 - math.exp(-R * t / L))
    I_max = V0 / R
    return {
        'result': f'At t={t:.6f}s: I = {I:.6f} A (max = {I_max:.6f} A), tau = {tau:.6e} s',
        'details': {'V0': V0, 'R': R, 'L': L, 't': t, 'tau': tau,
                    'current_I': I, 'I_max': I_max},
        'unit': 'A'
    }


def calc_inductor_energy(L: float = 0.01, I: float = 2.0) -> dict:
    """Energy stored in an inductor: U = 0.5 * L * I^2."""
    U = 0.5 * L * I * I
    return {
        'result': f'Inductor energy U = {U:.6f} J',
        'details': {'inductance_L': L, 'current_I': I, 'energy_U': U},
        'unit': 'J'
    }


# =============================================================================
# AC CIRCUITS
# =============================================================================

def calc_rms_values(V_peak: float = 170.0, I_peak: float = 5.0) -> dict:
    """RMS values from peak: V_rms = V_peak / sqrt(2), I_rms = I_peak / sqrt(2)."""
    sqrt2 = math.sqrt(2.0)
    V_rms = V_peak / sqrt2
    I_rms = I_peak / sqrt2
    P_avg = V_rms * I_rms
    return {
        'result': f'V_rms = {V_rms:.2f} V, I_rms = {I_rms:.2f} A, P_avg = {P_avg:.2f} W',
        'details': {'V_peak': V_peak, 'I_peak': I_peak, 'V_rms': V_rms,
                    'I_rms': I_rms, 'average_power': P_avg},
        'unit': 'V'
    }


def calc_inductive_reactance(L: float = 0.1, f: float = 60.0) -> dict:
    """Inductive reactance: X_L = omega * L = 2*pi*f * L."""
    omega = 2.0 * math.pi * f
    X_L = omega * L
    return {
        'result': f'X_L = {X_L:.4f} Ohm (omega = {omega:.4f} rad/s)',
        'details': {'inductance_L': L, 'frequency_f': f, 'omega': omega, 'X_L': X_L},
        'unit': 'Ohm'
    }


def calc_capacitive_reactance(C: float = 1e-6, f: float = 60.0) -> dict:
    """Capacitive reactance: X_C = 1 / (omega * C) = 1 / (2*pi*f * C)."""
    omega = 2.0 * math.pi * f
    X_C = 1.0 / (omega * C)
    return {
        'result': f'X_C = {X_C:.4f} Ohm (omega = {omega:.4f} rad/s)',
        'details': {'capacitance_C': C, 'frequency_f': f, 'omega': omega, 'X_C': X_C},
        'unit': 'Ohm'
    }


def calc_impedance_RLC(R: float = 100.0, L: float = 0.1, C: float = 1e-6, f: float = 1000.0) -> dict:
    """RLC series impedance: Z = sqrt(R^2 + (X_L - X_C)^2)."""
    omega = 2.0 * math.pi * f
    X_L = omega * L
    X_C = 1.0 / (omega * C)
    Z = math.sqrt(R * R + (X_L - X_C) ** 2)
    phi = math.atan2(X_L - X_C, R) if R != 0 else (math.pi / 2.0 if X_L > X_C else -math.pi / 2.0)
    phi_deg = math.degrees(phi)
    return {
        'result': f'Z = {Z:.4f} Ohm, X_L = {X_L:.4f} Ohm, X_C = {X_C:.4f} Ohm, phi = {phi_deg:.2f} deg',
        'details': {'R': R, 'L': L, 'C': C, 'f': f, 'omega': omega,
                    'X_L': X_L, 'X_C': X_C, 'Z': Z, 'phase_rad': phi, 'phase_deg': phi_deg},
        'unit': 'Ohm'
    }


def calc_lc_resonance(L: float = 0.01, C: float = 1e-6) -> dict:
    """LC circuit resonant frequency: omega_0 = 1 / sqrt(L*C), f_0 = omega_0 / (2*pi)."""
    omega_0 = 1.0 / math.sqrt(L * C)
    f_0 = omega_0 / (2.0 * math.pi)
    T = 1.0 / f_0
    return {
        'result': f'Resonance f_0 = {f_0:.2f} Hz, omega_0 = {omega_0:.2f} rad/s, T = {T:.6f} s',
        'details': {'L': L, 'C': C, 'omega_0': omega_0, 'f_0': f_0, 'period_T': T},
        'unit': 'Hz'
    }


def calc_phase_angle(X_L: float = 62.83, X_C: float = 26.53, R: float = 50.0) -> dict:
    """Phase angle in RLC circuit: phi = arctan((X_L - X_C) / R)."""
    phi = math.atan2(X_L - X_C, R)
    phi_deg = math.degrees(phi)
    pf = math.cos(phi)
    return {
        'result': f'Phase angle phi = {phi_deg:.2f} deg, Power factor cos(phi) = {pf:.4f}',
        'details': {'X_L': X_L, 'X_C': X_C, 'R': R, 'phi_rad': phi,
                    'phi_deg': phi_deg, 'power_factor': pf},
        'unit': 'rad'
    }


def calc_rlc_circuit_analysis(R: float = 100.0, L: float = 0.1, C: float = 1e-6,
                                V_rms: float = 120.0, f: float = 1000.0) -> dict:
    """Full RLC series circuit analysis at a given frequency."""
    omega = 2.0 * math.pi * f
    X_L = omega * L
    X_C = 1.0 / (omega * C)
    Z = math.sqrt(R * R + (X_L - X_C) ** 2)
    I_rms = V_rms / Z
    phi = math.atan2(X_L - X_C, R)
    phi_deg = math.degrees(phi)
    P_avg = V_rms * I_rms * math.cos(phi)
    V_R = I_rms * R
    V_L = I_rms * X_L
    V_C = I_rms * X_C
    Q_factor_lc = X_L / R if R > 0 else float('inf')
    return {
        'result': f'Z = {Z:.2f} Ohm, I_rms = {I_rms:.4f} A, phi = {phi_deg:.2f} deg, P_avg = {P_avg:.2f} W',
        'details': {'R': R, 'L': L, 'C': C, 'f': f, 'omega': omega,
                    'X_L': X_L, 'X_C': X_C, 'Z': Z, 'I_rms': I_rms,
                    'phi_rad': phi, 'phi_deg': phi_deg, 'P_avg': P_avg,
                    'V_R': V_R, 'V_L': V_L, 'V_C': V_C, 'Q_factor': Q_factor_lc},
        'unit': 'Ohm'
    }


# =============================================================================
# MAXWELL'S EQUATIONS AND EM WAVES
# =============================================================================

def calc_em_wave_speed(mu_r: float = 1.0, epsilon_r: float = 1.0) -> dict:
    """Speed of EM waves: c = 1 / sqrt(mu0*mu_r * epsilon0*epsilon_r)."""
    mu0 = 1.25663706212e-6
    epsilon0 = 8.8541878128e-12
    c = 1.0 / math.sqrt(mu0 * mu_r * epsilon0 * epsilon_r)
    c_vacuum = 1.0 / math.sqrt(mu0 * epsilon0)
    return {
        'result': f'c = {c:.2f} m/s (vacuum: {c_vacuum:.2f} m/s), n = {c_vacuum/c:.4f}',
        'details': {'mu_r': mu_r, 'epsilon_r': epsilon_r, 'c': c,
                    'c_vacuum': c_vacuum, 'refractive_index': c_vacuum / c},
        'unit': 'm/s'
    }


def calc_displacement_current(epsilon0: float = 8.8541878128e-12,
                                dE_dt: float = 1e12, A: float = 0.01) -> dict:
    """Displacement current: I_d = epsilon0 * dPhi_E/dt = epsilon0 * A * dE/dt."""
    I_d = epsilon0 * A * dE_dt
    return {
        'result': f'Displacement current I_d = {I_d:.4e} A',
        'details': {'epsilon0': epsilon0, 'dE_dt': dE_dt, 'area_A': A, 'I_d': I_d},
        'unit': 'A'
    }


def calc_poynting_vector(E: float = 1000.0, H: float = 2.65) -> dict:
    """Poynting vector magnitude: S = E * H (for perpendicular E and H)."""
    S = E * H
    return {
        'result': f'Poynting vector S = {S:.2f} W/m^2 (instantaneous power per area)',
        'details': {'electric_field_E': E, 'magnetic_field_H': H, 'poynting_S': S},
        'unit': 'W/m^2'
    }


def calc_em_wave_equation(f: float = 1e9) -> dict:
    """EM wave parameters: wavelength, wave number, angular frequency, impedance."""
    c = 299792458.0
    wavelength = c / f
    k = 2.0 * math.pi / wavelength
    omega = 2.0 * math.pi * f
    mu0 = 1.25663706212e-6
    epsilon0 = 8.8541878128e-12
    Z0 = math.sqrt(mu0 / epsilon0)
    return {
        'result': f'lambda = {wavelength:.4f} m, k = {k:.4f} rad/m, omega = {omega:.4e} rad/s, Z0 = {Z0:.2f} Ohm',
        'details': {'frequency_f': f, 'c': c, 'wavelength': wavelength,
                    'wave_number_k': k, 'angular_freq_omega': omega,
                    'impedance_free_space_Z0': Z0},
        'unit': 'm'
    }


# =============================================================================
# CHARGED PARTICLE MOTION
# =============================================================================

def calc_cyclotron_radius(m: float = 9.1093837e-31, v_perp: float = 1e6,
                           q: float = 1.602176634e-19, B: float = 0.5) -> dict:
    """Cyclotron (Larmor) radius: r = m * v_perp / (|q| * B)."""
    r = m * v_perp / (abs(q) * B)
    omega = abs(q) * B / m
    return {
        'result': f'Larmor radius r = {r:.4e} m, cyclotron freq omega_c = {omega:.4e} rad/s',
        'details': {'mass_m': m, 'v_perpendicular': v_perp, 'charge_q': q,
                    'B_field': B, 'larmor_radius_r': r, 'cyclotron_freq_omega': omega},
        'unit': 'm'
    }


def calc_cyclotron_frequency(q: float = 1.602176634e-19, B: float = 0.5,
                               m: float = 9.1093837e-31) -> dict:
    """Cyclotron frequency: omega_c = |q| * B / m."""
    omega_c = abs(q) * B / m
    f_c = omega_c / (2.0 * math.pi)
    T_c = 1.0 / f_c if f_c > 0 else float('inf')
    return {
        'result': f'omega_c = {omega_c:.4e} rad/s, f_c = {f_c:.4e} Hz, T_c = {T_c:.4e} s',
        'details': {'charge_q': q, 'B_field': B, 'mass_m': m,
                    'omega_c': omega_c, 'f_c': f_c, 'T_c': T_c},
        'unit': 'rad/s'
    }


def calc_exb_drift_velocity(E: float = 1000.0, B: float = 0.5) -> dict:
    """E x B drift velocity: v_drift = E / B (perpendicular E and B)."""
    v_drift = E / B
    return {
        'result': f'E x B drift velocity v = {v_drift:.2f} m/s',
        'details': {'E_field': E, 'B_field': B, 'drift_velocity': v_drift},
        'unit': 'm/s'
    }


def calc_charged_particle_trajectory(m: float = 9.1093837e-31, q: float = 1.602176634e-19,
                                       B: float = 0.5, E: float = 100.0,
                                       vx0: float = 1e6, vy0: float = 0.0,
                                       t: float = 1e-9) -> dict:
    """Charged particle position in crossed E(y) and B(z) fields at time t."""
    omega = abs(q) * B / m
    v_drift = E / B
    x = (vx0 / omega) * math.sin(omega * t) + v_drift * t
    y = (vx0 / omega) * (1.0 - math.cos(omega * t))
    z = vy0 * t
    vx = vx0 * math.cos(omega * t) + v_drift
    vy = vx0 * math.sin(omega * t)
    return {
        'result': f'At t={t:.4e}s: x={x:.6e} m, y={y:.6e} m, vx={vx:.4e} m/s, vy={vy:.4e} m/s',
        'details': {'m': m, 'q': q, 'B': B, 'E': E, 'omega': omega,
                    'v_drift': v_drift, 't': t, 'x': x, 'y': y, 'z': z,
                    'vx': vx, 'vy': vy},
        'unit': 'm'
    }


# =============================================================================
# ADDITIONAL EM FUNCTIONS
# =============================================================================

def calc_electric_dipole_moment(q: float = 1e-9, d: float = 0.001) -> dict:
    """Electric dipole moment: p = q * d."""
    p = q * d
    return {
        'result': f'Dipole moment p = {p:.4e} C*m',
        'details': {'charge_q': q, 'separation_d': d, 'dipole_moment_p': p},
        'unit': 'C*m'
    }


def calc_electric_dipole_field(p: float = 1e-12, r: float = 0.01, theta_deg: float = 0.0) -> dict:
    """Electric field from a dipole at (r, theta): E_r = k*2p*cos(theta)/r^3, E_theta = k*p*sin(theta)/r^3."""
    k = 8.9875517923e9
    theta = math.radians(theta_deg)
    E_r = k * 2.0 * p * math.cos(theta) / (r ** 3)
    E_theta = k * p * math.sin(theta) / (r ** 3)
    E_mag = math.sqrt(E_r * E_r + E_theta * E_theta)
    return {
        'result': f'E_mag = {E_mag:.2f} N/C, E_r = {E_r:.2f}, E_theta = {E_theta:.2f}',
        'details': {'p': p, 'r': r, 'theta_deg': theta_deg, 'E_r': E_r, 'E_theta': E_theta, 'E_mag': E_mag},
        'unit': 'N/C'
    }


def calc_biot_savart(dl: float = 0.01, I: float = 10.0, r: float = 0.05, angle_deg: float = 90.0) -> dict:
    """Biot-Savart law: dB = (mu0/4pi) * I * dl * sin(theta) / r^2."""
    mu0 = 1.25663706212e-6
    theta = math.radians(angle_deg)
    dB = (mu0 / (4.0 * math.pi)) * I * dl * math.sin(theta) / (r * r)
    return {
        'result': f'dB = {dB:.4e} T',
        'details': {'dl': dl, 'I': I, 'r': r, 'angle_deg': angle_deg, 'dB': dB},
        'unit': 'T'
    }


def calc_inductance_solenoid(N: float = 500.0, A: float = 0.001, l: float = 0.1) -> dict:
    """Inductance of a solenoid: L = mu0 * N^2 * A / l."""
    mu0 = 1.25663706212e-6
    L = mu0 * N * N * A / l
    return {
        'result': f'Inductance L = {L:.4e} H = {L*1e3:.4f} mH',
        'details': {'turns_N': N, 'area_A': A, 'length_l': l, 'mu0': mu0, 'inductance_L': L},
        'unit': 'H'
    }


def calc_transformer_voltage(Np: float = 500.0, Ns: float = 100.0, Vp: float = 240.0) -> dict:
    """Ideal transformer: Vs/Vp = Ns/Np, Ip/Is = Ns/Np."""
    Vs = Vp * Ns / Np
    ratio = Ns / Np
    return {
        'result': f'Vs = {Vs:.2f} V, turns ratio = {ratio:.4f}',
        'details': {'N_primary': Np, 'N_secondary': Ns, 'V_primary': Vp,
                    'V_secondary': Vs, 'turns_ratio': ratio},
        'unit': 'V'
    }


def calc_complex_impedance(R: float = 100.0, X: float = 50.0) -> dict:
    """Complex impedance: Z = R + jX, |Z| = sqrt(R^2 + X^2)."""
    Z_mag = math.sqrt(R * R + X * X)
    phi = math.degrees(math.atan2(X, R))
    return {
        'result': f'|Z| = {Z_mag:.4f} Ohm, phi = {phi:.4f} deg',
        'details': {'R': R, 'X': X, 'Z_magnitude': Z_mag, 'phase_deg': phi},
        'unit': 'Ohm'
    }


def calc_q_factor_series(L: float = 0.01, C: float = 1e-6, R: float = 10.0) -> dict:
    """Quality factor for series RLC: Q = (1/R)*sqrt(L/C)."""
    Q = math.sqrt(L / C) / R
    omega_0 = 1.0 / math.sqrt(L * C)
    bandwidth = omega_0 / Q
    return {
        'result': f'Q = {Q:.4f}, BW = {bandwidth:.4f} rad/s = {bandwidth/(2*math.pi):.4f} Hz',
        'details': {'L': L, 'C': C, 'R': R, 'Q_factor': Q,
                    'omega_0': omega_0, 'bandwidth_rad_s': bandwidth},
        'unit': 'dimensionless'
    }


def calc_skin_depth(f: float = 1e6, sigma: float = 5.8e7, mu_r: float = 1.0) -> dict:
    """Skin depth: delta = sqrt(2/(omega*mu0*mu_r*sigma))."""
    mu0 = 1.25663706212e-6
    omega = 2.0 * math.pi * f
    delta = math.sqrt(2.0 / (omega * mu0 * mu_r * sigma))
    return {
        'result': f'Skin depth delta = {delta:.4e} m = {delta*1e3:.4f} mm',
        'details': {'frequency_f': f, 'conductivity_sigma': sigma, 'mu_r': mu_r,
                    'omega': omega, 'skin_depth_delta': delta},
        'unit': 'm'
    }


def calc_waveguide_cutoff(a: float = 0.02286, b: float = 0.01016, mode_m: float = 1.0,
                             mode_n: float = 0.0, epsilon_r: float = 1.0,
                             mu_r: float = 1.0) -> dict:
    """Rectangular waveguide TE_mn cutoff frequency: f_c = c/(2*sqrt(mu_r*epsilon_r)) * sqrt((m/a)^2 + (n/b)^2)."""
    c = 299792458.0
    v = c / math.sqrt(mu_r * epsilon_r)
    f_c = (v / 2.0) * math.sqrt((mode_m / a) ** 2 + (mode_n / b) ** 2)
    lambda_c = v / f_c
    return {
        'result': f'fc_TE{mode_m:.0f}{mode_n:.0f} = {f_c/1e9:.4f} GHz, lambda_c = {lambda_c*1e3:.4f} mm',
        'details': {'a': a, 'b': b, 'm': mode_m, 'n': mode_n,
                    'f_cutoff': f_c, 'lambda_cutoff': lambda_c},
        'unit': 'Hz'
    }


def calc_hall_voltage(I: float = 10.0, B: float = 0.5, d: float = 0.001,
                       n: float = 8.5e28, q: float = -1.602e-19) -> dict:
    """Hall voltage: V_H = I*B/(n*q*d)."""
    V_H = I * B / (n * abs(q) * d)
    R_H = 1.0 / (n * abs(q))
    return {
        'result': f'Hall voltage V_H = {V_H:.4e} V, Hall coefficient R_H = {R_H:.4e} m^3/C',
        'details': {'I': I, 'B': B, 'thickness_d': d, 'carrier_density_n': n,
                    'V_H': V_H, 'R_H': R_H},
        'unit': 'V'
    }


def calc_joule_heating(I: float = 5.0, R: float = 24.0, t: float = 60.0) -> dict:
    """Joule heating energy: Q = I^2 * R * t."""
    Q = I * I * R * t
    P = I * I * R
    return {
        'result': f'Heat energy Q = {Q:.2f} J, Power P = {P:.2f} W',
        'details': {'current_I': I, 'resistance_R': R, 'time_t': t,
                    'energy_Q': Q, 'power_P': P},
        'unit': 'J'
    }


def calc_maxwell_equation_parameters(epsilon0: float = 8.8541878128e-12,
                                       mu0: float = 1.25663706212e-6) -> dict:
    """Key Maxwell equation parameters: c, Z0, and wave impedance."""
    c = 1.0 / math.sqrt(mu0 * epsilon0)
    Z0 = math.sqrt(mu0 / epsilon0)
    return {
        'result': f'c = {c:.2f} m/s, Z0 = {Z0:.2f} Ohm, epsilon0 = {epsilon0:.4e} F/m, mu0 = {mu0:.4e} H/m',
        'details': {'c': c, 'Z0': Z0, 'epsilon0': epsilon0, 'mu0': mu0},
        'unit': 'm/s'
    }


def calc_wheatstone_bridge(R1: float = 100.0, R2: float = 200.0, R3: float = 150.0,
                              V_supply: float = 12.0) -> dict:
    """Wheatstone bridge balanced condition: R4 = R2*R3/R1, bridge voltage calculation."""
    R4_balance = R2 * R3 / R1
    R4 = R4_balance  # balanced
    V_AB = V_supply * (R3 / (R3 + R1) - R4 / (R4 + R2))
    return {
        'result': f'R4_balanced = {R4_balance:.4f} Ohm, V_bridge = {V_AB:.6f} V',
        'details': {'R1': R1, 'R2': R2, 'R3': R3, 'R4': R4,
                    'V_supply': V_supply, 'V_bridge': V_AB, 'balanced': abs(V_AB) < 1e-9},
        'unit': 'Ohm / V'
    }


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Electrostatics
    'coulomb_force': {'func': calc_coulomb_force, 'params': ['q1', 'q2', 'r'],
                      'desc': "Coulomb's law F = k*q1*q2/r^2"},
    'electric_field': {'func': calc_electric_field, 'params': ['q', 'r'],
                       'desc': 'Electric field from point charge E = kq/r^2'},
    'electric_field_force': {'func': calc_electric_field_force, 'params': ['q', 'E'],
                              'desc': 'Force on charge in E field F = qE'},
    'electric_potential': {'func': calc_electric_potential, 'params': ['q', 'r'],
                            'desc': 'Electric potential V = kq/r'},
    'potential_energy': {'func': calc_potential_energy, 'params': ['q1', 'q2', 'r'],
                          'desc': 'Electrostatic potential energy U = k*q1*q2/r'},
    'electric_field_superposition': {'func': calc_electric_field_superposition,
                                      'params': ['q1', 'x1', 'y1', 'q2', 'x2', 'y2', 'xP', 'yP'],
                                      'desc': 'Superposition of E-field from two charges'},
    'gauss_law_charge': {'func': calc_gauss_law_charge, 'params': ['flux', 'epsilon0'],
                          'desc': "Gauss's law Q_enc = epsilon0*flux"},
    'capacitance_parallel_plate': {'func': calc_capacitance_parallel_plate,
                                    'params': ['A', 'd', 'epsilon0', 'kappa'],
                                    'desc': 'Parallel plate capacitance C = kappa*epsilon0*A/d'},
    'capacitance_series': {'func': calc_capacitance_series, 'params': ['C_list'],
                            'desc': 'Equivalent capacitance for series'},
    'capacitance_parallel': {'func': calc_capacitance_parallel, 'params': ['C_list'],
                              'desc': 'Equivalent capacitance for parallel'},
    'capacitor_energy': {'func': calc_capacitor_energy, 'params': ['C', 'V'],
                          'desc': 'Energy in capacitor U = 0.5*C*V^2'},
    # DC Circuits
    'ohms_law': {'func': calc_ohms_law, 'params': ['V', 'I', 'R'],
                 'desc': "Ohm's law V=IR; set unknown to None"},
    'resistance': {'func': calc_resistance, 'params': ['rho', 'L', 'A'],
                   'desc': 'Wire resistance R = rho*L/A'},
    'resistance_series': {'func': calc_resistance_series, 'params': ['R_list'],
                           'desc': 'Resistors in series R_eq = sum(R_i)'},
    'resistance_parallel': {'func': calc_resistance_parallel, 'params': ['R_list'],
                             'desc': 'Resistors in parallel 1/R_eq = sum(1/R_i)'},
    'electric_power_VI': {'func': calc_electric_power_VI, 'params': ['V', 'I'],
                           'desc': 'Power P = V*I'},
    'electric_power_IR': {'func': calc_electric_power_IR, 'params': ['I', 'R'],
                           'desc': 'Joule heating P = I^2*R'},
    'kirchhoff_voltage': {'func': calc_kirchhoff_voltage, 'params': ['V_supply', 'R_list'],
                           'desc': "Kirchhoff's voltage law for series circuit"},
    'kirchhoff_current': {'func': calc_kirchhoff_current, 'params': ['I_in_list', 'I_out_list'],
                           'desc': "Kirchhoff's current law sum(I_in)=sum(I_out)"},
    'rc_charging': {'func': calc_rc_charging, 'params': ['V0', 'R', 'C', 't'],
                     'desc': 'RC circuit charging Vc = V0*(1 - e^{-t/RC})'},
    'rc_discharging': {'func': calc_rc_discharging, 'params': ['V0', 'R', 'C', 't'],
                        'desc': 'RC circuit discharging Vc = V0*e^{-t/RC}'},
    # Magnetostatics
    'magnetic_field_wire': {'func': calc_magnetic_field_wire, 'params': ['I', 'r'],
                             'desc': 'B-field around long wire B = mu0*I/(2*pi*r)'},
    'magnetic_field_solenoid': {'func': calc_magnetic_field_solenoid, 'params': ['n', 'I'],
                                 'desc': 'B-field inside solenoid B = mu0*n*I'},
    'amperes_law': {'func': calc_amperes_law, 'params': ['I_enclosed', 'r'],
                     'desc': "Ampere's law B*(2*pi*r) = mu0*I_enc"},
    'force_on_current_wire': {'func': calc_force_on_current_wire,
                               'params': ['I', 'L', 'B', 'angle_deg'],
                               'desc': 'Force on current wire F = ILB sin(theta)'},
    'lorentz_force': {'func': calc_lorentz_force, 'params': ['q', 'v', 'B', 'angle_deg'],
                       'desc': 'Lorentz force F = qvB sin(theta)'},
    'torque_on_loop': {'func': calc_torque_on_loop, 'params': ['N', 'I', 'A', 'B', 'angle_deg'],
                        'desc': 'Torque on current loop tau = NIAB sin(theta)'},
    # EM Induction
    'faraday_emf': {'func': calc_faraday_emf, 'params': ['N', 'delta_flux', 'delta_t'],
                     'desc': "Faraday's law emf = -N*dPhi/dt"},
    'motional_emf': {'func': calc_motional_emf, 'params': ['B', 'L', 'v'],
                      'desc': 'Motional EMF epsilon = BLv'},
    'self_inductance_emf': {'func': calc_self_inductance_emf, 'params': ['L', 'delta_I', 'delta_t'],
                             'desc': 'Self-induced EMF epsilon = -L*dI/dt'},
    'mutual_inductance_emf': {'func': calc_mutual_inductance_emf,
                               'params': ['M', 'delta_I1', 'delta_t'],
                               'desc': 'Mutual EMF epsilon2 = -M*dI1/dt'},
    'lr_circuit_current': {'func': calc_lr_circuit_current, 'params': ['V0', 'R', 'L', 't'],
                            'desc': 'LR circuit I(t) = (V0/R)*(1 - e^{-Rt/L})'},
    'inductor_energy': {'func': calc_inductor_energy, 'params': ['L', 'I'],
                         'desc': 'Energy in inductor U = 0.5*L*I^2'},
    # AC Circuits
    'rms_values': {'func': calc_rms_values, 'params': ['V_peak', 'I_peak'],
                    'desc': 'RMS values from peak V/sqrt(2), I/sqrt(2)'},
    'inductive_reactance': {'func': calc_inductive_reactance, 'params': ['L', 'f'],
                              'desc': 'Inductive reactance X_L = 2*pi*f*L'},
    'capacitive_reactance': {'func': calc_capacitive_reactance, 'params': ['C', 'f'],
                               'desc': 'Capacitive reactance X_C = 1/(2*pi*f*C)'},
    'impedance_RLC': {'func': calc_impedance_RLC, 'params': ['R', 'L', 'C', 'f'],
                       'desc': 'RLC impedance Z = sqrt(R^2+(XL-XC)^2)'},
    'lc_resonance': {'func': calc_lc_resonance, 'params': ['L', 'C'],
                      'desc': 'LC resonance f_0 = 1/(2*pi*sqrt(LC))'},
    'phase_angle': {'func': calc_phase_angle, 'params': ['X_L', 'X_C', 'R'],
                     'desc': 'Phase angle phi = arctan((XL-XC)/R)'},
    'rlc_circuit_analysis': {'func': calc_rlc_circuit_analysis,
                               'params': ['R', 'L', 'C', 'V_rms', 'f'],
                               'desc': 'Full RLC series circuit analysis'},
    # Maxwell & EM Waves
    'em_wave_speed': {'func': calc_em_wave_speed, 'params': ['mu_r', 'epsilon_r'],
                       'desc': 'EM wave speed c = 1/sqrt(mu*epsilon)'},
    'displacement_current': {'func': calc_displacement_current, 'params': ['epsilon0', 'dE_dt', 'A'],
                              'desc': 'Displacement current I_d = epsilon0*A*dE/dt'},
    'poynting_vector': {'func': calc_poynting_vector, 'params': ['E', 'H'],
                          'desc': 'Poynting vector S = E x H'},
    'em_wave_equation': {'func': calc_em_wave_equation, 'params': ['f'],
                           'desc': 'EM wave parameters: lambda, k, omega, Z0'},
    # Charged Particle Motion
    'cyclotron_radius': {'func': calc_cyclotron_radius, 'params': ['m', 'v_perp', 'q', 'B'],
                          'desc': 'Cyclotron/Larmor radius r = mv/(qB)'},
    'cyclotron_frequency': {'func': calc_cyclotron_frequency, 'params': ['q', 'B', 'm'],
                             'desc': 'Cyclotron frequency omega_c = qB/m'},
    'exb_drift_velocity': {'func': calc_exb_drift_velocity, 'params': ['E', 'B'],
                             'desc': 'E x B drift velocity v = E/B'},
    'charged_particle_trajectory': {'func': calc_charged_particle_trajectory,
                                      'params': ['m', 'q', 'B', 'E', 'vx0', 'vy0', 't'],
                                      'desc': 'Charged particle trajectory in E x B fields'},
    # Additional
    'electric_dipole_moment': {'func': calc_electric_dipole_moment, 'params': ['q', 'd'],
                                'desc': 'Electric dipole moment p = q*d'},
    'electric_dipole_field': {'func': calc_electric_dipole_field, 'params': ['p', 'r', 'theta_deg'],
                               'desc': 'Electric field from dipole at (r, theta)'},
    'biot_savart': {'func': calc_biot_savart, 'params': ['dl', 'I', 'r', 'angle_deg'],
                     'desc': 'Biot-Savart law dB = (mu0/4pi)*I*dl*sin(theta)/r^2'},
    'inductance_solenoid': {'func': calc_inductance_solenoid, 'params': ['N', 'A', 'l'],
                             'desc': 'Solenoid inductance L = mu0*N^2*A/l'},
    'transformer_voltage': {'func': calc_transformer_voltage, 'params': ['Np', 'Ns', 'Vp'],
                             'desc': 'Ideal transformer Vs/Vp = Ns/Np'},
    'complex_impedance': {'func': calc_complex_impedance, 'params': ['R', 'X'],
                           'desc': 'Complex impedance Z = R + jX'},
    'q_factor_series': {'func': calc_q_factor_series, 'params': ['L', 'C', 'R'],
                          'desc': 'Quality factor Q = (1/R)*sqrt(L/C)'},
    'skin_depth': {'func': calc_skin_depth, 'params': ['f', 'sigma', 'mu_r'],
                    'desc': 'Skin depth delta = sqrt(2/(omega*mu*sigma))'},
    'waveguide_cutoff': {'func': calc_waveguide_cutoff,
                          'params': ['a', 'b', 'mode_m', 'mode_n', 'epsilon_r', 'mu_r'],
                          'desc': 'Rectangular waveguide TE_mn cutoff frequency'},
    'hall_voltage': {'func': calc_hall_voltage, 'params': ['I', 'B', 'd', 'n', 'q'],
                      'desc': 'Hall effect voltage V_H = I*B/(n*q*d)'},
    'joule_heating': {'func': calc_joule_heating, 'params': ['I', 'R', 't'],
                       'desc': 'Joule heating Q = I^2*R*t'},
    'maxwell_equation_parameters': {'func': calc_maxwell_equation_parameters,
                                      'params': ['epsilon0', 'mu0'],
                                      'desc': 'Key EM constants c, Z0'},
    'wheatstone_bridge': {'func': calc_wheatstone_bridge, 'params': ['R1', 'R2', 'R3', 'V_supply'],
                           'desc': 'Wheatstone bridge balanced condition and voltage'},
}
