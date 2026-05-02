"""
Classical Mechanics - Physics Computation Module
"""
import math
import numpy as np

COMMANDS = {}


# =============================================================================
# KINEMATICS - Linear Motion
# =============================================================================

def calc_linear_velocity(u: float = 0.0, a: float = 9.81, t: float = 1.0) -> dict:
    """Calculate final velocity from initial velocity, acceleration and time: v = u + at."""
    v = u + a * t
    return {
        'result': f'Final velocity v = {v:.4f} m/s',
        'details': {'initial_velocity_u': u, 'acceleration_a': a, 'time_t': t, 'final_velocity_v': v},
        'unit': 'm/s'
    }


def calc_linear_displacement(u: float = 0.0, a: float = 9.81, t: float = 1.0) -> dict:
    """Calculate displacement: s = ut + 0.5at^2."""
    s = u * t + 0.5 * a * t * t
    return {
        'result': f'Displacement s = {s:.4f} m',
        'details': {'initial_velocity_u': u, 'acceleration_a': a, 'time_t': t, 'displacement_s': s},
        'unit': 'm'
    }


def calc_velocity_displacement(u: float = 0.0, a: float = 9.81, s: float = 10.0) -> dict:
    """Calculate final velocity without time: v^2 = u^2 + 2as."""
    v_sq = u * u + 2.0 * a * s
    if v_sq < 0:
        return {'result': 'No real solution (v^2 < 0)', 'details': {'u': u, 'a': a, 's': s, 'v_squared': v_sq}, 'unit': 'm/s'}
    v = math.sqrt(v_sq)
    return {
        'result': f'Final velocity v = {v:.4f} m/s',
        'details': {'initial_velocity_u': u, 'acceleration_a': a, 'displacement_s': s, 'final_velocity_v': v},
        'unit': 'm/s'
    }


def calc_time_from_distance(u: float = 0.0, a: float = 9.81, s: float = 10.0) -> dict:
    """Solve for time given u, a, s using quadratic: 0.5at^2 + ut - s = 0."""
    if abs(a) < 1e-15:
        if abs(u) < 1e-15:
            return {'result': 'No motion (u=0, a=0)', 'details': {}, 'unit': 's'}
        t = s / u
        t = max(t, 0.0)
        return {
            'result': f'Time t = {t:.4f} s (constant velocity)',
            'details': {'u': u, 'a': a, 's': s, 't': t},
            'unit': 's'
        }
    disc = u * u + 2.0 * a * s
    if disc < 0:
        return {'result': 'No real solution (discriminant < 0)', 'details': {'discriminant': disc}, 'unit': 's'}
    sqrt_disc = math.sqrt(disc)
    t1 = (-u + sqrt_disc) / a
    t2 = (-u - sqrt_disc) / a
    t_positive = max(t1, t2) if max(t1, t2) >= 0 else (t1 if t1 >= 0 else t2)
    return {
        'result': f'Time t = {t_positive:.4f} s',
        'details': {'u': u, 'a': a, 's': s, 't1': t1, 't2': t2, 't_positive': t_positive},
        'unit': 's'
    }


def calc_acceleration(u: float = 0.0, v: float = 20.0, t: float = 2.0) -> dict:
    """Calculate acceleration: a = (v - u) / t."""
    a = (v - u) / t
    return {
        'result': f'Acceleration a = {a:.4f} m/s^2',
        'details': {'initial_velocity_u': u, 'final_velocity_v': v, 'time_t': t, 'acceleration_a': a},
        'unit': 'm/s^2'
    }


# =============================================================================
# KINEMATICS - Projectile Motion
# =============================================================================

def calc_projectile_range(v0: float = 20.0, angle_deg: float = 45.0, g: float = 9.81) -> dict:
    """Calculate projectile range: R = v0^2 * sin(2*theta) / g."""
    theta = math.radians(angle_deg)
    R = v0 * v0 * math.sin(2.0 * theta) / g
    return {
        'result': f'Range R = {R:.4f} m',
        'details': {'initial_velocity_v0': v0, 'angle_deg': angle_deg, 'angle_rad': theta,
                    'gravity_g': g, 'range_R': R},
        'unit': 'm'
    }


def calc_max_height(v0: float = 20.0, angle_deg: float = 45.0, g: float = 9.81) -> dict:
    """Calculate maximum height: H = (v0*sin(theta))^2 / (2g)."""
    theta = math.radians(angle_deg)
    vy = v0 * math.sin(theta)
    H = vy * vy / (2.0 * g)
    return {
        'result': f'Max height H = {H:.4f} m',
        'details': {'initial_velocity_v0': v0, 'angle_deg': angle_deg, 'angle_rad': theta,
                    'vertical_velocity_vy': vy, 'gravity_g': g, 'max_height_H': H},
        'unit': 'm'
    }


def calc_time_of_flight(v0: float = 20.0, angle_deg: float = 45.0, g: float = 9.81) -> dict:
    """Calculate time of flight: T = 2*v0*sin(theta)/g."""
    theta = math.radians(angle_deg)
    vy = v0 * math.sin(theta)
    T = 2.0 * vy / g
    return {
        'result': f'Time of flight T = {T:.4f} s',
        'details': {'initial_velocity_v0': v0, 'angle_deg': angle_deg, 'angle_rad': theta,
                    'vertical_velocity_vy': vy, 'gravity_g': g, 'time_of_flight_T': T},
        'unit': 's'
    }


def calc_projectile_trajectory(v0: float = 20.0, angle_deg: float = 45.0, g: float = 9.81,
                               t: float = 1.0) -> dict:
    """Calculate projectile position (x, y) at time t."""
    theta = math.radians(angle_deg)
    vx = v0 * math.cos(theta)
    vy = v0 * math.sin(theta)
    x = vx * t
    y = vy * t - 0.5 * g * t * t
    return {
        'result': f'Position at t={t:.2f}s: x = {x:.4f} m, y = {y:.4f} m',
        'details': {'t': t, 'vx': vx, 'vy': vy, 'x': x, 'y': y},
        'unit': 'm'
    }


def calc_optimal_angle(v0: float = 20.0, g: float = 9.81) -> dict:
    """Optimal launch angle for maximum range (45 degrees on flat ground)."""
    theta_opt = math.radians(45.0)
    R_max = v0 * v0 / g
    return {
        'result': f'Optimal angle = 45 deg, Max range = {R_max:.4f} m',
        'details': {'optimal_angle_deg': 45.0, 'optimal_angle_rad': theta_opt,
                    'initial_velocity_v0': v0, 'max_range': R_max},
        'unit': 'm'
    }


# =============================================================================
# KINEMATICS - Circular Motion
# =============================================================================

def calc_angular_velocity_from_rpm(rpm: float = 120.0) -> dict:
    """Convert rpm to angular velocity: omega = 2*pi*rpm/60."""
    omega = 2.0 * math.pi * rpm / 60.0
    freq = rpm / 60.0
    T = 1.0 / freq if freq > 0 else float('inf')
    return {
        'result': f'Angular velocity omega = {omega:.4f} rad/s, f = {freq:.4f} Hz, T = {T:.4f} s',
        'details': {'rpm': rpm, 'omega_rad_s': omega, 'frequency_Hz': freq, 'period_s': T},
        'unit': 'rad/s'
    }


def calc_circ_tangential_velocity(r: float = 1.0, omega: float = 6.283) -> dict:
    """Tangential velocity in circular motion: v = r * omega."""
    v = r * omega
    return {
        'result': f'Tangential velocity v = {v:.4f} m/s',
        'details': {'radius_r': r, 'angular_velocity_omega': omega, 'tangential_velocity_v': v},
        'unit': 'm/s'
    }


