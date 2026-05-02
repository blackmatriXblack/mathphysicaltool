"""
Geometry & Trigonometry - Mathematics Computation Module
"""
import math
import numpy as np

COMMANDS = {}

# ==============================================================================
# PLANE GEOMETRY
# ==============================================================================

def calc_distance_points(x1: float = 0.0, y1: float = 0.0, x2: float = 3.0, y2: float = 4.0) -> dict:
    """Calculate distance between two points in 2D."""
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return {
        'result': f'Distance = {d:.6f}',
        'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'distance': d},
        'unit': 'length'
    }

def calc_midpoint(x1: float = 0.0, y1: float = 0.0, x2: float = 4.0, y2: float = 6.0) -> dict:
    """Calculate midpoint between two points."""
    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2
    return {
        'result': f'Midpoint = ({mx:.4f}, {my:.4f})',
        'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'midpoint': (mx, my)},
        'unit': 'point'
    }

def calc_line_slope_intercept(m: float = 2.0, b: float = 3.0) -> dict:
    """Return line equation in slope-intercept form y = mx + b."""
    return {
        'result': f'y = {m}x + {b}',
        'details': {'slope': m, 'intercept': b, 'form': 'slope-intercept', 'equation': f'y = {m}x + {b}'},
        'unit': 'equation'
    }

def calc_line_point_slope(x0: float = 1.0, y0: float = 2.0, m: float = 2.0) -> dict:
    """Return line equation in point-slope form (y - y0) = m(x - x0)."""
    return {
        'result': f'(y - {y0}) = {m}(x - {x0})',
        'details': {'x0': x0, 'y0': y0, 'slope': m, 'form': 'point-slope', 'equation': f'y - {y0} = {m}(x - {x0})'},
        'unit': 'equation'
    }

def calc_line_general(A: float = 2.0, B: float = -1.0, C: float = 3.0) -> dict:
    """Return line equation in general form Ax + By + C = 0. Also returns slope and intercepts."""
    if B == 0:
        if A == 0:
            return {
                'result': 'Degenerate: A and B both zero',
                'details': {'A': A, 'B': B, 'C': C, 'type': 'degenerate'},
                'unit': 'equation'
            }
        x_int = -C / A
        return {
            'result': f'{A}x + {C} = 0 (vertical line, x = {x_int:.4f})',
            'details': {'A': A, 'B': B, 'C': C, 'x_intercept': x_int, 'slope': 'undefined', 'type': 'vertical'},
            'unit': 'equation'
        }
    slope = -A / B
    y_int = -C / B
    x_int = -C / A if A != 0 else None
    return {
        'result': f'{A}x + {B}y + {C} = 0 (slope = {slope:.4f})',
        'details': {'A': A, 'B': B, 'C': C, 'slope': slope, 'x_intercept': x_int, 'y_intercept': y_int, 'type': 'general'},
        'unit': 'equation'
    }

def calc_angle_between_lines(m1: float = 1.0, m2: float = 2.0) -> dict:
    """Calculate the acute angle between two lines given their slopes."""
    if abs(1 + m1 * m2) < 1e-12:
        angle_rad = math.pi / 2
    else:
        angle_rad = math.atan(abs((m2 - m1) / (1 + m1 * m2)))
    angle_deg = math.degrees(angle_rad)
    return {
        'result': f'Angle = {angle_rad:.6f} rad = {angle_deg:.4f} degrees',
        'details': {'m1': m1, 'm2': m2, 'angle_rad': angle_rad, 'angle_deg': angle_deg},
        'unit': 'radian'
    }

def calc_triangle_area_heron(a: float = 3.0, b: float = 4.0, c: float = 5.0) -> dict:
    """Calculate triangle area using Heron's formula."""
    if a + b <= c or b + c <= a or c + a <= b:
        return {
            'result': 'Error: Triangle inequality violated - these sides cannot form a triangle',
            'details': {'a': a, 'b': b, 'c': c, 'error': 'triangle inequality'},
            'unit': 'area'
        }
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return {
        'result': f'Area = {area:.6f} (semi-perimeter s = {s:.4f})',
        'details': {'a': a, 'b': b, 'c': c, 'semi_perimeter': s, 'area': area},
        'unit': 'area'
    }

def calc_triangle_area_sas(a: float = 3.0, b: float = 4.0, angle_c_deg: float = 90.0) -> dict:
    """Calculate triangle area using formula (1/2)*a*b*sin(C)."""
    angle_c = math.radians(angle_c_deg)
    area = 0.5 * a * b * math.sin(angle_c)
    return {
        'result': f'Area = 0.5 * {a} * {b} * sin({angle_c_deg}°) = {area:.6f}',
        'details': {'a': a, 'b': b, 'angle_C_deg': angle_c_deg, 'angle_C_rad': angle_c, 'area': area},
        'unit': 'area'
    }

def calc_triangle_area_base_height(base: float = 5.0, height: float = 3.0) -> dict:
    """Calculate triangle area using (1/2)*base*height."""
    area = 0.5 * base * height
    return {
        'result': f'Area = 0.5 * {base} * {height} = {area:.6f}',
        'details': {'base': base, 'height': height, 'area': area},
        'unit': 'area'
    }

def calc_triangle_solver_sss(a: float = 3.0, b: float = 4.0, c: float = 5.0) -> dict:
    """Solve triangle given three sides (SSS) using Law of Cosines."""
    if a + b <= c or b + c <= a or c + a <= b:
        return {
            'result': 'Error: These sides cannot form a triangle',
            'details': {'a': a, 'b': b, 'c': c, 'error': 'triangle inequality'},
            'unit': 'triangle'
        }
    A = math.degrees(math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
    B = math.degrees(math.acos((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)))
    C = 180 - A - B
    area = 0.5 * a * b * math.sin(math.radians(C))
    return {
        'result': f'A = {A:.4f}°, B = {B:.4f}°, C = {C:.4f}°; Area = {area:.4f}',
        'details': {'a': a, 'b': b, 'c': c, 'A_deg': A, 'B_deg': B, 'C_deg': C, 'area': area},
        'unit': 'triangle'
    }

def calc_triangle_solver_sas(a: float = 3.0, b: float = 4.0, angle_c_deg: float = 90.0) -> dict:
    """Solve triangle given two sides and included angle (SAS)."""
    C = math.radians(angle_c_deg)
    c = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))
    if c == 0:
        return {
            'result': 'Error: Degenerate triangle',
            'details': {'a': a, 'b': b, 'angle_C_deg': angle_c_deg, 'error': 'degenerate'},
            'unit': 'triangle'
        }
    A = math.degrees(math.asin(a * math.sin(C) / c))
    B = 180 - A - angle_c_deg
    area = 0.5 * a * b * math.sin(C)
    return {
        'result': f'c = {c:.4f}, A = {A:.4f}°, B = {B:.4f}°; Area = {area:.4f}',
        'details': {'a': a, 'b': b, 'C_deg': angle_c_deg, 'c': c, 'A_deg': A, 'B_deg': B, 'area': area},
        'unit': 'triangle'
    }

