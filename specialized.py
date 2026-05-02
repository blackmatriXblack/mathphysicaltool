"""
Specialized Physics Branches - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_hookes_law_3d(lambda_lame: float = 2.0e10, mu_lame: float = 3.0e10, epsilon_xx: float = 0.001, epsilon_yy: float = 0.0005, epsilon_zz: float = 0.0002, gamma_xy: float = 0.0, gamma_xz: float = 0.0, gamma_yz: float = 0.0) -> dict:
    """Generalized Hooke's law: sigma_ij = lambda*delta_ij*eps_kk + 2*mu*eps_ij."""
    eps_kk = epsilon_xx + epsilon_yy + epsilon_zz
    sigma = np.zeros((3, 3))
    strain = np.array([[epsilon_xx, gamma_xy/2, gamma_xz/2],
                       [gamma_xy/2, epsilon_yy, gamma_yz/2],
                       [gamma_xz/2, gamma_yz/2, epsilon_zz]])
    for i in range(3):
        for j in range(3):
            sigma[i, j] = 2.0 * mu_lame * strain[i, j]
            if i == j:
                sigma[i, j] += lambda_lame * eps_kk
    sigma_vm = np.sqrt(0.5 * ((sigma[0,0]-sigma[1,1])**2 + (sigma[1,1]-sigma[2,2])**2 + (sigma[2,2]-sigma[0,0])**2 + 6*(sigma[0,1]**2 + sigma[1,2]**2 + sigma[0,2]**2)))
    return {
        'result': f'sigma_xx={sigma[0,0]:.4e}, sigma_yy={sigma[1,1]:.4e}, sigma_zz={sigma[2,2]:.4e}, sigma_vM={sigma_vm:.4e} Pa',
        'details': {'lambda_Pa': lambda_lame, 'mu_Pa': mu_lame, 'epsilon': {'xx': epsilon_xx, 'yy': epsilon_yy, 'zz': epsilon_zz}, 'eps_kk': eps_kk, 'sigma_tensor': sigma.tolist(), 'von_Mises_stress': sigma_vm},
        'unit': 'Pa'
    }

def calc_strain_tensor_from_displacement(du_dx: float = 0.001, du_dy: float = 0.0005, du_dz: float = 0.0001, dv_dx: float = 0.0003, dv_dy: float = 0.002, dv_dz: float = 0.0002, dw_dx: float = 0.0001, dw_dy: float = 0.0002, dw_dz: float = 0.0005) -> dict:
    """Strain tensor: epsilon_ij = (1/2)*(du_i/dx_j + du_j/dx_i)."""
    eps = np.array([
        [du_dx, 0.5*(du_dy + dv_dx), 0.5*(du_dz + dw_dx)],
        [0.5*(dv_dx + du_dy), dv_dy, 0.5*(dv_dz + dw_dy)],
        [0.5*(dw_dx + du_dz), 0.5*(dw_dy + dv_dz), dw_dz]
    ])
    volumetric_strain = np.trace(eps)
    deviatoric = eps - np.eye(3) * volumetric_strain / 3.0
    return {
        'result': f'eps_kk = {volumetric_strain:.6f}',
        'details': {'strain_tensor': eps.tolist(), 'volumetric_strain': volumetric_strain, 'deviatoric_strain': deviatoric.tolist()},
        'unit': 'dimensionless'
    }

def calc_navier_cauchy(u_field_info: dict = None) -> dict:
    """Navier-Cauchy equation: mu*del^2(u) + (lambda+mu)*grad(div*u) + F = rho*u_tt."""
    if u_field_info is None:
        u_field_info = {'L': 1.0, 'displacement_scale': 0.001}
    L = u_field_info.get('L', 1.0)
    v_p = np.sqrt((2.0 * 3e10 + 2e10) / 2700.0)
    v_s = np.sqrt(3e10 / 2700.0)
    return {
        'result': f'P-wave speed = {v_p:.4f} m/s, S-wave speed = {v_s:.4f} m/s',
        'details': {'L': L, 'v_p_ms': v_p, 'v_s_ms': v_s, 'v_p_over_v_s': v_p / v_s},
        'unit': 'm/s'
    }

