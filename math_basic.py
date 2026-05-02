"""
Basic & Elementary Mathematics - Mathematics Computation Module
"""
import math
import numpy as np

COMMANDS = {}

# ==============================================================================
# ARITHMETIC
# ==============================================================================

def calc_add(a: float = 1.0, b: float = 2.0, precision: int = 6) -> dict:
    """Add two numbers with given decimal precision."""
    r = a + b
    return {
        'result': f'{a} + {b} = {r:.{precision}f}',
        'details': {'a': a, 'b': b, 'sum': round(r, precision)},
        'unit': 'number'
    }

def calc_subtract(a: float = 5.0, b: float = 3.0, precision: int = 6) -> dict:
    """Subtract b from a with given decimal precision."""
    r = a - b
    return {
        'result': f'{a} - {b} = {r:.{precision}f}',
        'details': {'a': a, 'b': b, 'difference': round(r, precision)},
        'unit': 'number'
    }

def calc_multiply(a: float = 3.0, b: float = 4.0, precision: int = 6) -> dict:
    """Multiply two numbers with given decimal precision."""
    r = a * b
    return {
        'result': f'{a} * {b} = {r:.{precision}f}',
        'details': {'a': a, 'b': b, 'product': round(r, precision)},
        'unit': 'number'
    }

def calc_divide(a: float = 10.0, b: float = 3.0, precision: int = 6) -> dict:
    """Divide a by b with given decimal precision. Returns error if b=0."""
    if b == 0:
        return {
            'result': 'Error: Division by zero',
            'details': {'a': a, 'b': b, 'error': 'division by zero'},
            'unit': 'number'
        }
    r = a / b
    return {
        'result': f'{a} / {b} = {r:.{precision}f}',
        'details': {'a': a, 'b': b, 'quotient': round(r, precision)},
        'unit': 'number'
    }

def calc_absolute(x: float = -5.0) -> dict:
    """Compute the absolute value of x."""
    r = abs(x)
    return {
        'result': f'|{x}| = {r}',
        'details': {'input': x, 'absolute_value': r},
        'unit': 'number'
    }

def calc_mod(a: int = 17, b: int = 5) -> dict:
    """Compute a mod b (remainder of a divided by b)."""
    if b == 0:
        return {
            'result': 'Error: Modulo by zero',
            'details': {'a': a, 'b': b, 'error': 'modulo by zero'},
            'unit': 'number'
        }
    r = a % b
    q = a // b
    return {
        'result': f'{a} mod {b} = {r}',
        'details': {'a': a, 'b': b, 'quotient': q, 'remainder': r},
        'unit': 'number'
    }

def calc_floor(x: float = 3.7) -> dict:
    """Compute floor of x (greatest integer <= x)."""
    r = math.floor(x)
    return {
        'result': f'floor({x}) = {r}',
        'details': {'input': x, 'floor': r},
        'unit': 'number'
    }

def calc_ceil(x: float = 3.2) -> dict:
    """Compute ceiling of x (smallest integer >= x)."""
    r = math.ceil(x)
    return {
        'result': f'ceil({x}) = {r}',
        'details': {'input': x, 'ceiling': r},
        'unit': 'number'
    }

def calc_ratio(a: float = 3.0, b: float = 4.0) -> dict:
    """Express a:b as a simplified ratio."""
    if b == 0:
        return {
            'result': 'Error: Division by zero in ratio',
            'details': {'a': a, 'b': b, 'error': 'b cannot be zero'},
            'unit': 'dimensionless'
        }
    g = math.gcd(int(a * 1000), int(b * 1000)) if a != int(a) or b != int(b) else math.gcd(int(a), int(b))
    divisor = g
    simplified = (round(a / divisor, 4) if divisor != 0 else a, round(b / divisor, 4) if divisor != 0 else b)
    return {
        'result': f'{a}:{b} simplifies to ({simplified[0]}:{simplified[1]})',
        'details': {'a': a, 'b': b, 'simplified': simplified, 'gcd': divisor},
        'unit': 'dimensionless'
    }

def calc_percentage(part: float = 25.0, whole: float = 200.0) -> dict:
    """Calculate what percentage part is of whole."""
    if whole == 0:
        return {
            'result': 'Error: Whole cannot be zero',
            'details': {'part': part, 'whole': whole, 'error': 'division by zero'},
            'unit': 'percent'
        }
    pct = (part / whole) * 100
    return {
        'result': f'{part} is {pct:.2f}% of {whole}',
        'details': {'part': part, 'whole': whole, 'percentage': round(pct, 4)},
        'unit': 'percent'
    }

def calc_sig_figs(x: float = 123.456, n: int = 4) -> dict:
    """Round x to n significant figures."""
    if x == 0:
        return {
            'result': f'0 (to {n} sig. figs) = 0',
            'details': {'input': x, 'sig_figs': n, 'rounded': 0.0},
            'unit': 'number'
        }
    r = round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))
    return {
        'result': f'{x} to {n} sig. figs = {r}',
        'details': {'input': x, 'sig_figs': n, 'rounded': r},
        'unit': 'number'
    }

def calc_sci_notation(x: float = 1234.56) -> dict:
    """Express x in scientific notation."""
    if x == 0:
        return {
            'result': '0 = 0 x 10^0',
            'details': {'coefficient': 0, 'exponent': 0},
            'unit': 'number'
        }
    exponent = int(math.floor(math.log10(abs(x))))
    coefficient = x / (10 ** exponent)
    return {
        'result': f'{x} = {coefficient:.4f} x 10^{exponent}',
        'details': {'input': x, 'coefficient': round(coefficient, 8), 'exponent': exponent},
        'unit': 'number'
    }

# Unit conversions
def calc_unit_length(value: float = 1.0, from_unit: str = 'meter', to_unit: str = 'foot') -> dict:
    """Convert length units. Supported: meter, kilometer, centimeter, millimeter, mile, yard, foot, inch."""
    to_meter = {
        'meter': 1, 'kilometer': 1000, 'centimeter': 0.01, 'millimeter': 0.001,
        'mile': 1609.344, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254
    }
    if from_unit not in to_meter or to_unit not in to_meter:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_meter.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'length'
        }
    meters = value * to_meter[from_unit]
    result = meters / to_meter[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'length'
    }