def calc_centripetal_acceleration(v: float = 10.0, r: float = 2.0) -> dict:
    """Centripetal acceleration: a_c = v^2 / r."""
    a_c = v * v / r
    omega = v / r
    return {
        'result': f'Centripetal acceleration a_c = {a_c:.4f} m/s^2',
        'details': {'velocity_v': v, 'radius_r': r, 'centripetal_accel_a_c': a_c,
                    'angular_velocity_omega': omega},
        'unit': 'm/s^2'
    }


def calc_angular_acceleration(omega0: float = 0.0, omega: float = 10.0, t: float = 2.0) -> dict:
    """Angular acceleration: alpha = (omega - omega0) / t."""
    alpha = (omega - omega0) / t
    return {
        'result': f'Angular acceleration alpha = {alpha:.4f} rad/s^2',
        'details': {'omega_initial': omega0, 'omega_final': omega, 'time_t': t,
                    'alpha': alpha},
        'unit': 'rad/s^2'
    }


def calc_centripetal_force(m: float = 1.0, v: float = 10.0, r: float = 2.0) -> dict:
    """Centripetal force: F_c = m*v^2/r."""
    F_c = m * v * v / r
    return {
        'result': f'Centripetal force F_c = {F_c:.4f} N',
        'details': {'mass_m': m, 'velocity_v': v, 'radius_r': r, 'force_F_c': F_c},
        'unit': 'N'
    }


# =============================================================================
# DYNAMICS - Newton's Laws and Forces
# =============================================================================

def calc_newton2_force(m: float = 10.0, a: float = 2.0) -> dict:
    """Newton's 2nd law: F = m*a."""
    F = m * a
    return {
        'result': f'Force F = {F:.4f} N',
        'details': {'mass_m': m, 'acceleration_a': a, 'force_F': F},
        'unit': 'N'
    }


def calc_newton2_acceleration(F: float = 50.0, m: float = 10.0) -> dict:
    """Newton's 2nd law: a = F/m."""
    if m == 0:
        return {'result': 'Mass cannot be zero', 'details': {}, 'unit': 'm/s^2'}
    a = F / m
    return {
        'result': f'Acceleration a = {a:.4f} m/s^2',
        'details': {'force_F': F, 'mass_m': m, 'acceleration_a': a},
        'unit': 'm/s^2'
    }


def calc_weight(m: float = 70.0, g: float = 9.81) -> dict:
    """Weight: W = m*g."""
    W = m * g
    return {
        'result': f'Weight W = {W:.4f} N',
        'details': {'mass_m': m, 'gravity_g': g, 'weight_W': W},
        'unit': 'N'
    }


def calc_friction(mu: float = 0.3, N: float = 100.0) -> dict:
    """Friction force: f = mu * N (static or kinetic generic)."""
    f = mu * N
    return {
        'result': f'Friction force f = {f:.4f} N',
        'details': {'coefficient_mu': mu, 'normal_force_N': N, 'friction_force_f': f},
        'unit': 'N'
    }


def calc_static_friction_max(mu_s: float = 0.5, N: float = 100.0) -> dict:
    """Maximum static friction: f_s_max = mu_s * N."""
    f_s = mu_s * N
    return {
        'result': f'Max static friction f_s_max = {f_s:.4f} N',
        'details': {'mu_static': mu_s, 'normal_force_N': N, 'f_s_max': f_s},
        'unit': 'N'
    }


def calc_spring_force(k: float = 100.0, x: float = 0.1) -> dict:
    """Hooke's law spring force: F = -k*x."""
    F = -k * x
    U = 0.5 * k * x * x
    return {
        'result': f'Spring force F = {F:.4f} N, Potential energy U = {U:.4f} J',
        'details': {'spring_constant_k': k, 'displacement_x': x, 'force_F': F,
                    'potential_energy_U': U},
        'unit': 'N'
    }


def calc_gravitational_force(m1: float = 5.97e24, m2: float = 7.35e22,
                              r: float = 3.84e8) -> dict:
    """Newton's law of gravitation: F = G*m1*m2/r^2."""
    G = 6.67430e-11
    F = G * m1 * m2 / (r * r)
    return {
        'result': f'Gravitational force F = {F:.4e} N',
        'details': {'G': G, 'm1': m1, 'm2': m2, 'distance_r': r, 'force_F': F},
        'unit': 'N'
    }


def calc_resultant_force_2d(F1x: float = 10.0, F1y: float = 0.0,
                             F2x: float = 0.0, F2y: float = 10.0) -> dict:
    """Calculate resultant of two 2D force vectors."""
    Rx = F1x + F2x
    Ry = F1y + F2y
    R = math.sqrt(Rx * Rx + Ry * Ry)
    angle = math.degrees(math.atan2(Ry, Rx))
    return {
        'result': f'Resultant R = {R:.4f} N at {angle:.2f} degrees',
        'details': {'Rx': Rx, 'Ry': Ry, 'magnitude_R': R, 'angle_deg': angle},
        'unit': 'N'
    }


# =============================================================================
# WORK AND ENERGY
# =============================================================================

def calc_work(F: float = 50.0, d: float = 2.0, angle_deg: float = 0.0) -> dict:
    """Work done: W = F*d*cos(theta)."""
    theta = math.radians(angle_deg)
    W = F * d * math.cos(theta)
    return {
        'result': f'Work W = {W:.4f} J',
        'details': {'force_F': F, 'displacement_d': d, 'angle_deg': angle_deg,
                    'theta_rad': theta, 'work_W': W},
        'unit': 'J'
    }


def calc_kinetic_energy(m: float = 10.0, v: float = 5.0) -> dict:
    """Kinetic energy: KE = 0.5*m*v^2."""
    KE = 0.5 * m * v * v
    return {
        'result': f'Kinetic energy KE = {KE:.4f} J',
        'details': {'mass_m': m, 'velocity_v': v, 'KE': KE},
        'unit': 'J'
    }


def calc_potential_energy_grav(m: float = 10.0, h: float = 5.0, g: float = 9.81) -> dict:
    """Gravitational potential energy: PE = m*g*h."""
    PE = m * g * h
    return {
        'result': f'Gravitational PE = {PE:.4f} J',
        'details': {'mass_m': m, 'height_h': h, 'gravity_g': g, 'PE': PE},
        'unit': 'J'
    }


def calc_potential_energy_spring(k: float = 100.0, x: float = 0.1) -> dict:
    """Spring potential energy: U = 0.5*k*x^2."""
    U = 0.5 * k * x * x
    return {
        'result': f'Spring potential energy U = {U:.4f} J',
        'details': {'spring_constant_k': k, 'displacement_x': x, 'U': U},
        'unit': 'J'
    }


def calc_mechanical_energy(KE: float = 100.0, PE: float = 50.0) -> dict:
    """Total mechanical energy: E = KE + PE."""
    E = KE + PE
    return {
        'result': f'Total mechanical energy E = {E:.4f} J',
        'details': {'KE': KE, 'PE': PE, 'total_E': E},
        'unit': 'J'
    }


def calc_power_work(W: float = 500.0, t: float = 10.0) -> dict:
    """Power: P = W/t."""
    P = W / t if t > 0 else float('inf')
    return {
        'result': f'Power P = {P:.4f} W',
        'details': {'work_W': W, 'time_t': t, 'power_P': P},
        'unit': 'W'
    }


def calc_power_force_velocity(F: float = 100.0, v: float = 5.0) -> dict:
    """Power from force and velocity: P = F*v."""
    P = F * v
    return {
        'result': f'Power P = {P:.4f} W',
        'details': {'force_F': F, 'velocity_v': v, 'power_P': P},
        'unit': 'W'
    }


