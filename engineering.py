"""
Engineering Physics - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_beam_bending_stress(bending_moment: float = 500.0, y_distance: float = 0.05, moment_of_inertia: float = 1.0e-6) -> dict:
    """Bending stress: sigma = M * y / I."""
    sigma = bending_moment * y_distance / moment_of_inertia
    return {
        'result': f'sigma = {sigma:.4e} Pa',
        'details': {'M_Nm': bending_moment, 'y_m': y_distance, 'I_m4': moment_of_inertia, 'stress_Pa': sigma},
        'unit': 'Pa'
    }

def calc_beam_deflection(load: float = 1000.0, length: float = 3.0, E_modulus: float = 200e9, I_moment: float = 1.0e-6, support_type: str = 'simply_supported_center') -> dict:
    """Beam deflection formulas for various loading types."""
    if support_type == 'simply_supported_center':
        delta = load * length**3 / (48.0 * E_modulus * I_moment)
    elif support_type == 'cantilever_end':
        delta = load * length**3 / (3.0 * E_modulus * I_moment)
    elif support_type == 'fixed_center':
        delta = load * length**3 / (192.0 * E_modulus * I_moment)
    elif support_type == 'simply_supported_uniform':
        w = load / length
        delta = 5.0 * w * length**4 / (384.0 * E_modulus * I_moment)
    elif support_type == 'cantilever_uniform':
        w = load / length
        delta = w * length**4 / (8.0 * E_modulus * I_moment)
    else:
        delta = load * length**3 / (48.0 * E_modulus * I_moment)
    return {
        'result': f'delta_max = {delta:.6e} m = {delta*1e3:.4f} mm',
        'details': {'load_N': load, 'length_m': length, 'E_Pa': E_modulus, 'I_m4': I_moment, 'support': support_type, 'deflection_m': delta},
        'unit': 'm'
    }

def calc_euler_buckling(E_modulus: float = 200e9, I_moment: float = 1.0e-6, length: float = 2.0, K_factor: float = 1.0) -> dict:
    """Euler buckling load: P_cr = pi^2 * E * I / (K*L)^2."""
    P_cr = np.pi**2 * E_modulus * I_moment / (K_factor * length)**2
    return {
        'result': f'P_cr = {P_cr:.4e} N',
        'details': {'E_Pa': E_modulus, 'I_m4': I_moment, 'L_m': length, 'K': K_factor, 'critical_load_N': P_cr},
        'unit': 'N'
    }

def calc_truss_forces(joint_forces: list = None, member_angles: list = None) -> dict:
    """Simple truss analysis for a 2-member joint using force equilibrium."""
    if joint_forces is None:
        joint_forces = [0.0, -1000.0]
    if member_angles is None:
        member_angles = [np.radians(30), np.radians(-45)]
    A = np.zeros((2, 2))
    for i, angle in enumerate(member_angles):
        A[0, i] = np.cos(angle)
        A[1, i] = np.sin(angle)
    b = np.array(joint_forces)
    if np.linalg.matrix_rank(A) >= 2:
        forces = np.linalg.solve(A, -b)
    else:
        forces = np.zeros(len(member_angles))
    results = []
    for i, f in enumerate(forces):
        state = 'tension' if f > 0 else 'compression'
        results.append({'member': i, 'force_N': float(f), 'state': state})
    return {
        'result': f'Member forces: {[f"{r["force_N"]:.2f} N ({r["state"]})" for r in results]}',
        'details': {'joint_forces': joint_forces, 'member_angles_deg': [np.degrees(a) for a in member_angles], 'forces': results},
        'unit': 'N'
    }

def calc_drag_force(rho: float = 1.225, velocity: float = 20.0, area: float = 0.5, Cd: float = 0.3) -> dict:
    """Drag force: F_d = 0.5 * rho * v^2 * Cd * A."""
    F_d = 0.5 * rho * velocity**2 * Cd * area
    power = F_d * velocity
    return {
        'result': f'F_d = {F_d:.4f} N, power = {power:.4f} W',
        'details': {'rho_kgm3': rho, 'velocity_ms': velocity, 'area_m2': area, 'Cd': Cd, 'drag_force_N': F_d, 'drag_power_W': power},
        'unit': 'N'
    }

def calc_lift_force(rho: float = 1.225, velocity: float = 80.0, area: float = 30.0, Cl: float = 1.5) -> dict:
    """Lift force: F_L = 0.5 * rho * v^2 * Cl * A."""
    F_L = 0.5 * rho * velocity**2 * Cl * area
    return {
        'result': f'Lift force F_L = {F_L:.4e} N = {F_L/9.81:.2f} kg-force',
        'details': {'rho_kgm3': rho, 'velocity_ms': velocity, 'area_m2': area, 'Cl': Cl, 'lift_force_N': F_L},
        'unit': 'N'
    }

def calc_darcy_weisbach(friction_factor: float = 0.02, length: float = 100.0, diameter: float = 0.1, velocity: float = 2.0, rho: float = 1000.0) -> dict:
    """Darcy-Weisbach head loss: h_f = f * (L/D) * v^2/(2g)."""
    g = 9.81
    h_f = friction_factor * (length / diameter) * velocity**2 / (2.0 * g)
    delta_p = h_f * rho * g
    return {
        'result': f'h_f = {h_f:.4f} m, delta_p = {delta_p:.4e} Pa',
        'details': {'f': friction_factor, 'L_m': length, 'D_m': diameter, 'v_ms': velocity, 'rho_kgm3': rho, 'head_loss_m': h_f, 'pressure_drop_Pa': delta_p},
        'unit': 'm'
    }

def calc_pump_power(flow_rate: float = 0.01, head: float = 30.0, rho: float = 1000.0, efficiency: float = 0.75) -> dict:
    """Pump power: P = rho * g * Q * H / eta."""
    g = 9.81
    P_hydraulic = rho * g * flow_rate * head
    P_shaft = P_hydraulic / efficiency
    return {
        'result': f'P_hydraulic = {P_hydraulic:.4f} W, P_shaft = {P_shaft:.4f} W',
        'details': {'flow_rate_m3s': flow_rate, 'head_m': head, 'rho_kgm3': rho, 'efficiency': efficiency, 'hydraulic_power_W': P_hydraulic, 'shaft_power_W': P_shaft},
        'unit': 'W'
    }

def calc_wind_turbine_power(rho: float = 1.225, swept_area: float = 100.0, wind_speed: float = 10.0, Cp: float = 0.45) -> dict:
    """Wind turbine power: P = 0.5 * rho * A * v^3 * Cp."""
    P = 0.5 * rho * swept_area * wind_speed**3 * Cp
    Betz_limit = 0.5 * rho * swept_area * wind_speed**3 * 0.593
    return {
        'result': f'P = {P:.4e} W = {P/1000:.2f} kW, Betz limit = {Betz_limit/1000:.2f} kW',
        'details': {'rho_kgm3': rho, 'swept_area_m2': swept_area, 'wind_speed_ms': wind_speed, 'Cp': Cp, 'power_W': P, 'Betz_limit_W': Betz_limit},
        'unit': 'W'
    }

def calc_wave_energy(wave_height: float = 2.0, wave_period: float = 8.0, rho: float = 1025.0) -> dict:
    """Ocean wave energy flux: P = (rho * g^2 * H^2 * T) / (32 * pi) per meter crest."""
    g = 9.81
    P_per_meter = rho * g**2 * wave_height**2 * wave_period / (32.0 * np.pi)
    return {
        'result': f'Wave power = {P_per_meter:.4e} W/m',
        'details': {'wave_height_m': wave_height, 'period_s': wave_period, 'rho_kgm3': rho, 'power_per_meter_W_m': P_per_meter, 'energy_flux': P_per_meter * wave_period},
        'unit': 'W/m'
    }

def calc_composite_wall_conduction(conductivities: list = None, thicknesses: list = None, area: float = 1.0, T_hot: float = 100.0, T_cold: float = 20.0) -> dict:
    """Heat conduction through composite wall: Q = (T_hot - T_cold) / sum(L_i/(k_i*A))."""
    if conductivities is None:
        conductivities = [1.0, 0.04, 0.8]
    if thicknesses is None:
        thicknesses = [0.01, 0.05, 0.02]
    R_total = 0.0
    R_values = []
    T_interfaces = [T_hot]
    for k, L in zip(conductivities, thicknesses):
        R = L / (k * area)
        R_total += R
        R_values.append(R)
    Q = (T_hot - T_cold) / R_total
    T_current = T_hot
    for R in R_values[:-1]:
        T_current = T_current - Q * R
        T_interfaces.append(T_current)
    T_interfaces.append(T_cold)
    return {
        'result': f'Q = {Q:.4f} W, R_total = {R_total:.4f} K/W',
        'details': {'conductivities': conductivities, 'thicknesses_m': thicknesses, 'area_m2': area, 'T_hot': T_hot, 'T_cold': T_cold, 'Q_W': Q, 'R_total': R_total, 'R_per_layer': R_values, 'T_interfaces': T_interfaces},
        'unit': 'W'
    }

def calc_lmtd_heat_exchanger(T_h_in: float = 100.0, T_h_out: float = 60.0, T_c_in: float = 20.0, T_c_out: float = 50.0, flow_type: str = 'counterflow') -> dict:
    """Log mean temperature difference: LMTD = (delta_T1 - delta_T2) / ln(delta_T1/delta_T2)."""
    if flow_type == 'counterflow':
        dT1 = T_h_in - T_c_out
        dT2 = T_h_out - T_c_in
    else:
        dT1 = T_h_in - T_c_in
        dT2 = T_h_out - T_c_out
    if dT1 <= 0 or dT2 <= 0 or abs(dT1 - dT2) < 1e-10:
        LMTD = (dT1 + dT2) / 2.0
    else:
        LMTD = (dT1 - dT2) / np.log(dT1 / dT2)
    return {
        'result': f'LMTD = {LMTD:.4f} K ({flow_type})',
        'details': {'T_h_in': T_h_in, 'T_h_out': T_h_out, 'T_c_in': T_c_in, 'T_c_out': T_c_out, 'dT1': dT1, 'dT2': dT2, 'LMTD_K': LMTD, 'flow_type': flow_type},
        'unit': 'K'
    }

def calc_ntu_method(UA: float = 1000.0, C_min: float = 500.0, C_max: float = 1000.0, exchanger_type: str = 'counterflow') -> dict:
    """NTU method for heat exchanger effectiveness."""
    NTU = UA / C_min
    Cr = C_min / C_max
    if exchanger_type == 'counterflow':
        if abs(1.0 - Cr) < 1e-10:
            effectiveness = NTU / (1.0 + NTU)
        else:
            effectiveness = (1.0 - np.exp(-NTU * (1.0 - Cr))) / (1.0 - Cr * np.exp(-NTU * (1.0 - Cr)))
    elif exchanger_type == 'parallel':
        effectiveness = (1.0 - np.exp(-NTU * (1.0 + Cr))) / (1.0 + Cr)
    else:
        effectiveness = 1.0 - np.exp(-NTU)
    return {
        'result': f'Effectiveness = {effectiveness:.4f}, NTU = {NTU:.4f}',
        'details': {'UA': UA, 'C_min': C_min, 'C_max': C_max, 'NTU': NTU, 'Cr': Cr, 'effectiveness': effectiveness, 'type': exchanger_type},
        'unit': 'dimensionless'
    }

def calc_radiation_heat_transfer(T1: float = 500.0, T2: float = 300.0, area: float = 1.0, emissivity: float = 0.8) -> dict:
    """Radiation between two gray bodies: Q = epsilon * sigma * A * (T1^4 - T2^4)."""
    sigma_sb = 5.670374419e-8
    Q = emissivity * sigma_sb * area * (T1**4 - T2**4)
    return {
        'result': f'Q_rad = {Q:.4f} W',
        'details': {'T1_K': T1, 'T2_K': T2, 'area_m2': area, 'emissivity': emissivity, 'Q_W': Q},
        'unit': 'W'
    }

def calc_fin_efficiency(length: float = 0.1, perimeter: float = 0.02, k: float = 200.0, h_conv: float = 50.0, area_cross: float = 0.0001) -> dict:
    """Cooling fin efficiency: eta = tanh(m*L)/(m*L), m = sqrt(h*P/(k*A))."""
    m = np.sqrt(h_conv * perimeter / (k * area_cross))
    mL = m * length
    efficiency = np.tanh(mL) / mL if mL > 0 else 1.0
    return {
        'result': f'Fin efficiency = {efficiency:.4f}, m = {m:.4f} m^(-1)',
        'details': {'L_m': length, 'P_m': perimeter, 'k_W_mK': k, 'h_W_m2K': h_conv, 'A_cross_m2': area_cross, 'm': m, 'mL': mL, 'efficiency': efficiency},
        'unit': 'dimensionless'
    }

def calc_transformer(primary_voltage: float = 240.0, primary_turns: float = 1000.0, secondary_turns: float = 100.0) -> dict:
    """Ideal transformer: V_p/V_s = N_p/N_s."""
    Vs = primary_voltage * secondary_turns / primary_turns
    Is_Ip_ratio = primary_turns / secondary_turns
    return {
        'result': f'V_s = {Vs:.4f} V, turns ratio = {Is_Ip_ratio:.4f}:1',
        'details': {'Vp_V': primary_voltage, 'Np': primary_turns, 'Ns': secondary_turns, 'Vs_V': Vs, 'turns_ratio': Is_Ip_ratio},
        'unit': 'V'
    }

def calc_motor_torque(power: float = 1500.0, rpm: float = 1800.0) -> dict:
    """Motor torque: tau = P / omega = 60*P/(2*pi*RPM)."""
    omega = rpm * 2.0 * np.pi / 60.0
    torque = power / omega
    return {
        'result': f'Torque = {torque:.4f} N*m',
        'details': {'power_W': power, 'rpm': rpm, 'omega_rad_s': omega, 'torque_Nm': torque},
        'unit': 'N*m'
    }

def calc_antenna_gain(antenna_area: float = 1.0, wavelength: float = 0.1, efficiency: float = 0.7) -> dict:
    """Antenna gain: G = 4*pi*A*eta/lambda^2."""
    G = 4.0 * np.pi * antenna_area * efficiency / wavelength**2
    G_dBi = 10.0 * np.log10(G)
    return {
        'result': f'G = {G:.4e} = {G_dBi:.4f} dBi',
        'details': {'area_m2': antenna_area, 'wavelength_m': wavelength, 'efficiency': efficiency, 'gain_linear': G, 'gain_dBi': G_dBi},
        'unit': 'dBi'
    }

def calc_transmission_line_impedance(L_per_m: float = 2.5e-7, C_per_m: float = 1.0e-10) -> dict:
    """Characteristic impedance of lossless transmission line: Z0 = sqrt(L/C)."""
    Z0 = np.sqrt(L_per_m / C_per_m)
    v_propagation = 1.0 / np.sqrt(L_per_m * C_per_m)
    return {
        'result': f'Z0 = {Z0:.4f} Ohm, v_prop = {v_propagation:.4e} m/s',
        'details': {'L_H_m': L_per_m, 'C_F_m': C_per_m, 'Z0_Ohm': Z0, 'propagation_velocity_ms': v_propagation},
        'unit': 'Ohm'
    }

def calc_skin_depth(frequency: float = 1e6, conductivity: float = 5.8e7, mu_r: float = 1.0) -> dict:
    """Skin depth: delta = sqrt(2/(omega*mu*sigma))."""
    mu_0 = 4.0 * np.pi * 1e-7
    mu = mu_0 * mu_r
    omega = 2.0 * np.pi * frequency
    delta = np.sqrt(2.0 / (omega * mu * conductivity))
    return {
        'result': f'delta = {delta:.4e} m = {delta*1e3:.4f} mm',
        'details': {'frequency_Hz': frequency, 'conductivity_Sm': conductivity, 'mu_r': mu_r, 'skin_depth_m': delta, 'skin_depth_mm': delta * 1000},
        'unit': 'm'
    }

def calc_waveguide_cutoff(waveguide_type: str = 'rectangular', a_dim: float = 0.02286, b_dim: float = 0.01016, mode: str = 'TE10') -> dict:
    """Waveguide cutoff frequency: f_c = c/(2*a) for TE10 rectangular."""
    c = 2.99792458e8
    if waveguide_type == 'rectangular' and mode == 'TE10':
        f_c = c / (2.0 * a_dim)
        lambda_c = 2.0 * a_dim
    elif waveguide_type == 'circular' and mode == 'TE11':
        f_c = 1.8412 * c / (2.0 * np.pi * a_dim)
        lambda_c = 2.0 * np.pi * a_dim / 1.8412
    elif waveguide_type == 'rectangular':
        m = int(mode[2]) if len(mode) > 2 else 1
        n = int(mode[3]) if len(mode) > 3 else 0
        f_c = (c / 2.0) * np.sqrt((m/a_dim)**2 + (n/b_dim)**2)
        lambda_c = 2.0 / np.sqrt((m/a_dim)**2 + (n/b_dim)**2)
    else:
        f_c = c / (2.0 * a_dim)
        lambda_c = 2.0 * a_dim
    return {
        'result': f'f_c = {f_c/1e9:.4f} GHz, lambda_c = {lambda_c*1e3:.4f} mm',
        'details': {'type': waveguide_type, 'mode': mode, 'a_m': a_dim, 'b_m': b_dim, 'cutoff_freq_Hz': f_c, 'cutoff_wavelength_m': lambda_c},
        'unit': 'Hz'
    }

def calc_sn_curve_fatigue(N_cycles: float = 1e5, S_ut: float = 500e6) -> dict:
    """S-N fatigue curve: S_f = S_ut * (N/1000)^b where b approx -0.085."""
    b = -0.085
    S_1000 = 0.9 * S_ut
    S_f = S_1000 * (N_cycles / 1000.0)**b
    return {
        'result': f'S_f = {S_f:.4e} Pa at N = {N_cycles:.0f} cycles',
        'details': {'N_cycles': N_cycles, 'S_ut_Pa': S_ut, 'fatigue_strength_Pa': S_f, 'exponent_b': b},
        'unit': 'Pa'
    }

def calc_miners_rule(stress_levels: list = None, cycles_at_level: list = None, cycles_to_failure: list = None) -> dict:
    """Miner's rule: D = sum(n_i / N_i)."""
    if stress_levels is None:
        stress_levels = [300e6, 200e6, 150e6]
    if cycles_at_level is None:
        cycles_at_level = [5000, 20000, 50000]
    if cycles_to_failure is None:
        cycles_to_failure = [10000, 100000, 500000]
    D = sum(n / N for n, N in zip(cycles_at_level, cycles_to_failure))
    failure = D >= 1.0
    return {
        'result': f'Damage D = {D:.6f}, failure predicted: {failure}',
        'details': {'stress_levels_Pa': stress_levels, 'applied_cycles': cycles_at_level, 'failure_cycles': cycles_to_failure, 'damage': D, 'failure': failure},
        'unit': 'dimensionless'
    }

