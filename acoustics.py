"""
Acoustics - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}


# =============================================================================
# SOUND PROPAGATION
# =============================================================================

def calc_speed_of_sound_gas(gamma: float = 1.4, R: float = 287.0, T: float = 293.15,
                              M_molar: float = 0.02896) -> dict:
    """Speed of sound in an ideal gas: v = sqrt(gamma * R * T / M) using specific gas constant R."""
    v = math.sqrt(gamma * R * T / M_molar) if M_molar > 0 else 0.0
    v_alt = math.sqrt(gamma * 8.314462618 * T / M_molar)
    return {
        'result': f'Speed of sound v = {v:.2f} m/s (alt: {v_alt:.2f} m/s)',
        'details': {'gamma': gamma, 'R_specific': R, 'T_K': T, 'M_molar_kg_per_mol': M_molar,
                    'v_sound': v, 'v_using_universal_R': v_alt},
        'unit': 'm/s'
    }


def calc_speed_of_sound_solid(E: float = 2.0e11, rho: float = 7800.0) -> dict:
    """Speed of sound in a solid bar: v = sqrt(E / rho)."""
    v = math.sqrt(E / rho)
    return {
        'result': f'Speed of sound in solid v = {v:.2f} m/s',
        'details': {'youngs_modulus_E_Pa': E, 'density_rho_kg_m3': rho, 'v_sound': v},
        'unit': 'm/s'
    }


def calc_speed_of_sound_fluid(B: float = 2.2e9, rho: float = 1000.0) -> dict:
    """Speed of sound in a fluid: v = sqrt(B / rho) (B = bulk modulus)."""
    v = math.sqrt(B / rho)
    return {
        'result': f'Speed of sound in fluid v = {v:.2f} m/s',
        'details': {'bulk_modulus_B_Pa': B, 'density_rho_kg_m3': rho, 'v_sound': v},
        'unit': 'm/s'
    }


def calc_wavelength(f: float = 440.0, v: float = 343.0) -> dict:
    """Acoustic wavelength: lambda = v / f."""
    wavelength = v / f
    k = 2.0 * math.pi / wavelength
    return {
        'result': f'Wavelength lambda = {wavelength:.4f} m, wave number k = {k:.4f} rad/m',
        'details': {'frequency_f_Hz': f, 'speed_of_sound_v': v,
                    'wavelength_lambda': wavelength, 'wave_number_k': k},
        'unit': 'm'
    }


def calc_acoustic_frequency(wavelength: float = 1.0, v: float = 343.0) -> dict:
    """Acoustic frequency: f = v / lambda."""
    f = v / wavelength
    T = 1.0 / f
    omega = 2.0 * math.pi * f
    return {
        'result': f'Frequency f = {f:.2f} Hz, period T = {T:.4f} s',
        'details': {'wavelength_lambda': wavelength, 'speed_of_sound_v': v,
                    'frequency_f': f, 'period_T': T, 'angular_freq_omega': omega},
        'unit': 'Hz'
    }


def calc_acoustic_impedance(rho: float = 1.225, v: float = 343.0) -> dict:
    """Characteristic acoustic impedance: Z = rho * v."""
    Z = rho * v
    return {
        'result': f'Acoustic impedance Z = {Z:.2f} kg/(m^2*s) = {Z:.2f} rayls',
        'details': {'density_rho': rho, 'speed_of_sound_v': v, 'impedance_Z': Z},
        'unit': 'kg/(m^2*s)'
    }


# =============================================================================
# SOUND LEVELS
# =============================================================================

def calc_sound_pressure_level(P: float = 0.02, P0: float = 2.0e-5) -> dict:
    """Sound pressure level: SPL = 20 * log10(P / P0) dB."""
    if P <= 0 or P0 <= 0:
        return {'result': 'Pressures must be positive', 'details': {}, 'unit': 'dB'}
    SPL = 20.0 * math.log10(P / P0)
    return {
        'result': f'SPL = {SPL:.2f} dB (re {P0*1e6:.0f} uPa)',
        'details': {'pressure_P_Pa': P, 'reference_pressure_P0': P0,
                    'SPL_dB': SPL, 'pressure_ratio': P / P0},
        'unit': 'dB'
    }


def calc_pressure_from_SPL(SPL: float = 94.0, P0: float = 2.0e-5) -> dict:
    """Pressure from SPL: P = P0 * 10^(SPL/20)."""
    P = P0 * (10.0 ** (SPL / 20.0))
    return {
        'result': f'Pressure P = {P:.4e} Pa = {P*1e6:.2f} uPa',
        'details': {'SPL_dB': SPL, 'reference_pressure_P0': P0, 'pressure_P': P},
        'unit': 'Pa'
    }


def calc_sound_intensity_from_pressure(P: float = 0.02, rho: float = 1.225, v: float = 343.0) -> dict:
    """Sound intensity from pressure: I = P^2 / (2 * rho * v)."""
    I = P * P / (2.0 * rho * v)
    I0 = 1e-12
    SIL = 10.0 * math.log10(I / I0) if I > 0 else float('-inf')
    return {
        'result': f'Intensity I = {I:.4e} W/m^2, SIL = {SIL:.2f} dB',
        'details': {'pressure_P': P, 'density_rho': rho, 'v_sound': v,
                    'intensity_I': I, 'SIL_dB': SIL},
        'unit': 'W/m^2'
    }


def calc_sound_intensity_from_power(P_acoustic: float = 1.0, A: float = 10.0) -> dict:
    """Sound intensity from power and area: I = P_acoustic / A."""
    I = P_acoustic / A
    return {
        'result': f'Intensity I = {I:.4f} W/m^2',
        'details': {'acoustic_power_W': P_acoustic, 'area_A_m2': A, 'intensity_I': I},
        'unit': 'W/m^2'
    }


def calc_sound_power_level(P_acoustic: float = 0.001, P0: float = 1e-12) -> dict:
    """Sound power level: SWL = 10 * log10(P / P0) dB."""
    SWL = 10.0 * math.log10(P_acoustic / P0)
    return {
        'result': f'Sound power level SWL = {SWL:.2f} dB',
        'details': {'acoustic_power': P_acoustic, 'reference_power': P0, 'SWL_dB': SWL},
        'unit': 'dB'
    }


def calc_add_decibels(dB_list: list = None) -> dict:
    """Add multiple sound levels (incoherent): L_total = 10*log10(sum(10^(L_i/10)))."""
    if dB_list is None:
        dB_list = [80.0, 83.0, 78.0]
    total_linear = sum(10.0 ** (L / 10.0) for L in dB_list)
    L_total = 10.0 * math.log10(total_linear)
    return {
        'result': f'Total SPL = {L_total:.2f} dB',
        'details': {'individual_levels': dB_list, 'total_level': L_total,
                    'linear_pressure_sum': total_linear},
        'unit': 'dB'
    }


def calc_distance_attenuation(SPL_ref: float = 100.0, r_ref: float = 1.0, r: float = 10.0) -> dict:
    """Inverse square law attenuation: SPL(r) = SPL_ref - 20*log10(r/r_ref)."""
    SPL = SPL_ref - 20.0 * math.log10(r / r_ref)
    attenuation = 20.0 * math.log10(r / r_ref)
    return {
        'result': f'SPL at r={r:.1f} m = {SPL:.2f} dB (attenuation = {attenuation:.2f} dB)',
        'details': {'SPL_ref': SPL_ref, 'r_ref': r_ref, 'r': r,
                    'SPL_at_r': SPL, 'attenuation_dB': attenuation},
        'unit': 'dB'
    }


# =============================================================================
# ROOM ACOUSTICS
# =============================================================================

def calc_sabine_reverberation(V: float = 100.0, A_total: float = 20.0) -> dict:
    """Sabine reverberation time: RT60 = 0.161 * V / A (in metric)."""
    RT60 = 0.161 * V / A_total
    return {
        'result': f'RT60 = {RT60:.4f} s',
        'details': {'room_volume_V_m3': V, 'total_absorption_A_m2': A_total,
                    'RT60_s': RT60, 'formula': 'Sabine'},
        'unit': 's'
    }


def calc_eyring_reverberation(V: float = 100.0, S: float = 80.0, alpha_avg: float = 0.25) -> dict:
    """Eyring reverberation time: RT60 = 0.161 * V / (-S * ln(1 - alpha_avg))."""
    if alpha_avg >= 1.0:
        return {'result': 'Alpha must be less than 1', 'details': {}, 'unit': 's'}
    A_eq = -S * math.log(1.0 - alpha_avg)
    RT60 = 0.161 * V / A_eq
    return {
        'result': f'RT60 (Eyring) = {RT60:.4f} s',
        'details': {'volume_V': V, 'surface_area_S': S, 'avg_absorption_alpha': alpha_avg,
                    'equivalent_absorption_A': A_eq, 'RT60': RT60, 'formula': 'Eyring'},
        'unit': 's'
    }


def calc_absorption_coefficient_area(alpha_i_list: list = None, S_i_list: list = None) -> dict:
    """Total absorption: A = sum(alpha_i * S_i)."""
    if alpha_i_list is None:
        alpha_i_list = [0.1, 0.3, 0.8]
    if S_i_list is None:
        S_i_list = [30.0, 20.0, 10.0]
    A_total = sum(a * s for a, s in zip(alpha_i_list, S_i_list))
    S_total = sum(S_i_list)
    alpha_avg = A_total / S_total if S_total > 0 else 0.0
    return {
        'result': f'Total absorption A = {A_total:.2f} m^2, avg alpha = {alpha_avg:.4f}',
        'details': {'alpha_list': alpha_i_list, 'area_list': S_i_list,
                    'A_total': A_total, 'S_total': S_total, 'alpha_average': alpha_avg},
        'unit': 'm^2'
    }


def calc_room_modes_rectangular(Lx: float = 5.0, Ly: float = 4.0, Lz: float = 3.0,
                                   v: float = 343.0) -> dict:
    """Calculate room mode frequencies for a rectangular room (up to n=3 each axis)."""
    freqs = []
    for nx in range(1, 4):
        for ny in range(1, 4):
            for nz in range(1, 4):
                f = (v / 2.0) * math.sqrt(
                    (nx / Lx) ** 2 + (ny / Ly) ** 2 + (nz / Lz) ** 2
                )
                if f < 500.0:
                    freqs.append((nx, ny, nz, f))
    freqs.sort(key=lambda x: x[3])
    n_modes = len(freqs)
    if n_modes > 5:
        first_5 = ', '.join([f'({n[0]},{n[1]},{n[2]})={n[3]:.1f}Hz' for n in freqs[:5]])
        result_str = f'{n_modes} modes found below 500 Hz. First 5: {first_5} ...'
    elif n_modes > 0:
        result_str = f'{n_modes} modes: ' + ', '.join([f'({n[0]},{n[1]},{n[2]})={n[3]:.1f}Hz' for n in freqs])
    else:
        result_str = 'No modes found below 500 Hz'
    return {
        'result': result_str,
        'details': {'room_dims': (Lx, Ly, Lz), 'v_sound': v,
                    'mode_count_under_500Hz': len(freqs),
                    'first_five_modes': freqs[:5]},
        'unit': 'Hz'
    }


def calc_standing_wave_room(L: float = 5.0, n: float = 1.0, v: float = 343.0) -> dict:
    """Axial standing wave frequency in a room: f_n = n * v / (2 * L)."""
    n_int = max(1, int(n))
    f_n = n_int * v / (2.0 * L)
    return {
        'result': f'Axial mode n={n_int}: f = {f_n:.2f} Hz',
        'details': {'length_L': L, 'mode_number_n': n_int, 'v_sound': v,
                    'frequency': f_n},
        'unit': 'Hz'
    }


# =============================================================================
# NONLINEAR ACOUSTICS
# =============================================================================

def calc_mach_number(v: float = 343.0, v_sound: float = 343.0) -> dict:
    """Mach number: M = v / v_sound."""
    M = v / v_sound
    if M < 0.3:
        regime = 'subsonic (incompressible approx)'
    elif M < 0.8:
        regime = 'subsonic'
    elif M < 1.0:
        regime = 'transonic'
    elif abs(M - 1.0) < 0.05:
        regime = 'sonic'
    elif M < 5.0:
        regime = 'supersonic'
    else:
        regime = 'hypersonic'
    return {
        'result': f'Mach number M = {M:.4f} ({regime})',
        'details': {'velocity_v': v, 'speed_of_sound': v_sound,
                    'Mach_number': M, 'regime': regime},
        'unit': 'dimensionless'
    }


def calc_mach_cone_angle(M: float = 2.0) -> dict:
    """Mach cone half-angle: sin(mu) = 1/M (for M > 1)."""
    if M <= 1.0:
        return {'result': 'Mach cone only defined for M > 1 (supersonic)', 'details': {'M': M}, 'unit': 'deg'}
    mu = math.degrees(math.asin(1.0 / M))
    return {
        'result': f'Mach cone half-angle mu = {mu:.4f} deg',
        'details': {'Mach_number': M, 'mu_deg': mu, 'mu_rad': math.radians(mu)},
        'unit': 'deg'
    }


def calc_shock_wave_relations(M1: float = 2.0, gamma: float = 1.4) -> dict:
    """Normal shock wave relations (supersonic to subsonic transition)."""
    M1_sq = M1 * M1
    M2 = math.sqrt((1.0 + (gamma - 1.0) * M1_sq / 2.0) /
                   (gamma * M1_sq - (gamma - 1.0) / 2.0))
    P_ratio = 1.0 + 2.0 * gamma * (M1_sq - 1.0) / (gamma + 1.0)
    rho_ratio = (gamma + 1.0) * M1_sq / (2.0 + (gamma - 1.0) * M1_sq)
    return {
        'result': f'M2 = {M2:.4f}, P2/P1 = {P_ratio:.4f}, rho2/rho1 = {rho_ratio:.4f}',
        'details': {'M1': M1, 'gamma': gamma, 'M2': M2,
                    'pressure_ratio': P_ratio, 'density_ratio': rho_ratio},
        'unit': 'dimensionless'
    }


def calc_sonic_boom_overpressure(W: float = 100000.0, h: float = 10000.0,
                                    M: float = 1.5, gamma: float = 1.4) -> dict:
    """Estimate sonic boom overpressure (simplified model)."""
    delta_P = W / (h * M)
    SPL = 20.0 * math.log10(delta_P / 2.0e-5)
    return {
        'result': f'Overpressure delta_P ~ {delta_P:.4f} Pa (~ {SPL:.2f} dB)',
        'details': {'aircraft_weight_W_N': W, 'altitude_h_m': h,
                    'Mach_M': M, 'delta_P_est': delta_P, 'SPL_est': SPL,
                    'note': 'simplified estimate'},
        'unit': 'Pa'
    }


# =============================================================================
# ULTRASOUND
# =============================================================================

def calc_ultrasound_attenuation(I0: float = 1.0, alpha: float = 0.5, x: float = 0.1,
                                   f: float = 1e6) -> dict:
    """Ultrasound attenuation: I(x) = I0 * exp(-alpha * x)."""
    I = I0 * math.exp(-alpha * x)
    attenuation_dB = 10.0 * math.log10(I / I0) if I > 0 else float('-inf')
    return {
        'result': f'I(x) = {I:.6f} W/m^2 ({attenuation_dB:.2f} dB loss)',
        'details': {'I0': I0, 'alpha_Np_per_m': alpha, 'distance_x': x,
                    'frequency_f_Hz': f, 'I_x': I, 'attenuation_dB': attenuation_dB},
        'unit': 'W/m^2'
    }


def calc_reflection_coefficient(Z1: float = 1.225 * 343.0, Z2: float = 1000.0 * 1500.0) -> dict:
    """Acoustic reflection coefficient at normal incidence: R = (Z2 - Z1) / (Z2 + Z1)."""
    R = (Z2 - Z1) / (Z2 + Z1)
    T_coeff = 1.0 - abs(R)
    return {
        'result': f'Reflection coeff R = {R:.6f}, Transmission coeff T = {T_coeff:.6f}',
        'details': {'Z1': Z1, 'Z2': Z2, 'reflection_coefficient_R': R,
                    'transmission_coefficient_T': T_coeff},
        'unit': 'dimensionless'
    }


def calc_transmission_coefficient_intensity(Z1: float = 430.0, Z2: float = 1.5e6) -> dict:
    """Intensity transmission coefficient: T_I = 4*Z1*Z2/(Z1+Z2)^2."""
    T_I = 4.0 * Z1 * Z2 / ((Z1 + Z2) ** 2)
    return {
        'result': f'Intensity transmission coeff T_I = {T_I:.6f}',
        'details': {'Z1': Z1, 'Z2': Z2, 'T_I': T_I},
        'unit': 'dimensionless'
    }


def calc_doppler_shift_ultrasound(f0: float = 2.0e6, v_target: float = 0.5,
                                    v_sound: float = 1540.0, theta_deg: float = 0.0) -> dict:
    """Doppler shift for ultrasound: delta_f = 2 * f0 * v * cos(theta) / v_sound."""
    theta = math.radians(theta_deg)
    delta_f = 2.0 * f0 * v_target * math.cos(theta) / v_sound
    f_received = f0 + delta_f
    return {
        'result': f'Doppler shift delta_f = {delta_f:.4f} Hz, f_received = {f_received:.4f} Hz',
        'details': {'f0_Hz': f0, 'target_velocity': v_target, 'v_sound': v_sound,
                    'angle_deg': theta_deg, 'delta_f': delta_f, 'f_received': f_received},
        'unit': 'Hz'
    }


def calc_doppler_simple(f0: float = 440.0, v_source: float = 20.0, v_observer: float = 0.0,
                          v_sound: float = 343.0) -> dict:
    """General Doppler effect: f' = f0 * (v_sound + v_observer) / (v_sound + v_source)."""
    f_prime = f0 * (v_sound + v_observer) / (v_sound + v_source)
    delta_f = f_prime - f0
    return {
        'result': f"f' = {f_prime:.4f} Hz, delta_f = {delta_f:.4f} Hz",
        'details': {'f0': f0, 'v_source': v_source, 'v_observer': v_observer,
                    'v_sound': v_sound, 'f_prime': f_prime, 'delta_f': delta_f},
        'unit': 'Hz'
    }