# =============================================================================
# MOMENTUM AND IMPULSE
# =============================================================================

def calc_momentum(m: float = 10.0, v: float = 5.0) -> dict:
    """Linear momentum: p = m*v."""
    p = m * v
    return {
        'result': f'Momentum p = {p:.4f} kg*m/s',
        'details': {'mass_m': m, 'velocity_v': v, 'momentum_p': p},
        'unit': 'kg*m/s'
    }


def calc_impulse(F: float = 100.0, dt: float = 0.5) -> dict:
    """Impulse: J = F*dt = delta_p."""
    J = F * dt
    return {
        'result': f'Impulse J = {J:.4f} N*s',
        'details': {'force_F': F, 'time_interval_dt': dt, 'impulse_J': J},
        'unit': 'N*s'
    }


def calc_momentum_conservation_1d(m1: float = 2.0, v1: float = 5.0,
                                   m2: float = 3.0, v2: float = 0.0,
                                   v1_prime: float = 1.0) -> dict:
    """Calculate v2' from conservation of momentum: m1*v1 + m2*v2 = m1*v1' + m2*v2'."""
    p_initial = m1 * v1 + m2 * v2
    v2_prime = (p_initial - m1 * v1_prime) / m2 if m2 != 0 else float('inf')
    p_final = m1 * v1_prime + m2 * v2_prime
    return {
        'result': f'v2_prime = {v2_prime:.4f} m/s',
        'details': {'m1': m1, 'v1': v1, 'm2': m2, 'v2': v2,
                    'v1_prime': v1_prime, 'v2_prime': v2_prime,
                    'p_initial': p_initial, 'p_final': p_final},
        'unit': 'm/s'
    }


def calc_elastic_collision_1d(m1: float = 2.0, v1: float = 5.0,
                               m2: float = 3.0, v2: float = 0.0) -> dict:
    """Elastic collision in 1D: v1' = ((m1-m2)/(m1+m2))*v1 + (2*m2/(m1+m2))*v2."""
    m_sum = m1 + m2
    v1_p = (m1 - m2) / m_sum * v1 + (2.0 * m2) / m_sum * v2
    v2_p = (2.0 * m1) / m_sum * v1 + (m2 - m1) / m_sum * v2
    KE_i = 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2
    KE_f = 0.5 * m1 * v1_p * v1_p + 0.5 * m2 * v2_p * v2_p
    return {
        'result': f"v1' = {v1_p:.4f} m/s, v2' = {v2_p:.4f} m/s",
        'details': {'m1': m1, 'v1': v1, 'm2': m2, 'v2': v2,
                    'v1_prime': v1_p, 'v2_prime': v2_p,
                    'KE_initial': KE_i, 'KE_final': KE_f, 'KE_conserved': abs(KE_i - KE_f) < 1e-9},
        'unit': 'm/s'
    }


def calc_perfectly_inelastic_collision(m1: float = 2.0, v1: float = 5.0,
                                        m2: float = 3.0, v2: float = 0.0) -> dict:
    """Perfectly inelastic collision: v_f = (m1*v1 + m2*v2)/(m1 + m2)."""
    m_sum = m1 + m2
    v_f = (m1 * v1 + m2 * v2) / m_sum
    KE_i = 0.5 * m1 * v1 * v1 + 0.5 * m2 * v2 * v2
    KE_f = 0.5 * m_sum * v_f * v_f
    KE_loss = KE_i - KE_f
    return {
        'result': f'Final velocity v_f = {v_f:.4f} m/s, KE loss = {KE_loss:.4f} J',
        'details': {'m1': m1, 'v1': v1, 'm2': m2, 'v2': v2,
                    'v_final': v_f, 'KE_initial': KE_i, 'KE_final': KE_f, 'KE_loss': KE_loss},
        'unit': 'm/s'
    }


# =============================================================================
# RIGID BODY DYNAMICS
# =============================================================================

def calc_moment_of_inertia_point(m: float = 1.0, r: float = 1.0) -> dict:
    """Moment of inertia of a point mass: I = m*r^2."""
    I = m * r * r
    return {
        'result': f'Moment of inertia I = {I:.4f} kg*m^2',
        'details': {'mass_m': m, 'distance_r': r, 'I': I},
        'unit': 'kg*m^2'
    }


def calc_moment_of_inertia_rod(m: float = 2.0, L: float = 1.0, axis: str = 'center') -> dict:
    """Moment of inertia of a thin rod about center (I=mL^2/12) or end (I=mL^2/3)."""
    if axis.lower() == 'center':
        I = m * L * L / 12.0
        desc = 'about center'
    elif axis.lower() == 'end':
        I = m * L * L / 3.0
        desc = 'about end'
    else:
        return {'result': 'axis must be "center" or "end"', 'details': {}, 'unit': 'kg*m^2'}
    return {
        'result': f'Moment of inertia I = {I:.4f} kg*m^2 ({desc})',
        'details': {'mass_m': m, 'length_L': L, 'axis': axis, 'I': I},
        'unit': 'kg*m^2'
    }


def calc_moment_of_inertia_disk(m: float = 2.0, R: float = 0.5) -> dict:
    """Moment of inertia of a solid disk: I = 0.5*m*R^2."""
    I = 0.5 * m * R * R
    return {
        'result': f'Moment of inertia I = {I:.4f} kg*m^2',
        'details': {'mass_m': m, 'radius_R': R, 'shape': 'solid_disk', 'I': I},
        'unit': 'kg*m^2'
    }


def calc_moment_of_inertia_sphere(m: float = 2.0, R: float = 0.5) -> dict:
    """Moment of inertia of a solid sphere: I = (2/5)*m*R^2."""
    I = 0.4 * m * R * R  # 2/5 = 0.4
    return {
        'result': f'Moment of inertia I = {I:.4f} kg*m^2',
        'details': {'mass_m': m, 'radius_R': R, 'shape': 'solid_sphere', 'I': I},
        'unit': 'kg*m^2'
    }


def calc_moment_of_inertia_hoop(m: float = 2.0, R: float = 0.5) -> dict:
    """Moment of inertia of a thin hoop: I = m*R^2."""
    I = m * R * R
    return {
        'result': f'Moment of inertia I = {I:.4f} kg*m^2',
        'details': {'mass_m': m, 'radius_R': R, 'shape': 'thin_hoop', 'I': I},
        'unit': 'kg*m^2'
    }


def calc_torque(r: float = 0.5, F: float = 20.0, angle_deg: float = 90.0) -> dict:
    """Torque: tau = r * F * sin(theta)."""
    theta = math.radians(angle_deg)
    tau = r * F * math.sin(theta)
    return {
        'result': f'Torque tau = {tau:.4f} N*m',
        'details': {'lever_arm_r': r, 'force_F': F, 'angle_deg': angle_deg,
                    'theta_rad': theta, 'torque_tau': tau},
        'unit': 'N*m'
    }


def calc_angular_momentum(I: float = 1.0, omega: float = 10.0) -> dict:
    """Angular momentum: L = I * omega."""
    L = I * omega
    return {
        'result': f'Angular momentum L = {L:.4f} kg*m^2/s',
        'details': {'moment_of_inertia_I': I, 'angular_velocity_omega': omega, 'L': L},
        'unit': 'kg*m^2/s'
    }


def calc_rotational_kinetic_energy(I: float = 1.0, omega: float = 10.0) -> dict:
    """Rotational kinetic energy: KE_rot = 0.5 * I * omega^2."""
    KE = 0.5 * I * omega * omega
    return {
        'result': f'Rotational KE = {KE:.4f} J',
        'details': {'I': I, 'omega': omega, 'KE_rot': KE},
        'unit': 'J'
    }


