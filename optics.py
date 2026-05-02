"""
Optics - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}


# =============================================================================
# GEOMETRIC OPTICS
# =============================================================================

def calc_snells_law(n1: float = 1.0, theta1_deg: float = 30.0, n2: float = 1.5) -> dict:
    """Snell's law: n1 * sin(theta1) = n2 * sin(theta2)."""
    theta1 = math.radians(theta1_deg)
    sin_theta2 = n1 * math.sin(theta1) / n2
    if abs(sin_theta2) > 1.0:
        return {'result': 'Total internal reflection (sin theta2 > 1)', 'details': {
            'n1': n1, 'theta1_deg': theta1_deg, 'n2': n2, 'sin_theta2': sin_theta2}, 'unit': 'deg'}
    theta2 = math.degrees(math.asin(sin_theta2))
    return {
        'result': f'theta2 = {theta2:.4f} deg',
        'details': {'n1': n1, 'theta1_deg': theta1_deg, 'theta1_rad': theta1,
                    'n2': n2, 'theta2_deg': theta2, 'theta2_rad': math.radians(theta2),
                    'sin_theta2': sin_theta2},
        'unit': 'deg'
    }


def calc_critical_angle(n1: float = 1.5, n2: float = 1.0) -> dict:
    """Critical angle for total internal reflection: theta_c = arcsin(n2/n1)."""
    if n2 >= n1:
        return {'result': 'No critical angle (n2 >= n1)', 'details': {'n1': n1, 'n2': n2}, 'unit': 'deg'}
    theta_c = math.degrees(math.asin(n2 / n1))
    return {
        'result': f'Critical angle theta_c = {theta_c:.4f} deg',
        'details': {'n1': n1, 'n2': n2, 'critical_angle_deg': theta_c,
                    'critical_angle_rad': math.radians(theta_c)},
        'unit': 'deg'
    }


def calc_lens_equation(u: float = 30.0, f: float = 10.0) -> dict:
    """Thin lens equation: 1/f = 1/u + 1/v. Solve for v (image distance)."""
    if abs(u - f) < 1e-12:
        return {'result': 'Object at focal point: image at infinity', 'details': {
            'u': u, 'f': f, 'v': float('inf')}, 'unit': 'cm'}
    v = 1.0 / (1.0 / f - 1.0 / u)
    m = -v / u
    if v > 0:
        image_type = 'real, inverted'
    else:
        image_type = 'virtual, upright'
    return {
        'result': f'Image distance v = {v:.4f} cm, magnification m = {m:.4f} ({image_type})',
        'details': {'object_distance_u': u, 'focal_length_f': f, 'image_distance_v': v,
                    'magnification_m': m, 'image_type': image_type},
        'unit': 'cm'
    }


def calc_lens_eq_solve(u: float | None = None, v: float | None = None, f: float = 10.0) -> dict:
    """Thin lens equation: 1/f = 1/u + 1/v. Set unknown to None."""
    if u is None and v is not None and f is not None:
        u = 1.0 / (1.0 / f - 1.0 / v) if abs(1.0/f - 1.0/v) > 1e-15 else float('inf')
        solved = 'u'
    elif v is None and u is not None and f is not None:
        v = 1.0 / (1.0 / f - 1.0 / u) if abs(1.0/f - 1.0/u) > 1e-15 else float('inf')
        solved = 'v'
    elif f is None and u is not None and v is not None:
        f = 1.0 / (1.0 / u + 1.0 / v) if abs(1.0/u + 1.0/v) > 1e-15 else float('inf')
        solved = 'f'
    else:
        v_check = 1.0 / (1.0 / f - 1.0 / u) if abs(1.0/f - 1.0/u) > 1e-15 else float('inf')
        m = -v_check / u if abs(u) > 1e-15 else float('inf')
        return {
            'result': f'v = {v_check:.4f} cm, m = {m:.4f}',
            'details': {'u': u, 'v': v_check, 'f': f, 'm': m},
            'unit': 'cm'
        }
    values = {'u': u, 'v': v, 'f': f}
    return {
        'result': f'{solved} = {values[solved]:.4f} cm',
        'details': values,
        'unit': 'cm'
    }


def calc_magnification(u: float = 30.0, v: float = 15.0) -> dict:
    """Lateral magnification: m = -v/u."""
    m = -v / u
    if m > 0:
        orientation = 'upright'
    else:
        orientation = 'inverted'
    return {
        'result': f'Magnification m = {m:.4f} ({orientation})',
        'details': {'object_distance_u': u, 'image_distance_v': v,
                    'magnification_m': m, 'orientation': orientation,
                    'image_size_ratio': abs(m)},
        'unit': 'dimensionless'
    }


def calc_lens_makers_formula(n: float = 1.5, R1: float = 20.0, R2: float = -20.0) -> dict:
    """Lens maker's formula: 1/f = (n-1)*(1/R1 - 1/R2). All units in cm."""
    f_inv = (n - 1.0) * (1.0 / R1 - 1.0 / R2)
    if abs(f_inv) < 1e-15:
        return {'result': 'No focusing power (f is infinite)', 'details': {'n': n, 'R1': R1, 'R2': R2}, 'unit': 'cm'}
    f = 1.0 / f_inv
    P = 1.0 / (f / 100.0)  # power in diopters (f converted to meters)
    lens_type = 'converging' if f > 0 else 'diverging'
    return {
        'result': f'f = {f:.4f} cm, P = {P:.4f} D ({lens_type})',
        'details': {'refractive_index_n': n, 'R1_cm': R1, 'R2_cm': R2, 'focal_length_f_cm': f,
                    'optical_power_P_diopters': P, 'lens_type': lens_type},
        'unit': 'cm'
    }


