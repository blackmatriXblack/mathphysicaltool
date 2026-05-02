"""
Advanced Geometry & Topology - Mathematics Computation Module
"""
import math

COMMANDS = {}

# ============================================================
# Affine Geometry
# ============================================================

def calc_affine_transform_2d(x: float = 1.0, y: float = 1.0,
                             tx: float = 2.0, ty: float = 3.0,
                             sx: float = 1.0, sy: float = 1.0,
                             angle: float = 0.0, shear: float = 0.0) -> dict:
    """Apply affine transformations: translation, scaling, rotation, shear, reflection."""
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    a11 = sx * cos_a - sy * sin_a * shear
    a12 = -sx * sin_a + sy * cos_a * shear
    a13 = tx
    a21 = sx * sin_a + sy * cos_a * shear
    a22 = sx * cos_a + sy * sin_a * shear
    a23 = ty
    x_new = a11 * x + a12 * y + a13
    y_new = a21 * x + a22 * y + a23
    matrix = [[a11, a12, a13], [a21, a22, a23], [0, 0, 1]]
    return {
        'result': f'Transformed: ({x:.2f}, {y:.2f}) -> ({x_new:.4f}, {y_new:.4f})',
        'details': {
            'original': (x, y),
            'transformed': (round(x_new, 6), round(y_new, 6)),
            'translation': (tx, ty),
            'scaling': (sx, sy),
            'rotation_angle_rad': angle,
            'rotation_angle_deg': math.degrees(angle),
            'shear': shear,
            'matrix_3x3': [[round(v, 6) for v in row] for row in matrix]
        },
        'unit': 'dimensionless'
    }