def calc_alfven_speed(B: float = 0.1, rho: float = 1.67e-21) -> dict:
    """Alfven speed: v_A = B / sqrt(mu_0 * rho)."""
    mu_0 = 4.0 * np.pi * 1e-7
    v_A = B / np.sqrt(mu_0 * rho)
    return {
        'result': f'v_A = {v_A:.4e} m/s = {v_A/1000:.4f} km/s',
        'details': {'B_T': B, 'rho_kgm3': rho, 'mu_0': mu_0, 'alfven_speed_ms': v_A},
        'unit': 'm/s'
    }

def calc_magnetic_reynolds_number(velocity: float = 1e4, length: float = 1e6, magnetic_diffusivity: float = 1.0) -> dict:
    """Magnetic Reynolds number: Rm = v * L / eta."""
    Rm = velocity * length / magnetic_diffusivity
    dynamo_possible = Rm > 10
    return {
        'result': f'R_m = {Rm:.4e}, dynamo possible: {dynamo_possible}',
        'details': {'velocity_ms': velocity, 'length_m': length, 'magnetic_diffusivity': magnetic_diffusivity, 'Rm': Rm, 'dynamo_possible': dynamo_possible},
        'unit': 'dimensionless'
    }

def calc_plasma_beta(B: float = 0.1, pressure: float = 100.0) -> dict:
    """Plasma beta: beta = 2 * mu_0 * p / B^2."""
    mu_0 = 4.0 * np.pi * 1e-7
    beta = 2.0 * mu_0 * pressure / B**2
    regime = 'pressure-dominated' if beta > 1 else 'magnetic-dominated'
    return {
        'result': f'beta = {beta:.6f} ({regime})',
        'details': {'B_T': B, 'p_Pa': pressure, 'mu_0': mu_0, 'plasma_beta': beta, 'regime': regime},
        'unit': 'dimensionless'
    }

def calc_frozen_in_flux(Rm: float = 100.0) -> dict:
    """Frozen-in flux condition: high Rm => flux is frozen into plasma."""
    frozen = "flux frozen-in" if Rm > 100 else "flux diffuses" if Rm < 1 else "transitional"
    return {
        'result': f'Rm = {Rm}, regime: {frozen}',
        'details': {'Rm': Rm, 'flux_regime': frozen},
        'unit': 'dimensionless'
    }

def calc_radiation_attenuation(I0: float = 1.0, mu: float = 0.1, thickness: float = 5.0) -> dict:
    """Attenuation: I = I0 * exp(-mu * x)."""
    I = I0 * np.exp(-mu * thickness)
    transmission = I / I0
    return {
        'result': f'I = {I:.6e}, transmission = {transmission:.6f}',
        'details': {'I0': I0, 'mu_cm': mu, 'thickness_cm': thickness, 'I': I, 'transmission': transmission},
        'unit': 'dimensionless'
    }

def calc_half_value_layer(mu: float = 0.1) -> dict:
    """Half-value layer: HVL = ln(2) / mu."""
    HVL = np.log(2.0) / mu
    TVL = np.log(10.0) / mu
    return {
        'result': f'HVL = {HVL:.4f} cm, TVL = {TVL:.4f} cm',
        'details': {'mu_cm': mu, 'HVL_cm': HVL, 'TVL_cm': TVL},
        'unit': 'cm'
    }

def calc_buildup_factor(energy_MeV: float = 1.0, mean_free_paths: float = 5.0, material: str = 'water') -> dict:
    """Buildup factor (approximate, linear model): B = 1 + k * (mu*x)."""
    k = 0.5
    B = 1.0 + k * mean_free_paths
    return {
        'result': f'Buildup factor B = {B:.4f}',
        'details': {'energy_MeV': energy_MeV, 'mean_free_paths': mean_free_paths, 'material': material, 'buildup_factor': B, 'k': k},
        'unit': 'dimensionless'
    }

def calc_radiation_dose(energy_J: float = 1.0e-3, mass_kg: float = 70.0, quality_factor: float = 1.0) -> dict:
    """Absorbed dose (Gy) and equivalent dose (Sv): D = E/m, H = Q*D."""
    dose_Gy = energy_J / mass_kg
    dose_Sv = quality_factor * dose_Gy
    return {
        'result': f'D = {dose_Gy:.4e} Gy, H = {dose_Sv:.4e} Sv',
        'details': {'energy_J': energy_J, 'mass_kg': mass_kg, 'quality_factor': quality_factor, 'absorbed_dose_Gy': dose_Gy, 'equivalent_dose_Sv': dose_Sv},
        'unit': 'Gy / Sv'
    }