def calc_rigid_body_equilibrium(forces: list = None, distances: list = None) -> dict:
    """Check rigid body equilibrium: sum of forces = 0, sum of torques = 0."""
    if forces is None:
        forces = [10.0, -10.0]
    if distances is None:
        distances = [0.5, 0.5]
    F_sum = sum(forces)
    tau_sum = sum(f * d for f, d in zip(forces, distances))
    in_equilibrium = abs(F_sum) < 1e-12 and abs(tau_sum) < 1e-12
    return {
        'result': f'Equilibrium: {in_equilibrium} (sum_F={F_sum:.4e}, sum_tau={tau_sum:.4e})',
        'details': {'sum_forces': F_sum, 'sum_torques': tau_sum, 'in_equilibrium': in_equilibrium},
        'unit': 'N / N*m'
    }


def calc_gyroscope_precession(I: float = 0.01, omega_spin: float = 200.0, tau: float = 0.5) -> dict:
    """Gyroscope precession angular velocity: omega_p = tau / (I * omega_spin)."""
    L = I * omega_spin
    if abs(L) < 1e-15:
        return {'result': 'Angular momentum L is zero', 'details': {'L': L}, 'unit': 'rad/s'}
    omega_p = tau / L
    T_p = 2.0 * math.pi / abs(omega_p) if abs(omega_p) > 1e-15 else float('inf')
    return {
        'result': f'Precession omega_p = {omega_p:.4f} rad/s, Period T_p = {T_p:.4f} s',
        'details': {'I': I, 'omega_spin': omega_spin, 'torque_tau': tau,
                    'angular_momentum_L': L, 'omega_precession': omega_p, 'period_precession': T_p},
        'unit': 'rad/s'
    }


# =============================================================================
# FLUID MECHANICS
# =============================================================================

def calc_hydrostatic_pressure(rho: float = 1000.0, h: float = 10.0, g: float = 9.81,
                               P_atm: float = 101325.0) -> dict:
    """Hydrostatic pressure: P = P_atm + rho * g * h."""
    P_gauge = rho * g * h
    P_abs = P_atm + P_gauge
    return {
        'result': f'Absolute P = {P_abs:.2f} Pa, Gauge P = {P_gauge:.2f} Pa',
        'details': {'density_rho': rho, 'depth_h': h, 'gravity_g': g,
                    'atmospheric_pressure': P_atm, 'gauge_pressure': P_gauge, 'absolute_pressure': P_abs},
        'unit': 'Pa'
    }


def calc_buoyancy_force(rho_fluid: float = 1000.0, V_submerged: float = 0.001, g: float = 9.81) -> dict:
    """Archimedes buoyancy force: F_b = rho_fluid * V_submerged * g."""
    F_b = rho_fluid * V_submerged * g
    return {
        'result': f'Buoyancy force F_b = {F_b:.4f} N',
        'details': {'fluid_density': rho_fluid, 'submerged_volume': V_submerged, 'g': g,
                    'buoyancy_force': F_b},
        'unit': 'N'
    }


def calc_bernoulli(P1: float = 101325.0, rho: float = 1000.0, v1: float = 1.0,
                   h1: float = 0.0, v2: float = 3.0, h2: float = 0.0, g: float = 9.81) -> dict:
    """Bernoulli equation: P1 + 0.5*rho*v1^2 + rho*g*h1 = P2 + 0.5*rho*v2^2 + rho*g*h2."""
    P2 = P1 + 0.5 * rho * (v1 * v1 - v2 * v2) + rho * g * (h1 - h2)
    return {
        'result': f'Pressure P2 = {P2:.2f} Pa',
        'details': {'P1': P1, 'rho': rho, 'v1': v1, 'v2': v2, 'h1': h1, 'h2': h2,
                    'P2': P2},
        'unit': 'Pa'
    }


def calc_flow_rate(A: float = 0.01, v: float = 2.0) -> dict:
    """Volumetric flow rate: Q = A * v."""
    Q = A * v
    return {
        'result': f'Flow rate Q = {Q:.6f} m^3/s',
        'details': {'cross_section_A': A, 'velocity_v': v, 'flow_rate_Q': Q},
        'unit': 'm^3/s'
    }


def calc_poiseuille_flow(R: float = 0.01, delta_P: float = 100.0, eta: float = 0.001,
                          L: float = 1.0) -> dict:
    """Poiseuille flow rate in a pipe: Q = (pi * R^4 * delta_P) / (8 * eta * L)."""
    Q = math.pi * (R ** 4) * delta_P / (8.0 * eta * L)
    return {
        'result': f'Flow rate Q = {Q:.4e} m^3/s',
        'details': {'radius_R': R, 'pressure_drop': delta_P, 'viscosity_eta': eta,
                    'length_L': L, 'flow_rate_Q': Q},
        'unit': 'm^3/s'
    }


def calc_reynolds_number(rho: float = 1.225, v: float = 10.0, L: float = 1.0, eta: float = 1.81e-5) -> dict:
    """Reynolds number: Re = rho * v * L / eta."""
    Re = rho * v * L / eta
    if Re < 2300:
        regime = 'laminar'
    elif Re < 4000:
        regime = 'transitional'
    else:
        regime = 'turbulent'
    return {
        'result': f'Re = {Re:.2f} ({regime})',
        'details': {'rho': rho, 'v': v, 'characteristic_length_L': L,
                    'viscosity_eta': eta, 'Re': Re, 'regime': regime},
        'unit': 'dimensionless'
    }


def calc_terminal_velocity(rho_p: float = 7800.0, rho_f: float = 1000.0,
                            r: float = 0.01, eta: float = 0.001, g: float = 9.81) -> dict:
    """Stokes terminal velocity for a sphere: v_t = (2/9)*(r^2*g*(rho_p-rho_f))/eta."""
    v_t = (2.0 / 9.0) * (r * r * g * (rho_p - rho_f)) / eta
    return {
        'result': f'Terminal velocity v_t = {v_t:.6f} m/s',
        'details': {'particle_density': rho_p, 'fluid_density': rho_f, 'radius_r': r,
                    'viscosity_eta': eta, 'terminal_velocity': v_t},
        'unit': 'm/s'
    }


# =============================================================================
# N-BODY / ORBITAL MECHANICS
# =============================================================================

def calc_reduced_mass(m1: float = 5.97e24, m2: float = 7.35e22) -> dict:
    """Reduced mass: mu = (m1 * m2) / (m1 + m2)."""
    mu = m1 * m2 / (m1 + m2)
    return {
        'result': f'Reduced mass mu = {mu:.4e} kg',
        'details': {'m1': m1, 'm2': m2, 'reduced_mass_mu': mu},
        'unit': 'kg'
    }


def calc_orbital_velocity(M: float = 5.97e24, r: float = 6.37e6 + 4.0e5) -> dict:
    """Circular orbital velocity: v = sqrt(G*M/r)."""
    G = 6.67430e-11
    v = math.sqrt(G * M / r)
    T = 2.0 * math.pi * r / v
    return {
        'result': f'Orbital velocity v = {v:.2f} m/s, Period T = {T:.2f} s = {T/3600:.2f} hr',
        'details': {'G': G, 'central_mass_M': M, 'orbital_radius_r': r,
                    'orbital_velocity_v': v, 'period_T': T},
        'unit': 'm/s'
    }


def calc_kepler_third_law(a: float = 1.496e11, M: float = 1.989e30) -> dict:
    """Kepler's 3rd law: T^2 = 4*pi^2 * a^3 / (G*M)."""
    G = 6.67430e-11
    T_sq = 4.0 * math.pi * math.pi * (a ** 3) / (G * M)
    T = math.sqrt(T_sq)
    return {
        'result': f'Orbital period T = {T:.4e} s = {T/(86400*365.25):.4f} years',
        'details': {'semi_major_axis_a': a, 'central_mass_M': M, 'G': G,
                    'T_squared': T_sq, 'period_T': T},
        'unit': 's'
    }