def calc_mirror_equation(u: float = 30.0, f: float = 15.0) -> dict:
    """Spherical mirror equation: 1/f = 1/u + 1/v (f = R/2 for spherical mirror)."""
    if abs(u - f) < 1e-12:
        return {'result': 'Object at focal point: image at infinity', 'details': {
            'u': u, 'f': f, 'v': float('inf')}, 'unit': 'cm'}
    v = 1.0 / (1.0 / f - 1.0 / u)
    m = -v / u
    R = 2.0 * f
    return {
        'result': f'v = {v:.4f} cm, m = {m:.4f}, R = {R:.4f} cm',
        'details': {'object_distance_u': u, 'focal_length_f': f, 'image_distance_v': v,
                    'magnification_m': m, 'radius_of_curvature_R': R},
        'unit': 'cm'
    }


def calc_prism_deviation(n: float = 1.5, A_deg: float = 60.0, i1_deg: float = 45.0) -> dict:
    """Prism deviation angle: delta = i1 + i2 - A."""
    A = math.radians(A_deg)
    i1 = math.radians(i1_deg)
    sin_r1 = math.sin(i1) / n
    if abs(sin_r1) > 1.0:
        return {'result': 'Ray does not enter prism (sin r1 > 1)', 'details': {}, 'unit': 'deg'}
    r1 = math.asin(sin_r1)
    r2 = A - r1
    if r2 < 0:
        return {'result': 'Ray does not exit prism (r2 < 0)', 'details': {}, 'unit': 'deg'}
    sin_i2 = n * math.sin(r2)
    if abs(sin_i2) > 1.0:
        return {'result': 'Total internal reflection at second face', 'details': {}, 'unit': 'deg'}
    i2 = math.asin(sin_i2)
    delta = i1 + i2 - A
    delta_deg = math.degrees(delta)
    return {
        'result': f'Deviation delta = {delta_deg:.4f} deg',
        'details': {'n': n, 'prism_angle_A_deg': A_deg, 'incident_angle_i1_deg': i1_deg,
                    'r1_deg': math.degrees(r1), 'r2_deg': math.degrees(r2),
                    'i2_deg': math.degrees(i2), 'deviation_deg': delta_deg},
        'unit': 'deg'
    }


def calc_minimum_deviation(n: float = 1.5, A_deg: float = 60.0) -> dict:
    """Minimum deviation of a prism: n = sin((A+delta_min)/2) / sin(A/2)."""
    A = math.radians(A_deg)
    sin_arg = n * math.sin(A / 2.0)
    if abs(sin_arg) > 1.0:
        return {'result': 'Not physically possible (n * sin(A/2) > 1)', 'details': {}, 'unit': 'deg'}
    delta_min = 2.0 * math.asin(sin_arg) - A
    delta_min_deg = math.degrees(delta_min)
    return {
        'result': f'Minimum deviation delta_min = {delta_min_deg:.4f} deg',
        'details': {'n': n, 'prism_angle_A_deg': A_deg, 'A_rad': A,
                    'delta_min_deg': delta_min_deg, 'delta_min_rad': delta_min},
        'unit': 'deg'
    }


def calc_optical_power(f: float = 0.25) -> dict:
    """Optical power: P = 1/f (in meters, result in diopters)."""
    P = 1.0 / f
    return {
        'result': f'P = {P:.4f} D (diopters)',
        'details': {'focal_length_f_m': f, 'optical_power_P_diopters': P},
        'unit': 'D'
    }


def calc_two_lens_system(f1: float = 10.0, f2: float = 5.0, d: float = 12.0,
                          u1: float = 30.0) -> dict:
    """Two-lens system: compute final image position and total magnification."""
    if abs(u1 - f1) < 1e-12:
        return {'result': 'Object at first focal point', 'details': {}, 'unit': 'cm'}
    v1 = 1.0 / (1.0 / f1 - 1.0 / u1)
    u2 = d - v1
    if abs(u2) < 1e-12:
        return {'result': 'Intermediate image at second lens surface', 'details': {
            'v1': v1, 'd': d, 'u2': u2}, 'unit': 'cm'}
    if abs(u2 - f2) < 1e-12:
        return {'result': 'Intermediate image at second focal point: image at infinity', 'details': {
            'v1': v1, 'u2': u2, 'f2': f2}, 'unit': 'cm'}
    v2 = 1.0 / (1.0 / f2 - 1.0 / u2)
    m1 = -v1 / u1
    m2 = -v2 / u2
    m_total = m1 * m2
    return {
        'result': f'Final image at v2 = {v2:.4f} cm, total m = {m_total:.4f}',
        'details': {'f1': f1, 'f2': f2, 'lens_separation_d': d, 'u1': u1,
                    'v1': v1, 'u2': u2, 'v2': v2, 'm1': m1, 'm2': m2, 'm_total': m_total},
        'unit': 'cm'
    }


# =============================================================================
# WAVE OPTICS
# =============================================================================