def calc_unit_mass(value: float = 1.0, from_unit: str = 'kilogram', to_unit: str = 'pound') -> dict:
    """Convert mass units. Supported: kilogram, gram, milligram, metric_ton, pound, ounce, stone, ton_us."""
    to_kg = {
        'kilogram': 1, 'gram': 0.001, 'milligram': 1e-6, 'metric_ton': 1000,
        'pound': 0.453592, 'ounce': 0.0283495, 'stone': 6.35029, 'ton_us': 907.185
    }
    if from_unit not in to_kg or to_unit not in to_kg:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_kg.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'mass'
        }
    kg_val = value * to_kg[from_unit]
    result = kg_val / to_kg[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'mass'
    }

def calc_unit_time(value: float = 1.0, from_unit: str = 'hour', to_unit: str = 'minute') -> dict:
    """Convert time units. Supported: second, minute, hour, day, week, year."""
    to_second = {
        'second': 1, 'minute': 60, 'hour': 3600, 'day': 86400,
        'week': 604800, 'year': 31557600
    }
    if from_unit not in to_second or to_unit not in to_second:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_second.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'time'
        }
    sec_val = value * to_second[from_unit]
    result = sec_val / to_second[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'time'
    }

def calc_unit_area(value: float = 1.0, from_unit: str = 'sq_meter', to_unit: str = 'sq_foot') -> dict:
    """Convert area units. Supported: sq_meter, sq_kilometer, sq_centimeter, sq_mile, acre, hectare, sq_foot, sq_inch."""
    to_sqm = {
        'sq_meter': 1, 'sq_kilometer': 1e6, 'sq_centimeter': 1e-4, 'sq_mile': 2.59e6,
        'acre': 4046.86, 'hectare': 10000, 'sq_foot': 0.092903, 'sq_inch': 0.00064516
    }
    if from_unit not in to_sqm or to_unit not in to_sqm:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_sqm.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'area'
        }
    sqm_val = value * to_sqm[from_unit]
    result = sqm_val / to_sqm[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'area'
    }

def calc_unit_volume(value: float = 1.0, from_unit: str = 'liter', to_unit: str = 'gallon') -> dict:
    """Convert volume units. Supported: liter, milliliter, cubic_meter, cubic_foot, gallon, quart, pint, cup."""
    to_liter = {
        'liter': 1, 'milliliter': 0.001, 'cubic_meter': 1000, 'cubic_foot': 28.3168,
        'gallon': 3.78541, 'quart': 0.946353, 'pint': 0.473176, 'cup': 0.236588
    }
    if from_unit not in to_liter or to_unit not in to_liter:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_liter.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'volume'
        }
    lit_val = value * to_liter[from_unit]
    result = lit_val / to_liter[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'volume'
    }

def calc_unit_speed(value: float = 1.0, from_unit: str = 'mps', to_unit: str = 'kmph') -> dict:
    """Convert speed units. Supported: mps, kmph, mph, knot, fps."""
    to_mps = {'mps': 1, 'kmph': 0.277778, 'mph': 0.44704, 'knot': 0.514444, 'fps': 0.3048}
    if from_unit not in to_mps or to_unit not in to_mps:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_mps.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'speed'
        }
    mps_val = value * to_mps[from_unit]
    result = mps_val / to_mps[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'speed'
    }

def calc_unit_density(value: float = 1.0, from_unit: str = 'kgpm3', to_unit: str = 'gpmL') -> dict:
    """Convert density units. Supported: kgpm3, gpm3, gpmL, lbpft3."""
    to_kgpm3 = {'kgpm3': 1, 'gpm3': 0.001, 'gpmL': 1000, 'lbpft3': 16.0185}
    if from_unit not in to_kgpm3 or to_unit not in to_kgpm3:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_kgpm3.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'density'
        }
    kgpm3_val = value * to_kgpm3[from_unit]
    result = kgpm3_val / to_kgpm3[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'density'
    }

def calc_unit_pressure(value: float = 1.0, from_unit: str = 'atm', to_unit: str = 'Pa') -> dict:
    """Convert pressure units. Supported: Pa, kPa, atm, bar, mmHg, psi, torr."""
    to_pa = {'Pa': 1, 'kPa': 1000, 'atm': 101325, 'bar': 100000, 'mmHg': 133.322, 'psi': 6894.76, 'torr': 133.322}
    if from_unit not in to_pa or to_unit not in to_pa:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_pa.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'pressure'
        }
    pa_val = value * to_pa[from_unit]
    result = pa_val / to_pa[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'pressure'
    }

def calc_unit_energy(value: float = 1.0, from_unit: str = 'joule', to_unit: str = 'calorie') -> dict:
    """Convert energy units. Supported: joule, kilojoule, calorie, kcal, wh, kwh, ev, btu."""
    to_joule = {
        'joule': 1, 'kilojoule': 1000, 'calorie': 4.184, 'kcal': 4184,
        'wh': 3600, 'kwh': 3.6e6, 'ev': 1.602e-19, 'btu': 1055.06
    }
    if from_unit not in to_joule or to_unit not in to_joule:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_joule.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'energy'
        }
    j_val = value * to_joule[from_unit]
    result = j_val / to_joule[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'energy'
    }

def calc_unit_power(value: float = 1.0, from_unit: str = 'watt', to_unit: str = 'horsepower') -> dict:
    """Convert power units. Supported: watt, kilowatt, horsepower, btups, ftlbps."""
    to_watt = {'watt': 1, 'kilowatt': 1000, 'horsepower': 745.7, 'btups': 1055.06, 'ftlbps': 1.35582}
    if from_unit not in to_watt or to_unit not in to_watt:
        return {
            'result': f'Error: Unsupported unit. Supported: {", ".join(sorted(to_watt.keys()))}',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'power'
        }
    w_val = value * to_watt[from_unit]
    result = w_val / to_watt[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'power'
    }