def calc_homogeneous_coords(x: float = 2.0, y: float = 3.0, w: float = 1.0) -> dict:
    """Convert to/from homogeneous coordinates."""
    if w != 0:
        cartesian_x = x / w
        cartesian_y = y / w
    else:
        cartesian_x = 'inf'
        cartesian_y = 'inf'
    return {
        'result': f'Homogeneous ({x}, {y}, {w}) -> Cartesian ({cartesian_x}, {cartesian_y})',
        'details': {
            'homogeneous': (x, y, w),
            'cartesian': (round(x / w, 6) if w != 0 else 'inf', round(y / w, 6) if w != 0 else 'inf'),
            'is_point_at_infinity': w == 0
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Projective Geometry
# ============================================================

def calc_cross_ratio(z1_real: float = 0.0, z1_imag: float = 0.0,
                     z2_real: float = 1.0, z2_imag: float = 0.0,
                     z3_real: float = 2.0, z3_imag: float = 0.0,
                     z4_real: float = 3.0, z4_imag: float = 0.0) -> dict:
    """Cross ratio of four collinear points: (z1,z2;z3,z4) = (z1-z3)(z2-z4)/((z1-z4)(z2-z3))."""
    z1 = complex(z1_real, z1_imag)
    z2 = complex(z2_real, z2_imag)
    z3 = complex(z3_real, z3_imag)
    z4 = complex(z4_real, z4_imag)
    num = (z1 - z3) * (z2 - z4)
    den = (z1 - z4) * (z2 - z3)
    if den == 0:
        cr = complex(float('inf'), 0)
    else:
        cr = num / den
    return {
        'result': f'Cross ratio = {cr.real:.6f}' + (f' + {cr.imag:.6f}i' if abs(cr.imag) > 1e-10 else ''),
        'details': {
            'z1': str(z1), 'z2': str(z2), 'z3': str(z3), 'z4': str(z4),
            'cross_ratio': str(cr),
            'is_real': abs(cr.imag) < 1e-10,
            'invariant': 'Projective invariant'
        },
        'unit': 'dimensionless'
    }

def calc_projective_matrix(h11: float = 1.0, h12: float = 0.0, h13: float = 0.0,
                           h21: float = 0.0, h22: float = 1.0, h23: float = 0.0,
                           h31: float = 0.0, h32: float = 0.0, h33: float = 1.0,
                           x: float = 1.0, y: float = 2.0) -> dict:
    """Apply projective transformation (homography) to point (x,y)."""
    det = h11 * (h22 * h33 - h23 * h32) - h12 * (h21 * h33 - h23 * h31) + h13 * (h21 * h32 - h22 * h31)
    xp = h11 * x + h12 * y + h13
    yp = h21 * x + h22 * y + h23
    wp = h31 * x + h32 * y + h33
    if wp != 0:
        xn, yn = xp / wp, yp / wp
    else:
        xn, yn = float('inf'), float('inf')
    return {
        'result': f'Projective transform of ({x},{y}) -> ({xn:.4f}, {yn:.4f})',
        'details': {
            'H_matrix': [[h11, h12, h13], [h21, h22, h23], [h31, h32, h33]],
            'determinant': det,
            'original': (x, y),
            'transformed': (round(xn, 6) if xn != float('inf') else 'inf',
                          round(yn, 6) if yn != float('inf') else 'inf')
        },
        'unit': 'dimensionless'
    }

def calc_points_at_infinity() -> dict:
    """Demonstrate points at infinity in projective geometry."""
    return {
        'result': 'Points at infinity: (x, y, 0) represent directions',
        'details': {
            'direction_horizontal': '(1, 0, 0)',
            'direction_vertical': '(0, 1, 0)',
            'direction_slope_m': '(1, m, 0)',
            'line_at_infinity': 'w = 0',
            'duality': 'Points and lines are dual in the projective plane'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Non-Euclidean Geometry
# ============================================================

def calc_hyperbolic_distance(x1: float = 0.0, y1: float = 0.0,
                             x2: float = 0.5, y2: float = 0.0) -> dict:
    """Hyperbolic distance in Poincare disk model."""
    r1_sq = x1**2 + y1**2
    r2_sq = x2**2 + y2**2
    if r1_sq >= 1 or r2_sq >= 1:
        return {'result': 'Points must be inside unit disk', 'details': {'r1_sq': r1_sq, 'r2_sq': r2_sq}, 'unit': 'dimensionless'}
    dist_sq = (x1 - x2)**2 + (y1 - y2)**2
    arg = 1 + 2 * dist_sq / ((1 - r1_sq) * (1 - r2_sq))
    d = math.acosh(arg) if arg >= 1 else 0
    return {
        'result': f'Hyperbolic distance = {d:.6f}',
        'details': {
            'P': (x1, y1), 'Q': (x2, y2),
            '|P|^2': r1_sq, '|Q|^2': r2_sq,
            'distance': d,
            'model': 'Poincare disk',
            'metric': 'ds^2 = 4(dx^2+dy^2)/(1-x^2-y^2)^2'
        },
        'unit': 'dimensionless'
    }

def calc_hyperbolic_triangle_area(alpha: float = 0.5, beta: float = 0.5, gamma: float = 0.5) -> dict:
    """Area of hyperbolic triangle: Area = pi - (alpha + beta + gamma)."""
    angle_sum = alpha + beta + gamma
    area = math.pi - angle_sum
    if area <= 0:
        return {
            'result': f'Invalid triangle: angle sum = {angle_sum:.4f} >= pi',
            'details': {'alpha': alpha, 'beta': beta, 'gamma': gamma, 'sum': angle_sum, 'area': area},
            'unit': 'dimensionless'
        }
    return {
        'result': f'Hyperbolic triangle area = {area:.6f} (in units of curvature)',
        'details': {
            'angles_rad': (alpha, beta, gamma),
            'angles_deg': tuple(math.degrees(a) for a in (alpha, beta, gamma)),
            'angle_sum': angle_sum,
            'defect': area,
            'formula': 'Area = pi - (alpha + beta + gamma)'
        },
        'unit': 'dimensionless'
    }

def calc_spherical_distance(lat1: float = 0.0, lon1: float = 0.0,
                            lat2: float = 45.0, lon2: float = 45.0,
                            R: float = 6371.0) -> dict:
    """Great circle distance (Haversine formula)."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return {
        'result': f'Spherical distance = {d:.2f} km (R={R} km)',
        'details': {
            'point1': (lat1, lon1), 'point2': (lat2, lon2),
            'R': R, 'distance': round(d, 4),
            'angular_distance_rad': c,
            'angular_distance_deg': math.degrees(c),
            'formula': 'Haversine'
        },
        'unit': 'km'
    }

def calc_spherical_triangle_area(A: float = 1.0, B: float = 1.0, C: float = 1.0,
                                 R: float = 6371.0) -> dict:
    """Spherical triangle area: E = R^2 * (A + B + C - pi)."""
    angle_sum = A + B + C
    E = angle_sum - math.pi
    if E <= 0:
        return {
            'result': f'Invalid: angle sum = {angle_sum:.4f} <= pi',
            'details': {'A': A, 'B': B, 'C': C, 'sum': angle_sum, 'excess': E},
            'unit': 'km^2'
        }
    area = R * R * E
    return {
        'result': f'Spherical triangle area = {area:.2f} km^2',
        'details': {
            'angles_rad': (A, B, C),
            'angles_deg': tuple(math.degrees(a) for a in (A, B, C)),
            'spherical_excess_rad': E,
            'spherical_excess_deg': math.degrees(E),
            'area': round(area, 4), 'R': R,
            'formula': 'E = R^2 * (A + B + C - pi)'
        },
        'unit': 'km^2'
    }

# ============================================================
# Differential Geometry
# ============================================================

def calc_curve_curvature(t: float = 0.5) -> dict:
    """Curvature of helix r(t) = (cos t, sin t, t): kappa = |r' x r''| / |r'|^3 = 1/2."""
    rp_x, rp_y, rp_z = -math.sin(t), math.cos(t), 1.0
    rpp_x, rpp_y, rpp_z = -math.cos(t), -math.sin(t), 0.0
    cx = rp_y * rpp_z - rp_z * rpp_y
    cy = rp_z * rpp_x - rp_x * rpp_z
    cz = rp_x * rpp_y - rp_y * rpp_x
    cross_norm = math.sqrt(cx*cx + cy*cy + cz*cz)
    rp_norm = math.sqrt(rp_x*rp_x + rp_y*rp_y + rp_z*rp_z)
    kappa = cross_norm / (rp_norm ** 3) if rp_norm > 0 else 0
    return {
        'result': f'kappa(t={t}) = {kappa:.6f}',
        'details': {
            'curve': 'r(t) = (cos t, sin t, t)',
            't': t,
            'point': (math.cos(t), math.sin(t), t),
            'r_prime': (rp_x, rp_y, rp_z),
            'r_double': (rpp_x, rpp_y, rpp_z),
            'curvature': kappa,
            'formula': 'kappa = |r\' x r\'\'| / |r\'|^3'
        },
        'unit': '1/length'
    }

def calc_curve_torsion(t: float = 0.5) -> dict:
    """Torsion of helix r(t) = (cos t, sin t, t): tau = (r' x r'') . r''' / |r' x r''|^2 = 1/2."""
    rp = (-math.sin(t), math.cos(t), 1.0)
    rpp = (-math.cos(t), -math.sin(t), 0.0)
    rppp = (math.sin(t), -math.cos(t), 0.0)
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cross_norm_sq = cx*cx + cy*cy + cz*cz
    num = cx * rppp[0] + cy * rppp[1] + cz * rppp[2]
    tau = num / cross_norm_sq if cross_norm_sq > 0 else 0
    return {
        'result': f'tau(t={t}) = {tau:.6f}',
        'details': {
            'curve': 'r(t) = (cos t, sin t, t)',
            't': t,
            'point': (math.cos(t), math.sin(t), t),
            'torsion': tau,
            'formula': 'tau = (r\' x r\'\') . r\'\'\' / |r\' x r\'\'|^2'
        },
        'unit': '1/length'
    }

def calc_frenet_frame(t: float = 0.5) -> dict:
    """Frenet-Serret frame (T, N, B) for helix."""
    rp = (-math.sin(t), math.cos(t), 1.0)
    rpp = (-math.cos(t), -math.sin(t), 0.0)
    rp_norm = math.sqrt(sum(v*v for v in rp))
    T = tuple(v / rp_norm for v in rp) if rp_norm > 0 else (0, 0, 0)
    cx = rp[1] * rpp[2] - rp[2] * rpp[1]
    cy = rp[2] * rpp[0] - rp[0] * rpp[2]
    cz = rp[0] * rpp[1] - rp[1] * rpp[0]
    cross_norm = math.sqrt(cx*cx + cy*cy + cz*cz)
    B = tuple(v / cross_norm for v in (cx, cy, cz)) if cross_norm > 0 else (0, 0, 0)
    N = (B[1]*T[2] - B[2]*T[1], B[2]*T[0] - B[0]*T[2], B[0]*T[1] - B[1]*T[0])
    kappa = cross_norm / (rp_norm**3) if rp_norm > 0 else 0
    return {
        'result': f'Frenet frame: T=({T[0]:.4f},{T[1]:.4f},{T[2]:.4f})',
        'details': {
            'curve': 'r(t) = (cos t, sin t, t)',
            't': t,
            'position': (math.cos(t), math.sin(t), t),
            'T_tangent': tuple(round(v, 6) for v in T),
            'N_normal': tuple(round(v, 6) for v in N),
            'B_binormal': tuple(round(v, 6) for v in B),
            'curvature': kappa,
            'Frenet_equations': "T' = k*N, N' = -k*T + tau*B, B' = -tau*N"
        },
        'unit': 'dimensionless'
    }

def calc_surface_forms(u: float = 0.5, v: float = 0.5) -> dict:
    """Fundamental forms for paraboloid r(u,v) = (u, v, u^2 + v^2)."""
    ru = (1.0, 0.0, 2*u)
    rv = (0.0, 1.0, 2*v)
    ruu = (0.0, 0.0, 2.0)
    ruv = (0.0, 0.0, 0.0)
    rvv = (0.0, 0.0, 2.0)
    E = ru[0]*ru[0] + ru[1]*ru[1] + ru[2]*ru[2]
    F = ru[0]*rv[0] + ru[1]*rv[1] + ru[2]*rv[2]
    G = rv[0]*rv[0] + rv[1]*rv[1] + rv[2]*rv[2]
    nx = ru[1]*rv[2] - ru[2]*rv[1]
    ny = ru[2]*rv[0] - ru[0]*rv[2]
    nz = ru[0]*rv[1] - ru[1]*rv[0]
    n_norm = math.sqrt(nx*nx + ny*ny + nz*nz)
    n = (nx/n_norm, ny/n_norm, nz/n_norm) if n_norm > 0 else (0, 0, 0)
    L = n[0]*ruu[0] + n[1]*ruu[1] + n[2]*ruu[2]
    M = n[0]*ruv[0] + n[1]*ruv[1] + n[2]*ruv[2]
    N_ = n[0]*rvv[0] + n[1]*rvv[1] + n[2]*rvv[2]
    det1 = E*G - F*F
    det2 = L*N_ - M*M
    K = det2 / det1 if det1 != 0 else 0
    H = (E*N_ + G*L - 2*F*M) / (2*det1) if det1 != 0 else 0
    disc = max(0, H*H - K)
    k1 = H + math.sqrt(disc)
    k2 = H - math.sqrt(disc)
    return {
        'result': f'K = {K:.6f}, H = {H:.6f}',
        'details': {
            'surface': 'r(u,v) = (u, v, u^2+v^2)',
            'first_form': {'E': E, 'F': F, 'G': G},
            'second_form': {'L': L, 'M': M, 'N': N_},
            'normal': tuple(round(x, 6) for x in n),
            'gaussian_curvature_K': K,
            'mean_curvature_H': H,
            'principal_curvatures': (k1, k2),
            'classification': 'elliptic' if K > 0 else ('hyperbolic' if K < 0 else ('parabolic' if H != 0 else 'flat'))
        },
        'unit': '1/length^2'
    }

def calc_gaussian_curvature_from_forms(E: float = 1.0, F: float = 0.0, G: float = 1.0,
                                       L: float = 0.0, M: float = 0.0, N: float = 0.0) -> dict:
    """Compute Gaussian curvature K = (LN - M^2)/(EG - F^2) and mean curvature."""
    det1 = E*G - F*F
    det2 = L*N - M*M
    K = det2 / det1 if det1 != 0 else 0
    H = (E*N + G*L - 2*F*M) / (2*det1) if det1 != 0 else 0
    disc = max(0, H*H - K)
    k1 = H + math.sqrt(disc)
    k2 = H - math.sqrt(disc)
    return {
        'result': f'K = {K:.6f}, H = {H:.6f}',
        'details': {
            'first_form': {'E': E, 'F': F, 'G': G},
            'second_form': {'L': L, 'M': M, 'N': N},
            'gaussian_curvature': K, 'mean_curvature': H,
            'principal_curvatures': (k1, k2),
            'classification': 'elliptic' if K > 0 else ('hyperbolic' if K < 0 else ('parabolic' if H != 0 else 'flat'))
        },
        'unit': '1/length^2'
    }

def calc_geodesic_curvature(theta: float = 0.785398, R: float = 1.0) -> dict:
    """Geodesic curvature for latitude circle on sphere. kg = 1/(R tan theta)."""
    kg = 1.0 / (R * math.tan(theta)) if abs(math.tan(theta)) > 1e-15 else 0
    return {
        'result': f'Geodesic curvature = {kg:.6f}',
        'details': {
            'R': R, 'colatitude_theta': theta,
            'geodesic_curvature': kg,
            'note': 'kg=0 for great circles (geodesics on sphere)'
        },
        'unit': '1/length'
    }

def calc_christoffel_symbols(u: float = 0.5, v: float = 0.5) -> dict:
    """Numerical Christoffel symbols for paraboloid r(u,v) = (u, v, u^2 - v^2)."""
    h = 1e-5
    def r(uu, vv):
        return (uu, vv, uu*uu - vv*vv)
    def partial_du(uu, vv):
        rp = r(uu+h, vv)
        rm = r(uu-h, vv)
        return tuple((rp[i]-rm[i])/(2*h) for i in range(3))
    def partial_dv(uu, vv):
        rp = r(uu, vv+h)
        rm = r(uu, vv-h)
        return tuple((rp[i]-rm[i])/(2*h) for i in range(3))
    def partial_duu(uu, vv):
        r0 = r(uu, vv)
        rp = r(uu+h, vv)
        rm = r(uu-h, vv)
        return tuple((rp[i]-2*r0[i]+rm[i])/(h*h) for i in range(3))
    def partial_duv(uu, vv):
        rpp = r(uu+h, vv+h)
        rpm = r(uu+h, vv-h)
        rmp = r(uu-h, vv+h)
        rmm = r(uu-h, vv-h)
        return tuple((rpp[i]-rpm[i]-rmp[i]+rmm[i])/(4*h*h) for i in range(3))
    def partial_dvv(uu, vv):
        r0 = r(uu, vv)
        rp = r(uu, vv+h)
        rm = r(uu, vv-h)
        return tuple((rp[i]-2*r0[i]+rm[i])/(h*h) for i in range(3))
    ru = partial_du(u, v)
    rv = partial_dv(u, v)
    ruu = partial_duu(u, v)
    ruv = partial_duv(u, v)
    rvv = partial_dvv(u, v)
    E = sum(ru[i]*ru[i] for i in range(3))
    F = sum(ru[i]*rv[i] for i in range(3))
    G = sum(rv[i]*rv[i] for i in range(3))
    det = E*G - F*F
    if abs(det) < 1e-12:
        return {'result': 'Degenerate metric', 'details': {}, 'unit': 'dimensionless'}
    Eu = 2*sum(ru[i]*ruu[i] for i in range(3))
    Ev = 2*sum(ru[i]*ruv[i] for i in range(3))
    Fu = sum(ruu[i]*rv[i] + ru[i]*ruv[i] for i in range(3))
    Fv = sum(ruv[i]*rv[i] + ru[i]*rvv[i] for i in range(3))
    Gu = 2*sum(rv[i]*ruv[i] for i in range(3))
    Gv = 2*sum(rv[i]*rvv[i] for i in range(3))
    G1_uu = (G*Eu - F*(2*Fu - Ev)) / (2*det)
    G2_uu = (E*(2*Fu - Ev) - F*Eu) / (2*det)
    G1_uv = (G*Ev - F*Gu) / (2*det)
    G2_uv = (E*Gu - F*Ev) / (2*det)
    G1_vv = (G*(2*Fv - Gu) - F*Gv) / (2*det)
    G2_vv = (E*Gv - F*(2*Fv - Gu)) / (2*det)
    return {
        'result': f'Christoffel symbols at (u={u}, v={v})',
        'details': {
            'Gamma^u_uu': round(G1_uu, 6),
            'Gamma^v_uu': round(G2_uu, 6),
            'Gamma^u_uv': round(G1_uv, 6),
            'Gamma^v_uv': round(G2_uv, 6),
            'Gamma^u_vv': round(G1_vv, 6),
            'Gamma^v_vv': round(G2_vv, 6)
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Topology
# ============================================================

def calc_euler_characteristic(V: int = 8, E: int = 12, F: int = 6) -> dict:
    """Euler characteristic chi = V - E + F."""
    chi = V - E + F
    if chi % 2 == 0:
        genus = (2 - chi) // 2
    else:
        genus = None
    return {
        'result': f'chi = {chi}, genus g = {genus}',
        'details': {
            'vertices': V, 'edges': E, 'faces': F,
            'euler_characteristic': chi, 'genus': genus,
            'examples': {'sphere': 'chi=2, g=0', 'torus': 'chi=0, g=1', 'double_torus': 'chi=-2, g=2'}
        },
        'unit': 'dimensionless'
    }

def calc_genus(V: int = 8, E: int = 12, F: int = 6) -> dict:
    """Genus from Euler characteristic: g = (2 - chi)/2."""
    chi = V - E + F
    if chi % 2 == 0:
        g = (2 - chi) // 2
    else:
        g = (2 - chi) / 2
    return {
        'result': f'Genus g = {g}',
        'details': {'V': V, 'E': E, 'F': F, 'chi': chi, 'genus': g},
        'unit': 'dimensionless'
    }

def calc_orientability(faces: list = None) -> dict:
    """Check orientability of simplicial complex via edge adjacency."""
    if faces is None:
        faces = [[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]]
    edge_count = {}
    for f in faces:
        for i in range(3):
            a, b = f[i], f[(i+1)%3]
            key = (min(a, b), max(a, b))
            edge_count[key] = edge_count.get(key, 0) + 1
    closed = all(c == 2 for c in edge_count.values())
    return {
        'result': f'Mesh closed: {closed}, orientable: {closed}',
        'details': {
            'faces': faces,
            'edge_counts': edge_count,
            'orientable': closed,
            'note': 'Heuristic: all edges appear in exactly 2 faces'
        },
        'unit': 'dimensionless'
    }

def calc_betti_numbers(vertices: list = None, edges: list = None) -> dict:
    """Betti numbers for a simplicial complex: b0 = components, b1 = cycles."""
    if vertices is None:
        vertices = [0, 1, 2, 3]
    if edges is None:
        edges = [(0, 1), (1, 2), (2, 0), (0, 3)]
    parent = {v: v for v in vertices}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry
    for a, b in edges:
        union(a, b)
    components = set(find(v) for v in vertices)
    b0 = len(components)
    b1 = len(edges) - len(vertices) + b0
    return {
        'result': f'b0 = {b0}, b1 = {b1}',
        'details': {
            'vertices': vertices, 'edges': edges,
            'b0_components': b0, 'b1_cycles': b1,
            'components': sorted(components)
        },
        'unit': 'dimensionless'
    }

def calc_fundamental_group(shape: str = 'circle') -> dict:
    """Fundamental group of common topological spaces."""
    groups = {
        'circle': 'Z (infinite cyclic)',
        'sphere_S2': 'trivial',
        'torus': 'Z x Z',
        'real_projective_plane': 'Z_2 (cyclic order 2)',
        'figure_eight': 'Z * Z (free group on 2 generators)',
        'disk': 'trivial',
        'cylinder': 'Z',
        'mobius_strip': 'Z',
        'klein_bottle': '<a,b | abab^{-1}=1>'
    }
    return {
        'result': f'pi_1({shape}) = {groups.get(shape, "unknown")}',
        'details': {
            'shape': shape,
            'fundamental_group': groups.get(shape, 'Not in table'),
            'available_shapes': list(groups.keys())
        },
        'unit': 'dimensionless'
    }

def calc_homology_components(adj_matrix: list = None) -> dict:
    """H0: count connected components from adjacency matrix."""
    if adj_matrix is None:
        adj_matrix = [[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
    n = len(adj_matrix)
    visited = [False] * n
    components = 0
    comp_nodes = []
    for i in range(n):
        if not visited[i]:
            components += 1
            comp = []
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    comp.append(node)
                    for j in range(n):
                        if adj_matrix[node][j] and not visited[j]:
                            stack.append(j)
            comp_nodes.append(comp)
    return {
        'result': f'H0 = {components} connected component(s)',
        'details': {
            'adj_matrix': adj_matrix,
            'num_components': components,
            'components': comp_nodes,
            'b0': components
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Higher Dimensions
# ============================================================

def calc_nsphere_volume(n: int = 3, R: float = 1.0) -> dict:
    """Volume of n-sphere: V_n = pi^(n/2) R^n / Gamma(n/2 + 1)."""
    if n == 1:
        V = 2 * R
    elif n == 2:
        V = math.pi * R * R
    elif n == 3:
        V = (4.0/3.0) * math.pi * R**3
    elif n == 4:
        V = (math.pi**2 / 2) * R**4
    elif n == 5:
        V = (8 * math.pi**2 / 15) * R**5
    elif n == 6:
        V = (math.pi**3 / 6) * R**6
    elif n == 7:
        V = (16 * math.pi**3 / 105) * R**7
    else:
        V = math.pi**(n/2) * (R**n) / math.gamma(n/2 + 1)
    return {
        'result': f'V_{n}(R={R}) = {V:.6f}',
        'details': {
            'n': n, 'R': R, 'volume': V,
            'formula': 'V_n = pi^(n/2) R^n / Gamma(n/2 + 1)'
        },
        'unit': 'length^n'
    }

def calc_ncube_diagonal(n: int = 4, side: float = 1.0) -> dict:
    """Diagonal of n-cube: d = side * sqrt(n)."""
    d = side * math.sqrt(n)
    return {
        'result': f'{n}-cube diagonal = {d:.6f}',
        'details': {'n': n, 'side': side, 'diagonal': d, 'formula': 'd = side * sqrt(n)'},
        'unit': 'length'
    }

def calc_nsimplex_volume(n: int = 3, side: float = 1.0) -> dict:
    """Volume of regular n-simplex: V_n = sqrt(n+1)/(n! * 2^(n/2)) * a^n."""
    V = math.sqrt(n+1) / (math.factorial(n) * (2**(n/2))) * (side**n)
    return {
        'result': f'{n}-simplex volume = {V:.8f}',
        'details': {
            'n': n, 'side': side, 'volume': V,
            'formula': 'V_n = sqrt(n+1)/(n! * 2^(n/2)) * a^n',
            'examples': {
                'n=1': 'side (segment)',
                'n=2': 'sqrt(3)/4 * side^2 (triangle)',
                'n=3': 'sqrt(2)/12 * side^3 (tetrahedron)'
            }
        },
        'unit': 'length^n'
    }

def calc_hypersphere_surface(n: int = 3, R: float = 1.0) -> dict:
    """Surface area of n-sphere boundary: S_{n-1} = n * V_n / R."""
    if n == 1:
        S = 2
    elif n == 2:
        S = 2 * math.pi * R
    elif n == 3:
        S = 4 * math.pi * R**2
    elif n == 4:
        S = 2 * math.pi**2 * R**3
    elif n == 5:
        S = (8 * math.pi**2 / 3) * R**4
    elif n == 6:
        S = math.pi**3 * R**5
    elif n == 7:
        S = (16 * math.pi**3 / 15) * R**6
    else:
        S = 2 * math.pi**(n/2) / math.gamma(n/2) * R**(n-1)
    return {
        'result': f'Surface of {n}-sphere = {S:.6f}',
        'details': {
            'n': n, 'R': R, 'surface_area': S,
            'formula': 'S_{n-1} = 2*pi^(n/2)/Gamma(n/2) * R^(n-1)'
        },
        'unit': 'length^(n-1)'
    }


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'affine_transform': {'func': calc_affine_transform_2d, 'params': ['x', 'y', 'tx', 'ty', 'sx', 'sy', 'angle', 'shear'], 'desc': '2D affine transformation'},
    'homogeneous_coords': {'func': calc_homogeneous_coords, 'params': ['x', 'y', 'w'], 'desc': 'Homogeneous coordinate conversion'},
    'cross_ratio': {'func': calc_cross_ratio, 'params': ['z1_real', 'z1_imag', 'z2_real', 'z2_imag', 'z3_real', 'z3_imag', 'z4_real', 'z4_imag'], 'desc': 'Cross ratio of 4 points'},
    'projective_matrix': {'func': calc_projective_matrix, 'params': ['h11', 'h12', 'h13', 'h21', 'h22', 'h23', 'h31', 'h32', 'h33', 'x', 'y'], 'desc': 'Projective transformation'},
    'points_at_infinity': {'func': calc_points_at_infinity, 'params': [], 'desc': 'Points at infinity concepts'},
    'hyperbolic_distance': {'func': calc_hyperbolic_distance, 'params': ['x1', 'y1', 'x2', 'y2'], 'desc': 'Hyperbolic distance in Poincare disk'},
    'hyperbolic_triangle_area': {'func': calc_hyperbolic_triangle_area, 'params': ['alpha', 'beta', 'gamma'], 'desc': 'Hyperbolic triangle area'},
    'spherical_distance': {'func': calc_spherical_distance, 'params': ['lat1', 'lon1', 'lat2', 'lon2', 'R'], 'desc': 'Great circle distance (Haversine)'},
    'spherical_triangle_area': {'func': calc_spherical_triangle_area, 'params': ['A', 'B', 'C', 'R'], 'desc': 'Spherical triangle area'},
    'curve_curvature': {'func': calc_curve_curvature, 'params': ['t'], 'desc': 'Helix curvature: kappa=1/2'},
    'curve_torsion': {'func': calc_curve_torsion, 'params': ['t'], 'desc': 'Helix torsion: tau=1/2'},
    'frenet_frame': {'func': calc_frenet_frame, 'params': ['t'], 'desc': 'Frenet-Serret frame (T, N, B)'},
    'surface_forms': {'func': calc_surface_forms, 'params': ['u', 'v'], 'desc': 'First and second fundamental forms'},
    'gaussian_curvature': {'func': calc_gaussian_curvature_from_forms, 'params': ['E', 'F', 'G', 'L', 'M', 'N'], 'desc': 'Gaussian curvature from forms'},
    'geodesic_curvature': {'func': calc_geodesic_curvature, 'params': ['theta', 'R'], 'desc': 'Geodesic curvature on sphere'},
    'christoffel_symbols': {'func': calc_christoffel_symbols, 'params': ['u', 'v'], 'desc': 'Christoffel symbols (numerical)'},
    'euler_characteristic': {'func': calc_euler_characteristic, 'params': ['V', 'E', 'F'], 'desc': 'Euler characteristic chi=V-E+F'},
    'genus': {'func': calc_genus, 'params': ['V', 'E', 'F'], 'desc': 'Genus g=(2-chi)/2'},
    'orientability': {'func': calc_orientability, 'params': ['faces'], 'desc': 'Check simplicial complex orientability'},
    'betti_numbers': {'func': calc_betti_numbers, 'params': ['vertices', 'edges'], 'desc': 'Betti numbers b0, b1'},
    'fundamental_group': {'func': calc_fundamental_group, 'params': ['shape'], 'desc': 'Fundamental group of common spaces'},
    'homology_components': {'func': calc_homology_components, 'params': ['adj_matrix'], 'desc': 'H0: connected components count'},
    'nsphere_volume': {'func': calc_nsphere_volume, 'params': ['n', 'R'], 'desc': 'Volume of n-sphere'},
    'ncube_diagonal': {'func': calc_ncube_diagonal, 'params': ['n', 'side'], 'desc': 'Diagonal of n-cube'},
    'nsimplex_volume': {'func': calc_nsimplex_volume, 'params': ['n', 'side'], 'desc': 'Volume of regular n-simplex'},
    'hypersphere_surface': {'func': calc_hypersphere_surface, 'params': ['n', 'R'], 'desc': 'Surface area of n-sphere'},
}