def calc_youngs_double_slit(wavelength: float = 632.8e-9, d: float = 0.5e-3,
                              D: float = 1.0, m: float = 1.0) -> dict:
    """Young's double slit: y_m = m * lambda * D / d (bright fringe position)."""
    y = m * wavelength * D / d
    fringe_spacing = wavelength * D / d
    return {
        'result': f'Position of m={m:.0f} bright fringe: y = {y:.6e} m, fringe spacing = {fringe_spacing:.6e} m',
        'details': {'wavelength_m': wavelength, 'slit_separation_d': d,
                    'screen_distance_D': D, 'order_m': m, 'y_position_m': y,
                    'fringe_spacing_m': fringe_spacing},
        'unit': 'm'
    }


def calc_double_slit_angular(wavelength: float = 632.8e-9, d: float = 0.5e-3,
                               m: float = 1.0) -> dict:
    """Angular position of bright fringe: d * sin(theta) = m * lambda."""
    sin_theta = m * wavelength / d
    if abs(sin_theta) > 1.0:
        return {'result': f'Order m={m:.0f} is beyond 90 degrees', 'details': {
            'm': m, 'sin_theta': sin_theta}, 'unit': 'deg'}
    theta = math.degrees(math.asin(sin_theta))
    return {
        'result': f'Angular position theta = {theta:.6f} deg for m={m:.0f}',
        'details': {'wavelength': wavelength, 'slit_separation_d': d, 'order_m': m,
                    'theta_deg': theta, 'theta_rad': math.radians(theta), 'sin_theta': sin_theta},
        'unit': 'deg'
    }


def calc_thin_film_interference(n: float = 1.33, t: float = 500e-9, m: float = 1.0,
                                  wavelength_vacuum: float = 550e-9) -> dict:
    """Thin film interference: 2*n*t = m*lambda (constructive for thin film in air)."""
    optical_path = 2.0 * n * t
    lambda_film = wavelength_vacuum / n
    order_approx = optical_path / wavelength_vacuum
    return {
        'result': f'Optical path = {optical_path:.4e} m, lambda in film = {lambda_film:.4e} m, order ~ {order_approx:.2f}',
        'details': {'n_film': n, 'thickness_t': t, 'order_m': m,
                    'wavelength_vacuum': wavelength_vacuum, 'optical_path': optical_path,
                    'lambda_in_film': lambda_film, 'order_approx': order_approx},
        'unit': 'm'
    }


def calc_single_slit_diffraction(wavelength: float = 632.8e-9, a: float = 0.1e-3,
                                   m: float = 1.0) -> dict:
    """Single slit diffraction minima: a * sin(theta) = m * lambda."""
    sin_theta = m * wavelength / a
    if abs(sin_theta) > 1.0:
        return {'result': f'Order m={m:.0f} is beyond 90 degrees', 'details': {}, 'unit': 'deg'}
    theta = math.degrees(math.asin(sin_theta))
    angular_width = 2.0 * wavelength / a
    return {
        'result': f'Minima at theta = {theta:.6f} deg for m={m:.0f}, central max width = {angular_width:.6e} rad',
        'details': {'wavelength': wavelength, 'slit_width_a': a, 'order_m': m,
                    'theta_deg': theta, 'theta_rad': math.radians(theta),
                    'central_max_angular_width_rad': angular_width},
        'unit': 'deg'
    }


def calc_grating_equation(d: float = 2e-6, wavelength: float = 500e-9, m: float = 1.0) -> dict:
    """Diffraction grating equation: d * sin(theta) = m * lambda."""
    sin_theta = m * wavelength / d
    if abs(sin_theta) > 1.0:
        return {'result': f'Order m={m:.0f} does not exist (sin > 1)', 'details': {
            'm': m, 'sin_theta': sin_theta}, 'unit': 'deg'}
    theta = math.degrees(math.asin(sin_theta))
    N = 1.0 / d
    return {
        'result': f'theta = {theta:.4f} deg for m={m:.0f}, grating = {N:.0f} lines/m = {N/1000:.0f} lines/mm',
        'details': {'grating_spacing_d': d, 'wavelength': wavelength, 'order_m': m,
                    'sin_theta': sin_theta, 'theta_deg': theta, 'lines_per_m': N},
        'unit': 'deg'
    }


def calc_grating_resolution(N: float = 10000.0, m: float = 1.0) -> dict:
    """Resolving power of diffraction grating: R = lambda/delta_lambda = N * m."""
    R = N * m
    return {
        'result': f'Resolving power R = {R:.0f}',
        'details': {'total_lines_N': N, 'order_m': m, 'resolving_power_R': R},
        'unit': 'dimensionless'
    }


def calc_malus_law(I0: float = 100.0, theta_deg: float = 45.0) -> dict:
    """Malus's law for polarization: I = I0 * cos^2(theta)."""
    theta = math.radians(theta_deg)
    I = I0 * math.cos(theta) ** 2
    return {
        'result': f'Transmitted intensity I = {I:.4f} W/m^2 ({I/I0*100:.2f}% of I0)',
        'details': {'I0': I0, 'theta_deg': theta_deg, 'theta_rad': theta,
                    'I': I, 'transmission_ratio': I / I0},
        'unit': 'W/m^2'
    }


def calc_brewster_angle(n1: float = 1.0, n2: float = 1.5) -> dict:
    """Brewster's angle: tan(theta_B) = n2/n1."""
    theta_B = math.degrees(math.atan(n2 / n1))
    return {
        'result': f'Brewster angle theta_B = {theta_B:.4f} deg',
        'details': {'n1': n1, 'n2': n2, 'theta_B_deg': theta_B,
                    'theta_B_rad': math.radians(theta_B)},
        'unit': 'deg'
    }