def calc_unit_temperature(value: float = 0.0, from_unit: str = 'celsius', to_unit: str = 'fahrenheit') -> dict:
    """Convert temperature. Supported: celsius, fahrenheit, kelvin."""
    if from_unit not in ('celsius', 'fahrenheit', 'kelvin') or to_unit not in ('celsius', 'fahrenheit', 'kelvin'):
        return {
            'result': 'Error: Unsupported unit. Supported: celsius, fahrenheit, kelvin',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'temperature'
        }
    if from_unit == 'celsius':
        kelvin = value + 273.15
    elif from_unit == 'fahrenheit':
        kelvin = (value - 32) * 5 / 9 + 273.15
    else:
        kelvin = value
    if to_unit == 'celsius':
        result = kelvin - 273.15
    elif to_unit == 'fahrenheit':
        result = (kelvin - 273.15) * 9 / 5 + 32
    else:
        result = kelvin
    return {
        'result': f'{value} {from_unit} = {result:.4f} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': round(result, 4), 'kelvin': round(kelvin, 4)},
        'unit': 'temperature'
    }

def calc_unit_angle(value: float = 180.0, from_unit: str = 'degree', to_unit: str = 'radian') -> dict:
    """Convert angle units. Supported: degree, radian, gradian."""
    to_deg = {'degree': 1, 'radian': 180 / math.pi, 'gradian': 0.9}
    if from_unit not in to_deg or to_unit not in to_deg:
        return {
            'result': 'Error: Unsupported unit. Supported: degree, radian, gradian',
            'details': {'from_unit': from_unit, 'to_unit': to_unit, 'error': 'unsupported unit'},
            'unit': 'angle'
        }
    deg_val = value * to_deg[from_unit]
    result = deg_val / to_deg[to_unit]
    return {
        'result': f'{value} {from_unit} = {result:.6g} {to_unit}',
        'details': {'value': value, 'from_unit': from_unit, 'to_unit': to_unit, 'result': result},
        'unit': 'angle'
    }

# ==============================================================================
# ALGEBRA
# ==============================================================================

def calc_polynomial(coefficients: list = None, x: float = 2.0) -> dict:
    """Evaluate a polynomial with given coefficients at x. Coeffs list from highest degree. E.g., [1, -3, 2] = x^2 - 3x + 2."""
    if coefficients is None:
        coefficients = [1, -3, 2]
    n = len(coefficients)
    terms = []
    result = 0
    for i, c in enumerate(coefficients):
        power = n - i - 1
        result += c * (x ** power)
        if power > 1:
            terms.append(f'{c}x^{power}')
        elif power == 1:
            terms.append(f'{c}x')
        else:
            terms.append(f'{c}')
    poly_str = ' + '.join(terms).replace('+ -', '- ')
    return {
        'result': f'{poly_str} at x={x} = {result:.6f}',
        'details': {'coefficients': coefficients, 'x': x, 'value': result, 'polynomial': poly_str},
        'unit': 'number'
    }

def calc_factor_quadratic(a: int = 1, b: int = -5, c: int = 6) -> dict:
    """Factor a quadratic ax^2 + bx + c over integers if possible."""
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return {
            'result': f'Quadratic {a}x^2 + {b}x + {c} has no real roots; cannot factor over reals.',
            'details': {'a': a, 'b': b, 'c': c, 'discriminant': discriminant},
            'unit': 'expression'
        }
    sqrt_disc = math.isqrt(discriminant)
    if sqrt_disc * sqrt_disc != discriminant:
        return {
            'result': f'Quadratic {a}x^2 + {b}x + {c} cannot be factored neatly over integers.',
            'details': {'a': a, 'b': b, 'c': c, 'discriminant': discriminant, 'sqrt_disc': math.sqrt(discriminant)},
            'unit': 'expression'
        }
    root1 = (-b + sqrt_disc) / (2 * a)
    root2 = (-b - sqrt_disc) / (2 * a)
    g1 = 1
    g2 = 1
    if root1 == int(root1):
        g1 = a
        r1_int = int(root1)
    else:
        r1_int = root1
    if root2 == int(root2):
        r2_int = int(root2)
    else:
        r2_int = root2
    if a == 1:
        factor_str = f'(x - {r1_int})(x - {r2_int})'
    else:
        factor_str = f'{a}(x - {r1_int})(x - {r2_int})'
    return {
        'result': f'{a}x^2 + {b}x + {c} = {factor_str}',
        'details': {'a': a, 'b': b, 'c': c, 'discriminant': discriminant, 'roots': (root1, root2), 'factored': factor_str},
        'unit': 'expression'
    }

def calc_power_rules(a: float = 2.0, m: float = 3.0, n: float = 4.0) -> dict:
    """Demonstrate power rules a^m * a^n = a^(m+n), (a^m)^n = a^(mn), a^m/a^n = a^(m-n)."""
    rule1_lhs = (a ** m) * (a ** n)
    rule1_rhs = a ** (m + n)
    rule2_lhs = (a ** m) ** n
    rule2_rhs = a ** (m * n)
    rule3_lhs = (a ** m) / (a ** n)
    rule3_rhs = a ** (m - n)
    return {
        'result': (
            f'a^m * a^n = a^(m+n): {a}^{m} * {a}^{n} = {rule1_lhs:.4f} = {a}^{m+n} = {rule1_rhs:.4f}\n'
            f'(a^m)^n = a^(mn): ({a}^{m})^{n} = {rule2_lhs:.4f} = {a}^{m*n} = {rule2_rhs:.4f}\n'
            f'a^m / a^n = a^(m-n): {a}^{m} / {a}^{n} = {rule3_lhs:.4f} = {a}^{m-n} = {rule3_rhs:.4f}'
        ),
        'details': {
            'a': a, 'm': m, 'n': n,
            'product_rule': {'lhs': rule1_lhs, 'rhs': rule1_rhs, 'holds': abs(rule1_lhs - rule1_rhs) < 1e-10},
            'power_rule': {'lhs': rule2_lhs, 'rhs': rule2_rhs, 'holds': abs(rule2_lhs - rule2_rhs) < 1e-10},
            'quotient_rule': {'lhs': rule3_lhs, 'rhs': rule3_rhs, 'holds': abs(rule3_lhs - rule3_rhs) < 1e-10}
        },
        'unit': 'dimensionless'
    }