def calc_triangle_solver_asa(angle_a_deg: float = 60.0, c: float = 5.0, angle_b_deg: float = 60.0) -> dict:
    """Solve triangle given two angles and included side (ASA)."""
    if angle_a_deg + angle_b_deg >= 180:
        return {
            'result': 'Error: Sum of angles must be less than 180 degrees',
            'details': {'A_deg': angle_a_deg, 'c': c, 'B_deg': angle_b_deg, 'error': 'angle sum >= 180'},
            'unit': 'triangle'
        }
    C = 180 - angle_a_deg - angle_b_deg
    A_rad = math.radians(angle_a_deg)
    B_rad = math.radians(angle_b_deg)
    C_rad = math.radians(C)
    a = c * math.sin(A_rad) / math.sin(C_rad)
    b = c * math.sin(B_rad) / math.sin(C_rad)
    area = 0.5 * a * b * math.sin(C_rad)
    return {
        'result': f'a = {a:.4f}, b = {b:.4f}, C = {C:.4f}°; Area = {area:.4f}',
        'details': {'A_deg': angle_a_deg, 'B_deg': angle_b_deg, 'C_deg': C, 'side_c': c, 'a': a, 'b': b, 'area': area},
        'unit': 'triangle'
    }

def calc_triangle_solver_aas(angle_a_deg: float = 30.0, angle_b_deg: float = 70.0, a: float = 5.0) -> dict:
    """Solve triangle given two angles and non-included side (AAS)."""
    if angle_a_deg + angle_b_deg >= 180:
        return {
            'result': 'Error: Sum of angles must be less than 180 degrees',
            'details': {'A_deg': angle_a_deg, 'B_deg': angle_b_deg, 'a': a, 'error': 'angle sum >= 180'},
            'unit': 'triangle'
        }
    C = 180 - angle_a_deg - angle_b_deg
    A_rad = math.radians(angle_a_deg)
    B_rad = math.radians(angle_b_deg)
    C_rad = math.radians(C)
    b = a * math.sin(B_rad) / math.sin(A_rad)
    c_val = a * math.sin(C_rad) / math.sin(A_rad)
    area = 0.5 * a * b * math.sin(C_rad)
    return {
        'result': f'b = {b:.4f}, c = {c_val:.4f}, C = {C:.4f}°; Area = {area:.4f}',
        'details': {'A_deg': angle_a_deg, 'B_deg': angle_b_deg, 'C_deg': C, 'side_a': a, 'b': b, 'c': c_val, 'area': area},
        'unit': 'triangle'
    }

def calc_circle(radius: float = 5.0) -> dict:
    """Calculate circle area, circumference, diameter."""
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    diameter = 2 * radius
    return {
        'result': f'Area = {area:.6f}, Circumference = {circumference:.6f}, Diameter = {diameter:.6f}',
        'details': {'radius': radius, 'area': area, 'circumference': circumference, 'diameter': diameter},
        'unit': 'circle'
    }

def calc_arc_length(radius: float = 5.0, angle_deg: float = 60.0) -> dict:
    """Calculate arc length s = r*theta."""
    theta = math.radians(angle_deg)
    arc_len = radius * theta
    chord = 2 * radius * math.sin(theta / 2)
    return {
        'result': f'Arc length = {arc_len:.6f}, Chord length = {chord:.6f}',
        'details': {'radius': radius, 'angle_deg': angle_deg, 'angle_rad': theta, 'arc_length': arc_len, 'chord_length': chord},
        'unit': 'length'
    }

def calc_sector(radius: float = 5.0, angle_deg: float = 60.0) -> dict:
    """Calculate sector area = (1/2)*r^2*theta."""
    theta = math.radians(angle_deg)
    area = 0.5 * radius ** 2 * theta
    arc_len = radius * theta
    return {
        'result': f'Sector area = {area:.6f}, Arc length = {arc_len:.6f}',
        'details': {'radius': radius, 'angle_deg': angle_deg, 'angle_rad': theta, 'area': area, 'arc_length': arc_len},
        'unit': 'area'
    }

def calc_polygon_area(n: int = 6, side: float = 5.0) -> dict:
    """Calculate area of a regular n-gon with given side length."""
    if n < 3:
        return {
            'result': 'Error: n must be >= 3 for a polygon',
            'details': {'n': n, 'side': side, 'error': 'n < 3'},
            'unit': 'area'
        }
    area = (n * side ** 2) / (4 * math.tan(math.pi / n))
    perimeter = n * side
    apothem = side / (2 * math.tan(math.pi / n))
    inradius = apothem
    circumradius = side / (2 * math.sin(math.pi / n))
    interior_angle = (n - 2) * 180 / n
    return {
        'result': f'Area = {area:.6f}, Perimeter = {perimeter:.4f}',
        'details': {'n': n, 'side': side, 'area': area, 'perimeter': perimeter, 'apothem': apothem,
                     'inradius': inradius, 'circumradius': circumradius, 'interior_angle_deg': interior_angle},
        'unit': 'area'
    }

def calc_inscribed_circle(sides: list = None) -> dict:
    """Calculate the radius of a circle inscribed in a triangle (incircle). Given three side lengths."""
    if sides is None:
        sides = [3, 4, 5]
    a, b, c = sides
    if a + b <= c or b + c <= a or c + a <= b:
        return {
            'result': 'Error: Triangle inequality violated',
            'details': {'sides': sides, 'error': 'triangle inequality'},
            'unit': 'radius'
        }
    s = (a + b + c) / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    r = area / s
    R = (a * b * c) / (4 * area)
    return {
        'result': f'Inradius r = {r:.6f}, Circumradius R = {R:.6f}',
        'details': {'sides': sides, 'semi_perimeter': s, 'area': area, 'inradius': r, 'circumradius': R},
        'unit': 'radius'
    }

# ==============================================================================
# SOLID GEOMETRY
# ==============================================================================

def calc_cube(side: float = 5.0) -> dict:
    """Calculate volume, surface area, and face diagonal of a cube."""
    volume = side ** 3
    surface = 6 * side ** 2
    diagonal = side * math.sqrt(3)
    face_diag = side * math.sqrt(2)
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}, Diagonal = {diagonal:.6f}',
        'details': {'side': side, 'volume': volume, 'surface_area': surface, 'space_diagonal': diagonal, 'face_diagonal': face_diag},
        'unit': 'solid'
    }

def calc_cuboid(length: float = 3.0, width: float = 4.0, height: float = 5.0) -> dict:
    """Calculate volume, surface area, and diagonal of a cuboid."""
    volume = length * width * height
    surface = 2 * (length * width + width * height + height * length)
    diagonal = math.sqrt(length ** 2 + width ** 2 + height ** 2)
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}, Diagonal = {diagonal:.6f}',
        'details': {'length': length, 'width': width, 'height': height, 'volume': volume, 'surface_area': surface, 'diagonal': diagonal},
        'unit': 'solid'
    }