def calc_dispersion_cauchy(n_values: list = None, wavelength_values: list = None) -> dict:
    """Cauchy dispersion approximation: n(lambda) = A + B/lambda^2."""
    if n_values is None:
        n_values = [1.51, 1.52, 1.55]
    if wavelength_values is None:
        wavelength_values = [700e-9, 550e-9, 400e-9]
    if len(n_values) < 2 or len(wavelength_values) < 2:
        return {'result': 'Need at least 2 data points', 'details': {}, 'unit': 'dimensionless'}
    inv_lambda_sq = [1.0 / (wl ** 2) for wl in wavelength_values]
    p = np.polyfit(inv_lambda_sq, n_values, 1)
    A, B = p[1], p[0]
    return {
        'result': f'Cauchy: n(lambda) = {A:.6f} + {B:.4e}/lambda^2',
        'details': {'A_coefficient': A, 'B_coefficient': B,
                    'description': 'Cauchy dispersion relation'},
        'unit': 'dimensionless'
    }


# =============================================================================
# PHOTOMETRY
# =============================================================================

def calc_luminous_flux(I: float = 100.0, omega: float = 0.5) -> dict:
    """Luminous flux: Phi = I * omega (intensity * solid angle)."""
    Phi = I * omega
    return {
        'result': f'Luminous flux Phi = {Phi:.4f} lm',
        'details': {'luminous_intensity_I_cd': I, 'solid_angle_omega_sr': omega,
                    'luminous_flux_Phi_lm': Phi},
        'unit': 'lm'
    }


def calc_illuminance(Phi: float = 1000.0, A: float = 4.0) -> dict:
    """Illuminance: E = Phi / A (luminous flux per area)."""
    E = Phi / A
    return {
        'result': f'Illuminance E = {E:.4f} lx (lux = lm/m^2)',
        'details': {'luminous_flux_Phi_lm': Phi, 'area_A_m2': A, 'illuminance_E_lx': E},
        'unit': 'lx'
    }


def calc_inverse_square_law_light(I: float = 100.0, r: float = 2.0) -> dict:
    """Inverse square law for light: E = I / r^2."""
    E = I / (r * r)
    return {
        'result': f'Illuminance E = {E:.4f} lx at distance r = {r:.4f} m',
        'details': {'luminous_intensity_I_cd': I, 'distance_r_m': r, 'illuminance_E_lx': E},
        'unit': 'lx'
    }


def calc_luminance(I: float = 500.0, A: float = 0.01, theta_deg: float = 0.0) -> dict:
    """Luminance: L = I / (A * cos(theta))."""
    theta = math.radians(theta_deg)
    if abs(math.cos(theta)) < 1e-15:
        return {'result': 'Luminance infinite at 90 degrees', 'details': {}, 'unit': 'cd/m^2'}
    L = I / (A * math.cos(theta))
    return {
        'result': f'Luminance L = {L:.4f} cd/m^2',
        'details': {'luminous_intensity_I_cd': I, 'area_A_m2': A, 'theta_deg': theta_deg,
                    'luminance_L_cd_m2': L},
        'unit': 'cd/m^2'
    }


# =============================================================================
# LASER OPTICS
# =============================================================================

def calc_gaussian_beam_width(z: float = 0.0, w0: float = 1e-3, wavelength: float = 632.8e-9) -> dict:
    """Gaussian beam width: w(z) = w0 * sqrt(1 + (z/zR)^2)."""
    zR = math.pi * w0 * w0 / wavelength
    w_z = w0 * math.sqrt(1.0 + (z / zR) ** 2)
    if abs(z) < 1e-15:
        R_z = float('inf')
    else:
        R_z = z * (1.0 + (zR / z) ** 2)
    return {
        'result': f'w(z) = {w_z:.6e} m, zR = {zR:.4e} m',
        'details': {'waist_w0': w0, 'axial_position_z': z, 'wavelength': wavelength,
                    'rayleigh_range_zR': zR, 'beam_width_w_z': w_z,
                    'radius_of_curvature_R_z': R_z},
        'unit': 'm'
    }


def calc_rayleigh_range(w0: float = 1e-3, wavelength: float = 632.8e-9) -> dict:
    """Rayleigh range: zR = pi * w0^2 / wavelength."""
    zR = math.pi * w0 * w0 / wavelength
    return {
        'result': f'Rayleigh range zR = {zR:.4e} m',
        'details': {'beam_waist_w0': w0, 'wavelength': wavelength, 'rayleigh_range_zR': zR},
        'unit': 'm'
    }


def calc_beam_divergence(w0: float = 1e-3, wavelength: float = 632.8e-9) -> dict:
    """Far-field beam divergence half-angle: theta = wavelength / (pi * w0)."""
    theta = wavelength / (math.pi * w0)
    theta_mrad = theta * 1000.0
    full_angle = 2.0 * theta
    return {
        'result': f'Half-angle theta = {theta:.4e} rad = {theta_mrad:.4f} mrad, full angle = {full_angle:.4e} rad',
        'details': {'waist_w0': w0, 'wavelength': wavelength,
                    'half_angle_rad': theta, 'half_angle_mrad': theta_mrad,
                    'full_angle_rad': full_angle},
        'unit': 'rad'
    }