def calc_orbital_energy(M: float = 5.97e24, m: float = 1000.0, a: float = 7.0e6) -> dict:
    """Total orbital energy: E = -G*M*m/(2*a)."""
    G = 6.67430e-11
    E = -G * M * m / (2.0 * a)
    return {
        'result': f'Orbital energy E = {E:.4e} J',
        'details': {'G': G, 'M': M, 'm': m, 'semi_major_axis_a': a, 'total_energy_E': E},
        'unit': 'J'
    }


def calc_escape_velocity(M: float = 5.97e24, r: float = 6.37e6) -> dict:
    """Escape velocity: v_esc = sqrt(2*G*M/r)."""
    G = 6.67430e-11
    v_esc = math.sqrt(2.0 * G * M / r)
    return {
        'result': f'Escape velocity v_esc = {v_esc:.2f} m/s = {v_esc/1000:.2f} km/s',
        'details': {'G': G, 'mass_M': M, 'distance_r': r, 'escape_velocity': v_esc},
        'unit': 'm/s'
    }


def calc_orbital_perturbation(a: float = 1.496e11, delta_F: float = 1e18, m: float = 1000.0,
                               dt: float = 1.0) -> dict:
    """Estimate orbital perturbation: delta_v = delta_F * dt / m."""
    delta_v = delta_F * dt / m
    return {
        'result': f'Velocity perturbation delta_v = {delta_v:.4e} m/s',
        'details': {'perturbing_force': delta_F, 'dt': dt, 'mass_m': m, 'delta_v': delta_v},
        'unit': 'm/s'
    }


# =============================================================================
# VIBRATION AND WAVES
# =============================================================================

def calc_shm_position(A: float = 0.1, omega: float = 6.283, t: float = 0.0, phi: float = 0.0) -> dict:
    """Simple harmonic motion position: x = A * cos(omega*t + phi)."""
    x = A * math.cos(omega * t + phi)
    v = -A * omega * math.sin(omega * t + phi)
    a = -A * omega * omega * math.cos(omega * t + phi)
    return {
        'result': f'x = {x:.6f} m, v = {v:.6f} m/s, a = {a:.6f} m/s^2',
        'details': {'amplitude_A': A, 'omega': omega, 't': t, 'phase_phi': phi,
                    'x': x, 'v': v, 'a': a},
        'unit': 'm'
    }


def calc_shm_period_spring(m: float = 1.0, k: float = 100.0) -> dict:
    """Period of mass-spring system: T = 2*pi*sqrt(m/k)."""
    T = 2.0 * math.pi * math.sqrt(m / k)
    f = 1.0 / T
    omega = 2.0 * math.pi * f
    return {
        'result': f'T = {T:.4f} s, f = {f:.4f} Hz, omega = {omega:.4f} rad/s',
        'details': {'mass_m': m, 'spring_constant_k': k, 'period_T': T,
                    'frequency_f': f, 'angular_frequency_omega': omega},
        'unit': 's'
    }


def calc_shm_period_pendulum(L: float = 1.0, g: float = 9.81) -> dict:
    """Period of simple pendulum: T = 2*pi*sqrt(L/g)."""
    T = 2.0 * math.pi * math.sqrt(L / g)
    f = 1.0 / T
    return {
        'result': f'T = {T:.4f} s, f = {f:.4f} Hz',
        'details': {'length_L': L, 'gravity_g': g, 'period_T': T, 'frequency_f': f},
        'unit': 's'
    }


def calc_damped_harmonic(m: float = 1.0, k: float = 100.0, b: float = 1.0) -> dict:
    """Analyze damped harmonic oscillator: omega0 = sqrt(k/m), zeta = b/(2*sqrt(m*k))."""
    omega0 = math.sqrt(k / m)
    zeta = b / (2.0 * math.sqrt(m * k))
    if zeta < 1.0:
        regime = 'underdamped'
        omega_d = omega0 * math.sqrt(1.0 - zeta * zeta)
    elif abs(zeta - 1.0) < 1e-12:
        regime = 'critically damped'
        omega_d = 0.0
    else:
        regime = 'overdamped'
        omega_d = 0.0
    return {
        'result': f'Damping ratio zeta = {zeta:.4f} ({regime}), omega0 = {omega0:.4f} rad/s',
        'details': {'mass_m': m, 'k': k, 'damping_coefficient_b': b,
                    'natural_freq_omega0': omega0, 'damping_ratio_zeta': zeta,
                    'regime': regime, 'damped_freq_omega_d': omega_d},
        'unit': 'rad/s'
    }


def calc_forced_oscillation(m: float = 1.0, k: float = 100.0, b: float = 1.0,
                              F0: float = 10.0, omega_drive: float = 8.0) -> dict:
    """Steady-state amplitude of forced oscillator: A = F0 / sqrt((k-m*omega^2)^2 + (b*omega)^2)."""
    omega0 = math.sqrt(k / m)
    A = F0 / math.sqrt((k - m * omega_drive * omega_drive) ** 2 + (b * omega_drive) ** 2)
    resonance_condition = abs(omega_drive - omega0) / omega0 < 0.05 if omega0 > 0 else False
    return {
        'result': f'Steady-state amplitude A = {A:.6f} m (resonance: {resonance_condition})',
        'details': {'m': m, 'k': k, 'b': b, 'F0': F0,
                    'omega_drive': omega_drive, 'omega0': omega0,
                    'amplitude_A': A, 'near_resonance': resonance_condition},
        'unit': 'm'
    }


def calc_wave_speed(f: float = 440.0, wavelength: float = 0.78) -> dict:
    """Wave speed: v = f * lambda."""
    v = f * wavelength
    T = 1.0 / f if f > 0 else float('inf')
    k = 2.0 * math.pi / wavelength if wavelength > 0 else float('inf')
    return {
        'result': f'Wave speed v = {v:.4f} m/s',
        'details': {'frequency_f': f, 'wavelength_lambda': wavelength,
                    'wave_speed_v': v, 'period_T': T, 'wave_number_k': k},
        'unit': 'm/s'
    }


def calc_wave_equation_solution(A: float = 1.0, k: float = 6.283, omega: float = 12.566,
                                  x: float = 0.0, t: float = 0.0, phi: float = 0.0) -> dict:
    """Wave function: y(x,t) = A * sin(k*x - omega*t + phi)."""
    y = A * math.sin(k * x - omega * t + phi)
    v_p = omega / k if abs(k) > 1e-15 else float('inf')
    return {
        'result': f'y(x,t) = {y:.6f} m at x={x:.3f} m, t={t:.3f} s',
        'details': {'amplitude_A': A, 'wave_number_k': k, 'omega': omega,
                    'x': x, 't': t, 'phase_phi': phi, 'y': y, 'phase_velocity_vp': v_p},
        'unit': 'm'
    }


def calc_interference(A1: float = 1.0, A2: float = 1.0, delta_phi: float = 0.0) -> dict:
    """Superposition of two waves: resultant amplitude via phasor addition."""
    A_result = math.sqrt(A1 * A1 + A2 * A2 + 2.0 * A1 * A2 * math.cos(delta_phi))
    if delta_phi == 0.0:
        inter_type = 'constructive'
    elif abs(delta_phi - math.pi) < 1e-12:
        inter_type = 'destructive'
    else:
        inter_type = 'intermediate'
    return {
        'result': f'Resultant amplitude A = {A_result:.4f} ({inter_type} interference)',
        'details': {'A1': A1, 'A2': A2, 'phase_difference_rad': delta_phi,
                    'resultant_amplitude': A_result, 'interference_type': inter_type},
        'unit': 'm'
    }