def calc_prism(base_area: float = 25.0, height: float = 10.0, base_perimeter: float = 20.0) -> dict:
    """Calculate volume and surface area of a prism."""
    volume = base_area * height
    lateral = base_perimeter * height
    surface = lateral + 2 * base_area
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}',
        'details': {'base_area': base_area, 'height': height, 'base_perimeter': base_perimeter, 'volume': volume, 'lateral_area': lateral, 'surface_area': surface},
        'unit': 'solid'
    }

def calc_pyramid(base_area: float = 25.0, height: float = 10.0, slant_height: float = 0.0) -> dict:
    """Calculate volume of a pyramid = (1/3)*base_area*height. Surface if slant_height given."""
    volume = base_area * height / 3
    details = {'base_area': base_area, 'height': height, 'volume': volume}
    if slant_height > 0:
        lateral = 0.5 * math.sqrt(base_area) * 4 * slant_height
        surface = lateral + base_area
        details['lateral_area'] = lateral
        details['surface_area'] = surface
        return {
            'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}',
            'details': details,
            'unit': 'solid'
        }
    return {
        'result': f'Volume = {volume:.6f}',
        'details': details,
        'unit': 'solid'
    }

def calc_cylinder(radius: float = 3.0, height: float = 5.0) -> dict:
    """Calculate volume, lateral surface, and total surface area of a cylinder."""
    volume = math.pi * radius ** 2 * height
    lateral = 2 * math.pi * radius * height
    surface = lateral + 2 * math.pi * radius ** 2
    return {
        'result': f'Volume = {volume:.6f}, Lateral area = {lateral:.6f}, Total surface = {surface:.6f}',
        'details': {'radius': radius, 'height': height, 'volume': volume, 'lateral_area': lateral, 'surface_area': surface},
        'unit': 'solid'
    }

def calc_cone(radius: float = 3.0, height: float = 5.0) -> dict:
    """Calculate volume, slant height, lateral surface, and total surface area of a cone."""
    slant = math.sqrt(radius ** 2 + height ** 2)
    volume = math.pi * radius ** 2 * height / 3
    lateral = math.pi * radius * slant
    surface = lateral + math.pi * radius ** 2
    apex_angle = 2 * math.degrees(math.atan(radius / height))
    return {
        'result': f'Volume = {volume:.6f}, Lateral area = {lateral:.6f}, Total surface = {surface:.6f}',
        'details': {'radius': radius, 'height': height, 'slant_height': slant, 'volume': volume, 'lateral_area': lateral, 'surface_area': surface, 'apex_angle_deg': apex_angle},
        'unit': 'solid'
    }

def calc_sphere(radius: float = 5.0) -> dict:
    """Calculate volume and surface area of a sphere."""
    volume = 4 / 3 * math.pi * radius ** 3
    surface = 4 * math.pi * radius ** 2
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}',
        'details': {'radius': radius, 'volume': volume, 'surface_area': surface},
        'unit': 'solid'
    }

def calc_frustum(r1: float = 3.0, r2: float = 2.0, height: float = 5.0) -> dict:
    """Calculate volume and surface area of a conical frustum."""
    slant = math.sqrt((r1 - r2) ** 2 + height ** 2)
    volume = math.pi * height * (r1 ** 2 + r2 ** 2 + r1 * r2) / 3
    lateral = math.pi * (r1 + r2) * slant
    surface = lateral + math.pi * (r1 ** 2 + r2 ** 2)
    return {
        'result': f'Volume = {volume:.6f}, Lateral area = {lateral:.6f}, Total surface = {surface:.6f}',
        'details': {'r1': r1, 'r2': r2, 'height': height, 'slant_height': slant, 'volume': volume, 'lateral_area': lateral, 'surface_area': surface},
        'unit': 'solid'
    }

def calc_torus(major_radius: float = 5.0, minor_radius: float = 2.0) -> dict:
    """Calculate volume and surface area of a torus."""
    volume = 2 * math.pi ** 2 * major_radius * minor_radius ** 2
    surface = 4 * math.pi ** 2 * major_radius * minor_radius
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}',
        'details': {'major_radius': major_radius, 'minor_radius': minor_radius, 'volume': volume, 'surface_area': surface},
        'unit': 'solid'
    }

def calc_platonic_solid(solid_type: str = 'tetrahedron', edge: float = 1.0) -> dict:
    """Calculate volume and surface area of Platonic solids. Types: tetrahedron, cube, octahedron, dodecahedron, icosahedron."""
    solid = solid_type.lower()
    if solid == 'tetrahedron':
        volume = edge ** 3 / (6 * math.sqrt(2))
        surface = math.sqrt(3) * edge ** 2
        faces, vertices = 4, 4
    elif solid == 'cube':
        volume = edge ** 3
        surface = 6 * edge ** 2
        faces, vertices = 6, 8
    elif solid == 'octahedron':
        volume = math.sqrt(2) * edge ** 3 / 3
        surface = 2 * math.sqrt(3) * edge ** 2
        faces, vertices = 8, 6
    elif solid == 'dodecahedron':
        phi = (1 + math.sqrt(5)) / 2
        volume = (15 + 7 * math.sqrt(5)) * edge ** 3 / 4
        surface = 3 * math.sqrt(25 + 10 * math.sqrt(5)) * edge ** 2
        faces, vertices = 12, 20
    elif solid == 'icosahedron':
        volume = 5 * (3 + math.sqrt(5)) * edge ** 3 / 12
        surface = 5 * math.sqrt(3) * edge ** 2
        faces, vertices = 20, 12
    else:
        return {
            'result': f'Error: Unknown solid "{solid_type}". Supported: tetrahedron, cube, octahedron, dodecahedron, icosahedron',
            'details': {'solid_type': solid_type, 'edge': edge, 'error': 'unknown solid'},
            'unit': 'solid'
        }
    return {
        'result': f'Volume = {volume:.6f}, Surface area = {surface:.6f}',
        'details': {'solid': solid, 'edge': edge, 'volume': volume, 'surface_area': surface, 'faces': faces, 'vertices': vertices},
        'unit': 'solid'
    }

# ==============================================================================
# TRIGONOMETRY
# ==============================================================================

def calc_sin(angle_deg: float = 30.0) -> dict:
    """Calculate sine of an angle in degrees."""
    rad = math.radians(angle_deg)
    val = math.sin(rad)
    return {
        'result': f'sin({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'sin': val},
        'unit': 'dimensionless'
    }

def calc_cos(angle_deg: float = 60.0) -> dict:
    """Calculate cosine of an angle in degrees."""
    rad = math.radians(angle_deg)
    val = math.cos(rad)
    return {
        'result': f'cos({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'cos': val},
        'unit': 'dimensionless'
    }