def calc_laser_cavity_modes(L: float = 0.5, wavelength: float = 632.8e-9) -> dict:
    """Longitudinal modes of a laser cavity: nu_m = m * c / (2L), FSR = c/(2L)."""
    c = 299792458.0
    FSR = c / (2.0 * L)
    return {
        'result': f'Free spectral range FSR = {FSR:.4e} Hz = {FSR/1e6:.4f} MHz',
        'details': {'cavity_length_L': L, 'wavelength': wavelength, 'c': c,
                    'FSR_Hz': FSR, 'FSR_MHz': FSR / 1e6},
        'unit': 'Hz'
    }


# =============================================================================
# NONLINEAR OPTICS
# =============================================================================

def calc_shg_phase_matching(n_fund: float = 1.6, n_shg: float = 1.6, wavelength: float = 1064e-9) -> dict:
    """SHG phase matching condition: delta_k = (4*pi/lambda)*(n_shg - n_fund)."""
    delta_k = (4.0 * math.pi / wavelength) * (n_shg - n_fund)
    phase_matched = abs(delta_k) < 1e-12
    if abs(delta_k) > 1e-15:
        coherence_length = math.pi / abs(delta_k)
    else:
        coherence_length = float('inf')
    return {
        'result': f'Phase mismatch delta_k = {delta_k:.4e} m^-1, matched: {phase_matched}, Lc = {coherence_length:.4e} m',
        'details': {'n_fundamental': n_fund, 'n_SHG': n_shg, 'wavelength': wavelength,
                    'delta_k': delta_k, 'phase_matched': phase_matched,
                    'coherence_length_Lc': coherence_length},
        'unit': 'm^-1'
    }


def calc_kerr_effect(n0: float = 1.5, n2: float = 3e-20, I: float = 1e14) -> dict:
    """Kerr effect nonlinear refractive index: n = n0 + n2 * I."""
    n_total = n0 + n2 * I
    delta_n = n2 * I
    return {
        'result': f'n = {n_total:.6f} (delta_n = {delta_n:.4e})',
        'details': {'n0_linear': n0, 'n2_m2_per_W': n2, 'intensity_I_W_m2': I,
                    'delta_n': delta_n, 'n_total': n_total},
        'unit': 'dimensionless'
    }


def calc_pockels_effect(n0: float = 2.2, r: float = 30e-12, E: float = 1e6) -> dict:
    """Pockels effect: delta_n = 0.5 * r * n0^3 * E."""
    delta_n = 0.5 * r * (n0 ** 3) * E
    n_total = n0 + delta_n
    return {
        'result': f'delta_n = {delta_n:.4e}, n = {n_total:.6f} at E = {E:.2e} V/m',
        'details': {'n0': n0, 'electro_optic_coeff_r_m_V': r, 'E_field': E,
                    'delta_n': delta_n, 'n_total': n_total},
        'unit': 'dimensionless'
    }


# =============================================================================
# FOURIER OPTICS
# =============================================================================

def calc_abbe_resolution(wavelength: float = 550e-9, NA: float = 0.5) -> dict:
    """Abbe diffraction limit: d = wavelength / (2 * NA)."""
    d = wavelength / (2.0 * NA)
    return {
        'result': f'Resolution limit d = {d:.4e} m = {d*1e6:.4f} um = {d*1e9:.2f} nm',
        'details': {'wavelength_m': wavelength, 'numerical_aperture_NA': NA,
                    'resolution_limit_d_m': d},
        'unit': 'm'
    }


def calc_spatial_frequency(feature_size: float = 1e-6) -> dict:
    """Spatial frequency: nu = 1 / feature_size (cycles per meter)."""
    nu = 1.0 / feature_size
    return {
        'result': f'Spatial frequency nu = {nu:.4e} cycles/m = {nu*1e-3:.4f} lp/mm',
        'details': {'feature_size_m': feature_size, 'spatial_frequency_cycles_per_m': nu,
                    'lp_per_mm': nu * 1e-3},
        'unit': 'cycles/m'
    }


def calc_otf_cutoff(wavelength: float = 550e-9, NA: float = 0.5) -> dict:
    """Optical transfer function cutoff frequency: nu_c = 2*NA / wavelength."""
    nu_c = 2.0 * NA / wavelength
    return {
        'result': f'Cutoff frequency nu_c = {nu_c:.4e} cycles/m = {nu_c*1e-3:.4f} lp/mm',
        'details': {'wavelength': wavelength, 'NA': NA,
                    'cutoff_spatial_frequency': nu_c},
        'unit': 'cycles/m'
    }


def calc_holography_recording(wavelength: float = 632.8e-9, theta_deg: float = 30.0) -> dict:
    """Holographic grating period: d = wavelength / (2 * sin(theta/2))."""
    theta = math.radians(theta_deg)
    d = wavelength / (2.0 * math.sin(theta / 2.0))
    freq = 1.0 / d
    return {
        'result': f'Grating period d = {d:.4e} m, spatial freq = {freq:.4e} lines/m',
        'details': {'wavelength': wavelength, 'angle_between_beams_deg': theta_deg,
                    'grating_period_d': d, 'spatial_frequency': freq},
        'unit': 'm'
    }


# =============================================================================
# ADDITIONAL OPTICS FUNCTIONS
# =============================================================================