def calc_poiseuille_flow(radius: float = 0.001, length: float = 0.1, delta_P: float = 1000.0, viscosity: float = 0.0035) -> dict:
    """Hagen-Poiseuille blood flow: Q = pi*R^4*delta_P/(8*eta*L)."""
    Q = np.pi * radius**4 * delta_P / (8.0 * viscosity * length)
    velocity_avg = Q / (np.pi * radius**2)
    Re = 1060.0 * velocity_avg * 2.0 * radius / viscosity
    return {
        'result': f'Q = {Q:.4e} m^3/s, v_avg = {velocity_avg:.4f} m/s, Re = {Re:.2f}',
        'details': {'radius_m': radius, 'length_m': length, 'delta_P_Pa': delta_P, 'viscosity_Pas': viscosity, 'flow_rate_m3s': Q, 'avg_velocity_ms': velocity_avg, 'Reynolds': Re},
        'unit': 'm^3/s'
    }

def calc_ficks_law_diffusion(D: float = 1.0e-9, concentration_gradient: float = 100.0, area: float = 1.0e-4) -> dict:
    """Fick's first law: J = -D * dC/dx."""
    flux = -D * concentration_gradient
    mass_rate = abs(flux) * area
    return {
        'result': f'J = {flux:.4e} mol/(m^2*s), mass rate = {mass_rate:.4e} mol/s',
        'details': {'diffusion_coeff_m2s': D, 'dC_dx': concentration_gradient, 'area_m2': area, 'flux': flux, 'mass_flow_rate': mass_rate},
        'unit': 'mol/(m^2*s)'
    }

def calc_hodgkin_huxley_simple(Vm: float = -70.0, gNa: float = 120.0, gK: float = 36.0, gL: float = 0.3, ENa: float = 55.0, EK: float = -77.0, EL: float = -54.4) -> dict:
    """Simplified Hodgkin-Huxley membrane: I = gNa*(Vm-ENa) + gK*(Vm-EK) + gL*(Vm-EL)."""
    I_Na = gNa * (Vm - ENa)
    I_K = gK * (Vm - EK)
    I_L = gL * (Vm - EL)
    I_total = I_Na + I_K + I_L
    resting_vm = (gNa*ENa + gK*EK + gL*EL) / (gNa + gK + gL) if (gNa+gK+gL) > 0 else 0.0
    return {
        'result': f'I_total = {I_total:.4f}, resting Vm = {resting_vm:.4f} mV',
        'details': {'Vm_mV': Vm, 'gNa': gNa, 'gK': gK, 'gL': gL, 'I_Na': I_Na, 'I_K': I_K, 'I_L': I_L, 'I_total': I_total, 'resting_Vm_mV': resting_vm},
        'unit': 'nA (normalized)'
    }

def calc_bone_mechanics(force: float = 1000.0, area: float = 0.0005, length: float = 0.3, youngs_modulus: float = 17e9) -> dict:
    """Mechanical properties of bone: stress, strain, elongation."""
    sigma = force / area
    epsilon = sigma / youngs_modulus
    delta_L = epsilon * length
    return {
        'result': f'sigma={sigma:.4e} Pa, epsilon={epsilon:.6e}, delta_L={delta_L:.6e} m',
        'details': {'force_N': force, 'area_m2': area, 'length_m': length, 'E_Pa': youngs_modulus, 'stress_Pa': sigma, 'strain': epsilon, 'elongation_m': delta_L},
        'unit': 'Pa'
    }

def calc_bouguer_gravity_anomaly(thickness: float = 5000.0, density_contrast: float = 500.0) -> dict:
    """Bouguer gravity anomaly: delta_g = 2*pi*G*delta_rho*h."""
    G = 6.67430e-11
    delta_g = 2.0 * np.pi * G * density_contrast * thickness
    delta_g_mGal = delta_g * 1e5
    return {
        'result': f'delta_g = {delta_g:.4e} m/s^2 = {delta_g_mGal:.4f} mGal',
        'details': {'thickness_m': thickness, 'density_contrast_kgm3': density_contrast, 'G': G, 'delta_g_ms2': delta_g, 'delta_g_mGal': delta_g_mGal},
        'unit': 'm/s^2'
    }