def calc_tan(angle_deg: float = 45.0) -> dict:
    """Calculate tangent of an angle in degrees."""
    rad = math.radians(angle_deg)
    if abs(math.cos(rad)) < 1e-12:
        return {
            'result': f'tan({angle_deg}°) = undefined (asymptote)',
            'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'tan': 'undefined'},
            'unit': 'dimensionless'
        }
    val = math.tan(rad)
    return {
        'result': f'tan({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'tan': val},
        'unit': 'dimensionless'
    }

def calc_csc(angle_deg: float = 30.0) -> dict:
    """Calculate cosecant of an angle in degrees."""
    rad = math.radians(angle_deg)
    s = math.sin(rad)
    if abs(s) < 1e-12:
        return {
            'result': f'csc({angle_deg}°) = undefined',
            'details': {'angle_deg': angle_deg, 'csc': 'undefined'},
            'unit': 'dimensionless'
        }
    val = 1 / s
    return {
        'result': f'csc({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'csc': val},
        'unit': 'dimensionless'
    }

def calc_sec(angle_deg: float = 60.0) -> dict:
    """Calculate secant of an angle in degrees."""
    rad = math.radians(angle_deg)
    c = math.cos(rad)
    if abs(c) < 1e-12:
        return {
            'result': f'sec({angle_deg}°) = undefined',
            'details': {'angle_deg': angle_deg, 'sec': 'undefined'},
            'unit': 'dimensionless'
        }
    val = 1 / c
    return {
        'result': f'sec({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'sec': val},
        'unit': 'dimensionless'
    }

def calc_cot(angle_deg: float = 45.0) -> dict:
    """Calculate cotangent of an angle in degrees."""
    rad = math.radians(angle_deg)
    t = math.tan(rad)
    if abs(t) < 1e-12:
        return {
            'result': f'cot({angle_deg}°) = undefined',
            'details': {'angle_deg': angle_deg, 'cot': 'undefined'},
            'unit': 'dimensionless'
        }
    val = 1 / t
    return {
        'result': f'cot({angle_deg}°) = {val:.6f}',
        'details': {'angle_deg': angle_deg, 'angle_rad': rad, 'cot': val},
        'unit': 'dimensionless'
    }

def calc_arcsin(value: float = 0.5) -> dict:
    """Calculate arcsin (inverse sine) in both radians and degrees."""
    if abs(value) > 1:
        return {
            'result': f'Error: arcsin({value}) is undefined (|x| > 1)',
            'details': {'value': value, 'error': 'domain error'},
            'unit': 'angle'
        }
    rad = math.asin(value)
    deg = math.degrees(rad)
    return {
        'result': f'arcsin({value}) = {rad:.6f} rad = {deg:.4f}°',
        'details': {'value': value, 'radians': rad, 'degrees': deg},
        'unit': 'angle'
    }

def calc_arccos(value: float = 0.5) -> dict:
    """Calculate arccos (inverse cosine) in both radians and degrees."""
    if abs(value) > 1:
        return {
            'result': f'Error: arccos({value}) is undefined (|x| > 1)',
            'details': {'value': value, 'error': 'domain error'},
            'unit': 'angle'
        }
    rad = math.acos(value)
    deg = math.degrees(rad)
    return {
        'result': f'arccos({value}) = {rad:.6f} rad = {deg:.4f}°',
        'details': {'value': value, 'radians': rad, 'degrees': deg},
        'unit': 'angle'
    }

def calc_arctan(value: float = 1.0) -> dict:
    """Calculate arctan (inverse tangent) in both radians and degrees."""
    rad = math.atan(value)
    deg = math.degrees(rad)
    return {
        'result': f'arctan({value}) = {rad:.6f} rad = {deg:.4f}°',
        'details': {'value': value, 'radians': rad, 'degrees': deg},
        'unit': 'angle'
    }

def calc_angle_convert(value: float = 180.0, from_unit: str = 'deg', to_unit: str = 'rad') -> dict:
    """Convert between degrees and radians."""
    if from_unit == 'deg' and to_unit == 'rad':
        result = math.radians(value)
    elif from_unit == 'rad' and to_unit == 'deg':
        result = math.degrees(value)
    elif from_unit == to_unit:
        result = value
    else:
        return {
            'result': f'Error: Unsupported conversion {from_unit} -> {to_unit}. Use deg or rad.',
            'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported conversion'},
            'unit': 'angle'
        }
    return {
        'result': f'{value} {from_unit} = {result:.6f} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'angle'
    }

def calc_trig_identities(angle_deg: float = 30.0) -> dict:
    """Verify Pythagorean identity sin^2 + cos^2 = 1."""
    rad = math.radians(angle_deg)
    s = math.sin(rad)
    c = math.cos(rad)
    pythag = s ** 2 + c ** 2
    t = math.tan(rad) if abs(c) > 1e-12 else None
    tan_identity = 1 + (t ** 2 if t is not None else 0)
    sec_sq = 1 / (c ** 2) if abs(c) > 1e-12 else None
    return {
        'result': f'sin^2 + cos^2 = {pythag:.10f} (should be 1). 1 + tan^2 = sec^2 = {tan_identity:.8f}' if t else f'sin^2 + cos^2 = {pythag:.10f} (should be 1)',
        'details': {'angle_deg': angle_deg, 'sin^2+cos^2': pythag, '1+tan^2': tan_identity, 'sec^2': sec_sq},
        'unit': 'dimensionless'
    }

def calc_sum_diff_angles(alpha_deg: float = 30.0, beta_deg: float = 45.0) -> dict:
    """Verify sine/cosine sum and difference identities."""
    a = math.radians(alpha_deg)
    b = math.radians(beta_deg)
    sin_sum_lhs = math.sin(a + b)
    sin_sum_rhs = math.sin(a) * math.cos(b) + math.cos(a) * math.sin(b)
    sin_diff_lhs = math.sin(a - b)
    sin_diff_rhs = math.sin(a) * math.cos(b) - math.cos(a) * math.sin(b)
    cos_sum_lhs = math.cos(a + b)
    cos_sum_rhs = math.cos(a) * math.cos(b) - math.sin(a) * math.sin(b)
    cos_diff_lhs = math.cos(a - b)
    cos_diff_rhs = math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b)
    return {
        'result': (
            f'sin({alpha_deg}°+{beta_deg}°) = {sin_sum_lhs:.6f} | RHS = {sin_sum_rhs:.6f}\n'
            f'sin({alpha_deg}°-{beta_deg}°) = {sin_diff_lhs:.6f} | RHS = {sin_diff_rhs:.6f}\n'
            f'cos({alpha_deg}°+{beta_deg}°) = {cos_sum_lhs:.6f} | RHS = {cos_sum_rhs:.6f}\n'
            f'cos({alpha_deg}°-{beta_deg}°) = {cos_diff_lhs:.6f} | RHS = {cos_diff_rhs:.6f}'
        ),
        'details': {
            'alpha_deg': alpha_deg, 'beta_deg': beta_deg,
            'sin_sum': {'lhs': sin_sum_lhs, 'rhs': sin_sum_rhs, 'ok': abs(sin_sum_lhs - sin_sum_rhs) < 1e-10},
            'sin_diff': {'lhs': sin_diff_lhs, 'rhs': sin_diff_rhs, 'ok': abs(sin_diff_lhs - sin_diff_rhs) < 1e-10},
            'cos_sum': {'lhs': cos_sum_lhs, 'rhs': cos_sum_rhs, 'ok': abs(cos_sum_lhs - cos_sum_rhs) < 1e-10},
            'cos_diff': {'lhs': cos_diff_lhs, 'rhs': cos_diff_rhs, 'ok': abs(cos_diff_lhs - cos_diff_rhs) < 1e-10},
        },
        'unit': 'dimensionless'
    }