def calc_numerical_aperture(n: float = 1.0, theta_deg: float = 30.0) -> dict:
    """Numerical aperture: NA = n * sin(theta)."""
    theta = math.radians(theta_deg)
    NA = n * math.sin(theta)
    return {
        'result': f'NA = {NA:.4f}',
        'details': {'refractive_index_n': n, 'half_angle_deg': theta_deg, 'NA': NA},
        'unit': 'dimensionless'
    }


def calc_f_number(f: float = 50.0, D: float = 25.0) -> dict:
    """f-number: f/# = f / D."""
    f_number = f / D
    return {
        'result': f'f/# = f/{f_number:.2f}',
        'details': {'focal_length_f': f, 'aperture_diameter_D': f_number,
                    'f_number': f / D},
        'unit': 'dimensionless'
    }


def calc_fiber_NA(n_core: float = 1.48, n_clad: float = 1.46) -> dict:
    """Fiber optic numerical aperture: NA = sqrt(n_core^2 - n_clad^2)."""
    NA = math.sqrt(n_core * n_core - n_clad * n_clad)
    theta_accept = math.degrees(math.asin(NA))
    return {
        'result': f'NA = {NA:.4f}, acceptance angle = {theta_accept:.4f} deg',
        'details': {'n_core': n_core, 'n_clad': n_clad, 'NA': NA,
                    'acceptance_angle_deg': theta_accept},
        'unit': 'dimensionless'
    }


def calc_fiber_v_number(a: float = 5e-6, wavelength: float = 1550e-9,
                          n_core: float = 1.48, n_clad: float = 1.46) -> dict:
    """V-parameter of an optical fiber: V = (2*pi*a/lambda)*sqrt(n_core^2 - n_clad^2)."""
    NA = math.sqrt(n_core * n_core - n_clad * n_clad)
    V = 2.0 * math.pi * a * NA / wavelength
    single_mode = V < 2.405
    n_modes = (V * V / 2.0) if V > 2.405 else 1.0
    return {
        'result': f'V = {V:.4f} ({"single-mode" if single_mode else "multi-mode"}, ~{n_modes:.0f} modes)',
        'details': {'core_radius_a': a, 'wavelength': wavelength, 'NA': NA,
                    'V_parameter': V, 'single_mode': single_mode, 'estimated_modes': n_modes},
        'unit': 'dimensionless'
    }


def calc_fresnel_reflection(n1: float = 1.0, n2: float = 1.5, theta_i_deg: float = 0.0) -> dict:
    """Fresnel reflection coefficient at normal incidence: R = ((n1-n2)/(n1+n2))^2."""
    theta_i = math.radians(theta_i_deg)
    if abs(theta_i) < 1e-9:
        R = ((n1 - n2) / (n1 + n2)) ** 2
        T = 1.0 - R
    else:
        theta_t = math.asin(n1 * math.sin(theta_i) / n2)
        Rs = ((n1 * math.cos(theta_i) - n2 * math.cos(theta_t)) /
              (n1 * math.cos(theta_i) + n2 * math.cos(theta_t))) ** 2
        Rp = ((n1 * math.cos(theta_t) - n2 * math.cos(theta_i)) /
              (n1 * math.cos(theta_t) + n2 * math.cos(theta_i))) ** 2
        R = (Rs + Rp) / 2.0
        T = 1.0 - R
    return {
        'result': f'Reflection R = {R:.6f}, Transmission T = {T:.6f} (normal incidence)',
        'details': {'n1': n1, 'n2': n2, 'theta_i_deg': theta_i_deg,
                    'R': R, 'T': T},
        'unit': 'dimensionless'
    }


def calc_wave_plate_retardance(delta_n: float = 0.009, t: float = 0.1e-3,
                                  wavelength: float = 632.8e-9) -> dict:
    """Wave plate retardance in waves: Gamma = delta_n * t / wavelength."""
    Gamma = delta_n * t / wavelength
    phase_shift = Gamma * 2.0 * math.pi
    phase_shift_deg = Gamma * 360.0
    return {
        'result': f'Retardance = {Gamma:.4f} waves = {phase_shift_deg:.2f} deg ({phase_shift:.4f} rad)',
        'details': {'delta_n': delta_n, 'thickness_t': t, 'wavelength': wavelength,
                    'retardance_waves': Gamma, 'phase_shift_rad': phase_shift,
                    'phase_shift_deg': phase_shift_deg},
        'unit': 'waves'
    }


def calc_quarter_wave_plate(wavelength: float = 632.8e-9, delta_n: float = 0.009) -> dict:
    """Quarter-wave plate thickness: t = lambda/(4*delta_n)."""
    t = wavelength / (4.0 * delta_n)
    return {
        'result': f'QWP thickness t = {t:.4e} m = {t*1e6:.4f} um',
        'details': {'wavelength': wavelength, 'delta_n': delta_n, 'thickness': t},
        'unit': 'm'
    }


def calc_half_wave_plate(wavelength: float = 632.8e-9, delta_n: float = 0.009) -> dict:
    """Half-wave plate thickness: t = lambda/(2*delta_n)."""
    t = wavelength / (2.0 * delta_n)
    return {
        'result': f'HWP thickness t = {t:.4e} m = {t*1e6:.4f} um',
        'details': {'wavelength': wavelength, 'delta_n': delta_n, 'thickness': t},
        'unit': 'm'
    }