# =============================================================================
# ADDITIONAL ACOUSTICS FUNCTIONS
# =============================================================================

def calc_helmholtz_resonator(V: float = 0.001, A: float = 0.0001, L: float = 0.01,
                                v_sound: float = 343.0) -> dict:
    """Helmholtz resonator frequency: f = (v/(2*pi)) * sqrt(A/(V*L_eff))."""
    f = (v_sound / (2.0 * math.pi)) * math.sqrt(A / (V * L))
    return {
        'result': f'Helmholtz resonance f = {f:.2f} Hz',
        'details': {'volume_V': V, 'neck_area_A': A, 'neck_length_L': L,
                    'v_sound': v_sound, 'frequency_f': f},
        'unit': 'Hz'
    }


def calc_near_field_distance(D: float = 0.1, wavelength: float = 0.01,
                                v_sound: float = 343.0) -> dict:
    """Near-field to far-field transition distance: d_ff = D^2 / (4*lambda)."""
    d_ff = D * D / (4.0 * wavelength)
    f = v_sound / wavelength
    return {
        'result': f'Far-field distance d_ff = {d_ff:.4f} m (f = {f:.2f} Hz)',
        'details': {'transducer_size_D': D, 'wavelength': wavelength,
                    'near_field_distance': d_ff, 'frequency_f': f},
        'unit': 'm'
    }