def calc_beat_frequency(f1: float = 440.0, f2: float = 444.0) -> dict:
    """Beat frequency: f_beat = |f1 - f2|."""
    f_beat = abs(f1 - f2)
    return {
        'result': f'Beat frequency f_beat = {f_beat:.4f} Hz',
        'details': {'f1': f1, 'f2': f2, 'beat_frequency': f_beat},
        'unit': 'Hz'
    }


def calc_standing_wave_string(L: float = 1.0, n: float = 1.0, v: float = 100.0) -> dict:
    """Standing wave on a string: lambda_n = 2L/n, f_n = n*v/(2L)."""
    n_int = max(1, int(n))
    wavelength = 2.0 * L / n_int
    f_n = n_int * v / (2.0 * L)
    return {
        'result': f'Harmonic n={n_int}: lambda = {wavelength:.4f} m, f = {f_n:.4f} Hz',
        'details': {'length_L': L, 'harmonic_n': n_int, 'wave_speed_v': v,
                    'wavelength': wavelength, 'frequency': f_n},
        'unit': 'Hz'
    }


def calc_standing_wave_tube(L: float = 1.0, n: float = 1.0, v: float = 343.0,
                              closed_end: bool = True) -> dict:
    """Standing wave in an air column (open/open or closed/open)."""
    n_int = max(1, int(n))
    if closed_end:
        harmonic_odd = 2 * n_int - 1
        wavelength = 4.0 * L / harmonic_odd
        f_n = harmonic_odd * v / (4.0 * L)
    else:
        wavelength = 2.0 * L / n_int
        f_n = n_int * v / (2.0 * L)
    return {
        'result': f'Frequency f = {f_n:.4f} Hz, wavelength lambda = {wavelength:.4f} m',
        'details': {'length_L': L, 'harmonic': n_int, 'v_sound': v,
                    'closed_end': closed_end, 'frequency': f_n, 'wavelength': wavelength},
        'unit': 'Hz'
    }


# =============================================================================
# ADDITIONAL FUNCTIONS
# =============================================================================

def calc_normal_force_incline(m: float = 10.0, g: float = 9.81, angle_deg: float = 30.0) -> dict:
    """Normal force on an inclined plane: N = m*g*cos(theta)."""
    theta = math.radians(angle_deg)
    N = m * g * math.cos(theta)
    F_parallel = m * g * math.sin(theta)
    return {
        'result': f'N = {N:.4f} N, F_parallel = {F_parallel:.4f} N',
        'details': {'mass_m': m, 'g': g, 'angle_deg': angle_deg, 'theta_rad': theta,
                    'normal_force_N': N, 'parallel_force': F_parallel},
        'unit': 'N'
    }


def calc_atwood_machine(m1: float = 5.0, m2: float = 3.0, g: float = 9.81) -> dict:
    """Atwood machine acceleration: a = g*(m1 - m2)/(m1 + m2)."""
    m_sum = m1 + m2
    a = g * (m1 - m2) / m_sum
    T = 2.0 * m1 * m2 * g / m_sum
    return {
        'result': f'a = {a:.4f} m/s^2, Tension T = {T:.4f} N',
        'details': {'m1': m1, 'm2': m2, 'g': g, 'acceleration_a': a, 'tension_T': T},
        'unit': 'm/s^2'
    }


def calc_banked_curve(v: float = 20.0, R: float = 50.0, g: float = 9.81) -> dict:
    """Ideal banking angle: tan(theta) = v^2/(R*g)."""
    tan_theta = v * v / (R * g)
    theta_deg = math.degrees(math.atan(tan_theta))
    return {
        'result': f'Ideal bank angle = {theta_deg:.4f} deg',
        'details': {'velocity_v': v, 'radius_R': R, 'g': g, 'tan_theta': tan_theta,
                    'theta_deg': theta_deg},
        'unit': 'deg'
    }


def calc_parallel_axis_theorem(I_cm: float = 1.0, m: float = 2.0, d: float = 0.5) -> dict:
    """Parallel axis theorem: I = I_cm + m*d^2."""
    I = I_cm + m * d * d
    return {
        'result': f'I = {I:.4f} kg*m^2',
        'details': {'I_cm': I_cm, 'mass_m': m, 'offset_d': d,
                    'I_parallel_axis': I, 'added_md2': m * d * d},
        'unit': 'kg*m^2'
    }


def calc_rolling_without_slipping(m: float = 2.0, R: float = 0.1, I_cm: float = 0.01,
                                    incline_deg: float = 30.0, g: float = 9.81) -> dict:
    """Rolling without slipping acceleration: a = g*sin(theta)/(1 + I_cm/(m*R^2))."""
    theta = math.radians(incline_deg)
    factor = 1.0 + I_cm / (m * R * R)
    a = g * math.sin(theta) / factor
    return {
        'result': f'Linear acceleration a = {a:.4f} m/s^2',
        'details': {'mass_m': m, 'radius_R': R, 'I_cm': I_cm, 'incline_deg': incline_deg,
                    'theta_rad': theta, 'factor': factor, 'acceleration_a': a},
        'unit': 'm/s^2'
    }


def calc_hydraulic_press(F1: float = 100.0, A1: float = 0.001, A2: float = 0.01) -> dict:
    """Hydraulic press: F1/A1 = F2/A2 -> F2 = F1 * A2/A1."""
    F2 = F1 * A2 / A1
    return {
        'result': f'Output force F2 = {F2:.4f} N',
        'details': {'input_force_F1': F1, 'input_area_A1': A1, 'output_area_A2': A2,
                    'output_force_F2': F2, 'mechanical_advantage': A2 / A1},
        'unit': 'N'
    }


def calc_power_in_wave(mu: float = 0.01, omega: float = 300.0, A: float = 0.05, v: float = 100.0) -> dict:
    """Average power transmitted by a sinusoidal wave on a string: P = 0.5*mu*omega^2*A^2*v."""
    P = 0.5 * mu * omega * omega * A * A * v
    return {
        'result': f'Average wave power P = {P:.4f} W',
        'details': {'linear_density_mu': mu, 'angular_freq_omega': omega,
                    'amplitude_A': A, 'wave_speed_v': v, 'power_P': P},
        'unit': 'W'
    }


def calc_group_velocity(omega_list: list = None, k_list: list = None) -> dict:
    """Group velocity: v_g = d(omega)/dk estimated from discrete (omega, k) pairs."""
    if omega_list is None:
        omega_list = [3.0, 4.0, 5.0]
    if k_list is None:
        k_list = [1.5, 2.0, 2.5]
    if len(omega_list) < 2 or len(k_list) < 2:
        return {'result': 'Need at least 2 points', 'details': {}, 'unit': 'm/s'}
    dk = k_list[1] - k_list[0]
    if abs(dk) < 1e-15:
        return {'result': 'k values too close', 'details': {}, 'unit': 'm/s'}
    vg = (omega_list[1] - omega_list[0]) / dk
    vp = omega_list[1] / k_list[1] if abs(k_list[1]) > 1e-15 else float('inf')
    return {
        'result': f'Group velocity v_g = {vg:.4f} m/s, Phase velocity v_p = {vp:.4f} m/s',
        'details': {'omega_values': omega_list, 'k_values': k_list, 'v_group': vg, 'v_phase': vp},
        'unit': 'm/s'
    }