def calc_abcd_matrix_lens(f: float = 10.0) -> dict:
    """ABCD matrix for a thin lens: [[1, 0], [-1/f, 1]]."""
    A, B, C, D = 1.0, 0.0, -1.0 / f, 1.0
    return {
        'result': f'Lens ABCD: [[{A}, {B}], [{C:.4f}, {D}]]',
        'details': {'focal_length_f': f, 'A': A, 'B': B, 'C': C, 'D': D},
        'unit': 'dimensionless'
    }


def calc_abcd_matrix_propagation(d: float = 10.0) -> dict:
    """ABCD matrix for free-space propagation of distance d: [[1, d], [0, 1]]."""
    return {
        'result': f'Free space ABCD: [[1, {d}], [0, 1]]',
        'details': {'distance_d': d, 'A': 1.0, 'B': d, 'C': 0.0, 'D': 1.0},
        'unit': 'dimensionless'
    }


def calc_etalon_transmission(R: float = 0.9, delta: float = math.pi / 2.0) -> dict:
    """Fabry-Perot etalon transmission: T = 1/(1 + F*sin^2(delta/2)), F = 4R/(1-R)^2."""
    F = 4.0 * R / ((1.0 - R) ** 2)
    T = 1.0 / (1.0 + F * math.sin(delta / 2.0) ** 2)
    return {
        'result': f'Transmission T = {T:.6f}, Finesse F = {F:.4f}',
        'details': {'reflectivity_R': R, 'phase_delta': delta, 'finesse_F': F, 'T': T},
        'unit': 'dimensionless'
    }