def calc_isostasy_airy(crustal_thickness: float = 30.0e3, crustal_density: float = 2700.0, mantle_density: float = 3300.0) -> dict:
    """Airy isostasy: root thickness = h * rho_c / (rho_m - rho_c)."""
    root = crustal_thickness * crustal_density / (mantle_density - crustal_density)
    total_thickness = crustal_thickness + root
    return {
        'result': f'Root = {root/1000:.4f} km, total crustal thickness = {total_thickness/1000:.4f} km',
        'details': {'crustal_thickness_m': crustal_thickness, 'rho_crust': crustal_density, 'rho_mantle': mantle_density, 'root_thickness_m': root, 'total_thickness_m': total_thickness},
        'unit': 'm'
    }

def calc_isostasy_pratt(elevation: float = 4000.0, reference_density: float = 3200.0, compensation_depth: float = 100e3) -> dict:
    """Pratt isostasy: compensation density varies to maintain equal pressure."""
    rho_comp = reference_density * compensation_depth / (compensation_depth + elevation)
    return {
        'result': f'Compensation density = {rho_comp:.4f} kg/m^3',
        'details': {'elevation_m': elevation, 'reference_density': reference_density, 'compensation_depth_m': compensation_depth, 'compensation_density': rho_comp},
        'unit': 'kg/m^3'
    }

def calc_seismic_wave_velocities(K_bulk: float = 1.0e11, G_shear: float = 4.0e10, density: float = 3300.0) -> dict:
    """Seismic velocities: Vp = sqrt((K+4G/3)/rho), Vs = sqrt(G/rho)."""
    Vp = np.sqrt((K_bulk + 4.0 * G_shear / 3.0) / density)
    Vs = np.sqrt(G_shear / density)
    Vp_Vs_ratio = Vp / Vs if Vs > 0 else float('inf')
    poisson = (Vp**2 - 2.0*Vs**2) / (2.0*(Vp**2 - Vs**2)) if abs(Vp**2 - Vs**2) > 1e-15 else 0.25
    return {
        'result': f'Vp = {Vp:.4f} m/s, Vs = {Vs:.4f} m/s, Vp/Vs = {Vp_Vs_ratio:.4f}, nu = {poisson:.4f}',
        'details': {'K_Pa': K_bulk, 'G_Pa': G_shear, 'density_kgm3': density, 'Vp_ms': Vp, 'Vs_ms': Vs, 'Vp_Vs_ratio': Vp_Vs_ratio, 'poisson_ratio': poisson},
        'unit': 'm/s'
    }

def calc_geothermal_gradient(heat_flux: float = 0.065, thermal_conductivity: float = 3.0) -> dict:
    """Geothermal gradient: dT/dz = q / k."""
    gradient = heat_flux / thermal_conductivity
    depth_100C = 100.0 / gradient if gradient > 0 else float('inf')
    return {
        'result': f'Gradient = {gradient:.4f} K/m = {gradient*1000:.4f} K/km',
        'details': {'heat_flux_W_m2': heat_flux, 'conductivity_W_mK': thermal_conductivity, 'gradient_K_m': gradient, 'gradient_K_km': gradient*1000, 'depth_to_100C_m': depth_100C},
        'unit': 'K/m'
    }

def calc_magnetic_dipole_field(magnetic_moment: float = 8.0e22, radius: float = 6.371e6, theta: float = np.pi/4) -> dict:
    """Magnetic dipole field: B = (mu_0/(4*pi))*(m/r^3)*sqrt(1+3*cos^2(theta))."""
    mu_0 = 4.0 * np.pi * 1e-7
    B = (mu_0 / (4.0 * np.pi)) * (magnetic_moment / radius**3) * np.sqrt(1.0 + 3.0 * np.cos(theta)**2)
    B_uT = B * 1e6
    return {
        'result': f'B = {B:.4e} T = {B_uT:.4f} uT',
        'details': {'magnetic_moment_Am2': magnetic_moment, 'radius_m': radius, 'theta_rad': theta, 'B_T': B, 'B_uT': B_uT},
        'unit': 'T'
    }

def calc_plate_tectonic_stress(strain_rate: float = 1e-14, viscosity: float = 1e21) -> dict:
    """Plate tectonic stress: sigma ~ 2*eta*epsilon_dot."""
    sigma = 2.0 * viscosity * strain_rate
    return {
        'result': f'sigma = {sigma:.4e} Pa = {sigma/1e6:.4f} MPa',
        'details': {'strain_rate_per_s': strain_rate, 'viscosity_Pa_s': viscosity, 'stress_Pa': sigma},
        'unit': 'Pa'
    }