def calc_directivity_factor(Q: float = 2.0) -> dict:
    """Directivity index: DI = 10*log10(Q)."""
    DI = 10.0 * math.log10(Q)
    return {
        'result': f'Directivity index DI = {DI:.2f} dB for Q = {Q:.2f}',
        'details': {'directivity_factor_Q': Q, 'DI_dB': DI},
        'unit': 'dB'
    }


def calc_vehicle_speed_from_doppler(f0: float = 24000.0, f_received: float = 24150.0,
                                       v_sound: float = 343.0) -> dict:
    """Vehicle speed from radar Doppler: v = (delta_f * v_sound) / (2 * f0)."""
    delta_f = f_received - f0
    v = delta_f * v_sound / (2.0 * f0)
    return {
        'result': f'vehicle speed v = {v:.4f} m/s = {v*3.6:.2f} km/h',
        'details': {'f0': f0, 'f_received': f_received, 'delta_f': delta_f,
                    'v_sound': v_sound, 'v_ms': v, 'v_kmh': v * 3.6},
        'unit': 'm/s'
    }


def calc_acoustic_power_from_SPL(SPL: float = 90.0, A: float = 1.0,
                                    rho: float = 1.225, v: float = 343.0) -> dict:
    """Acoustic power from SPL and area: P_ac = P_ref * 10^(SPL/20) and I = P^2/(2*rho*v)."""
    P0 = 2.0e-5
    P = P0 * (10.0 ** (SPL / 20.0))
    I = P * P / (2.0 * rho * v)
    P_ac = I * A
    return {
        'result': f'Acoustic power P_ac = {P_ac:.6f} W, I = {I:.6f} W/m^2',
        'details': {'SPL': SPL, 'area_A': A, 'pressure_rms': P,
                    'intensity_I': I, 'acoustic_power': P_ac},
        'unit': 'W'
    }