def calc_double_angle(angle_deg: float = 30.0) -> dict:
    """Verify double-angle identities."""
    a = math.radians(angle_deg)
    sin_2a_lhs = math.sin(2 * a)
    sin_2a_rhs = 2 * math.sin(a) * math.cos(a)
    cos_2a_lhs = math.cos(2 * a)
    cos_2a_rhs1 = math.cos(a) ** 2 - math.sin(a) ** 2
    cos_2a_rhs2 = 2 * math.cos(a) ** 2 - 1
    cos_2a_rhs3 = 1 - 2 * math.sin(a) ** 2
    return {
        'result': (
            f'sin(2*{angle_deg}°) = {sin_2a_lhs:.6f} = 2*sin*cos = {sin_2a_rhs:.6f}\n'
            f'cos(2*{angle_deg}°) = {cos_2a_lhs:.6f} = cos^2-sin^2 = {cos_2a_rhs1:.6f}'
        ),
        'details': {
            'angle_deg': angle_deg,
            'sin_2a': {'lhs': sin_2a_lhs, 'rhs': sin_2a_rhs},
            'cos_2a': {'lhs': cos_2a_lhs, 'rhs1': cos_2a_rhs1, 'rhs2': cos_2a_rhs2, 'rhs3': cos_2a_rhs3}
        },
        'unit': 'dimensionless'
    }

def calc_half_angle(angle_deg: float = 60.0) -> dict:
    """Verify half-angle identities."""
    a = math.radians(angle_deg)
    sin_half = math.sqrt((1 - math.cos(a)) / 2)
    cos_half = math.sqrt((1 + math.cos(a)) / 2)
    tan_half = math.sqrt((1 - math.cos(a)) / (1 + math.cos(a))) if 1 + math.cos(a) > 1e-12 else None
    return {
        'result': (
            f'sin({angle_deg}°/2) = {sin_half:.6f} | cos({angle_deg}°/2) = {cos_half:.6f}\n'
            f'tan({angle_deg}°/2) = {tan_half:.6f}' if tan_half else f'sin({angle_deg}°/2) = {sin_half:.6f} | cos({angle_deg}°/2) = {cos_half:.6f}'
        ),
        'details': {'angle_deg': angle_deg, 'sin_half': sin_half, 'cos_half': cos_half, 'tan_half': tan_half},
        'unit': 'dimensionless'
    }

def calc_product_to_sum_identities(a_deg: float = 30.0, b_deg: float = 45.0) -> dict:
    """Verify product-to-sum identities: sinA*sinB, cosA*cosB, sinA*cosB."""
    a = math.radians(a_deg)
    b = math.radians(b_deg)
    sinAsinB = math.sin(a) * math.sin(b)
    sinAsinB_rhs = 0.5 * (math.cos(a - b) - math.cos(a + b))
    cosAcosB = math.cos(a) * math.cos(b)
    cosAcosB_rhs = 0.5 * (math.cos(a - b) + math.cos(a + b))
    sinAcosB = math.sin(a) * math.cos(b)
    sinAcosB_rhs = 0.5 * (math.sin(a + b) + math.sin(a - b))
    return {
        'result': (
            f'sinA sinB = 0.5[cos(A-B)-cos(A+B)]: {sinAsinB:.6f} = {sinAsinB_rhs:.6f}\n'
            f'cosA cosB = 0.5[cos(A-B)+cos(A+B)]: {cosAcosB:.6f} = {cosAcosB_rhs:.6f}\n'
            f'sinA cosB = 0.5[sin(A+B)+sin(A-B)]: {sinAcosB:.6f} = {sinAcosB_rhs:.6f}'
        ),
        'details': {
            'a_deg': a_deg, 'b_deg': b_deg,
            'sin_sin': {'lhs': sinAsinB, 'rhs': sinAsinB_rhs, 'ok': abs(sinAsinB - sinAsinB_rhs) < 1e-10},
            'cos_cos': {'lhs': cosAcosB, 'rhs': cosAcosB_rhs, 'ok': abs(cosAcosB - cosAcosB_rhs) < 1e-10},
            'sin_cos': {'lhs': sinAcosB, 'rhs': sinAcosB_rhs, 'ok': abs(sinAcosB - sinAcosB_rhs) < 1e-10},
        },
        'unit': 'dimensionless'
    }

def calc_sine_law(a: float = 3.0, A_deg: float = 30.0, b: float = 0.0, B_deg: float = 0.0, c: float = 0.0, C_deg: float = 0.0) -> dict:
    """Solve triangle using Law of Sines: a/sin(A) = b/sin(B) = c/sin(C). Provide 2 known pairs, find the third."""
    pairs = []
    if a > 0 and A_deg > 0:
        pairs.append(('a', a, 'A', A_deg))
        R = a / math.sin(math.radians(A_deg))
    if b > 0 and B_deg > 0:
        pairs.append(('b', b, 'B', B_deg))
        R = b / math.sin(math.radians(B_deg))
    if c > 0 and C_deg > 0:
        pairs.append(('c', c, 'C', C_deg))
        R = c / math.sin(math.radians(C_deg))
    unknowns = {}
    if a == 0 and A_deg > 0:
        unknowns['a'] = R * math.sin(math.radians(A_deg))
    if A_deg == 0 and a > 0:
        unknowns['A_deg'] = math.degrees(math.asin(a / R)) if abs(a / R) <= 1 else None
    if b == 0 and B_deg > 0:
        unknowns['b'] = R * math.sin(math.radians(B_deg))
    if B_deg == 0 and b > 0:
        unknowns['B_deg'] = math.degrees(math.asin(b / R)) if abs(b / R) <= 1 else None
    if c == 0 and C_deg > 0:
        unknowns['c'] = R * math.sin(math.radians(C_deg))
    if C_deg == 0 and c > 0:
        unknowns['C_deg'] = math.degrees(math.asin(c / R)) if abs(c / R) <= 1 else None
    return {
        'result': f'a/sinA = b/sinB = c/sinC = {R:.6f}. Solved: {unknowns}',
        'details': {'given': [[a, A_deg], [b, B_deg], [c, C_deg]], 'R': R, 'unknowns': unknowns},
        'unit': 'dimensionless'
    }