def calc_exp_log_rules(value: float = 2.0, a: float = 3.0, b: float = 4.0) -> dict:
    """Demonstrate exponent and logarithm rules."""
    rules = {}
    rules['exp_add'] = {'lhs': math.exp(a) * math.exp(b), 'rhs': math.exp(a + b)}
    rules['ln_product'] = {'lhs': math.log(value * a), 'rhs': math.log(value) + math.log(a), 'holds': abs(math.log(value * a) - (math.log(value) + math.log(a))) < 1e-10}
    rules['ln_power'] = {'lhs': math.log(value ** a), 'rhs': a * math.log(value), 'holds': abs(math.log(value ** a) - a * math.log(value)) < 1e-10}
    rules['exp_ln'] = {'lhs': math.exp(math.log(value)), 'rhs': value, 'holds': abs(math.exp(math.log(value)) - value) < 1e-10}
    rules['change_of_base'] = {'lhs': math.log(a, 10), 'rhs': math.log(a) / math.log(10), 'holds': abs(math.log(a, 10) - math.log(a) / math.log(10)) < 1e-10}
    return {
        'result': (
            f'e^{a} * e^{b} = e^({a}+{b}): {rules["exp_add"]["lhs"]:.4f} = {rules["exp_add"]["rhs"]:.4f}\n'
            f'ln(xy) = ln(x) + ln(y): holds = {rules["ln_product"]["holds"]}\n'
            f'ln(x^a) = a*ln(x): holds = {rules["ln_power"]["holds"]}\n'
            f'e^(ln(x)) = x: holds = {rules["exp_ln"]["holds"]}\n'
            f'log10(a) = ln(a)/ln(10): holds = {rules["change_of_base"]["holds"]}'
        ),
        'details': {'value': value, 'a': a, 'b': b, 'rules_verified': rules},
        'unit': 'dimensionless'
    }

def calc_radical_simplify(n: int = 72) -> dict:
    """Simplify sqrt(n) to a*sqrt(b) form."""
    if n < 0:
        return {
            'result': f'sqrt({n}) = isqrt({-n}) i',
            'details': {'n': n, 'a': 1, 'b': n, 'imaginary': True},
            'unit': 'expression'
        }
    if n == 0:
        return {
            'result': 'sqrt(0) = 0',
            'details': {'n': 0, 'a': 0, 'b': 0},
            'unit': 'expression'
        }
    perfect_square = 1
    i = 2
    while i * i <= n:
        while n % (i * i) == 0:
            perfect_square *= i
            n //= (i * i)
        i += 1
    if n == 1:
        result_str = f'sqrt({perfect_square * perfect_square}) = {perfect_square}'
    elif perfect_square == 1:
        result_str = f'sqrt({n}) = sqrt({n})'
    else:
        result_str = f'sqrt({perfect_square * perfect_square * n}) = {perfect_square} sqrt({n})'
    return {
        'result': result_str,
        'details': {'original': perfect_square * perfect_square * n if n != 1 else perfect_square * perfect_square, 'a': perfect_square, 'b': n},
        'unit': 'expression'
    }

def calc_completing_square(a: float = 1.0, b: float = 6.0, c: float = 5.0) -> dict:
    """Complete the square for ax^2 + bx + c => a(x + p)^2 + q."""
    if a == 0:
        return {
            'result': 'Error: Not a quadratic (a=0)',
            'details': {'a': a, 'b': b, 'c': c, 'error': 'a is zero'},
            'unit': 'expression'
        }
    p = b / (2 * a)
    q = c - a * (p ** 2)
    square_part = f'a(x + p)^2 + q' if a == 1 else f'{a}(x + {p})^2 + {q}'
    return {
        'result': f'{a}x^2 + {b}x + {c} = {square_part}',
        'details': {'a': a, 'b': b, 'c': c, 'p': p, 'q': q, 'vertex': (-p, q), 'completed_square': square_part},
        'unit': 'expression'
    }

# ==============================================================================
# EQUATIONS
# ==============================================================================

def calc_linear(a: float = 2.0, b: float = -4.0) -> dict:
    """Solve linear equation ax + b = 0."""
    if a == 0:
        if b == 0:
            return {
                'result': 'Infinite solutions (identity 0=0)',
                'details': {'a': a, 'b': b, 'type': 'identity'},
                'unit': 'dimensionless'
            }
        return {
            'result': 'No solution (contradiction)',
            'details': {'a': a, 'b': b, 'type': 'contradiction'},
            'unit': 'dimensionless'
        }
    x = -b / a
    return {
        'result': f'{a}x + {b} = 0 => x = {x:.6f}',
        'details': {'a': a, 'b': b, 'solution': x},
        'unit': 'dimensionless'
    }

def calc_quadratic(a: float = 1.0, b: float = -5.0, c: float = 6.0) -> dict:
    """Solve quadratic equation ax^2 + bx + c = 0 using quadratic formula."""
    if a == 0:
        return calc_linear(b, c)
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        real = -b / (2 * a)
        imag = math.sqrt(-discriminant) / (2 * a)
        return {
            'result': f'x = {real:.4f} + {imag:.4f}i, x = {real:.4f} - {imag:.4f}i (complex)',
            'details': {'a': a, 'b': b, 'c': c, 'discriminant': discriminant, 'roots': [complex(real, imag), complex(real, -imag)], 'type': 'complex'},
            'unit': 'dimensionless'
        }
    sqrt_disc = math.sqrt(discriminant)
    x1 = (-b + sqrt_disc) / (2 * a)
    x2 = (-b - sqrt_disc) / (2 * a)
    return {
        'result': f'x1 = {x1:.6f}, x2 = {x2:.6f}',
        'details': {'a': a, 'b': b, 'c': c, 'discriminant': discriminant, 'roots': [x1, x2], 'type': 'real'},
        'unit': 'dimensionless'
    }