def calc_diffraction_efficiency(m: int = 1) -> dict:
    """Ideal blazed grating efficiency ~ sinc^2(pi*(m-order_opt/order_actual))."""
    order_opt = float(m)
    eta = math.sinc(order_opt) ** 2 if order_opt != 0 else 1.0
    return {
        'result': f'Diffraction efficiency (ideal) eta = {eta:.4f}',
        'details': {'order_m': m, 'eta': eta},
        'unit': 'dimensionless'
    }


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Geometric Optics
    'snells_law': {'func': calc_snells_law, 'params': ['n1', 'theta1_deg', 'n2'],
                   'desc': "Snell's law n1*sin(theta1) = n2*sin(theta2)"},
    'critical_angle': {'func': calc_critical_angle, 'params': ['n1', 'n2'],
                       'desc': 'Critical angle for total internal reflection'},
    'lens_equation': {'func': calc_lens_equation, 'params': ['u', 'f'],
                       'desc': 'Thin lens equation: 1/f = 1/u + 1/v'},
    'lens_eq_solve': {'func': calc_lens_eq_solve, 'params': ['u', 'v', 'f'],
                       'desc': 'Thin lens equation: solve for unknown; set None'},
    'magnification': {'func': calc_magnification, 'params': ['u', 'v'],
                      'desc': 'Lateral magnification m = -v/u'},
    'lens_makers_formula': {'func': calc_lens_makers_formula, 'params': ['n', 'R1', 'R2'],
                             'desc': "Lens maker's formula 1/f = (n-1)*(1/R1 - 1/R2)"},
    'mirror_equation': {'func': calc_mirror_equation, 'params': ['u', 'f'],
                         'desc': 'Spherical mirror 1/f = 1/u + 1/v'},
    'prism_deviation': {'func': calc_prism_deviation, 'params': ['n', 'A_deg', 'i1_deg'],
                         'desc': 'Prism deviation angle for given incidence'},
    'minimum_deviation': {'func': calc_minimum_deviation, 'params': ['n', 'A_deg'],
                           'desc': 'Minimum deviation of a prism'},
    'optical_power': {'func': calc_optical_power, 'params': ['f'],
                      'desc': 'Optical power P = 1/f in diopters'},
    'two_lens_system': {'func': calc_two_lens_system, 'params': ['f1', 'f2', 'd', 'u1'],
                         'desc': 'Two-lens system image position and magnification'},
    # Wave Optics
    'youngs_double_slit': {'func': calc_youngs_double_slit,
                            'params': ['wavelength', 'd', 'D', 'm'],
                            'desc': 'Young double slit fringe position y = m*lambda*D/d'},
    'double_slit_angular': {'func': calc_double_slit_angular,
                              'params': ['wavelength', 'd', 'm'],
                              'desc': 'Double slit angular position d*sin(theta) = m*lambda'},
    'thin_film_interference': {'func': calc_thin_film_interference,
                                'params': ['n', 't', 'm', 'wavelength_vacuum'],
                                'desc': 'Thin film interference 2nt = m*lambda'},
    'single_slit_diffraction': {'func': calc_single_slit_diffraction,
                                  'params': ['wavelength', 'a', 'm'],
                                  'desc': 'Single slit diffraction a*sin(theta) = m*lambda'},
    'grating_equation': {'func': calc_grating_equation,
                          'params': ['d', 'wavelength', 'm'],
                          'desc': 'Diffraction grating d*sin(theta) = m*lambda'},
    'grating_resolution': {'func': calc_grating_resolution, 'params': ['N', 'm'],
                            'desc': 'Grating resolving power R = N*m'},
    'malus_law': {'func': calc_malus_law, 'params': ['I0', 'theta_deg'],
                  'desc': "Malus law I = I0*cos^2(theta)"},
    'brewster_angle': {'func': calc_brewster_angle, 'params': ['n1', 'n2'],
                        'desc': "Brewster angle tan(theta_B) = n2/n1"},
    'dispersion_cauchy': {'func': calc_dispersion_cauchy,
                           'params': ['n_values', 'wavelength_values'],
                           'desc': 'Cauchy dispersion approximation n(lambda) = A + B/lambda^2'},
    # Photometry
    'luminous_flux': {'func': calc_luminous_flux, 'params': ['I', 'omega'],
                      'desc': 'Luminous flux Phi = I * omega (cd*sr -> lm)'},
    'illuminance': {'func': calc_illuminance, 'params': ['Phi', 'A'],
                    'desc': 'Illuminance E = Phi/A (lux = lm/m^2)'},
    'inverse_square_law_light': {'func': calc_inverse_square_law_light, 'params': ['I', 'r'],
                                  'desc': 'Inverse square law E = I/r^2'},
    'luminance': {'func': calc_luminance, 'params': ['I', 'A', 'theta_deg'],
                  'desc': 'Luminance L = I/(A*cos(theta))'},
    # Laser Optics
    'gaussian_beam_width': {'func': calc_gaussian_beam_width,
                             'params': ['z', 'w0', 'wavelength'],
                             'desc': 'Gaussian beam width w(z) and radius of curvature'},
    'rayleigh_range': {'func': calc_rayleigh_range, 'params': ['w0', 'wavelength'],
                        'desc': 'Rayleigh range zR = pi*w0^2/lambda'},
    'beam_divergence': {'func': calc_beam_divergence, 'params': ['w0', 'wavelength'],
                         'desc': 'Far-field beam divergence theta = lambda/(pi*w0)'},
    'laser_cavity_modes': {'func': calc_laser_cavity_modes, 'params': ['L', 'wavelength'],
                            'desc': 'Laser cavity longitudinal modes and FSR'},
    # Nonlinear Optics
    'shg_phase_matching': {'func': calc_shg_phase_matching,
                            'params': ['n_fund', 'n_shg', 'wavelength'],
                            'desc': 'SHG phase matching delta_k = (4pi/lambda)*(n_shg - n_fund)'},
    'kerr_effect': {'func': calc_kerr_effect, 'params': ['n0', 'n2', 'I'],
                     'desc': 'Kerr effect n = n0 + n2*I'},
    'pockels_effect': {'func': calc_pockels_effect, 'params': ['n0', 'r', 'E'],
                        'desc': 'Pockels effect delta_n = 0.5*r*n0^3*E'},
    # Fourier Optics
    'abbe_resolution': {'func': calc_abbe_resolution, 'params': ['wavelength', 'NA'],
                         'desc': 'Abbe diffraction limit d = lambda/(2*NA)'},
    'spatial_frequency': {'func': calc_spatial_frequency, 'params': ['feature_size'],
                           'desc': 'Spatial frequency nu = 1/feature_size'},
    'otf_cutoff': {'func': calc_otf_cutoff, 'params': ['wavelength', 'NA'],
                    'desc': 'OTF cutoff frequency nu_c = 2*NA/lambda'},
    'holography_recording': {'func': calc_holography_recording,
                               'params': ['wavelength', 'theta_deg'],
                               'desc': 'Holographic grating period d = lambda/(2*sin(theta/2))'},
    # Additional
    'numerical_aperture': {'func': calc_numerical_aperture, 'params': ['n', 'theta_deg'],
                            'desc': 'NA = n*sin(theta)'},
    'f_number': {'func': calc_f_number, 'params': ['f', 'D'],
                  'desc': 'f-number f/# = focal_length / aperture_diameter'},
    'fiber_NA': {'func': calc_fiber_NA, 'params': ['n_core', 'n_clad'],
                  'desc': 'Fiber NA = sqrt(n_core^2 - n_clad^2)'},
    'fiber_v_number': {'func': calc_fiber_v_number,
                        'params': ['a', 'wavelength', 'n_core', 'n_clad'],
                        'desc': 'Fiber V-parameter V = (2pi*a/lambda)*NA'},
    'fresnel_reflection': {'func': calc_fresnel_reflection,
                            'params': ['n1', 'n2', 'theta_i_deg'],
                            'desc': 'Fresnel reflection coefficient'},
    'wave_plate_retardance': {'func': calc_wave_plate_retardance,
                                'params': ['delta_n', 't', 'wavelength'],
                                'desc': 'Wave plate retardance in waves'},
    'quarter_wave_plate': {'func': calc_quarter_wave_plate, 'params': ['wavelength', 'delta_n'],
                            'desc': 'Quarter-wave plate thickness t = lambda/(4*delta_n)'},
    'half_wave_plate': {'func': calc_half_wave_plate, 'params': ['wavelength', 'delta_n'],
                         'desc': 'Half-wave plate thickness t = lambda/(2*delta_n)'},
    'abcd_matrix_lens': {'func': calc_abcd_matrix_lens, 'params': ['f'],
                          'desc': 'ABCD matrix for a thin lens'},
    'abcd_matrix_propagation': {'func': calc_abcd_matrix_propagation, 'params': ['d'],
                                 'desc': 'ABCD matrix for free-space propagation'},
    'etalon_transmission': {'func': calc_etalon_transmission, 'params': ['R', 'delta'],
                             'desc': 'Fabry-Perot etalon transmission function'},
    'diffraction_efficiency': {'func': calc_diffraction_efficiency, 'params': ['m'],
                                'desc': 'Diffraction efficiency of blazed grating'},
}