def calc_cosine_law(a: float = 3.0, b: float = 4.0, angle_c_deg: float = 90.0) -> dict:
    """Apply Law of Cosines: c^2 = a^2 + b^2 - 2ab*cos(C). Finds c."""
    C = math.radians(angle_c_deg)
    c_val = math.sqrt(a ** 2 + b ** 2 - 2 * a * b * math.cos(C))
    return {
        'result': f'c^2 = {a}^2 + {b}^2 - 2*{a}*{b}*cos({angle_c_deg}°) => c = {c_val:.6f}',
        'details': {'a': a, 'b': b, 'C_deg': angle_c_deg, 'C_rad': C, 'c': c_val},
        'unit': 'length'
    }

# ==============================================================================
# ANALYTIC GEOMETRY
# ==============================================================================

def calc_point_to_line(x0: float = 1.0, y0: float = 2.0, A: float = 1.0, B: float = -1.0, C: float = 0.0) -> dict:
    """Calculate distance from point (x0, y0) to line Ax + By + C = 0."""
    dist = abs(A * x0 + B * y0 + C) / math.sqrt(A ** 2 + B ** 2)
    return {
        'result': f'Distance = {dist:.6f}',
        'details': {'point': (x0, y0), 'line': f'{A}x+{B}y+{C}=0', 'distance': dist},
        'unit': 'length'
    }

def calc_point_to_plane(x0: float = 1.0, y0: float = 2.0, z0: float = 3.0, A: float = 1.0, B: float = 1.0, C: float = 1.0, D: float = -6.0) -> dict:
    """Calculate distance from point (x0, y0, z0) to plane Ax + By + Cz + D = 0."""
    dist = abs(A * x0 + B * y0 + C * z0 + D) / math.sqrt(A ** 2 + B ** 2 + C ** 2)
    return {
        'result': f'Distance = {dist:.6f}',
        'details': {'point': (x0, y0, z0), 'plane': f'{A}x+{B}y+{C}z+{D}=0', 'distance': dist},
        'unit': 'length'
    }

def calc_circle_from_3_points(x1: float = 0.0, y1: float = 0.0,
                                x2: float = 4.0, y2: float = 0.0,
                                x3: float = 2.0, y3: float = 3.0) -> dict:
    """Find the circle (center, radius) passing through three points."""
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-12:
        return {
            'result': 'Error: Points are collinear - no unique circle',
            'details': {'points': [(x1, y1), (x2, y2), (x3, y3)], 'error': 'collinear'},
            'unit': 'circle'
        }
    ux = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / d
    uy = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / d
    r = math.sqrt((x1 - ux) ** 2 + (y1 - uy) ** 2)
    return {
        'result': f'Center = ({ux:.6f}, {uy:.6f}), Radius = {r:.6f}',
        'details': {'points': [(x1, y1), (x2, y2), (x3, y3)], 'center': (ux, uy), 'radius': r},
        'unit': 'circle'
    }

def calc_line_circle_intersection(m: float = 1.0, b: float = 0.0, cx: float = 0.0, cy: float = 0.0, r: float = 5.0) -> dict:
    """Find intersection(s) of line y = mx + b with circle (x-cx)^2 + (y-cy)^2 = r^2."""
    A = 1 + m ** 2
    B = 2 * (m * (b - cy) - cx)
    C = cx ** 2 + (b - cy) ** 2 - r ** 2
    disc = B ** 2 - 4 * A * C
    if disc < -1e-12:
        return {
            'result': 'No intersection (line misses the circle)',
            'details': {'line': f'y={m}x+{b}', 'circle': f'(x-{cx})^2+(y-{cy})^2={r}^2', 'intersections': 0},
            'unit': 'intersection'
        }
    elif abs(disc) < 1e-12:
        x1 = -B / (2 * A)
        y1 = m * x1 + b
        return {
            'result': f'Tangent at ({x1:.6f}, {y1:.6f})',
            'details': {'line': f'y={m}x+{b}', 'circle': f'(x-{cx})^2+(y-{cy})^2={r}^2', 'intersections': 1, 'points': [(x1, y1)]},
            'unit': 'intersection'
        }
    else:
        sqrt_disc = math.sqrt(disc)
        x1 = (-B + sqrt_disc) / (2 * A)
        x2 = (-B - sqrt_disc) / (2 * A)
        y1 = m * x1 + b
        y2 = m * x2 + b
        return {
            'result': f'Intersections at ({x1:.6f}, {y1:.6f}) and ({x2:.6f}, {y2:.6f})',
            'details': {'line': f'y={m}x+{b}', 'circle': f'(x-{cx})^2+(y-{cy})^2={r}^2', 'intersections': 2, 'points': [(x1, y1), (x2, y2)]},
            'unit': 'intersection'
        }

def calc_circle_circle_intersection(cx1: float = 0.0, cy1: float = 0.0, r1: float = 5.0,
                                     cx2: float = 4.0, cy2: float = 0.0, r2: float = 3.0) -> dict:
    """Find intersection(s) of two circles."""
    d = math.sqrt((cx2 - cx1) ** 2 + (cy2 - cy1) ** 2)
    if d > r1 + r2 + 1e-10:
        return {
            'result': 'No intersection (circles are separate)',
            'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'd': d, 'intersections': 0},
            'unit': 'intersection'
        }
    if d < abs(r1 - r2) - 1e-10:
        return {
            'result': 'No intersection (one circle contains the other)',
            'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'd': d, 'intersections': 0},
            'unit': 'intersection'
        }
    if abs(d) < 1e-12:
        return {
            'result': 'Error: Circles have the same center',
            'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'error': 'concentric'},
            'unit': 'intersection'
        }
    a = (r1 ** 2 - r2 ** 2 + d ** 2) / (2 * d)
    h_sq = r1 ** 2 - a ** 2
    if h_sq < -1e-12:
        return {
            'result': 'No intersection (numerical issue)',
            'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'd': d, 'intersections': 0},
            'unit': 'intersection'
        }
    h = math.sqrt(max(0, h_sq))
    xm = cx1 + a * (cx2 - cx1) / d
    ym = cy1 + a * (cy2 - cy1) / d
    if abs(h) < 1e-10:
        return {
            'result': f'Tangent at ({xm:.6f}, {ym:.6f})',
            'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'd': d, 'intersections': 1, 'points': [(xm, ym)]},
            'unit': 'intersection'
        }
    rx = -(cy2 - cy1) * h / d
    ry = (cx2 - cx1) * h / d
    p1 = (xm + rx, ym + ry)
    p2 = (xm - rx, ym - ry)
    return {
        'result': f'Intersections at ({p1[0]:.6f}, {p1[1]:.6f}) and ({p2[0]:.6f}, {p2[1]:.6f})',
        'details': {'circle1': (cx1, cy1, r1), 'circle2': (cx2, cy2, r2), 'd': d, 'intersections': 2, 'points': [p1, p2]},
        'unit': 'intersection'
    }