def calc_composite_density(density_fiber: float = 1800.0, density_matrix: float = 1200.0, V_fiber: float = 0.6) -> dict:
    """Composite density: rho_c = rho_f*V_f + rho_m*(1-V_f)."""
    V_matrix = 1.0 - V_fiber
    rho_c = density_fiber * V_fiber + density_matrix * V_matrix
    return {
        'result': f'rho_c = {rho_c:.4f} kg/m^3',
        'details': {'rho_fiber': density_fiber, 'rho_matrix': density_matrix, 'V_fiber': V_fiber, 'V_matrix': V_matrix, 'composite_density': rho_c},
        'unit': 'kg/m^3'
    }

def calc_debye_length_plasma(T_e: float = 1e6, n_e: float = 1e20) -> dict:
    """Debye length: lambda_D = sqrt(epsilon_0 * k * T_e / (n_e * e^2))."""
    epsilon_0 = 8.8541878128e-12
    k_B = 1.380649e-23
    e = 1.602176634e-19
    lambda_D = np.sqrt(epsilon_0 * k_B * T_e / (n_e * e**2))
    return {
        'result': f'lambda_D = {lambda_D:.4e} m = {lambda_D*1e3:.4f} mm',
        'details': {'T_e_K': T_e, 'n_e_m3': n_e, 'Debye_length_m': lambda_D},
        'unit': 'm'
    }