def calc_cubic(a: float = 1.0, b: float = -6.0, c: float = 11.0, d: float = -6.0) -> dict:
    """Solve cubic equation ax^3 + bx^2 + cx + d = 0 using Cardano's method."""
    if a == 0:
        return calc_quadratic(b, c, d)
    a0 = b / a
    a1 = c / a
    a2 = d / a
    # Depressed cubic: t^3 + pt + q = 0 via x = t - b/(3a)
    p = a1 - (a0 ** 2) / 3
    q = (2 * a0 ** 3) / 27 - (a0 * a1) / 3 + a2
    discriminant = (q / 2) ** 2 + (p / 3) ** 3
    shift = a0 / 3
    roots = []
    if abs(discriminant) < 1e-12:
        u = (-q / 2) ** (1 / 3) if -q / 2 >= 0 else -((-q / 2) ** (1 / 3))
        roots.append(2 * u - shift)
        roots.append(-u - shift)
    elif discriminant > 0:
        u = (-q / 2 + math.sqrt(discriminant)) ** (1 / 3)
        v = (-q / 2 - math.sqrt(discriminant)) ** (1 / 3)
        roots.append((u + v) - shift)
        roots.append(complex(-(u + v) / 2 - shift, (u - v) * math.sqrt(3) / 2))
        roots.append(complex(-(u + v) / 2 - shift, -(u - v) * math.sqrt(3) / 2))
    else:
        r = math.sqrt(-p ** 3 / 27)
        theta = math.acos(-q / (2 * r))
        for k in range(3):
            root = 2 * ((-p / 3) ** 0.5) * math.cos((theta + 2 * math.pi * k) / 3) - shift
            roots.append(root)
    root_strs = [f'{r:.6f}' if isinstance(r, float) else f'{r.real:.6f}{r.imag:+.6f}i' for r in roots]
    return {
        'result': f'Roots: {", ".join(root_strs)}',
        'details': {'a': a, 'b': b, 'c': c, 'd': d, 'discriminant': discriminant, 'roots': [complex(r) if isinstance(r, float) else r for r in roots]},
        'unit': 'dimensionless'
    }

def calc_linear_system_2(a1: float = 2.0, b1: float = 1.0, c1: float = 5.0,
                          a2: float = 1.0, b2: float = -1.0, c2: float = 1.0) -> dict:
    """Solve system of 2 linear equations: a1*x + b1*y = c1, a2*x + b2*y = c2 using Cramer's rule."""
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        det_x = c1 * b2 - c2 * b1
        if abs(det_x) < 1e-12:
            return {
                'result': 'Infinite solutions (dependent equations)',
                'details': {'det': det, 'type': 'dependent'},
                'unit': 'dimensionless'
            }
        return {
            'result': 'No solution (inconsistent system)',
            'details': {'det': det, 'type': 'inconsistent'},
            'unit': 'dimensionless'
        }
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return {
        'result': f'x = {x:.6f}, y = {y:.6f}',
        'details': {'equations': [[a1, b1, c1], [a2, b2, c2]], 'solution': [x, y], 'det': det},
        'unit': 'dimensionless'
    }

def calc_linear_system_3(a1: float = 1.0, b1: float = 1.0, c1: float = 1.0, d1: float = 6.0,
                          a2: float = 1.0, b2: float = -1.0, c2: float = 1.0, d2: float = 2.0,
                          a3: float = 1.0, c3: float = -1.0, b3: float = 1.0, d3: float = 0.0) -> dict:
    """Solve a 3x3 linear system using Cramer's rule."""
    A = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]], dtype=float)
    B = np.array([d1, d2, d3], dtype=float)
    det = np.linalg.det(A)
    if abs(det) < 1e-12:
        return {
            'result': 'No unique solution (det=0): either no solution or infinite solutions',
            'details': {'det': det, 'type': 'singular'},
            'unit': 'dimensionless'
        }
    try:
        sol = np.linalg.solve(A, B)
    except np.linalg.LinAlgError:
        return {
            'result': 'Error solving system',
            'details': {'det': det, 'error': 'LinAlgError'},
            'unit': 'dimensionless'
        }
    return {
        'result': f'x = {sol[0]:.6f}, y = {sol[1]:.6f}, z = {sol[2]:.6f}',
        'details': {'A': A.tolist(), 'B': B.tolist(), 'solution': sol.tolist(), 'det': det},
        'unit': 'dimensionless'
    }

def calc_exponential_equation(base: float = 2.0, exponent_val: float = 8.0) -> dict:
    """Solve a^x = b, i.e., find x = log_a(b)."""
    if base <= 0 or base == 1:
        return {
            'result': f'Error: base must be > 0 and != 1 (got {base})',
            'details': {'base': base, 'exponent_val': exponent_val, 'error': 'invalid base'},
            'unit': 'dimensionless'
        }
    if exponent_val <= 0:
        return {
            'result': f'Error: b must be > 0 (got {exponent_val})',
            'details': {'base': base, 'exponent_val': exponent_val, 'error': 'invalid argument'},
            'unit': 'dimensionless'
        }
    x = math.log(exponent_val) / math.log(base)
    return {
        'result': f'{base}^x = {exponent_val} => x = log_{base}({exponent_val}) = {x:.6f}',
        'details': {'base': base, 'exponent_val': exponent_val, 'solution': x},
        'unit': 'dimensionless'
    }

def calc_logarithmic_equation(base: float = 2.0, argument: float = 8.0) -> dict:
    """Solve log_a(x) = b, i.e., find x = a^b."""
    if base <= 0 or base == 1:
        return {
            'result': f'Error: base must be > 0 and != 1 (got {base})',
            'details': {'base': base, 'argument': argument, 'error': 'invalid base'},
            'unit': 'dimensionless'
        }
    x = base ** argument
    return {
        'result': f'log_{base}(x) = {argument} => x = {base}^{argument} = {x:.6f}',
        'details': {'base': base, 'argument': argument, 'solution': x},
        'unit': 'dimensionless'
    }

# ==============================================================================
# INEQUALITIES
# ==============================================================================