# ==============================================================================
# CONIC SECTIONS
# ==============================================================================

def calc_parabola(p: float = 2.0, direction: str = 'up') -> dict:
    """Calculate parabola parameters y^2 = 4px (or x^2 = 4py). p = focal distance."""
    if direction in ('up', 'down'):
        if direction == 'up':
            focus = (0, p)
            directrix = f'y = {-p}'
            eq = f'x^2 = {4 * p}y'
        else:
            focus = (0, -p)
            directrix = f'y = {p}'
            eq = f'x^2 = {-4 * p}y'
    else:
        if direction == 'right':
            focus = (p, 0)
            directrix = f'x = {-p}'
            eq = f'y^2 = {4 * p}x'
        else:
            focus = (-p, 0)
            directrix = f'x = {p}'
            eq = f'y^2 = {-4 * p}x'
    latus_rectum = 4 * abs(p)
    return {
        'result': f'Parabola: {eq}, Focus = ({focus[0]}, {focus[1]}), Directrix = {directrix}, Latus rectum = {latus_rectum}',
        'details': {'p': p, 'direction': direction, 'equation': eq, 'focus': focus, 'directrix': directrix, 'vertex': (0, 0), 'latus_rectum': latus_rectum},
        'unit': 'conic'
    }

def calc_ellipse(a: float = 5.0, b: float = 3.0) -> dict:
    """Calculate ellipse parameters: x^2/a^2 + y^2/b^2 = 1 (a = semi-major axis, b = semi-minor axis)."""
    if a < b:
        a, b = b, a
    c = math.sqrt(a ** 2 - b ** 2)
    e = c / a
    area = math.pi * a * b
    circumference_approx = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    foci = [(-c, 0), (c, 0)]
    return {
        'result': f'Area = {area:.6f}, Foci = {foci}, Eccentricity = {e:.6f}, Circumference ~ {circumference_approx:.6f}',
        'details': {'a': a, 'b': b, 'c': c, 'eccentricity': e, 'area': area, 'foci': foci, 'circumference_approx': circumference_approx},
        'unit': 'conic'
    }

def calc_hyperbola(a: float = 4.0, b: float = 3.0) -> dict:
    """Calculate hyperbola parameters: x^2/a^2 - y^2/b^2 = 1."""
    c = math.sqrt(a ** 2 + b ** 2)
    e = c / a
    foci = [(-c, 0), (c, 0)]
    asymptotes = f'y = +/- ({b}/{a})x = +/- ({b / a:.4f})x'
    vertices = [(-a, 0), (a, 0)]
    return {
        'result': f'Foci = {foci}, Eccentricity = {e:.6f}, Asymptotes: {asymptotes}, Vertices = {vertices}',
        'details': {'a': a, 'b': b, 'c': c, 'eccentricity': e, 'foci': foci, 'asymptote_slope': b / a, 'vertices': vertices},
        'unit': 'conic'
    }