def calc_rutherford_scattering_angle(Z1: int = 2, Z2: int = 79, E_MeV: float = 5.0, impact_parameter: float = 1e-14) -> dict:
    """Rutherford scattering angle: theta = 2*arctan(b_0/(2*b)), b_0 = Z1*Z2*e^2/(4*pi*eps_0*E)."""
    e = 1.602176634e-19
    epsilon_0 = 8.8541878128e-12
    E_J = E_MeV * 1e6 * e
    b0 = Z1 * Z2 * e**2 / (4.0 * np.pi * epsilon_0 * E_J)
    if impact_parameter > 0:
        theta = 2.0 * np.arctan(b0 / (2.0 * impact_parameter))
    else:
        theta = np.pi
    theta_deg = np.degrees(theta)
    return {
        'result': f'theta = {theta:.6f} rad = {theta_deg:.4f} deg',
        'details': {'Z1': Z1, 'Z2': Z2, 'E_MeV': E_MeV, 'impact_parameter_m': impact_parameter, 'b0_m': b0, 'theta_rad': theta, 'theta_deg': theta_deg},
        'unit': 'rad'
    }

def calc_binary_collision_energy(m1: float = 1.67e-27, m2: float = 4.0*1.67e-27, E_incident: float = 1e-13, angle_CM_rad: float = np.pi/4) -> dict:
    """Energy transfer in binary collision: E_transferred = (4*m1*m2/(m1+m2)^2)*E_incident*sin^2(theta_CM/2)."""
    factor = 4.0 * m1 * m2 / (m1 + m2)**2
    E_transferred = factor * E_incident * np.sin(angle_CM_rad / 2.0)**2
    return {
        'result': f'Transferred energy = {E_transferred/1.602176634e-19:.4f} eV ({E_transferred/E_incident*100:.2f}%)',
        'details': {'m1_kg': m1, 'm2_kg': m2, 'E_incident_J': E_incident, 'angle_CM_rad': angle_CM_rad, 'kinematic_factor': factor, 'E_transferred_J': E_transferred, 'fraction': E_transferred / E_incident},
        'unit': 'J'
    }

def calc_biot_savart_simple(I: float = 10.0, segment_length: float = 0.01, distance: float = 0.05, angle_rad: float = np.pi/2) -> dict:
    """Biot-Savart law for short segment: dB = (mu_0/(4*pi))*I*dl*sin(theta)/r^2."""
    mu_0 = 4.0 * np.pi * 1e-7
    dB = (mu_0 / (4.0 * np.pi)) * I * segment_length * np.sin(angle_rad) / distance**2
    return {
        'result': f'dB = {dB:.4e} T',
        'details': {'I_A': I, 'dl_m': segment_length, 'r_m': distance, 'theta_rad': angle_rad, 'dB_T': dB},
        'unit': 'T'
    }

def calc_fluid_continuity(A1: float = 0.01, v1: float = 2.0, A2: float = 0.005) -> dict:
    """Continuity equation: A1*v1 = A2*v2."""
    v2 = A1 * v1 / A2 if A2 > 0 else float('inf')
    flow_rate = A1 * v1
    return {
        'result': f'v2 = {v2:.4f} m/s, Q = {flow_rate:.4f} m^3/s',
        'details': {'A1_m2': A1, 'v1_ms': v1, 'A2_m2': A2, 'v2_ms': v2, 'flow_rate_m3s': flow_rate},
        'unit': 'm/s'
    }

def calc_boundary_layer_thickness(Re_x: float = 5e5, x: float = 1.0, layer_type: str = 'laminar') -> dict:
    """Boundary layer thickness: delta_laminar = 5*x/sqrt(Re_x), delta_turbulent = 0.37*x/Re_x^(1/5)."""
    if layer_type == 'laminar':
        delta = 5.0 * x / np.sqrt(Re_x)
    else:
        delta = 0.37 * x / Re_x**0.2
    return {
        'result': f'delta = {delta:.6e} m ({layer_type})',
        'details': {'Re_x': Re_x, 'x_m': x, 'layer_type': layer_type, 'delta_m': delta},
        'unit': 'm'
    }

def calc_archimedes_principle(volume_submerged: float = 0.001, fluid_density: float = 1000.0) -> dict:
    """Buoyant force: F_b = rho_fluid * V_submerged * g."""
    g = 9.81
    F_b = fluid_density * volume_submerged * g
    return {
        'result': f'F_b = {F_b:.4f} N',
        'details': {'V_m3': volume_submerged, 'rho_kgm3': fluid_density, 'g': g, 'buoyant_force_N': F_b},
        'unit': 'N'
    }