def calc_plasma_frequency(n_e: float = 1e20) -> dict:
    """Plasma frequency: omega_p = sqrt(n_e * e^2 / (epsilon_0 * m_e))."""
    epsilon_0 = 8.8541878128e-12
    e = 1.602176634e-19
    m_e = 9.1093837015e-31
    omega_p = np.sqrt(n_e * e**2 / (epsilon_0 * m_e))
    f_p = omega_p / (2.0 * np.pi)
    return {
        'result': f'omega_p = {omega_p:.4e} rad/s, f_p = {f_p/1e9:.4f} GHz',
        'details': {'n_e_m3': n_e, 'omega_p_rad_s': omega_p, 'f_p_Hz': f_p, 'f_p_GHz': f_p/1e9},
        'unit': 'rad/s'
    }

def calc_larmor_radius(velocity: float = 1e5, B: float = 1.0, mass: float = 1.67e-27, charge: float = 1.6e-19) -> dict:
    """Larmor radius: r_L = m*v_perp / (q*B)."""
    r_L = mass * velocity / (charge * B)
    omega_c = charge * B / mass
    return {
        'result': f'r_L = {r_L:.4e} m, omega_c = {omega_c:.4e} rad/s',
        'details': {'velocity_ms': velocity, 'B_T': B, 'mass_kg': mass, 'charge_C': charge, 'Larmor_radius_m': r_L, 'cyclotron_freq': omega_c},
        'unit': 'm'
    }