def calc_conic_classifier(A: float = 1.0, B: float = 0.0, C: float = 1.0, D: float = 0.0, E: float = 0.0, F: float = -1.0) -> dict:
    """Classify conic section Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0 using discriminant B^2 - 4AC."""
    discriminant = B ** 2 - 4 * A * C
    if discriminant < -1e-10:
        conic_type = 'Ellipse'
        if A == C and B == 0:
            conic_type += ' (circle)'
    elif abs(discriminant) < 1e-10:
        conic_type = 'Parabola'
    else:
        conic_type = 'Hyperbola'
    det_mat = np.array([[A, B / 2, D / 2], [B / 2, C, E / 2], [D / 2, E / 2, F]])
    det = np.linalg.det(det_mat)
    if abs(det) < 1e-10:
        conic_type += ' (degenerate)'
    return {
        'result': f'Conic: {conic_type}, Discriminant B^2 - 4AC = {discriminant:.6f}',
        'details': {'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'F': F, 'discriminant': discriminant, 'determinant': det, 'type': conic_type},
        'unit': 'classification'
    }

def calc_polar_conic(eccentricity: float = 0.5, d: float = 2.0, theta_deg: float = 60.0) -> dict:
    """Compute radius in polar form of a conic: r = ed / (1 + e*cos(theta))."""
    theta = math.radians(theta_deg)
    denom = 1 + eccentricity * math.cos(theta)
    if abs(denom) < 1e-12:
        return {
            'result': f'Undefined: denominator is zero at theta = {theta_deg}°',
            'details': {'e': eccentricity, 'd': d, 'theta_deg': theta_deg, 'error': 'division by zero'},
            'unit': 'polar'
        }
    r = eccentricity * d / denom
    if eccentricity < 1:
        ctype = 'ellipse'
    elif abs(eccentricity - 1) < 1e-10:
        ctype = 'parabola'
    else:
        ctype = 'hyperbola'
    return {
        'result': f'r({theta_deg}°) = {r:.6f} (conic type: {ctype})',
        'details': {'eccentricity': eccentricity, 'd': d, 'theta_deg': theta_deg, 'theta_rad': theta, 'r': r, 'conic_type': ctype},
        'unit': 'polar'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    # Plane geometry
    'distance_points': {'func': calc_distance_points, 'params': ['x1', 'y1', 'x2', 'y2'], 'desc': 'Distance between two points in 2D'},
    'midpoint': {'func': calc_midpoint, 'params': ['x1', 'y1', 'x2', 'y2'], 'desc': 'Midpoint between two points'},
    'line_slope_intercept': {'func': calc_line_slope_intercept, 'params': ['m', 'b'], 'desc': 'Line in slope-intercept form y=mx+b'},
    'line_point_slope': {'func': calc_line_point_slope, 'params': ['x0', 'y0', 'm'], 'desc': 'Line in point-slope form'},
    'line_general': {'func': calc_line_general, 'params': ['A', 'B', 'C'], 'desc': 'Line in general form Ax+By+C=0'},
    'angle_between_lines': {'func': calc_angle_between_lines, 'params': ['m1', 'm2'], 'desc': 'Angle between two lines given slopes'},
    'triangle_area_heron': {'func': calc_triangle_area_heron, 'params': ['a', 'b', 'c'], 'desc': 'Triangle area by Heron formula'},
    'triangle_area_sas': {'func': calc_triangle_area_sas, 'params': ['a', 'b', 'angle_c_deg'], 'desc': 'Triangle area (1/2)ab sin(C)'},
    'triangle_area_base_height': {'func': calc_triangle_area_base_height, 'params': ['base', 'height'], 'desc': 'Triangle area (1/2)bh'},
    'triangle_solver_sss': {'func': calc_triangle_solver_sss, 'params': ['a', 'b', 'c'], 'desc': 'Solve triangle given three sides'},
    'triangle_solver_sas': {'func': calc_triangle_solver_sas, 'params': ['a', 'b', 'angle_c_deg'], 'desc': 'Solve triangle given two sides and included angle'},
    'triangle_solver_asa': {'func': calc_triangle_solver_asa, 'params': ['angle_a_deg', 'c', 'angle_b_deg'], 'desc': 'Solve triangle given two angles and included side'},
    'triangle_solver_aas': {'func': calc_triangle_solver_aas, 'params': ['angle_a_deg', 'angle_b_deg', 'a'], 'desc': 'Solve triangle given two angles and non-included side'},
    'circle': {'func': calc_circle, 'params': ['radius'], 'desc': 'Circle area, circumference, diameter'},
    'arc_length': {'func': calc_arc_length, 'params': ['radius', 'angle_deg'], 'desc': 'Arc length and chord length'},
    'sector': {'func': calc_sector, 'params': ['radius', 'angle_deg'], 'desc': 'Sector area and arc length'},
    'polygon_area': {'func': calc_polygon_area, 'params': ['n', 'side'], 'desc': 'Area of regular n-gon'},
    'inscribed_circle': {'func': calc_inscribed_circle, 'params': ['sides'], 'desc': 'Incircle/circumcircle of triangle'},
    # Solid geometry
    'cube': {'func': calc_cube, 'params': ['side'], 'desc': 'Cube volume, surface, diagonal'},
    'cuboid': {'func': calc_cuboid, 'params': ['length', 'width', 'height'], 'desc': 'Cuboid volume, surface, diagonal'},
    'prism': {'func': calc_prism, 'params': ['base_area', 'height', 'base_perimeter'], 'desc': 'Prism volume and surface'},
    'pyramid': {'func': calc_pyramid, 'params': ['base_area', 'height', 'slant_height'], 'desc': 'Pyramid volume'},
    'cylinder': {'func': calc_cylinder, 'params': ['radius', 'height'], 'desc': 'Cylinder volume and surface'},
    'cone': {'func': calc_cone, 'params': ['radius', 'height'], 'desc': 'Cone volume and surface'},
    'sphere': {'func': calc_sphere, 'params': ['radius'], 'desc': 'Sphere volume and surface'},
    'frustum': {'func': calc_frustum, 'params': ['r1', 'r2', 'height'], 'desc': 'Conical frustum volume and surface'},
    'torus': {'func': calc_torus, 'params': ['major_radius', 'minor_radius'], 'desc': 'Torus volume and surface'},
    'platonic_solid': {'func': calc_platonic_solid, 'params': ['solid_type', 'edge'], 'desc': 'Platonic solid volume and surface'},
    # Trigonometry
    'sin': {'func': calc_sin, 'params': ['angle_deg'], 'desc': 'Sine of an angle'},
    'cos': {'func': calc_cos, 'params': ['angle_deg'], 'desc': 'Cosine of an angle'},
    'tan': {'func': calc_tan, 'params': ['angle_deg'], 'desc': 'Tangent of an angle'},
    'csc': {'func': calc_csc, 'params': ['angle_deg'], 'desc': 'Cosecant of an angle'},
    'sec': {'func': calc_sec, 'params': ['angle_deg'], 'desc': 'Secant of an angle'},
    'cot': {'func': calc_cot, 'params': ['angle_deg'], 'desc': 'Cotangent of an angle'},
    'arcsin': {'func': calc_arcsin, 'params': ['value'], 'desc': 'Arcsin (inverse sine)'},
    'arccos': {'func': calc_arccos, 'params': ['value'], 'desc': 'Arccos (inverse cosine)'},
    'arctan': {'func': calc_arctan, 'params': ['value'], 'desc': 'Arctan (inverse tangent)'},
    'angle_convert': {'func': calc_angle_convert, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert deg/rad'},
    'trig_identities': {'func': calc_trig_identities, 'params': ['angle_deg'], 'desc': 'Verify Pythagorean identity'},
    'sum_diff_angles': {'func': calc_sum_diff_angles, 'params': ['alpha_deg', 'beta_deg'], 'desc': 'Verify sin/cos sum/diff identities'},
    'double_angle': {'func': calc_double_angle, 'params': ['angle_deg'], 'desc': 'Verify double-angle identities'},
    'half_angle': {'func': calc_half_angle, 'params': ['angle_deg'], 'desc': 'Verify half-angle identities'},
    'product_to_sum_identities': {'func': calc_product_to_sum_identities, 'params': ['a_deg', 'b_deg'], 'desc': 'Verify product-to-sum identities'},
    'sine_law': {'func': calc_sine_law, 'params': ['a', 'A_deg', 'b', 'B_deg', 'c', 'C_deg'], 'desc': 'Law of Sines'},
    'cosine_law': {'func': calc_cosine_law, 'params': ['a', 'b', 'angle_c_deg'], 'desc': 'Law of Cosines'},
    # Analytic geometry
    'point_to_line': {'func': calc_point_to_line, 'params': ['x0', 'y0', 'A', 'B', 'C'], 'desc': 'Distance from point to line'},
    'point_to_plane': {'func': calc_point_to_plane, 'params': ['x0', 'y0', 'z0', 'A', 'B', 'C', 'D'], 'desc': 'Distance from point to plane'},
    'circle_from_3_points': {'func': calc_circle_from_3_points, 'params': ['x1', 'y1', 'x2', 'y2', 'x3', 'y3'], 'desc': 'Circle through 3 points'},
    'line_circle_intersection': {'func': calc_line_circle_intersection, 'params': ['m', 'b', 'cx', 'cy', 'r'], 'desc': 'Line-circle intersection'},
    'circle_circle_intersection': {'func': calc_circle_circle_intersection, 'params': ['cx1', 'cy1', 'r1', 'cx2', 'cy2', 'r2'], 'desc': 'Circle-circle intersection'},
    # Conic sections
    'parabola': {'func': calc_parabola, 'params': ['p', 'direction'], 'desc': 'Parabola focus, directrix, vertex'},
    'ellipse': {'func': calc_ellipse, 'params': ['a', 'b'], 'desc': 'Ellipse foci, axis, eccentricity, area'},
    'hyperbola': {'func': calc_hyperbola, 'params': ['a', 'b'], 'desc': 'Hyperbola foci, asymptotes, eccentricity'},
    'conic_classifier': {'func': calc_conic_classifier, 'params': ['A', 'B', 'C', 'D', 'E', 'F'], 'desc': 'Classify general conic'},
    'polar_conic': {'func': calc_polar_conic, 'params': ['eccentricity', 'd', 'theta_deg'], 'desc': 'Polar form of conics'},
}