def calc_stokes_drag(radius: float = 0.001, velocity: float = 0.01, viscosity: float = 0.001, rho_fluid: float = 1000.0, rho_particle: float = 2500.0) -> dict:
    """Stokes drag: F_d = 6*pi*eta*r*v, terminal velocity: v_t = 2*(rho_p-rho_f)*g*r^2/(9*eta)."""
    g = 9.81
    F_d = 6.0 * np.pi * viscosity * radius * velocity
    v_terminal = 2.0 * (rho_particle - rho_fluid) * g * radius**2 / (9.0 * viscosity) if rho_particle > rho_fluid else 0.0
    return {
        'result': f'F_d = {F_d:.4e} N, terminal velocity = {v_terminal:.4f} m/s',
        'details': {'radius_m': radius, 'velocity_ms': velocity, 'viscosity_Pas': viscosity, 'drag_force_N': F_d, 'terminal_velocity_ms': v_terminal},
        'unit': 'N'
    }

def calc_coriolis_force(velocity: float = 10.0, angular_velocity: float = 7.2921e-5, latitude_deg: float = 45.0) -> dict:
    """Coriolis acceleration: a_c = 2 * Omega * v * sin(latitude)."""
    lat_rad = np.radians(latitude_deg)
    a_c = 2.0 * angular_velocity * velocity * np.sin(lat_rad)
    return {
        'result': f'a_c = {a_c:.6e} m/s^2',
        'details': {'velocity_ms': velocity, 'angular_velocity_rads': angular_velocity, 'latitude_deg': latitude_deg, 'coriolis_accel_ms2': a_c},
        'unit': 'm/s^2'
    }

def calc_froude_number(velocity: float = 5.0, characteristic_length: float = 2.0) -> dict:
    """Froude number: Fr = v / sqrt(g*L)."""
    g = 9.81
    Fr = velocity / np.sqrt(g * characteristic_length)
    regime = 'subcritical' if Fr < 1 else 'supercritical' if Fr > 1 else 'critical'
    return {
        'result': f'Fr = {Fr:.4f} ({regime})',
        'details': {'velocity_ms': velocity, 'length_m': characteristic_length, 'Fr': Fr, 'regime': regime},
        'unit': 'dimensionless'
    }

def calc_mach_number(velocity: float = 340.0, speed_of_sound: float = 343.0) -> dict:
    """Mach number: Ma = v / c."""
    Ma = velocity / speed_of_sound
    regime = 'subsonic' if Ma < 0.8 else 'transonic' if Ma < 1.2 else 'supersonic' if Ma < 5 else 'hypersonic'
    return {
        'result': f'Ma = {Ma:.4f} ({regime})',
        'details': {'velocity_ms': velocity, 'speed_of_sound_ms': speed_of_sound, 'Mach': Ma, 'regime': regime},
        'unit': 'dimensionless'
    }

def calc_strouhal_number(frequency: float = 1.0, length: float = 0.1, velocity: float = 1.0) -> dict:
    """Strouhal number: St = f * L / v."""
    St = frequency * length / velocity
    return {
        'result': f'St = {St:.4f}',
        'details': {'frequency_Hz': frequency, 'length_m': length, 'velocity_ms': velocity, 'Strouhal': St},
        'unit': 'dimensionless'
    }

def calc_peclet_number(velocity: float = 0.01, length: float = 0.1, diffusivity: float = 1e-9) -> dict:
    """Peclet number: Pe = v * L / D (ratio of advection to diffusion)."""
    Pe = velocity * length / diffusivity
    dominated_by = 'advection' if Pe > 1 else 'diffusion'
    return {
        'result': f'Pe = {Pe:.4e} (dominated by {dominated_by})',
        'details': {'velocity_ms': velocity, 'length_m': length, 'diffusivity_m2s': diffusivity, 'Pe': Pe, 'regime': dominated_by},
        'unit': 'dimensionless'
    }