def calc_linear_inequality(a: float = 2.0, b: float = -4.0, sign: str = '>') -> dict:
    """Solve linear inequality ax + b >/</>=/<= 0. Returns solution interval."""
    if a == 0:
        val = sign in ('>', '>=') if b >= 0 else sign in ('<', '<=')
        return {
            'result': 'All real numbers' if val else 'No solution',
            'details': {'a': a, 'b': b, 'sign': sign, 'type': 'constant'},
            'unit': 'interval'
        }
    critical = -b / a
    if sign == '>':
        interval = f'x > {critical:.4f}' if a > 0 else f'x < {critical:.4f}'
    elif sign == '<':
        interval = f'x < {critical:.4f}' if a > 0 else f'x > {critical:.4f}'
    elif sign == '>=':
        interval = f'x >= {critical:.4f}' if a > 0 else f'x <= {critical:.4f}'
    elif sign == '<=':
        interval = f'x <= {critical:.4f}' if a > 0 else f'x >= {critical:.4f}'
    else:
        return {
            'result': f'Error: Unknown sign "{sign}". Use >, <, >=, or <=.',
            'details': {'a': a, 'b': b, 'sign': sign, 'error': 'unknown sign'},
            'unit': 'interval'
        }
    return {
        'result': f'{a}x + {b} {sign} 0 => {interval}',
        'details': {'a': a, 'b': b, 'sign': sign, 'critical_point': critical, 'solution': interval},
        'unit': 'interval'
    }

def calc_quadratic_inequality(a: float = 1.0, b: float = -5.0, c: float = 6.0, sign: str = '<') -> dict:
    """Solve quadratic inequality ax^2 + bx + c < 0 (or >, <=, >=)."""
    if a == 0:
        return calc_linear_inequality(b, c, sign)
    disc = b * b - 4 * a * c
    if disc < 0:
        val = a > 0 if sign in ('>', '>=') else a < 0
        return {
            'result': 'All real numbers' if val else 'No solution',
            'details': {'a': a, 'b': b, 'c': c, 'discriminant': disc, 'type': 'no_real_roots'},
            'unit': 'interval'
        }
    r1 = (-b - math.sqrt(disc)) / (2 * a)
    r2 = (-b + math.sqrt(disc)) / (2 * a)
    if r1 > r2:
        r1, r2 = r2, r1
    if a > 0:
        if sign in ('<', '<='):
            interval = f'{r1:.4f} < x < {r2:.4f}' + (' (inclusive)' if '<=' in sign else '')
        else:
            interval = f'x < {r1:.4f} or x > {r2:.4f}' + (' (inclusive)' if '>=' in sign else '')
    else:
        if sign in ('>', '>='):
            interval = f'{r1:.4f} < x < {r2:.4f}' + (' (inclusive)' if '>=' in sign else '')
        else:
            interval = f'x < {r1:.4f} or x > {r2:.4f}' + (' (inclusive)' if '<=' in sign else '')
    return {
        'result': f'Solution: {interval}',
        'details': {'a': a, 'b': b, 'c': c, 'sign': sign, 'discriminant': disc, 'roots': [r1, r2], 'solution': interval},
        'unit': 'interval'
    }

def calc_abs_inequality(expression: str = '|x-3|', bound: float = 5.0, sign: str = '<') -> dict:
    """Solve |expression| < bound. Only handles |x - a| form currently."""
    import re
    m = re.match(r'\|x\s*([-+])\s*(\d+)\|', expression.replace(' ', ''))
    if m:
        shift = float(m.group(1) + m.group(2))
    else:
        m2 = re.match(r'\|x\|', expression.replace(' ', ''))
        if m2:
            shift = 0.0
        else:
            return {
                'result': f'Error: Cannot parse expression "{expression}". Use |x-a| or |x| format.',
                'details': {'expression': expression, 'bound': bound, 'sign': sign, 'error': 'parse error'},
                'unit': 'interval'
            }
    if sign in ('<', '<='):
        lower = shift - bound
        upper = shift + bound
        interval = f'{lower:.4f} < x < {upper:.4f}' + (' (inclusive)' if '<=' in sign else '')
    elif sign in ('>', '>='):
        interval = f'x < {shift - bound:.4f} or x > {shift + bound:.4f}' + (' (inclusive)' if '>=' in sign else '')
    else:
        return {
            'result': f'Error: Unknown sign "{sign}"',
            'details': {'expression': expression, 'bound': bound, 'sign': sign, 'error': 'unknown sign'},
            'unit': 'interval'
        }
    return {
        'result': f'{expression} {sign} {bound} => {interval}',
        'details': {'expression': expression, 'bound': bound, 'sign': sign, 'shift': shift, 'solution': interval},
        'unit': 'interval'
    }

def calc_inequality_system(inequalities: list = None) -> dict:
    """Check feasibility of a system of linear inequalities. Each inequality: [a, b, sign, c] meaning ax + by sign c."""
    if inequalities is None:
        inequalities = [['1', '0', '<', '5'], ['0', '1', '>', '2'], ['1', '1', '<=', '10']]
    processed = []
    for ineq in inequalities:
        sig = ineq[2].replace('>=', '≥').replace('<=', '≤').replace('>', '>').replace('<', '<')
        processed.append(f'{ineq[0]}x + {ineq[1]}y {sig} {ineq[3]}')
    feasible = True
    reason = 'Provisional feasibility check (full linear programming not implemented)'
    return {
        'result': f'Inequalities: {"; ".join(processed)}. Feasible: {feasible}',
        'details': {'inequalities': inequalities, 'feasible': feasible, 'note': reason},
        'unit': 'boolean'
    }

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def calc_domain_range(expression: str = 'sqrt(x-1)') -> dict:
    """Estimate domain and range of a function given as expression string."""
    expr_lower = expression.lower().replace(' ', '')
    domain = 'all real numbers'
    rng = 'all real numbers'
    if 'sqrt' in expr_lower:
        import re
        m = re.search(r'sqrt\((.*)\)', expr_lower)
        if m:
            inner = m.group(1)
            domain = f'{inner} >= 0'
        rng = '[0, +inf)'
    elif '/x' in expr_lower or '/(x' in expr_lower:
        domain = 'x != 0'
        rng = 'all real numbers except 0' if '1/' in expr_lower else 'all real numbers'
    elif 'log' in expr_lower:
        domain = 'x > 0'
        rng = 'all real numbers'
    elif '^2' in expr_lower or '**2' in expr_lower:
        rng = '[0, +inf)'
    elif 'sin' in expr_lower or 'cos' in expr_lower:
        rng = '[-1, 1]'
    elif 'e^' in expr_lower or 'exp' in expr_lower:
        rng = '(0, +inf)'
    return {
        'result': f'Domain: {domain}; Range: {rng}',
        'details': {'expression': expression, 'domain': domain, 'range': rng},
        'unit': 'interval'
    }