def calc_bernoulli(p1: float = 101325.0, v1: float = 5.0, h1: float = 0.0, v2: float = 10.0, h2: float = 0.0, rho: float = 1000.0) -> dict:
    """Bernoulli equation: p1 + 0.5*rho*v1^2 + rho*g*h1 = p2 + 0.5*rho*v2^2 + rho*g*h2."""
    g = 9.81
    p2 = p1 + 0.5 * rho * (v1**2 - v2**2) + rho * g * (h1 - h2)
    return {
        'result': f'p2 = {p2:.4f} Pa = {p2/101325:.4f} atm',
        'details': {'p1_Pa': p1, 'v1_ms': v1, 'h1_m': h1, 'v2_ms': v2, 'h2_m': h2, 'rho_kgm3': rho, 'p2_Pa': p2},
        'unit': 'Pa'
    }

def calc_reynolds_number(rho: float = 1000.0, velocity: float = 1.0, length: float = 0.1, viscosity: float = 0.001) -> dict:
    """Reynolds number: Re = rho * v * L / mu."""
    Re = rho * velocity * length / viscosity
    if Re < 2300:
        regime = 'laminar'
    elif Re < 4000:
        regime = 'transitional'
    else:
        regime = 'turbulent'
    return {
        'result': f'Re = {Re:.2f} ({regime})',
        'details': {'rho_kgm3': rho, 'velocity_ms': velocity, 'length_m': length, 'viscosity_Pas': viscosity, 'Re': Re, 'regime': regime},
        'unit': 'dimensionless'
    }