def calc_richardson_number(buoyancy_freq: float = 0.01, shear: float = 0.1) -> dict:
    """Gradient Richardson number: Ri = N^2 / (du/dz)^2."""
    Ri = buoyancy_freq**2 / (shear**2 + 1e-15)
    stability = 'stable' if Ri > 0.25 else 'potentially turbulent'
    return {
        'result': f'Ri = {Ri:.4f} ({stability})',
        'details': {'N_squared': buoyancy_freq**2, 'shear_squared': shear**2, 'Ri': Ri, 'stability': stability},
        'unit': 'dimensionless'
    }

def calc_acoustic_impedance(rho: float = 1000.0, c: float = 1500.0) -> dict:
    """Acoustic impedance: Z = rho * c."""
    Z = rho * c
    return {
        'result': f'Z = {Z:.4e} Rayl',
        'details': {'density_kgm3': rho, 'speed_of_sound_ms': c, 'impedance_Rayl': Z},
        'unit': 'Rayl (kg/(m^2*s))'
    }

def calc_doppler_effect_acoustic(source_freq: float = 1000.0, source_speed: float = 30.0, observer_speed: float = 0.0, speed_of_sound: float = 343.0) -> dict:
    """Doppler effect: f' = f * (c + v_o)/(c - v_s) (approaching)."""
    f_obs = source_freq * (speed_of_sound + observer_speed) / (speed_of_sound - source_speed)
    f_obs_receding = source_freq * (speed_of_sound - observer_speed) / (speed_of_sound + source_speed)
    return {
        'result': f'f_observed = {f_obs:.4f} Hz (approaching), {f_obs_receding:.4f} Hz (receding)',
        'details': {'source_freq_Hz': source_freq, 'source_speed_ms': source_speed, 'observer_speed_ms': observer_speed, 'c_ms': speed_of_sound, 'f_approach': f_obs, 'f_recede': f_obs_receding},
        'unit': 'Hz'
    }