def calc_equivalent_continuous_level(levels: list = None) -> dict:
    """Leq (equivalent continuous sound level) from list of dB values."""
    if levels is None:
        levels = [85.0, 90.0, 82.0, 88.0, 84.0]
    N = len(levels)
    if N == 0:
        return {'result': 'No levels provided', 'details': {}, 'unit': 'dB'}
    total_linear = sum(10.0 ** (L / 10.0) for L in levels)
    Leq = 10.0 * math.log10(total_linear / N)
    return {
        'result': f'Leq = {Leq:.2f} dB (over {N} samples)',
        'details': {'levels': levels, 'N': N, 'Leq': Leq},
        'unit': 'dB'
    }


def calc_stafford_wave(D: float = 1.0, rho: float = 1.225, P0: float = 101325.0,
                         v_sound: float = 340.0) -> dict:
    """Acoustic nonlinear parameter: B/A = rho * v^2 / P."""
    B_over_A = rho * v_sound * v_sound / P0
    return {'result': f'B/A = {B_over_A:.4f} (nonlinear parameter)', 'details': {'rho': rho, 'v_sound': v_sound, 'P0': P0, 'B_over_A': B_over_A}, 'unit': 'dimensionless'}


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Sound Propagation
    'speed_of_sound_gas': {'func': calc_speed_of_sound_gas,
                            'params': ['gamma', 'R', 'T', 'M_molar'],
                            'desc': 'Speed of sound in ideal gas v = sqrt(gamma*R*T/M)'},
    'speed_of_sound_solid': {'func': calc_speed_of_sound_solid, 'params': ['E', 'rho'],
                              'desc': 'Speed of sound in solid v = sqrt(E/rho)'},
    'speed_of_sound_fluid': {'func': calc_speed_of_sound_fluid, 'params': ['B', 'rho'],
                              'desc': 'Speed of sound in fluid v = sqrt(B/rho)'},
    'wavelength_acoustic': {'func': calc_wavelength, 'params': ['f', 'v'],
                             'desc': 'Acoustic wavelength lambda = v/f'},
    'acoustic_frequency': {'func': calc_acoustic_frequency, 'params': ['wavelength', 'v'],
                            'desc': 'Acoustic frequency f = v/lambda'},
    'acoustic_impedance': {'func': calc_acoustic_impedance, 'params': ['rho', 'v'],
                            'desc': 'Acoustic impedance Z = rho*v'},
    # Sound Levels
    'sound_pressure_level': {'func': calc_sound_pressure_level, 'params': ['P', 'P0'],
                              'desc': 'SPL = 20*log10(P/P0) dB'},
    'pressure_from_SPL': {'func': calc_pressure_from_SPL, 'params': ['SPL', 'P0'],
                           'desc': 'Pressure from SPL: P = P0 * 10^(SPL/20)'},
    'sound_intensity_from_pressure': {'func': calc_sound_intensity_from_pressure,
                                       'params': ['P', 'rho', 'v'],
                                       'desc': 'Sound intensity I = P^2/(2*rho*v)'},
    'sound_intensity_from_power': {'func': calc_sound_intensity_from_power,
                                    'params': ['P_acoustic', 'A'],
                                    'desc': 'Intensity I = P_acoustic/A'},
    'sound_power_level': {'func': calc_sound_power_level, 'params': ['P_acoustic', 'P0'],
                           'desc': 'Sound power level SWL = 10*log10(P/P0)'},
    'add_decibels': {'func': calc_add_decibels, 'params': ['dB_list'],
                      'desc': 'Add multiple incoherent sound levels'},
    'distance_attenuation': {'func': calc_distance_attenuation,
                              'params': ['SPL_ref', 'r_ref', 'r'],
                              'desc': 'SPL at distance r from reference'},
    # Room Acoustics
    'sabine_reverberation': {'func': calc_sabine_reverberation, 'params': ['V', 'A_total'],
                              'desc': 'Sabine RT60 = 0.161*V/A'},
    'eyring_reverberation': {'func': calc_eyring_reverberation, 'params': ['V', 'S', 'alpha_avg'],
                              'desc': 'Eyring RT60 = 0.161*V/(-S*ln(1-alpha))'},
    'absorption_coefficient_area': {'func': calc_absorption_coefficient_area,
                                      'params': ['alpha_i_list', 'S_i_list'],
                                      'desc': 'Total absorption A = sum(alpha_i * S_i)'},
    'room_modes_rectangular': {'func': calc_room_modes_rectangular,
                                 'params': ['Lx', 'Ly', 'Lz', 'v'],
                                 'desc': 'Calculate rectangular room modes'},
    'standing_wave_room': {'func': calc_standing_wave_room, 'params': ['L', 'n', 'v'],
                            'desc': 'Axial standing wave in room f = n*v/(2L)'},
    # Nonlinear Acoustics
    'mach_number': {'func': calc_mach_number, 'params': ['v', 'v_sound'],
                    'desc': 'Mach number M = v/v_sound'},
    'mach_cone_angle': {'func': calc_mach_cone_angle, 'params': ['M'],
                         'desc': 'Mach cone half-angle sin(mu) = 1/M'},
    'shock_wave_relations': {'func': calc_shock_wave_relations,
                              'params': ['M1', 'gamma'],
                              'desc': 'Normal shock wave relations'},
    'sonic_boom_overpressure': {'func': calc_sonic_boom_overpressure,
                                  'params': ['W', 'h', 'M', 'gamma'],
                                  'desc': 'Sonic boom overpressure estimate'},
    # Ultrasound
    'ultrasound_attenuation': {'func': calc_ultrasound_attenuation,
                                'params': ['I0', 'alpha', 'x', 'f'],
                                'desc': 'Ultrasound attenuation I = I0*exp(-alpha*x)'},
    'reflection_coefficient': {'func': calc_reflection_coefficient, 'params': ['Z1', 'Z2'],
                                'desc': 'Acoustic reflection coefficient R = (Z2-Z1)/(Z2+Z1)'},
    'transmission_coefficient_intensity': {'func': calc_transmission_coefficient_intensity,
                                            'params': ['Z1', 'Z2'],
                                            'desc': 'Intensity transmission coeff T_I = 4Z1Z2/(Z1+Z2)^2'},
    'doppler_shift_ultrasound': {'func': calc_doppler_shift_ultrasound,
                                  'params': ['f0', 'v_target', 'v_sound', 'theta_deg'],
                                  'desc': 'Ultrasound Doppler shift delta_f = 2f0*v*cos(theta)/c'},
    'doppler_simple': {'func': calc_doppler_simple,
                        'params': ['f0', 'v_source', 'v_observer', 'v_sound'],
                        'desc': "General Doppler effect f' = f0*(c+v_obs)/(c+v_src)"},
}