def calc_pipe_friction_factor(Re: float = 50000.0, roughness: float = 0.000045, diameter: float = 0.1) -> dict:
    """Colebrook friction factor (approximate): f = 0.25/[log10(e/(3.7D)+5.74/Re^0.9)]^2."""
    if Re < 2300:
        f = 64.0 / Re
    else:
        f = 0.25 / (np.log10(roughness / (3.7 * diameter) + 5.74 / Re**0.9))**2
    return {
        'result': f'Darcy friction factor f = {f:.6f}',
        'details': {'Re': Re, 'roughness_m': roughness, 'diameter_m': diameter, 'friction_factor': f, 'regime': 'laminar' if Re < 2300 else 'turbulent'},
        'unit': 'dimensionless'
    }

def calc_hardness_conversion(hardness_brinell: float = 200.0) -> dict:
    """Approximate hardness conversion between scales."""
    HB = hardness_brinell
    HRC = 0.13 * HB - 15.0
    HV = 0.92 * HB
    return {
        'result': f'HB={HB:.1f} -> HRC~{HRC:.1f}, HV~{HV:.1f}',
        'details': {'HB': HB, 'HRC_approx': HRC, 'HV_approx': HV},
        'unit': 'dimensionless'
    }

def calc_creep_rate(stress: float = 100e6, temperature: float = 900.0, A: float = 1e-15, n_stress: float = 5.0, Q_activation: float = 280e3) -> dict:
    """Norton creep law: epsilon_dot = A * sigma^n * exp(-Q/RT)."""
    R = 8.314462618
    epsilon_dot = A * stress**n_stress * np.exp(-Q_activation / (R * temperature))
    return {
        'result': f'Creep rate = {epsilon_dot:.4e} s^(-1)',
        'details': {'stress_Pa': stress, 'T_K': temperature, 'A': A, 'n': n_stress, 'Q_J_mol': Q_activation, 'creep_rate_per_s': epsilon_dot},
        'unit': 's^(-1)'
    }