def calc_hohmann_transfer(r1: float = 6.67e6, r2: float = 4.215e7, M: float = 5.97e24) -> dict:
    """Hohmann transfer orbit delta-v: v1 = sqrt(GM/r1), v_transfer at r1 = sqrt(2GM*r2/(r1*(r1+r2)))."""
    G = 6.67430e-11
    v1_circ = math.sqrt(G * M / r1)
    v2_circ = math.sqrt(G * M / r2)
    a_transfer = (r1 + r2) / 2.0
    v_peri = math.sqrt(2.0 * G * M * r2 / (r1 * (r1 + r2)))
    v_apo = math.sqrt(2.0 * G * M * r1 / (r2 * (r1 + r2)))
    dv1 = v_peri - v1_circ
    dv2 = v2_circ - v_apo
    dv_total = dv1 + dv2
    T_transfer = math.pi * math.sqrt(a_transfer ** 3 / (G * M))
    return {
        'result': f'dv_total = {dv_total:.2f} m/s, dv1 = {dv1:.2f} m/s, dv2 = {dv2:.2f} m/s, T_transfer = {T_transfer:.0f} s',
        'details': {'r1': r1, 'r2': r2, 'M': M, 'dv_perigee': dv1, 'dv_apogee': dv2,
                    'dv_total': dv_total, 'transfer_time': T_transfer},
        'unit': 'm/s'
    }


# =============================================================================
# COMMANDS REGISTRY
# =============================================================================