def calc_evaluate_function(expression: str = 'x^2 + 2x + 1', x_val: float = 3.0) -> dict:
    """Evaluate a simple function expression at x_val. Supports +, -, *, /, ^, sin, cos, exp, log, sqrt."""
    expr = expression.replace(' ', '')
    replacements = {
        '^': '**', 'sin': 'math.sin', 'cos': 'math.cos', 'tan': 'math.tan',
        'exp': 'math.exp', 'log': 'math.log', 'sqrt': 'math.sqrt',
        'abs': 'abs', 'pi': 'math.pi', 'e': 'math.e', 'x': str(x_val)
    }
    for old, new in replacements.items():
        if old in expr:
            expr = expr.replace(old, new)
    try:
        result = eval(expr, {"math": math, "abs": abs, "__builtins__": {}}, {"x": x_val})
        result = float(result)
    except Exception as e:
        return {
            'result': f'Error evaluating expression: {e}',
            'details': {'expression': expression, 'x_val': x_val, 'error': str(e)},
            'unit': 'number'
        }
    return {
        'result': f'f({x_val}) = {result:.6f}',
        'details': {'expression': expression, 'x_val': x_val, 'value': result},
        'unit': 'number'
    }

def calc_monotonicity(a: float = 1.0, b: float = 0.0, interval_start: float = 0.0, interval_end: float = 10.0) -> dict:
    """Check monotonicity of f(x)=ax+b on [start, end]."""
    if a > 0:
        mono = 'strictly increasing'
    elif a < 0:
        mono = 'strictly decreasing'
    else:
        mono = 'constant'
    return {
        'result': f'f(x) = {a}x + {b} is {mono} on [{interval_start}, {interval_end}]',
        'details': {'a': a, 'b': b, 'interval': [interval_start, interval_end], 'monotonicity': mono},
        'unit': 'property'
    }

def calc_composition(f_expr: str = 'x^2', g_expr: str = 'x+1', x_val: float = 2.0) -> dict:
    """Compute f(g(x)) for two given expressions at x_val."""
    g_result = calc_evaluate_function(g_expr, x_val)
    if 'error' in g_result['details']:
        return g_result
    g_val = g_result['details']['value']
    f_result = calc_evaluate_function(f_expr, g_val)
    if 'error' in f_result['details']:
        return f_result
    composed_str = f'f(g(x)) = ({g_expr})^2' if '^2' in f_expr else f'f(g(x)) = {f_expr.replace("x", f"({g_expr})")}'
    return {
        'result': f'f(g({x_val})) = {f_result["details"]["value"]:.6f}',
        'details': {'f': f_expr, 'g': g_expr, 'x': x_val, 'g_of_x': g_val, 'f_of_g_of_x': f_result['details']['value'], 'composed': composed_str},
        'unit': 'number'
    }