def calc_voltage_divider(V_in: float = 12.0, R1: float = 1000.0, R2: float = 2000.0) -> dict:
    """Voltage divider: V_out = V_in * R2/(R1+R2)."""
    V_out = V_in * R2 / (R1 + R2)
    I = V_in / (R1 + R2)
    return {
        'result': f'V_out = {V_out:.4f} V, I = {I:.6f} A',
        'details': {'V_in_V': V_in, 'R1_Ohm': R1, 'R2_Ohm': R2, 'V_out_V': V_out, 'current_A': I},
        'unit': 'V'
    }

def calc_rc_circuit(R: float = 1000.0, C: float = 1e-6, V0: float = 5.0, t: float = 0.001) -> dict:
    """RC circuit: V(t) = V0 * exp(-t/RC) discharging."""
    tau = R * C
    V_t = V0 * np.exp(-t / tau) if tau > 0 else 0.0
    return {
        'result': f'V({t}s) = {V_t:.6f} V, tau = {tau:.6f} s',
        'details': {'R_Ohm': R, 'C_F': C, 'V0_V': V0, 't_s': t, 'tau_s': tau, 'V_t_V': V_t},
        'unit': 'V'
    }

def calc_heat_equation_1d(k: float = 400.0, rho: float = 8900.0, cp: float = 385.0, dx: float = 0.001, dt: float = 0.01, n_steps: int = 100) -> dict:
    """1D heat equation stability: alpha*dt/dx^2 <= 0.5."""
    alpha = k / (rho * cp)
    fourier_number = alpha * dt / dx**2
    stable = fourier_number <= 0.5
    return {
        'result': f'Fo = {fourier_number:.4f}, stable: {stable}',
        'details': {'alpha_m2s': alpha, 'dx_m': dx, 'dt_s': dt, 'Fo': fourier_number, 'stable': stable},
        'unit': 'dimensionless'
    }