COMMANDS = {
    'hookes_law_3d': {'func': calc_hookes_law_3d, 'params': ['lambda_lame', 'mu_lame', 'epsilon_xx', 'epsilon_yy', 'epsilon_zz', 'gamma_xy', 'gamma_xz', 'gamma_yz'], 'desc': 'Generalized Hookes law with von Mises stress'},
    'strain_tensor': {'func': calc_strain_tensor_from_displacement, 'params': ['du_dx', 'du_dy', 'du_dz', 'dv_dx', 'dv_dy', 'dv_dz', 'dw_dx', 'dw_dy', 'dw_dz'], 'desc': 'Strain tensor from displacement gradients'},
    'navier_cauchy': {'func': calc_navier_cauchy, 'params': ['u_field_info'], 'desc': 'Navier-Cauchy wave speeds (P and S)'},
    'alfven_speed': {'func': calc_alfven_speed, 'params': ['B', 'rho'], 'desc': 'Alfven speed in MHD v_A = B/sqrt(mu0*rho)'},
    'magnetic_reynolds': {'func': calc_magnetic_reynolds_number, 'params': ['velocity', 'length', 'magnetic_diffusivity'], 'desc': 'Magnetic Reynolds number Rm = vL/eta'},
    'plasma_beta': {'func': calc_plasma_beta, 'params': ['B', 'pressure'], 'desc': 'Plasma beta = 2*mu0*p/B^2'},
    'frozen_in_flux': {'func': calc_frozen_in_flux, 'params': ['Rm'], 'desc': 'Frozen-in flux condition'},
    'radiation_attenuation': {'func': calc_radiation_attenuation, 'params': ['I0', 'mu', 'thickness'], 'desc': 'Radiation attenuation I = I0*exp(-mu*x)'},
    'half_value_layer': {'func': calc_half_value_layer, 'params': ['mu'], 'desc': 'Half-value layer (HVL) and TVL'},
    'buildup_factor': {'func': calc_buildup_factor, 'params': ['energy_MeV', 'mean_free_paths', 'material'], 'desc': 'Radiation buildup factor'},
    'radiation_dose': {'func': calc_radiation_dose, 'params': ['energy_J', 'mass_kg', 'quality_factor'], 'desc': 'Absorbed dose (Gy) and equivalent dose (Sv)'},
    'poiseuille': {'func': calc_poiseuille_flow, 'params': ['radius', 'length', 'delta_P', 'viscosity'], 'desc': 'Hagen-Poiseuille blood flow'},
    'ficks_law': {'func': calc_ficks_law_diffusion, 'params': ['D', 'concentration_gradient', 'area'], 'desc': 'Ficks law of diffusion'},
    'hodgkin_huxley': {'func': calc_hodgkin_huxley_simple, 'params': ['Vm', 'gNa', 'gK', 'gL', 'ENa', 'EK', 'EL'], 'desc': 'Simplified Hodgkin-Huxley neuron model'},
    'bone_mechanics': {'func': calc_bone_mechanics, 'params': ['force', 'area', 'length', 'youngs_modulus'], 'desc': 'Bone mechanical properties'},
    'bouguer_anomaly': {'func': calc_bouguer_gravity_anomaly, 'params': ['thickness', 'density_contrast'], 'desc': 'Bouguer gravity anomaly'},
    'isostasy_airy': {'func': calc_isostasy_airy, 'params': ['crustal_thickness', 'crustal_density', 'mantle_density'], 'desc': 'Airy isostasy model'},
    'isostasy_pratt': {'func': calc_isostasy_pratt, 'params': ['elevation', 'reference_density', 'compensation_depth'], 'desc': 'Pratt isostasy model'},
    'seismic_velocities': {'func': calc_seismic_wave_velocities, 'params': ['K_bulk', 'G_shear', 'density'], 'desc': 'Seismic P and S wave velocities'},
    'geothermal_gradient': {'func': calc_geothermal_gradient, 'params': ['heat_flux', 'thermal_conductivity'], 'desc': 'Geothermal gradient dT/dz = q/k'},
    'magnetic_dipole': {'func': calc_magnetic_dipole_field, 'params': ['magnetic_moment', 'radius', 'theta'], 'desc': 'Geomagnetic dipole field'},
    'plate_tectonics': {'func': calc_plate_tectonic_stress, 'params': ['strain_rate', 'viscosity'], 'desc': 'Plate tectonic deviatoric stress'},
    'rutherford_scattering': {'func': calc_rutherford_scattering_angle, 'params': ['Z1', 'Z2', 'E_MeV', 'impact_parameter'], 'desc': 'Rutherford scattering angle from impact parameter'},
    'binary_collision': {'func': calc_binary_collision_energy, 'params': ['m1', 'm2', 'E_incident', 'angle_CM_rad'], 'desc': 'Energy transfer in binary elastic collision'},
    'biot_savart': {'func': calc_biot_savart_simple, 'params': ['I', 'segment_length', 'distance', 'angle_rad'], 'desc': 'Biot-Savart law for short current segment'},
    'fluid_continuity': {'func': calc_fluid_continuity, 'params': ['A1', 'v1', 'A2'], 'desc': 'Continuity equation A1*v1 = A2*v2'},
    'boundary_layer': {'func': calc_boundary_layer_thickness, 'params': ['Re_x', 'x', 'layer_type'], 'desc': 'Boundary layer thickness'},
    'archimedes': {'func': calc_archimedes_principle, 'params': ['volume_submerged', 'fluid_density'], 'desc': 'Archimedes buoyant force'},
    'stokes_drag': {'func': calc_stokes_drag, 'params': ['radius', 'velocity', 'viscosity', 'rho_fluid', 'rho_particle'], 'desc': 'Stokes drag and terminal velocity'},
    'coriolis_force': {'func': calc_coriolis_force, 'params': ['velocity', 'angular_velocity', 'latitude_deg'], 'desc': 'Coriolis acceleration'},
    'froude_number': {'func': calc_froude_number, 'params': ['velocity', 'characteristic_length'], 'desc': 'Froude number Fr = v/sqrt(gL)'},
    'mach_number': {'func': calc_mach_number, 'params': ['velocity', 'speed_of_sound'], 'desc': 'Mach number Ma = v/c'},
    'strouhal_number': {'func': calc_strouhal_number, 'params': ['frequency', 'length', 'velocity'], 'desc': 'Strouhal number St = fL/v'},
    'peclet_number': {'func': calc_peclet_number, 'params': ['velocity', 'length', 'diffusivity'], 'desc': 'Peclet number Pe = vL/D'},
    'richardson_number': {'func': calc_richardson_number, 'params': ['buoyancy_freq', 'shear'], 'desc': 'Gradient Richardson number'},
    'acoustic_impedance': {'func': calc_acoustic_impedance, 'params': ['rho', 'c'], 'desc': 'Acoustic impedance Z = rho*c'},
    'doppler_acoustic': {'func': calc_doppler_effect_acoustic, 'params': ['source_freq', 'source_speed', 'observer_speed', 'speed_of_sound'], 'desc': 'Acoustic Doppler effect'}
}