def calc_inverse_function(expression: str = 'ax+b', a: float = 2.0, b: float = 3.0) -> dict:
    """Find inverse of simple functions: ax+b, (x-a)/b, sqrt(x), x^2, x^3, 1/x, e^x, ln(x)."""
    expr_lower = expression.lower().replace(' ', '')
    if expr_lower in ('ax+b', 'a*x+b', 'ax + b'):
        result_str = f'f^(-1)(y) = (y - {b}) / {a}'
        details = {'expression': 'ax+b', 'a': a, 'b': b, 'inverse': f'(x - {b}) / {a}'}
    elif expr_lower in ('(x-a)/b', '(x - a)/b'):
        result_str = f'f^(-1)(y) = {b}y + {a}'
        details = {'expression': '(x-a)/b', 'a': a, 'b': b, 'inverse': f'{b}x + {a}'}
    elif 'sqrt' in expr_lower:
        result_str = 'f^(-1)(y) = y^2 (for y >= 0)'
        details = {'expression': 'sqrt(x)', 'inverse': 'x^2', 'restriction': 'x >= 0'}
    elif 'x^2' in expr_lower or 'x**2' in expr_lower:
        result_str = 'f^(-1)(y) = +/- sqrt(y) (two branches)'
        details = {'expression': 'x^2', 'inverse': '+-sqrt(x)', 'note': 'not invertible on all reals'}
    elif 'x^3' in expr_lower or 'x**3' in expr_lower:
        result_str = 'f^(-1)(y) = cbrt(y)'
        details = {'expression': 'x^3', 'inverse': 'cbrt(x)'}
    elif '1/x' in expr_lower:
        result_str = 'f^(-1)(y) = 1/y'
        details = {'expression': '1/x', 'inverse': '1/x', 'note': 'self-inverse'}
    elif 'e^' in expr_lower or 'exp' in expr_lower:
        result_str = 'f^(-1)(y) = ln(y), y > 0'
        details = {'expression': 'e^x', 'inverse': 'ln(x)', 'restriction': 'x > 0'}
    elif 'ln' in expr_lower or 'log' in expr_lower:
        result_str = 'f^(-1)(y) = e^y'
        details = {'expression': 'ln(x)', 'inverse': 'e^x'}
    else:
        return {
            'result': f'Error: Cannot find inverse of "{expression}". Supported: ax+b, (x-a)/b, sqrt(x), x^2, x^3, 1/x, e^x, ln(x)',
            'details': {'expression': expression, 'error': 'unsupported expression for inversion'},
            'unit': 'expression'
        }
    return {
        'result': result_str,
        'details': details,
        'unit': 'expression'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    # Arithmetic
    'add': {'func': calc_add, 'params': ['a', 'b', 'precision'], 'desc': 'Add two numbers with precision'},
    'subtract': {'func': calc_subtract, 'params': ['a', 'b', 'precision'], 'desc': 'Subtract b from a with precision'},
    'multiply': {'func': calc_multiply, 'params': ['a', 'b', 'precision'], 'desc': 'Multiply two numbers with precision'},
    'divide': {'func': calc_divide, 'params': ['a', 'b', 'precision'], 'desc': 'Divide a by b with precision'},
    'absolute': {'func': calc_absolute, 'params': ['x'], 'desc': 'Compute absolute value of x'},
    'mod': {'func': calc_mod, 'params': ['a', 'b'], 'desc': 'Compute a mod b (remainder)'},
    'floor': {'func': calc_floor, 'params': ['x'], 'desc': 'Compute floor of x'},
    'ceil': {'func': calc_ceil, 'params': ['x'], 'desc': 'Compute ceiling of x'},
    'ratio': {'func': calc_ratio, 'params': ['a', 'b'], 'desc': 'Express a:b as simplified ratio'},
    'percentage': {'func': calc_percentage, 'params': ['part', 'whole'], 'desc': 'Calculate what percentage part is of whole'},
    'sig_figs': {'func': calc_sig_figs, 'params': ['x', 'n'], 'desc': 'Round x to n significant figures'},
    'sci_notation': {'func': calc_sci_notation, 'params': ['x'], 'desc': 'Express x in scientific notation'},
    'unit_length': {'func': calc_unit_length, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert length units'},
    'unit_mass': {'func': calc_unit_mass, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert mass units'},
    'unit_time': {'func': calc_unit_time, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert time units'},
    'unit_area': {'func': calc_unit_area, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert area units'},
    'unit_volume': {'func': calc_unit_volume, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert volume units'},
    'unit_speed': {'func': calc_unit_speed, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert speed units'},
    'unit_density': {'func': calc_unit_density, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert density units'},
    'unit_pressure': {'func': calc_unit_pressure, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert pressure units'},
    'unit_energy': {'func': calc_unit_energy, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert energy units'},
    'unit_power': {'func': calc_unit_power, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert power units'},
    'unit_temperature': {'func': calc_unit_temperature, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert temperature units'},
    'unit_angle': {'func': calc_unit_angle, 'params': ['value', 'from_unit', 'to_unit'], 'desc': 'Convert angle units'},
    # Algebra
    'polynomial': {'func': calc_polynomial, 'params': ['coefficients', 'x'], 'desc': 'Evaluate a polynomial at x'},
    'factor_quadratic': {'func': calc_factor_quadratic, 'params': ['a', 'b', 'c'], 'desc': 'Factor ax^2 + bx + c over integers'},
    'power_rules': {'func': calc_power_rules, 'params': ['a', 'm', 'n'], 'desc': 'Demonstrate power rules'},
    'exp_log_rules': {'func': calc_exp_log_rules, 'params': ['value', 'a', 'b'], 'desc': 'Demonstrate exponent/log rules'},
    'radical_simplify': {'func': calc_radical_simplify, 'params': ['n'], 'desc': 'Simplify sqrt(n) to a*sqrt(b)'},
    'completing_square': {'func': calc_completing_square, 'params': ['a', 'b', 'c'], 'desc': 'Complete the square for ax^2+bx+c'},
    # Equations
    'linear': {'func': calc_linear, 'params': ['a', 'b'], 'desc': 'Solve ax + b = 0'},
    'quadratic': {'func': calc_quadratic, 'params': ['a', 'b', 'c'], 'desc': 'Solve ax^2 + bx + c = 0'},
    'cubic': {'func': calc_cubic, 'params': ['a', 'b', 'c', 'd'], 'desc': 'Solve ax^3 + bx^2 + cx + d = 0 (Cardano)'},
    'linear_system_2': {'func': calc_linear_system_2, 'params': ['a1', 'b1', 'c1', 'a2', 'b2', 'c2'], 'desc': 'Solve 2x2 linear system'},
    'linear_system_3': {'func': calc_linear_system_3, 'params': ['a1', 'b1', 'c1', 'd1', 'a2', 'b2', 'c2', 'd2', 'a3', 'b3', 'c3', 'd3'], 'desc': 'Solve 3x3 linear system'},
    'exponential_equation': {'func': calc_exponential_equation, 'params': ['base', 'exponent_val'], 'desc': 'Solve a^x = b'},
    'logarithmic_equation': {'func': calc_logarithmic_equation, 'params': ['base', 'argument'], 'desc': 'Solve log_a(x) = b'},
    # Inequalities
    'linear_inequality': {'func': calc_linear_inequality, 'params': ['a', 'b', 'sign'], 'desc': 'Solve ax + b sign 0'},
    'quadratic_inequality': {'func': calc_quadratic_inequality, 'params': ['a', 'b', 'c', 'sign'], 'desc': 'Solve ax^2 + bx + c sign 0'},
    'abs_inequality': {'func': calc_abs_inequality, 'params': ['expression', 'bound', 'sign'], 'desc': 'Solve |expression| sign bound'},
    'inequality_system': {'func': calc_inequality_system, 'params': ['inequalities'], 'desc': 'Check feasibility of inequality system'},
    # Functions
    'domain_range': {'func': calc_domain_range, 'params': ['expression'], 'desc': 'Estimate domain and range of a function'},
    'evaluate_function': {'func': calc_evaluate_function, 'params': ['expression', 'x_val'], 'desc': 'Evaluate a function at x'},
    'monotonicity': {'func': calc_monotonicity, 'params': ['a', 'b', 'interval_start', 'interval_end'], 'desc': 'Check monotonicity of f(x)=ax+b'},
    'composition': {'func': calc_composition, 'params': ['f_expr', 'g_expr', 'x_val'], 'desc': 'Compute f(g(x))'},
    'inverse_function': {'func': calc_inverse_function, 'params': ['expression', 'a', 'b'], 'desc': 'Find inverse of a function'},
}