COMMANDS = {
    'bending_stress': {'func': calc_beam_bending_stress, 'params': ['bending_moment', 'y_distance', 'moment_of_inertia'], 'desc': 'Beam bending stress sigma = M*y/I'},
    'beam_deflection': {'func': calc_beam_deflection, 'params': ['load', 'length', 'E_modulus', 'I_moment', 'support_type'], 'desc': 'Beam deflection for various support types'},
    'euler_buckling': {'func': calc_euler_buckling, 'params': ['E_modulus', 'I_moment', 'length', 'K_factor'], 'desc': 'Euler buckling critical load'},
    'truss': {'func': calc_truss_forces, 'params': ['joint_forces', 'member_angles'], 'desc': 'Simple truss member force analysis'},
    'drag_force': {'func': calc_drag_force, 'params': ['rho', 'velocity', 'area', 'Cd'], 'desc': 'Drag force F_d = 0.5*rho*v^2*Cd*A'},
    'lift_force': {'func': calc_lift_force, 'params': ['rho', 'velocity', 'area', 'Cl'], 'desc': 'Lift force F_L = 0.5*rho*v^2*Cl*A'},
    'darcy_weisbach': {'func': calc_darcy_weisbach, 'params': ['friction_factor', 'length', 'diameter', 'velocity', 'rho'], 'desc': 'Darcy-Weisbach pipe head loss'},
    'pump_power': {'func': calc_pump_power, 'params': ['flow_rate', 'head', 'rho', 'efficiency'], 'desc': 'Pump shaft power calculation'},
    'wind_turbine': {'func': calc_wind_turbine_power, 'params': ['rho', 'swept_area', 'wind_speed', 'Cp'], 'desc': 'Wind turbine power and Betz limit'},
    'wave_energy': {'func': calc_wave_energy, 'params': ['wave_height', 'wave_period', 'rho'], 'desc': 'Ocean wave energy flux per meter crest'},
    'composite_wall': {'func': calc_composite_wall_conduction, 'params': ['conductivities', 'thicknesses', 'area', 'T_hot', 'T_cold'], 'desc': 'Heat conduction through composite wall'},
    'lmtd': {'func': calc_lmtd_heat_exchanger, 'params': ['T_h_in', 'T_h_out', 'T_c_in', 'T_c_out', 'flow_type'], 'desc': 'Log mean temperature difference'},
    'ntu_method': {'func': calc_ntu_method, 'params': ['UA', 'C_min', 'C_max', 'exchanger_type'], 'desc': 'NTU method for heat exchanger effectiveness'},
    'radiation_ht': {'func': calc_radiation_heat_transfer, 'params': ['T1', 'T2', 'area', 'emissivity'], 'desc': 'Radiation heat transfer between two bodies'},
    'fin_efficiency': {'func': calc_fin_efficiency, 'params': ['length', 'perimeter', 'k', 'h_conv', 'area_cross'], 'desc': 'Cooling fin efficiency'},
    'transformer': {'func': calc_transformer, 'params': ['primary_voltage', 'primary_turns', 'secondary_turns'], 'desc': 'Ideal transformer voltage and turns ratio'},
    'motor_torque': {'func': calc_motor_torque, 'params': ['power', 'rpm'], 'desc': 'Motor torque from power and RPM'},
    'antenna_gain': {'func': calc_antenna_gain, 'params': ['antenna_area', 'wavelength', 'efficiency'], 'desc': 'Antenna gain from aperture area'},
    'transmission_line': {'func': calc_transmission_line_impedance, 'params': ['L_per_m', 'C_per_m'], 'desc': 'Transmission line characteristic impedance'},
    'skin_depth': {'func': calc_skin_depth, 'params': ['frequency', 'conductivity', 'mu_r'], 'desc': 'EM skin depth delta = sqrt(2/(omega*mu*sigma))'},
    'waveguide_cutoff': {'func': calc_waveguide_cutoff, 'params': ['waveguide_type', 'a_dim', 'b_dim', 'mode'], 'desc': 'Waveguide cutoff frequency'},
    'sn_curve': {'func': calc_sn_curve_fatigue, 'params': ['N_cycles', 'S_ut'], 'desc': 'S-N fatigue curve strength at N cycles'},
    'miners_rule': {'func': calc_miners_rule, 'params': ['stress_levels', 'cycles_at_level', 'cycles_to_failure'], 'desc': 'Miner cumulative damage rule'},
    'composite_density': {'func': calc_composite_density, 'params': ['density_fiber', 'density_matrix', 'V_fiber'], 'desc': 'Composite density (rule of mixtures)'},
    'debye_length': {'func': calc_debye_length_plasma, 'params': ['T_e', 'n_e'], 'desc': 'Plasma Debye screening length'},
    'plasma_frequency': {'func': calc_plasma_frequency, 'params': ['n_e'], 'desc': 'Plasma frequency omega_p = sqrt(n*e^2/(eps0*m))'},
    'larmor_radius': {'func': calc_larmor_radius, 'params': ['velocity', 'B', 'mass', 'charge'], 'desc': 'Larmor radius r_L = m*v_perp/(q*B)'},
    'bernoulli': {'func': calc_bernoulli, 'params': ['p1', 'v1', 'h1', 'v2', 'h2', 'rho'], 'desc': 'Bernoulli equation solve for p2'},
    'reynolds': {'func': calc_reynolds_number, 'params': ['rho', 'velocity', 'length', 'viscosity'], 'desc': 'Reynolds number with flow regime'},
    'friction_factor': {'func': calc_pipe_friction_factor, 'params': ['Re', 'roughness', 'diameter'], 'desc': 'Colebrook pipe friction factor'},
    'hardness_convert': {'func': calc_hardness_conversion, 'params': ['hardness_brinell'], 'desc': 'Hardness conversion HB to HRC/HV'},
    'creep_rate': {'func': calc_creep_rate, 'params': ['stress', 'temperature', 'A', 'n_stress', 'Q_activation'], 'desc': 'Norton creep law strain rate'},
    'voltage_divider': {'func': calc_voltage_divider, 'params': ['V_in', 'R1', 'R2'], 'desc': 'Voltage divider V_out = V_in*R2/(R1+R2)'},
    'rc_circuit': {'func': calc_rc_circuit, 'params': ['R', 'C', 'V0', 't'], 'desc': 'RC circuit discharge V(t) = V0*exp(-t/RC)'},
    'heat_equation': {'func': calc_heat_equation_1d, 'params': ['k', 'rho', 'cp', 'dx', 'dt', 'n_steps'], 'desc': '1D heat equation Fourier stability number'}
}