COMMANDS = {
    # Kinematics - Linear
    'linear_velocity': {'func': calc_linear_velocity, 'params': ['u', 'a', 't'],
                        'desc': 'Final velocity v = u + at'},
    'linear_displacement': {'func': calc_linear_displacement, 'params': ['u', 'a', 't'],
                            'desc': 'Displacement s = ut + 0.5at^2'},
    'velocity_displacement': {'func': calc_velocity_displacement, 'params': ['u', 'a', 's'],
                              'desc': 'Final velocity v^2 = u^2 + 2as'},
    'time_from_distance': {'func': calc_time_from_distance, 'params': ['u', 'a', 's'],
                           'desc': 'Solve for time from u, a, s'},
    'acceleration': {'func': calc_acceleration, 'params': ['u', 'v', 't'],
                     'desc': 'Acceleration a = (v-u)/t'},
    # Kinematics - Projectile
    'projectile_range': {'func': calc_projectile_range, 'params': ['v0', 'angle_deg', 'g'],
                         'desc': 'Projectile range R = v0^2 sin(2theta)/g'},
    'max_height': {'func': calc_max_height, 'params': ['v0', 'angle_deg', 'g'],
                   'desc': 'Max height of projectile'},
    'time_of_flight': {'func': calc_time_of_flight, 'params': ['v0', 'angle_deg', 'g'],
                       'desc': 'Time of flight of projectile'},
    'projectile_trajectory': {'func': calc_projectile_trajectory, 'params': ['v0', 'angle_deg', 'g', 't'],
                              'desc': 'Projectile position (x,y) at time t'},
    'optimal_angle': {'func': calc_optimal_angle, 'params': ['v0', 'g'],
                      'desc': 'Optimal launch angle for max range'},
    # Kinematics - Circular
    'angular_velocity_from_rpm': {'func': calc_angular_velocity_from_rpm, 'params': ['rpm'],
                                   'desc': 'Convert rpm to angular velocity'},
    'circ_tangential_velocity': {'func': calc_circ_tangential_velocity, 'params': ['r', 'omega'],
                                  'desc': 'Tangent velocity v = r*omega'},
    'centripetal_acceleration': {'func': calc_centripetal_acceleration, 'params': ['v', 'r'],
                                  'desc': 'Centripetal acceleration a_c = v^2/r'},
    'angular_acceleration': {'func': calc_angular_acceleration, 'params': ['omega0', 'omega', 't'],
                              'desc': 'Angular acceleration alpha = (omega-omega0)/t'},
    'centripetal_force': {'func': calc_centripetal_force, 'params': ['m', 'v', 'r'],
                          'desc': 'Centripetal force F_c = mv^2/r'},
    # Dynamics
    'newton2_force': {'func': calc_newton2_force, 'params': ['m', 'a'],
                      'desc': "Newton's 2nd law F = ma"},
    'newton2_acceleration': {'func': calc_newton2_acceleration, 'params': ['F', 'm'],
                              'desc': "Newton's 2nd law a = F/m"},
    'weight': {'func': calc_weight, 'params': ['m', 'g'], 'desc': 'Weight W = mg'},
    'friction': {'func': calc_friction, 'params': ['mu', 'N'], 'desc': 'Friction f = mu*N'},
    'static_friction_max': {'func': calc_static_friction_max, 'params': ['mu_s', 'N'],
                            'desc': 'Max static friction f_s = mu_s*N'},
    'spring_force': {'func': calc_spring_force, 'params': ['k', 'x'],
                     'desc': "Hooke's law F = -kx"},
    'gravitational_force': {'func': calc_gravitational_force, 'params': ['m1', 'm2', 'r'],
                            'desc': "Newton's law of gravitation F = Gm1m2/r^2"},
    'resultant_force_2d': {'func': calc_resultant_force_2d, 'params': ['F1x', 'F1y', 'F2x', 'F2y'],
                           'desc': 'Resultant of two 2D force vectors'},
    # Work & Energy
    'work': {'func': calc_work, 'params': ['F', 'd', 'angle_deg'], 'desc': 'Work W = Fd cos(theta)'},
    'kinetic_energy': {'func': calc_kinetic_energy, 'params': ['m', 'v'],
                       'desc': 'Kinetic energy KE = 0.5mv^2'},
    'potential_energy_grav': {'func': calc_potential_energy_grav, 'params': ['m', 'h', 'g'],
                              'desc': 'Gravitational PE = mgh'},
    'potential_energy_spring': {'func': calc_potential_energy_spring, 'params': ['k', 'x'],
                                 'desc': 'Spring PE = 0.5kx^2'},
    'mechanical_energy': {'func': calc_mechanical_energy, 'params': ['KE', 'PE'],
                          'desc': 'Total mechanical energy E = KE + PE'},
    'power_work': {'func': calc_power_work, 'params': ['W', 't'], 'desc': 'Power P = W/t'},
    'power_force_velocity': {'func': calc_power_force_velocity, 'params': ['F', 'v'],
                              'desc': 'Power P = Fv'},
    # Momentum
    'momentum': {'func': calc_momentum, 'params': ['m', 'v'], 'desc': 'Momentum p = mv'},
    'impulse': {'func': calc_impulse, 'params': ['F', 'dt'], 'desc': 'Impulse J = F*dt'},
    'momentum_conservation_1d': {'func': calc_momentum_conservation_1d,
                                  'params': ['m1', 'v1', 'm2', 'v2', 'v1_prime'],
                                  'desc': 'Solve for v2_prime from momentum conservation'},
    'elastic_collision_1d': {'func': calc_elastic_collision_1d,
                              'params': ['m1', 'v1', 'm2', 'v2'],
                              'desc': 'Elastic collision in 1D'},
    'perfectly_inelastic_collision': {'func': calc_perfectly_inelastic_collision,
                                       'params': ['m1', 'v1', 'm2', 'v2'],
                                       'desc': 'Perfectly inelastic collision'},
    # Rigid Body
    'moment_of_inertia_point': {'func': calc_moment_of_inertia_point, 'params': ['m', 'r'],
                                 'desc': 'Moment of inertia of point mass I = mr^2'},
    'moment_of_inertia_rod': {'func': calc_moment_of_inertia_rod, 'params': ['m', 'L', 'axis'],
                               'desc': 'Moment of inertia of thin rod'},
    'moment_of_inertia_disk': {'func': calc_moment_of_inertia_disk, 'params': ['m', 'R'],
                                'desc': 'Moment of inertia of solid disk I = 0.5mR^2'},
    'moment_of_inertia_sphere': {'func': calc_moment_of_inertia_sphere, 'params': ['m', 'R'],
                                  'desc': 'Moment of inertia of solid sphere I = 2/5 mR^2'},
    'moment_of_inertia_hoop': {'func': calc_moment_of_inertia_hoop, 'params': ['m', 'R'],
                                'desc': 'Moment of inertia of thin hoop I = mR^2'},
    'torque': {'func': calc_torque, 'params': ['r', 'F', 'angle_deg'],
               'desc': 'Torque tau = rF sin(theta)'},
    'angular_momentum': {'func': calc_angular_momentum, 'params': ['I', 'omega'],
                          'desc': 'Angular momentum L = I*omega'},
    'rotational_kinetic_energy': {'func': calc_rotational_kinetic_energy, 'params': ['I', 'omega'],
                                   'desc': 'Rotational KE = 0.5 I omega^2'},
    'rigid_body_equilibrium': {'func': calc_rigid_body_equilibrium,
                                'params': ['forces', 'distances'],
                                'desc': 'Check rigid body equilibrium'},
    'gyroscope_precession': {'func': calc_gyroscope_precession,
                              'params': ['I', 'omega_spin', 'tau'],
                              'desc': 'Gyroscope precession omega_p = tau/L'},
    # Fluid Mechanics
    'hydrostatic_pressure': {'func': calc_hydrostatic_pressure,
                              'params': ['rho', 'h', 'g', 'P_atm'],
                              'desc': 'Hydrostatic pressure P = P_atm + rho*g*h'},
    'buoyancy_force': {'func': calc_buoyancy_force, 'params': ['rho_fluid', 'V_submerged', 'g'],
                       'desc': 'Buoyancy force F_b = rho*V*g'},
    'bernoulli': {'func': calc_bernoulli, 'params': ['P1', 'rho', 'v1', 'h1', 'v2', 'h2', 'g'],
                  'desc': "Bernoulli equation solve for P2"},
    'flow_rate': {'func': calc_flow_rate, 'params': ['A', 'v'], 'desc': 'Flow rate Q = A*v'},
    'poiseuille_flow': {'func': calc_poiseuille_flow, 'params': ['R', 'delta_P', 'eta', 'L'],
                         'desc': 'Poiseuille flow in a pipe'},
    'reynolds_number': {'func': calc_reynolds_number, 'params': ['rho', 'v', 'L', 'eta'],
                         'desc': 'Reynolds number Re = rho*v*L/eta'},
    'terminal_velocity': {'func': calc_terminal_velocity,
                           'params': ['rho_p', 'rho_f', 'r', 'eta', 'g'],
                           'desc': 'Stokes terminal velocity for a sphere'},
    # N-Body / Orbital
    'reduced_mass': {'func': calc_reduced_mass, 'params': ['m1', 'm2'],
                     'desc': 'Reduced mass mu = m1*m2/(m1+m2)'},
    'orbital_velocity': {'func': calc_orbital_velocity, 'params': ['M', 'r'],
                          'desc': 'Circular orbital velocity v = sqrt(GM/r)'},
    'kepler_third_law': {'func': calc_kepler_third_law, 'params': ['a', 'M'],
                          'desc': "Kepler's 3rd law T^2 = 4pi^2 a^3/(GM)"},
    'orbital_energy': {'func': calc_orbital_energy, 'params': ['M', 'm', 'a'],
                       'desc': 'Total orbital energy E = -GMm/(2a)'},
    'escape_velocity': {'func': calc_escape_velocity, 'params': ['M', 'r'],
                         'desc': 'Escape velocity v_esc = sqrt(2GM/r)'},
    'orbital_perturbation': {'func': calc_orbital_perturbation,
                              'params': ['a', 'delta_F', 'm', 'dt'],
                              'desc': 'Estimate orbital velocity perturbation'},
    # Vibration & Waves
    'shm_position': {'func': calc_shm_position, 'params': ['A', 'omega', 't', 'phi'],
                      'desc': 'SHM position x = A cos(omega*t + phi)'},
    'shm_period_spring': {'func': calc_shm_period_spring, 'params': ['m', 'k'],
                           'desc': 'Period of mass-spring T = 2pi sqrt(m/k)'},
    'shm_period_pendulum': {'func': calc_shm_period_pendulum, 'params': ['L', 'g'],
                             'desc': 'Period of pendulum T = 2pi sqrt(L/g)'},
    'damped_harmonic': {'func': calc_damped_harmonic, 'params': ['m', 'k', 'b'],
                         'desc': 'Damped harmonic oscillator analysis'},
    'forced_oscillation': {'func': calc_forced_oscillation,
                            'params': ['m', 'k', 'b', 'F0', 'omega_drive'],
                            'desc': 'Forced oscillator steady-state amplitude'},
    'wave_speed': {'func': calc_wave_speed, 'params': ['f', 'wavelength'],
                   'desc': 'Wave speed v = f*lambda'},
    'wave_equation_solution': {'func': calc_wave_equation_solution,
                                'params': ['A', 'k', 'omega', 'x', 't', 'phi'],
                                'desc': 'Wave function y(x,t) = A sin(kx - wt + phi)'},
    'interference': {'func': calc_interference, 'params': ['A1', 'A2', 'delta_phi'],
                     'desc': 'Superposition of two waves'},
    'beat_frequency': {'func': calc_beat_frequency, 'params': ['f1', 'f2'],
                        'desc': 'Beat frequency f_beat = |f1-f2|'},
    'standing_wave_string': {'func': calc_standing_wave_string, 'params': ['L', 'n', 'v'],
                              'desc': 'Standing wave on a string'},
    'standing_wave_tube': {'func': calc_standing_wave_tube, 'params': ['L', 'n', 'v', 'closed_end'],
                            'desc': 'Standing wave in an air column'},
    # Additional
    'normal_force_incline': {'func': calc_normal_force_incline, 'params': ['m', 'g', 'angle_deg'],
                              'desc': 'Normal force on inclined plane N = mg*cos(theta)'},
    'atwood_machine': {'func': calc_atwood_machine, 'params': ['m1', 'm2', 'g'],
                        'desc': 'Atwood machine acceleration and tension'},
    'banked_curve': {'func': calc_banked_curve, 'params': ['v', 'R', 'g'],
                      'desc': 'Ideal banking angle tan(theta) = v^2/(Rg)'},
    'parallel_axis_theorem': {'func': calc_parallel_axis_theorem, 'params': ['I_cm', 'm', 'd'],
                               'desc': 'Parallel axis theorem I = I_cm + m*d^2'},
    'rolling_without_slipping': {'func': calc_rolling_without_slipping,
                                   'params': ['m', 'R', 'I_cm', 'incline_deg', 'g'],
                                   'desc': 'Acceleration of rolling object on incline'},
    'hydraulic_press': {'func': calc_hydraulic_press, 'params': ['F1', 'A1', 'A2'],
                         'desc': 'Hydraulic press F1/A1 = F2/A2'},
    'power_in_wave': {'func': calc_power_in_wave, 'params': ['mu', 'omega', 'A', 'v'],
                       'desc': 'Average power in a sinusoidal wave on a string'},
    'group_velocity': {'func': calc_group_velocity, 'params': ['omega_list', 'k_list'],
                        'desc': 'Group velocity v_g = d(omega)/dk'},
    'hohmann_transfer': {'func': calc_hohmann_transfer, 'params': ['r1', 'r2', 'M'],
                          'desc': 'Hohmann transfer orbit delta-v calculation'},
}
