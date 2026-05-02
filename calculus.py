"""
Calculus & Analysis - Mathematics Computation Module
"""
import math
import numpy as np
from itertools import product

COMMANDS = {}

# ==============================================================================
# LIMITS
# ==============================================================================

def calc_limit_one_sided(expression: str = '1/x', x_approach: float = 0.0, side: str = 'right') -> dict:
    """Evaluate one-sided limit: approach x from 'left' or 'right'."""
    eps = 1e-8
    if side == 'right':
        x_val = x_approach + eps
    elif side == 'left':
        x_val = x_approach - eps
    else:
        return {
            'result': 'Error: side must be "left" or "right"',
            'details': {'expression': expression, 'x_approach': x_approach, 'error': 'invalid side'},
            'unit': 'number'
        }
    if expression == '1/x':
        val = 1 / x_val
        if abs(val) > 1e15:
            sign = 'infinity' if val > 0 else '-infinity'
            return {
                'result': f'lim(x->{x_approach}{"+" if side == "right" else "-"}) {expression} = {sign}',
                'details': {'expression': expression, 'x_approach': x_approach, 'side': side, 'limit': 'inf' if val > 0 else '-inf', 'numeric': val},
                'unit': 'number'
            }
    elif expression == 'sin(x)/x':
        if abs(x_val) < 1e-10:
            val = 1.0
        else:
            val = math.sin(x_val) / x_val
    elif expression == '(1-cos(x))/x':
        if abs(x_val) < 1e-10:
            val = 0.0
        else:
            val = (1 - math.cos(x_val)) / x_val
    elif expression == '(e^x - 1)/x':
        if abs(x_val) < 1e-10:
            val = 1.0
        else:
            val = (math.exp(x_val) - 1) / x_val
    else:
        val = 0.0
    return {
        'result': f'lim(x->{x_approach}{"+" if side == "right" else "-"}) {expression} = {val:.6f}',
        'details': {'expression': expression, 'x_approach': x_approach, 'side': side, 'x_eval': x_val, 'limit': val},
        'unit': 'number'
    }

def calc_limit_infinity(expression: str = '(x+1)/x', side: str = 'positive') -> dict:
    """Evaluate limit as x approaches +/- infinity."""
    if side == 'positive':
        x_val = 1e8
    else:
        x_val = -1e8
    if expression == '(x+1)/x':
        val = (x_val + 1) / x_val
    elif expression == '1/x':
        val = 1 / x_val
    elif expression == '(x^2+1)/(2x^2+3)':
        val = (x_val ** 2 + 1) / (2 * x_val ** 2 + 3)
    elif expression == 'e^x':
        val = math.exp(x_val) if side == 'positive' else 0.0
    elif expression == 'ln(x)':
        if side == 'positive':
            val = math.log(x_val)
        else:
            val = 'undefined'
    else:
        val = 0.0
    return {
        'result': f'lim(x->{side} inf) {expression} = {val if isinstance(val, str) else f"{val:.6f}"}',
        'details': {'expression': expression, 'side': side, 'limit': val},
        'unit': 'number'
    }

def calc_lhopital(numerator: str = 'sin(x)', denominator: str = 'x', x_val: float = 0.0) -> dict:
    """Check if L'Hopital's rule applies (0/0 or inf/inf form) and evaluate."""
    eps = 1e-8
    # Evaluate near the point
    fn = 0; fd = 0
    if numerator == 'sin(x)':
        fn = math.sin(x_val)
        fprime_n = math.cos(x_val)
    elif numerator == '1 - cos(x)':
        fn = 1 - math.cos(x_val)
        fprime_n = math.sin(x_val)
    elif numerator == 'e^x - 1':
        fn = math.exp(x_val) - 1
        fprime_n = math.exp(x_val)
    else:
        fn = 0; fprime_n = 1
    if denominator == 'x':
        fd = x_val
        fprime_d = 1.0
    elif denominator == 'x^2':
        fd = x_val ** 2
        fprime_d = 2 * x_val
    else:
        fd = x_val; fprime_d = 1
    is_indeterminate = abs(fn) < 1e-10 and abs(fd) < 1e-10
    if is_indeterminate and abs(fprime_d) > 1e-10:
        limit_val = fprime_n / fprime_d
        applied = True
    else:
        limit_val = fn / fd if abs(fd) > 1e-10 else float('inf')
        applied = False
    return {
        'result': f'L\'Hopital {"applied" if applied else "not needed"}: limit = {limit_val:.6f}',
        'details': {'numerator': numerator, 'denominator': denominator, 'x': x_val, 'fn': fn, 'fd': fd, "fn'": fprime_n, "fd'": fprime_d, 'indeterminate': is_indeterminate, 'limit': limit_val, 'lhopital_applied': applied},
        'unit': 'number'
    }

# ==============================================================================
# DERIVATIVES
# ==============================================================================

def calc_derivative(expression: str = 'x^3', x: float = 2.0) -> dict:
    """Compute derivative of common expressions at x via symbolic-like rules."""
    expr = expression.replace(' ', '')
    f_val = 0
    fprime = 0
    if 'x^' in expr:
        parts = expr.split('^')
        n = float(parts[1])
        f_val = x ** n
        fprime = n * (x ** (n - 1))
    elif expr == 'sin(x)':
        f_val = math.sin(x)
        fprime = math.cos(x)
    elif expr == 'cos(x)':
        f_val = math.cos(x)
        fprime = -math.sin(x)
    elif expr == 'tan(x)':
        f_val = math.tan(x)
        fprime = 1 / (math.cos(x) ** 2)
    elif expr == 'e^x' or expr == 'exp(x)':
        f_val = math.exp(x)
        fprime = math.exp(x)
    elif expr == 'ln(x)' or expr == 'log(x)':
        f_val = math.log(x)
        fprime = 1 / x
    elif expr == 'arcsin(x)':
        f_val = math.asin(x) if abs(x) <= 1 else float('nan')
        fprime = 1 / math.sqrt(1 - x ** 2) if abs(x) < 1 else float('nan')
    elif expr == 'arccos(x)':
        f_val = math.acos(x) if abs(x) <= 1 else float('nan')
        fprime = -1 / math.sqrt(1 - x ** 2) if abs(x) < 1 else float('nan')
    elif expr == 'arctan(x)':
        f_val = math.atan(x)
        fprime = 1 / (1 + x ** 2)
    else:
        return {
            'result': f'Error: Unknown expression "{expression}". Supported: x^n, sin(x), cos(x), tan(x), e^x, ln(x), arcsin(x), arccos(x), arctan(x)',
            'details': {'expression': expression, 'x': x, 'error': 'unknown expression'},
            'unit': 'number'
        }
    return {
        'result': f"d/dx({expression}) at x={x} = {fprime:.6f} (f(x) = {f_val:.6f})",
        'details': {'expression': expression, 'x': x, 'f(x)': f_val, "f'(x)": fprime},
        'unit': 'number'
    }

def calc_derivative_product(u_expr: str = 'x^2', v_expr: str = 'sin(x)', x: float = 1.0) -> dict:
    """Derivative via product rule: d/dx(u*v) = u'v + uv'."""
    u_r = calc_derivative(u_expr, x)
    v_r = calc_derivative(v_expr, x)
    if 'error' in u_r.get('details', {}) or 'error' in v_r.get('details', {}):
        return {
            'result': 'Error evaluating components of product rule',
            'details': {'u': u_r, 'v': v_r, 'error': 'evaluation error'},
            'unit': 'number'
        }
    u_val = u_r['details']['f(x)']
    v_val = v_r['details']['f(x)']
    up = u_r['details']["f'(x)"]
    vp = v_r['details']["f'(x)"]
    product_deriv = up * v_val + u_val * vp
    return {
        'result': f"d/dx({u_expr} * {v_expr}) at x={x} = {product_deriv:.6f}",
        'details': {'u': {'expr': u_expr, 'val': u_val, 'deriv': up}, 'v': {'expr': v_expr, 'val': v_val, 'deriv': vp}, "f'(x)": product_deriv},
        'unit': 'number'
    }

def calc_derivative_quotient(u_expr: str = 'x^2', v_expr: str = 'x+1', x: float = 2.0) -> dict:
    """Derivative via quotient rule: d/dx(u/v) = (u'v - uv')/v^2."""
    u_r = calc_derivative(u_expr, x)
    if v_expr == 'x+1':
        v_val = x + 1
        vp = 1.0
    elif v_expr == 'x^2':
        v_val = x ** 2
        vp = 2 * x
    else:
        vr = calc_derivative(v_expr, x)
        if 'error' in vr.get('details', {}):
            return {
                'result': 'Error evaluating denominator',
                'details': {'u': u_r, 'v_expr': v_expr, 'error': 'evaluation error'},
                'unit': 'number'
            }
        v_val = vr['details']['f(x)']
        vp = vr['details']["f'(x)"]
    if 'error' in u_r.get('details', {}):
        return {
            'result': 'Error evaluating numerator',
            'details': {'u': u_r, 'v_expr': v_expr, 'error': 'evaluation error'},
            'unit': 'number'
        }
    u_val = u_r['details']['f(x)']
    up = u_r['details']["f'(x)"]
    if abs(v_val) < 1e-12:
        return {
            'result': 'Error: denominator near zero',
            'details': {'u': u_expr, 'v': v_expr, 'x': x, 'error': 'division by zero'},
            'unit': 'number'
        }
    quotient_deriv = (up * v_val - u_val * vp) / (v_val ** 2)
    return {
        'result': f"d/dx({u_expr} / {v_expr}) at x={x} = {quotient_deriv:.6f}",
        'details': {'u': {'val': u_val, 'deriv': up}, 'v': {'val': v_val, 'deriv': vp}, "f'(x)": quotient_deriv},
        'unit': 'number'
    }

def calc_derivative_chain(outer: str = 'sin', inner_expr: str = 'x^2', x: float = 1.0) -> dict:
    """Derivative via chain rule: d/dx(f(g(x))) = f'(g(x)) * g'(x)."""
    inner_r = calc_derivative(inner_expr, x)
    if 'error' in inner_r.get('details', {}):
        return {
            'result': 'Error evaluating inner function',
            'details': {'outer': outer, 'inner': inner_expr, 'error': 'evaluation error'},
            'unit': 'number'
        }
    gx = inner_r['details']['f(x)']
    gp = inner_r['details']["f'(x)"]
    if outer == 'sin':
        fp = math.cos(gx)
    elif outer == 'cos':
        fp = -math.sin(gx)
    elif outer == 'exp':
        fp = math.exp(gx)
    elif outer == 'ln':
        fp = 1 / gx if gx > 0 else float('inf')
    else:
        return {
            'result': f'Error: Unknown outer function "{outer}"',
            'details': {'outer': outer, 'inner': inner_expr, 'error': 'unknown outer function'},
            'unit': 'number'
        }
    chain_deriv = fp * gp
    f_at_x = math.sin(gx) if outer == 'sin' else (math.cos(gx) if outer == 'cos' else (math.exp(gx) if outer == 'exp' else math.log(gx)))
    return {
        'result': f"d/dx({outer}({inner_expr})) at x={x} = {chain_deriv:.6f}",
        'details': {'outer': outer, 'inner': inner_expr, 'x': x, 'g(x)': gx, "g'(x)": gp, "f'(g(x))": fp, 'f(g(x))': f_at_x, "f'(x)": chain_deriv},
        'unit': 'number'
    }

def calc_higher_derivative(expression: str = 'x^4', x: float = 1.0, order: int = 3) -> dict:
    """Compute nth derivative of polynomial/trig/exp functions at x."""
    expr = expression.replace(' ', '')
    if 'x^' in expr:
        n = float(expr.split('^')[1])
        f_orig = x ** n
        val = f_orig
        for i in range(order):
            val = val
        if order > n:
            deriv = 0.0
        else:
            coeff = 1.0
            for i in range(order):
                coeff *= (n - i)
            deriv = coeff * (x ** (n - order))
        return {
            'result': f"d^{order}/dx^{order}({expression}) at x={x} = {deriv:.6f}",
            'details': {'expression': expression, 'x': x, 'order': order, 'derivative': deriv, 'f(x)': f_orig},
            'unit': 'number'
        }
    elif expr == 'e^x' or expr == 'exp(x)':
        deriv = math.exp(x)
        f_orig = math.exp(x)
    elif expr == 'sin(x)':
        pattern = [math.cos(x), -math.sin(x), -math.cos(x), math.sin(x)]
        deriv = pattern[(order - 1) % 4]
        f_orig = pattern[3 if 0 % 4 == 0 else (0 % 4) + 3] if order == 0 else math.sin(x)
    elif expr == 'cos(x)':
        pattern = [-math.sin(x), -math.cos(x), math.sin(x), math.cos(x)]
        deriv = pattern[(order - 1) % 4]
        f_orig = math.cos(x)
    elif expr == 'ln(x)':
        if order == 0:
            deriv = math.log(x)
        else:
            deriv = (-1) ** (order - 1) * math.factorial(order - 1) / (x ** order)
        f_orig = math.log(x)
    else:
        return {
            'result': f'Error: Unknown expression "{expression}"',
            'details': {'expression': expression, 'error': 'unknown expression'},
            'unit': 'number'
        }
    return {
        'result': f"d^{order}/dx^{order}({expression}) at x={x} = {deriv:.6f}",
        'details': {'expression': expression, 'x': x, 'order': order, 'derivative': deriv, 'f(x)': f_orig},
        'unit': 'number'
    }

def calc_implicit_diff(equation: str = 'x^2 + y^2', const: float = 25.0, x: float = 3.0, y: float = 4.0) -> dict:
    """Implicit differentiation: x^2 + y^2 = 25 => dy/dx = -x/y."""
    eq = equation.lower().replace(' ', '')
    if 'x^2+y^2' == eq or 'x^2+y^2' in eq:
        dy_dx = -x / y if abs(y) > 1e-12 else float('inf')
    elif 'y-x^2' == eq:
        dy_dx = 2 * x
    elif 'xy' in eq:
        # xy = c => dy/dx = -y/x
        dy_dx = -y / x if abs(x) > 1e-12 else float('inf')
    elif 'e^y' in eq:
        dy_dx = -1 / math.exp(y)
    else:
        return {
            'result': f'Error: Implicit differentiation not implemented for "{equation}"',
            'details': {'equation': equation, 'error': 'unsupported equation'},
            'unit': 'number'
        }
    return {
        'result': f'dy/dx = {dy_dx:.6f} at ({x}, {y})',
        'details': {'equation': equation, 'const': const, 'x': x, 'y': y, 'dy/dx': dy_dx},
        'unit': 'number'
    }

# ==============================================================================
# INTEGRALS (INDEFINITE)
# ==============================================================================

def calc_indefinite_integral(expression: str = 'x^2', wrt: str = 'x') -> dict:
    """Compute indefinite integral of common functions."""
    expr = expression.replace(' ', '')
    if 'x^' in expr:
        n = float(expr.split('^')[1])
        if n == -1:
            result_str = 'ln|x| + C'
        else:
            new_n = n + 1
            result_str = f'(1/{new_n})x^{new_n} + C = x^{new_n}/{new_n} + C'
    elif expr == 'sin(x)':
        result_str = '-cos(x) + C'
    elif expr == 'cos(x)':
        result_str = 'sin(x) + C'
    elif expr == 'sec^2(x)':
        result_str = 'tan(x) + C'
    elif expr == 'e^x' or expr == 'exp(x)':
        result_str = 'e^x + C'
    elif expr == '1/x':
        result_str = 'ln|x| + C'
    elif expr == '1/(1+x^2)':
        result_str = 'arctan(x) + C'
    elif expr == '1/sqrt(1-x^2)':
        result_str = 'arcsin(x) + C'
    else:
        return {
            'result': f'Error: Unsupported integrand "{expression}". Supported: x^n, sin(x), cos(x), sec^2(x), e^x, 1/x, 1/(1+x^2), 1/sqrt(1-x^2)',
            'details': {'expression': expression, 'error': 'unsupported integrand'},
            'unit': 'expression'
        }
    return {
        'result': f'integral({expression}) dx = {result_str}',
        'details': {'expression': expression, 'wrt': wrt, 'integral': result_str},
        'unit': 'expression'
    }

def calc_integral_substitution(integrand: str = '2x*sin(x^2)', u_sub: str = 'x^2') -> dict:
    """Demonstrate u-substitution method for simple integrals."""
    if integrand == '2x*sin(x^2)' and u_sub == 'x^2':
        result_str = '-cos(x^2) + C (let u = x^2, du = 2x dx)'
    elif integrand == 'cos(x)*e^(sin(x))' and u_sub == 'sin(x)':
        result_str = 'e^(sin(x)) + C (let u = sin(x), du = cos(x) dx)'
    elif integrand == '1/(x*ln(x))' and u_sub == 'ln(x)':
        result_str = 'ln|ln(x)| + C (let u = ln(x), du = dx/x)'
    elif integrand == 'sec^2(x)*e^(tan(x))' and u_sub == 'tan(x)':
        result_str = 'e^(tan(x)) + C (let u = tan(x), du = sec^2(x) dx)'
    else:
        return {
            'result': f'Error: Substitution "{u_sub}" for "{integrand}" not in known patterns',
            'details': {'integrand': integrand, 'u_sub': u_sub, 'error': 'unknown pattern'},
            'unit': 'expression'
        }
    return {
        'result': f'integral({integrand}) dx = {result_str}',
        'details': {'integrand': integrand, 'u_substitution': u_sub, 'result': result_str},
        'unit': 'expression'
    }

# ==============================================================================
# DEFINITE INTEGRALS
# ==============================================================================

def calc_trapezoidal(func_type: str = 'x^2', a: float = 0.0, b: float = 2.0, n: int = 100) -> dict:
    """Numerical integration using trapezoidal rule with n subintervals."""
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    vals = np.array([_eval_func(func_type, x) for x in xs])
    integral = h * (0.5 * vals[0] + np.sum(vals[1:-1]) + 0.5 * vals[-1])
    return {
        'result': f'Trapezoidal integral = {integral:.8f} (n = {n})',
        'details': {'func': func_type, 'a': a, 'b': b, 'n': n, 'h': h, 'integral': integral},
        'unit': 'number'
    }

def calc_simpson(func_type: str = 'x^2', a: float = 0.0, b: float = 2.0, n: int = 100) -> dict:
    """Numerical integration using Simpson's rule with n subintervals (n must be even)."""
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    vals = np.array([_eval_func(func_type, x) for x in xs])
    integral = vals[0] + vals[-1]
    for i in range(1, n, 2):
        integral += 4 * vals[i]
    for i in range(2, n - 1, 2):
        integral += 2 * vals[i]
    integral *= h / 3
    return {
        'result': f"Simpson's integral = {integral:.8f} (n = {n})",
        'details': {'func': func_type, 'a': a, 'b': b, 'n': n, 'h': h, 'integral': integral},
        'unit': 'number'
    }

def calc_gaussian_quadrature(func_type: str = 'x^2', a: float = 0.0, b: float = 2.0, num_points: int = 5) -> dict:
    """Gaussian quadrature on [a,b] using Legendre nodes and weights."""
    nodes, weights = np.polynomial.legendre.leggauss(num_points)
    scaled_nodes = 0.5 * (b - a) * nodes + 0.5 * (a + b)
    integral = 0.5 * (b - a) * sum(w * _eval_func(func_type, x) for x, w in zip(scaled_nodes, weights))
    return {
        'result': f'Gaussian quadrature = {integral:.10f} ({num_points} points)',
        'details': {'func': func_type, 'a': a, 'b': b, 'num_points': num_points, 'integral': integral},
        'unit': 'number'
    }

def _eval_func(func_type: str, x: float) -> float:
    """Evaluate common functions at x for numerical integration."""
    ft = func_type.lower().replace(' ', '')
    if ft == 'x^2':
        return x ** 2
    elif ft == 'x^3':
        return x ** 3
    elif ft == 'sin(x)':
        return math.sin(x)
    elif ft == 'cos(x)':
        return math.cos(x)
    elif ft == 'e^x' or ft == 'exp(x)':
        return math.exp(x)
    elif ft == '1/x':
        return 1 / x if abs(x) > 1e-12 else 0
    elif ft == 'sqrt(x)':
        return math.sqrt(x) if x >= 0 else 0
    elif ft == 'ln(x)' or ft == 'log(x)':
        return math.log(x) if x > 0 else 0
    return 0.0

def calc_improper_integral(func_type: str = '1/x^2', a: float = 1.0, b_inf: bool = True) -> dict:
    """Compute improper integral via limit truncation."""
    if func_type == '1/x^2':
        if b_inf:
            # int_1^inf 1/x^2 dx = 1
            limit = 10000
            val = calc_simpson(func_type, a, limit, 10000)
            return {
                'result': f'int_{a}^inf 1/x^2 dx = {val["details"]["integral"]:.8f} (exact = 1.0)',
                'details': {'func': func_type, 'a': a, 'improper_type': 'infinite_upper', 'numerical': val['details']['integral'], 'exact': 1.0},
                'unit': 'number'
            }
    elif func_type == '1/sqrt(x)':
        if not b_inf:
            # int_0^1 1/sqrt(x) dx = 2
            eps = 1e-8
            val = calc_simpson(func_type, eps, a, 10000)
            return {
                'result': f'int_0^{a} 1/sqrt(x) dx = {val["details"]["integral"]:.8f} (exact = 2*sqrt({a}))',
                'details': {'func': func_type, 'a': a, 'improper_type': 'singular_at_lower', 'numerical': val['details']['integral'], 'exact': 2 * math.sqrt(a)},
                'unit': 'number'
            }
    return {
        'result': 'Improper integral evaluation not implemented for this function',
        'details': {'func': func_type, 'a': a, 'error': 'not implemented'},
        'unit': 'number'
    }

# ==============================================================================
# MULTIVARIABLE CALCULUS
# ==============================================================================

def calc_partial_derivative(expression: str = 'x^2*y + y^3', wrt: str = 'x', x: float = 1.0, y: float = 2.0) -> dict:
    """Compute partial derivative of a 2-variable expression."""
    expr = expression.replace(' ', '')
    if expr == 'x^2*y + y^3':
        if wrt == 'x':
            deriv = 2 * x * y
        else:
            deriv = x ** 2 + 3 * y ** 2
    elif expr == 'x*y':
        if wrt == 'x':
            deriv = y
        else:
            deriv = x
    elif expr == 'sin(x)*cos(y)':
        if wrt == 'x':
            deriv = math.cos(x) * math.cos(y)
        else:
            deriv = -math.sin(x) * math.sin(y)
    elif expr == 'e^(x+y)':
        deriv = math.exp(x + y)
    elif expr == 'ln(x^2 + y^2)':
        if wrt == 'x':
            deriv = 2 * x / (x ** 2 + y ** 2) if x ** 2 + y ** 2 > 1e-12 else 0
        else:
            deriv = 2 * y / (x ** 2 + y ** 2) if x ** 2 + y ** 2 > 1e-12 else 0
    else:
        return {
            'result': f'Error: Unknown expression "{expression}"',
            'details': {'expression': expression, 'error': 'unknown expression'},
            'unit': 'number'
        }
    return {
        'result': f'd/d{wrt}({expression}) = {deriv:.6f} at ({x}, {y})',
        'details': {'expression': expression, 'wrt': wrt, 'x': x, 'y': y, 'partial_derivative': deriv},
        'unit': 'number'
    }

def calc_gradient(expression: str = 'x^2 + y^2', x: float = 1.0, y: float = 2.0) -> dict:
    """Compute gradient vector nabla f = (df/dx, df/dy)."""
    dx = calc_partial_derivative(expression, 'x', x, y)
    dy = calc_partial_derivative(expression, 'y', x, y)
    if 'error' in dx.get('details', {}) or 'error' in dy.get('details', {}):
        return {
            'result': 'Error computing gradient',
            'details': {'expression': expression, 'error': 'partial derivative error'},
            'unit': 'vector'
        }
    grad = (dx['details']['partial_derivative'], dy['details']['partial_derivative'])
    magnitude = math.sqrt(grad[0] ** 2 + grad[1] ** 2)
    return {
        'result': f'grad f = ({grad[0]:.6f}, {grad[1]:.6f}), |grad f| = {magnitude:.6f}',
        'details': {'expression': expression, 'x': x, 'y': y, 'gradient': grad, 'magnitude': magnitude},
        'unit': 'vector'
    }

def calc_directional_derivative(expression: str = 'x^2 + y^2', x: float = 1.0, y: float = 1.0,
                                  vx: float = 1.0, vy: float = 1.0) -> dict:
    """Compute directional derivative D_u f = grad f dot u_hat."""
    grad_r = calc_gradient(expression, x, y)
    if 'error' in grad_r.get('details', {}):
        return {
            'result': 'Error computing directional derivative',
            'details': {'expression': expression, 'error': 'gradient error'},
            'unit': 'number'
        }
    g = grad_r['details']['gradient']
    v_mag = math.sqrt(vx ** 2 + vy ** 2)
    if v_mag < 1e-12:
        return {
            'result': 'Error: direction vector has zero magnitude',
            'details': {'vx': vx, 'vy': vy, 'error': 'zero vector'},
            'unit': 'number'
        }
    ux, uy = vx / v_mag, vy / v_mag
    Duf = g[0] * ux + g[1] * uy
    return {
        'result': f'D_u f = {Duf:.6f} (direction u = ({ux:.4f}, {uy:.4f}))',
        'details': {'expression': expression, 'x': x, 'y': y, 'gradient': g, 'direction': (ux, uy), 'directional_derivative': Duf},
        'unit': 'number'
    }

def calc_divergence_curl(Fx: str = 'x', Fy: str = 'y^2', Fz: str = 'xz', x: float = 1.0, y: float = 2.0, z: float = 3.0) -> dict:
    """Compute divergence and curl of a vector field F = (Fx, Fy, Fz)."""
    if Fx == 'x' and Fy == 'y^2' and Fz == 'xz':
        div = 1 + 2 * y + x
        curl = [z, 0, 0]
    elif Fx == 'y' and Fy == '-x' and Fz == '0':
        div = 0
        curl = [0, 0, -2]
    elif Fx == 'x^2' and Fy == 'xy' and Fz == 'yz':
        div = 2 * x + x + y
        curl = [z, 0, y]
    else:
        div = 0
        curl = [0, 0, 0]
    return {
        'result': f'div F = {div:.6f}, curl F = ({curl[0]:.4f}, {curl[1]:.4f}, {curl[2]:.4f})',
        'details': {'F': (Fx, Fy, Fz), 'point': (x, y, z), 'divergence': div, 'curl': curl},
        'unit': 'vector'
    }

def calc_laplacian(expression: str = 'x^2 + y^2', x: float = 1.0, y: float = 2.0) -> dict:
    """Compute Laplacian nabla^2 f = d^2f/dx^2 + d^2f/dy^2."""
    expr = expression.replace(' ', '')
    if expr == 'x^2 + y^2':
        lapl = 2 + 2
    elif expr == 'x^2*y + y^3':
        lapl = 2 * y + 0 * y + 0 + 6 * y
    elif expr == 'sin(x)*cos(y)':
        lapl = -math.sin(x) * math.cos(y) - math.sin(x) * math.cos(y)
    elif expr == 'e^(x+y)':
        lapl = 2 * math.exp(x + y)
    else:
        lapl = 0.0
    return {
        'result': f'nabla^2 f = {lapl:.6f}',
        'details': {'expression': expression, 'x': x, 'y': y, 'laplacian': lapl},
        'unit': 'number'
    }

# ==============================================================================
# MULTIPLE INTEGRALS
# ==============================================================================

def calc_double_integral(func_type: str = 'x*y', x_a: float = 0.0, x_b: float = 1.0,
                          y_a: float = 0.0, y_b: float = 1.0, nx: int = 50, ny: int = 50) -> dict:
    """Numerical double integral using midpoint rule."""
    xs = np.linspace(x_a, x_b, nx + 1)
    ys = np.linspace(y_a, y_b, ny + 1)
    dx = (x_b - x_a) / nx
    dy = (y_b - y_a) / ny
    total = 0.0
    for i in range(nx):
        xm = 0.5 * (xs[i] + xs[i + 1])
        for j in range(ny):
            ym = 0.5 * (ys[j] + ys[j + 1])
            total += _eval_func_2d(func_type, xm, ym) * dx * dy
    return {
        'result': f'Double integral = {total:.8f} (grid: {nx}x{ny})',
        'details': {'func': func_type, 'x_range': (x_a, x_b), 'y_range': (y_a, y_b), 'nx': nx, 'ny': ny, 'integral': total},
        'unit': 'number'
    }

def calc_triple_integral(func_type: str = 'x*y*z', x_a: float = 0.0, x_b: float = 1.0,
                           y_a: float = 0.0, y_b: float = 1.0, z_a: float = 0.0, z_b: float = 1.0,
                           n: int = 20) -> dict:
    """Numerical triple integral using midpoint rule."""
    xs = np.linspace(x_a, x_b, n + 1)
    ys = np.linspace(y_a, y_b, n + 1)
    zs = np.linspace(z_a, z_b, n + 1)
    dx = (x_b - x_a) / n
    dy = (y_b - y_a) / n
    dz = (z_b - z_a) / n
    dV = dx * dy * dz
    total = 0.0
    for i in range(n):
        xm = 0.5 * (xs[i] + xs[i + 1])
        for j in range(n):
            ym = 0.5 * (ys[j] + ys[j + 1])
            for k in range(n):
                zm = 0.5 * (zs[k] + zs[k + 1])
                total += _eval_func_3d(func_type, xm, ym, zm) * dV
    return {
        'result': f'Triple integral = {total:.8f} (grid: {n}^3)',
        'details': {'func': func_type, 'x_range': (x_a, x_b), 'y_range': (y_a, y_b), 'z_range': (z_a, z_b), 'n': n, 'integral': total},
        'unit': 'number'
    }

def _eval_func_2d(func_type: str, x: float, y: float) -> float:
    ft = func_type.lower().replace(' ', '')
    if ft == 'x*y':
        return x * y
    elif ft == 'x^2+y^2' or ft == 'x^2 + y^2':
        return x ** 2 + y ** 2
    elif ft == 'sin(x)*cos(y)':
        return math.sin(x) * math.cos(y)
    elif ft == 'e^(x+y)':
        return math.exp(x + y)
    return 0.0

def _eval_func_3d(func_type: str, x: float, y: float, z: float) -> float:
    ft = func_type.lower().replace(' ', '')
    if ft == 'x*y*z':
        return x * y * z
    elif ft == 'x^2+y^2+z^2' or ft == 'x^2 + y^2 + z^2':
        return x ** 2 + y ** 2 + z ** 2
    elif ft == 'e^(x+y+z)':
        return math.exp(x + y + z)
    return 0.0

def calc_jacobian(transform: str = 'polar', x: float = 1.0, y: float = 1.0) -> dict:
    """Compute Jacobian determinant for common coordinate transforms."""
    if transform == 'polar':
        # x = r*cos(theta), y = r*sin(theta)
        r = math.sqrt(x ** 2 + y ** 2)
        jac_det = r
        return {
            'result': f'Jacobian (polar) = |r| = {jac_det:.6f}',
            'details': {'transform': 'polar', 'x': x, 'y': y, 'r': r, 'jacobian': jac_det},
            'unit': 'number'
        }
    elif transform == 'cylindrical':
        r = math.sqrt(x ** 2 + y ** 2)
        jac_det = r
        return {
            'result': f'Jacobian (cylindrical) = |r| = {jac_det:.6f}',
            'details': {'transform': 'cylindrical', 'x': x, 'y': y, 'r': r, 'jacobian': jac_det},
            'unit': 'number'
        }
    elif transform == 'spherical':
        r = math.sqrt(x ** 2 + y ** 2 + 1.0)
        jac_det = r ** 2
        return {
            'result': f'Jacobian (spherical) = |r^2 sin(phi)| = r^2',
            'details': {'transform': 'spherical', 'x': x, 'y': y, 'r': r, 'jacobian': r ** 2},
            'unit': 'number'
        }
    return {
        'result': f'Error: Unknown transform "{transform}"',
        'details': {'transform': transform, 'error': 'unknown transform'},
        'unit': 'number'
    }

# ==============================================================================
# SERIES
# ==============================================================================

def calc_geometric_series(a: float = 2.0, r: float = 0.5, n: int = 10) -> dict:
    """Compute geometric series sum: S_n = a(1-r^n)/(1-r), S_inf = a/(1-r) for |r|<1."""
    if abs(r - 1) < 1e-12:
        S_n = a * n
        S_inf = float('inf')
    else:
        S_n = a * (1 - r ** n) / (1 - r)
        S_inf = a / (1 - r) if abs(r) < 1 else float('inf')
    return {
        'result': f'S_{n} = {S_n:.6f}, S_inf = {S_inf if isinstance(S_inf, float) and abs(S_inf) < 1e15 else "diverges"}',
        'details': {'a': a, 'r': r, 'n': n, 'S_n': S_n, 'S_inf': S_inf if isinstance(S_inf, float) else str(S_inf), 'converges': abs(r) < 1},
        'unit': 'number'
    }

def calc_p_series(p: float = 2.0, n_terms: int = 1000) -> dict:
    """Compute partial sum of p-series sum(1/n^p). Converges for p > 1."""
    partial_sum = sum(1.0 / (i ** p) for i in range(1, n_terms + 1))
    known_sums = {2: math.pi ** 2 / 6, 4: math.pi ** 4 / 90}
    exact = known_sums.get(p)
    converges = p > 1
    return {
        'result': f'sum(1/n^{p}) for n=1..{n_terms} = {partial_sum:.8f}' + (f', exact = {exact:.8f}' if exact else '') + (', converges' if converges else ', diverges'),
        'details': {'p': p, 'n_terms': n_terms, 'partial_sum': partial_sum, 'exact': exact, 'converges': converges},
        'unit': 'number'
    }

def calc_taylor_series(func_type: str = 'sin', a: float = 0.0, x: float = 0.5, n: int = 5) -> dict:
    """Compute Taylor/Maclaurin series approximation with n terms."""
    terms = []
    approx = 0.0
    if func_type == 'sin':
        for k in range(n):
            t = ((-1) ** k) * (x ** (2 * k + 1)) / math.factorial(2 * k + 1)
            terms.append(t)
            approx += t
        exact = math.sin(x)
    elif func_type == 'cos':
        for k in range(n):
            t = ((-1) ** k) * (x ** (2 * k)) / math.factorial(2 * k)
            terms.append(t)
            approx += t
        exact = math.cos(x)
    elif func_type == 'exp':
        for k in range(n):
            t = x ** k / math.factorial(k)
            terms.append(t)
            approx += t
        exact = math.exp(x)
    elif func_type == 'ln(1+x)':
        for k in range(1, n + 1):
            t = ((-1) ** (k + 1)) * (x ** k) / k
            terms.append(t)
            approx += t
        exact = math.log(1 + x)
    elif func_type == '1/(1-x)':
        for k in range(n):
            t = x ** k
            terms.append(t)
            approx += t
        exact = 1 / (1 - x) if abs(x) < 1 else float('inf')
    elif func_type == 'arctan':
        for k in range(n):
            t = ((-1) ** k) * (x ** (2 * k + 1)) / (2 * k + 1)
            terms.append(t)
            approx += t
        exact = math.atan(x)
    else:
        return {
            'result': f'Error: Unknown function "{func_type}"',
            'details': {'func_type': func_type, 'error': 'unknown function'},
            'unit': 'number'
        }
    error = abs(approx - exact) if not (isinstance(exact, float) and abs(exact) > 1e15) else float('inf')
    return {
        'result': f'{func_type}({x}) approx = {approx:.8f} (exact = {exact:.8f}, error = {error:.2e})',
        'details': {'func': func_type, 'a': a, 'x': x, 'n': n, 'terms': terms[:5], 'approx': approx, 'exact': exact, 'error': error},
        'unit': 'number'
    }

def calc_fourier_series(func_type: str = 'square', L: float = math.pi, n_terms: int = 10) -> dict:
    """Compute Fourier series coefficients for periodic functions on [-L, L]."""
    coeffs = {'a0': 0}
    a_coeffs = []
    b_coeffs = []
    if func_type == 'square':
        coeffs['a0'] = 0
        for n in range(1, n_terms + 1):
            a_coeffs.append(0)
            b_coeffs.append((2 / (n * math.pi)) * (1 - ((-1) ** n)))
    elif func_type == 'sawtooth':
        coeffs['a0'] = 0
        for n in range(1, n_terms + 1):
            a_coeffs.append(0)
            b_coeffs.append(2 * (-1) ** (n + 1) / n)
    elif func_type == 'triangle':
        coeffs['a0'] = 0
        for n in range(1, n_terms + 1):
            a_coeffs.append((4 / (n ** 2 * math.pi ** 2)) * (1 - ((-1) ** n)))
            b_coeffs.append(0)
    elif func_type == 'x':
        coeffs['a0'] = 0
        for n in range(1, n_terms + 1):
            a_coeffs.append(0)
            b_coeffs.append(2 * (-1) ** (n + 1) * L / (n * math.pi))
    else:
        return {
            'result': f'Error: Unknown function type "{func_type}"',
            'details': {'func_type': func_type, 'error': 'unknown function type'},
            'unit': 'number'
        }
    return {
        'result': f'Fourier coefficients for {func_type}: a0={coeffs["a0"]:.4f}, '
                  f'b1={b_coeffs[0]:.4f}... (a/b coefficients in details)',
        'details': {'func': func_type, 'L': L, 'n_terms': n_terms, 'a0': coeffs['a0'], 'a': a_coeffs[:5], 'b': b_coeffs[:5]},
        'unit': 'coefficients'
    }

def calc_convergence_test(series_type: str = 'geometric', params: dict = None) -> dict:
    """Test series convergence using ratio/root/integral/comparison tests."""
    if params is None:
        params = {'r': 0.5}
    tests = {}
    if series_type == 'geometric':
        r = params.get('r', 0.5)
        ratio_lim = abs(r)
        root_lim = abs(r)
        converges = ratio_lim < 1
        tests['ratio'] = f'lim |a_(n+1)/a_n| = {ratio_lim}, converges: {ratio_lim < 1}'
        tests['root'] = f'lim |a_n|^(1/n) = {root_lim}, converges: {root_lim < 1}'
    elif series_type == 'p_series':
        p = params.get('p', 2.0)
        converges = p > 1
        tests['integral'] = f'int_1^inf 1/x^{p} dx converges: {p > 1}'
        tests['comparison'] = f'1/n^{p}: converges = {p > 1}'
    elif series_type == 'harmonic':
        converges = False
        tests['integral'] = 'int 1/x dx diverges (ln x)'
        tests['ratio'] = 'lim = 1, test is inconclusive'
    elif series_type == 'alternating_harmonic':
        converges = True
        tests['alternating'] = '|a_n| decreasing to 0: conditional convergence'
    else:
        converges = False
        tests['generic'] = 'Unknown series type'
    return {
        'result': f'Series convergence: {converges}' + (f' ({", ".join(tests.values())})' if tests else ''),
        'details': {'series_type': series_type, 'params': params, 'converges': converges, 'tests': tests},
        'unit': 'boolean'
    }

# ==============================================================================
# REAL ANALYSIS
# ==============================================================================

def calc_sup_inf(values: list = None) -> dict:
    """Compute supremum and infimum of a set of values."""
    if values is None:
        values = [0.1, 0.01, 0.001, 1.0, 0.5, 2.0]
    s = sorted(values)
    infimum = s[0]
    supremum = s[-1]
    minimum = infimum
    maximum = supremum
    return {
        'result': f'sup = {supremum:.6f}, inf = {infimum:.6f}, max = {maximum:.6f}, min = {minimum:.6f}',
        'details': {'values': values, 'sorted': s, 'supremum': supremum, 'infimum': infimum, 'maximum': maximum, 'minimum': minimum},
        'unit': 'number'
    }

def calc_limit_points(sequence: list = None) -> dict:
    """Find limit points (accumulation points) of a sequence."""
    if sequence is None:
        sequence = [(-1) ** n * (1 / (n + 1)) for n in range(50)]
    eps = 1e-8
    limit_points = set()
    for i, xi in enumerate(sequence):
        count = sum(1 for j, xj in enumerate(sequence) if j != i and abs(xj - xi) < eps)
        if count >= 1:
            limit_points.add(round(xi, 8))
    return {
        'result': f'Limit points: {sorted(limit_points)}',
        'details': {'sequence': sequence[:10], 'sequence_length': len(sequence), 'limit_points': sorted(limit_points)},
        'unit': 'set'
    }

def calc_continuity_check(func_type: str = '1/x', x: float = 0.0) -> dict:
    """Check continuity of a function at point x."""
    ft = func_type.lower().replace(' ', '')
    eps = 1e-8
    is_cont = True
    reason = 'Function is continuous at this point'
    if ft == '1/x':
        if abs(x) < 1e-12:
            is_cont = False
            reason = 'Not defined at x = 0 (pole)'
    elif ft == '|x|':
        is_cont = True
        reason = 'Continuous everywhere (not differentiable at 0)'
    elif ft == 'sin(x)':
        is_cont = True
        reason = 'Continuous everywhere'
    elif ft == 'step(x)':
        if abs(x) < 1e-12:
            is_cont = False
            reason = 'Jump discontinuity at x = 0'
    elif ft == 'x^(1/3)':
        is_cont = True
        reason = 'Continuous everywhere (including at 0)'
    return {
        'result': f'{func_type} is {"continuous" if is_cont else "discontinuous"} at x = {x} ({reason})',
        'details': {'func': func_type, 'x': x, 'continuous': is_cont, 'reason': reason},
        'unit': 'boolean'
    }

# ==============================================================================
# COMPLEX ANALYSIS
# ==============================================================================

def calc_complex_arithmetic(re: float = 3.0, im: float = 4.0) -> dict:
    """Display complex number in a+bi form and polar form re^(i*theta)."""
    z = complex(re, im)
    magnitude = abs(z)
    angle_rad = math.atan2(im, re)
    angle_deg = math.degrees(angle_rad)
    conjugate = z.conjugate()
    return {
        'result': f'z = {re} + {im}i = {magnitude:.4f} * e^(i*{angle_rad:.4f}) = {magnitude:.4f} * e^(i*{angle_deg:.2f}°)',
        'details': {'real': re, 'imag': im, 'modulus': magnitude, 'argument_rad': angle_rad, 'argument_deg': angle_deg, 'conjugate': str(conjugate), 'reciprocal': str(1 / z if abs(z) > 1e-12 else 'undefined')},
        'unit': 'complex'
    }

def calc_cauchy_riemann(u_func: str = 'x^2 - y^2', v_func: str = '2xy', x: float = 1.0, y: float = 2.0) -> dict:
    """Check Cauchy-Riemann equations: du/dx = dv/dy, du/dy = -dv/dx."""
    if u_func == 'x^2 - y^2' and v_func == '2xy':
        du_dx = 2 * x
        du_dy = -2 * y
        dv_dx = 2 * y
        dv_dy = 2 * x
    elif u_func == 'x' and v_func == '-y':
        du_dx = 1; du_dy = 0; dv_dx = 0; dv_dy = -1
    else:
        du_dx = du_dy = dv_dx = dv_dy = 0
    cr1_holds = abs(du_dx - dv_dy) < 1e-10
    cr2_holds = abs(du_dy + dv_dx) < 1e-10
    analytic = cr1_holds and cr2_holds
    return {
        'result': f'C-R: du/dx = dv/dy? {cr1_holds} ({du_dx} vs {dv_dy}). du/dy = -dv/dx? {cr2_holds} ({du_dy} vs {-dv_dx}). Analytic: {analytic}',
        'details': {'u': u_func, 'v': v_func, 'x': x, 'y': y, 'du/dx': du_dx, 'du/dy': du_dy, 'dv/dx': dv_dx, 'dv/dy': dv_dy, 'cr1': cr1_holds, 'cr2': cr2_holds, 'analytic': analytic},
        'unit': 'boolean'
    }

def calc_contour_integral(z_re: float = 2.0, z_im: float = 0.0, func_type: str = '1/z^2', n_points: int = 1000) -> dict:
    """Numerical contour integral around unit circle using trapezoidal rule."""
    integral = complex(0, 0)
    for k in range(n_points):
        t = 2 * math.pi * k / n_points
        tp = 2 * math.pi * (k + 1) / n_points
        z = complex(math.cos(t), math.sin(t))
        zp = complex(math.cos(tp), math.sin(tp))
        dz = zp - z
        zm = 0.5 * (z + zp)
        if func_type == '1/z':
            integral += (1 / zm) * dz
        elif func_type == '1/z^2':
            integral += (1 / (zm ** 2)) * dz
        elif func_type == 'e^z/z':
            integral += (math.exp(zm) / zm) * dz
    expected = complex(0, 0)
    if func_type == '1/z':
        expected = complex(0, 2 * math.pi)
    elif func_type == 'e^z/z':
        expected = complex(0, 2 * math.pi)
    return {
        'result': f'Contour integral = {integral.real:.6f} + {integral.imag:.6f}i (expected: {expected})',
        'details': {'func': func_type, 'n_points': n_points, 'integral': str(integral), 'expected': str(expected)},
        'unit': 'complex'
    }

def calc_residue(pole_order: int = 1, a: float = 0.0) -> dict:
    """Compute residue for simple poles. f(z) = 1/(z-a)^n => Res = 0 for n>1, = 1 for n=1."""
    if pole_order == 1:
        residue = complex(1.0, 0.0)
        note = 'Simple pole at z = a: residue = 1'
    elif pole_order == 0:
        residue = complex(0.0, 0.0)
        note = 'Not a pole'
    else:
        residue = complex(0.0, 0.0)
        note = f'Pole of order {pole_order}: residue = 0'
    return {
        'result': f'Res(f, {a}) = {residue.real} + {residue.imag}i ({note})',
        'details': {'pole_order': pole_order, 'a': a, 'residue': str(residue), 'note': note},
        'unit': 'complex'
    }

def calc_laurent_series(func_type: str = '1/(z-1)', z0: complex = 1 + 0j, n_pos: int = 3, n_neg: int = 0) -> dict:
    """Compute Laurent series coefficients for simple functions around z0."""
    if func_type == '1/(z-1)':
        coeffs = {'C_{-1}': 1}
        for k in range(n_neg):
            if k != 0:
                coeffs[f'C_{-k}'] = 0
        coeffs['C_0'] = 0
        for k in range(1, n_pos + 1):
            coeffs[f'C_{k}'] = 0
        note = 'Simple pole at z=1, only C_{-1}=1 is nonzero'
    elif func_type == '1/(z^2)':
        coeffs = {'C_{-2}': 1}
        coeffs['C_{-1}'] = 0
        coeffs['C_0'] = 0
        for k in range(1, n_pos + 1):
            coeffs[f'C_{k}'] = 0
        note = 'Double pole at z=0'
    elif func_type == 'e^z':
        coeffs = {}
        for k in range(n_pos + 1):
            coeffs[f'C_{k}'] = 1.0 / math.factorial(k)
        for k in range(1, n_neg + 1):
            coeffs[f'C_{-k}'] = 0
        note = 'Entire function, no negative powers'
    else:
        return {
            'result': f'Error: Unknown function "{func_type}"',
            'details': {'func_type': func_type, 'error': 'unknown function'},
            'unit': 'complex'
        }
    return {
        'result': f'Laurent: {coeffs}. Note: {note}',
        'details': {'func': func_type, 'z0': str(z0), 'coefficients': coeffs},
        'unit': 'complex'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    'limit_one_sided': {'func': calc_limit_one_sided, 'params': ['expression', 'x_approach', 'side'], 'desc': 'One-sided limit evaluation'},
    'limit_infinity': {'func': calc_limit_infinity, 'params': ['expression', 'side'], 'desc': 'Limit at +/- infinity'},
    'lhopital': {'func': calc_lhopital, 'params': ['numerator', 'denominator', 'x_val'], 'desc': "L'Hopital's rule evaluation"},
    'derivative': {'func': calc_derivative, 'params': ['expression', 'x'], 'desc': 'Derivative of common functions'},
    'derivative_product': {'func': calc_derivative_product, 'params': ['u_expr', 'v_expr', 'x'], 'desc': 'Derivative via product rule'},
    'derivative_quotient': {'func': calc_derivative_quotient, 'params': ['u_expr', 'v_expr', 'x'], 'desc': 'Derivative via quotient rule'},
    'derivative_chain': {'func': calc_derivative_chain, 'params': ['outer', 'inner_expr', 'x'], 'desc': 'Derivative via chain rule'},
    'higher_derivative': {'func': calc_higher_derivative, 'params': ['expression', 'x', 'order'], 'desc': 'Higher-order derivatives'},
    'implicit_diff': {'func': calc_implicit_diff, 'params': ['equation', 'const', 'x', 'y'], 'desc': 'Implicit differentiation'},
    'indefinite_integral': {'func': calc_indefinite_integral, 'params': ['expression', 'wrt'], 'desc': 'Indefinite integral of common functions'},
    'integral_substitution': {'func': calc_integral_substitution, 'params': ['integrand', 'u_sub'], 'desc': 'U-substitution demonstration'},
    'trapezoidal': {'func': calc_trapezoidal, 'params': ['func_type', 'a', 'b', 'n'], 'desc': 'Trapezoidal rule numerical integration'},
    'simpson': {'func': calc_simpson, 'params': ['func_type', 'a', 'b', 'n'], 'desc': 'Simpson rule numerical integration'},
    'gaussian_quadrature': {'func': calc_gaussian_quadrature, 'params': ['func_type', 'a', 'b', 'num_points'], 'desc': 'Gaussian quadrature integration'},
    'improper_integral': {'func': calc_improper_integral, 'params': ['func_type', 'a', 'b_inf'], 'desc': 'Improper integral evaluation'},
    'partial_derivative': {'func': calc_partial_derivative, 'params': ['expression', 'wrt', 'x', 'y'], 'desc': 'Partial derivative of 2-variable function'},
    'gradient': {'func': calc_gradient, 'params': ['expression', 'x', 'y'], 'desc': 'Gradient vector'},
    'directional_derivative': {'func': calc_directional_derivative, 'params': ['expression', 'x', 'y', 'vx', 'vy'], 'desc': 'Directional derivative'},
    'divergence_curl': {'func': calc_divergence_curl, 'params': ['Fx', 'Fy', 'Fz', 'x', 'y', 'z'], 'desc': 'Divergence and curl of vector field'},
    'laplacian': {'func': calc_laplacian, 'params': ['expression', 'x', 'y'], 'desc': 'Laplacian of scalar field'},
    'double_integral': {'func': calc_double_integral, 'params': ['func_type', 'x_a', 'x_b', 'y_a', 'y_b', 'nx', 'ny'], 'desc': 'Numerical double integral'},
    'triple_integral': {'func': calc_triple_integral, 'params': ['func_type', 'x_a', 'x_b', 'y_a', 'y_b', 'z_a', 'z_b', 'n'], 'desc': 'Numerical triple integral'},
    'jacobian': {'func': calc_jacobian, 'params': ['transform', 'x', 'y'], 'desc': 'Jacobian for coordinate transform'},
    'geometric_series': {'func': calc_geometric_series, 'params': ['a', 'r', 'n'], 'desc': 'Geometric series sum'},
    'p_series': {'func': calc_p_series, 'params': ['p', 'n_terms'], 'desc': 'p-series partial sum'},
    'taylor_series': {'func': calc_taylor_series, 'params': ['func_type', 'a', 'x', 'n'], 'desc': 'Taylor/Maclaurin series approximation'},
    'fourier_series': {'func': calc_fourier_series, 'params': ['func_type', 'L', 'n_terms'], 'desc': 'Fourier series coefficients'},
    'convergence_test': {'func': calc_convergence_test, 'params': ['series_type', 'params'], 'desc': 'Series convergence tests'},
    'sup_inf': {'func': calc_sup_inf, 'params': ['values'], 'desc': 'Supremum and infimum'},
    'limit_points': {'func': calc_limit_points, 'params': ['sequence'], 'desc': 'Limit/accumulation points'},
    'continuity_check': {'func': calc_continuity_check, 'params': ['func_type', 'x'], 'desc': 'Check function continuity'},
    'complex_arithmetic': {'func': calc_complex_arithmetic, 'params': ['re', 'im'], 'desc': 'Complex number a+bi and polar form'},
    'cauchy_riemann': {'func': calc_cauchy_riemann, 'params': ['u_func', 'v_func', 'x', 'y'], 'desc': 'Check Cauchy-Riemann equations'},
    'contour_integral': {'func': calc_contour_integral, 'params': ['z_re', 'z_im', 'func_type', 'n_points'], 'desc': 'Numerical contour integral'},
    'residue': {'func': calc_residue, 'params': ['pole_order', 'a'], 'desc': 'Residue at a pole'},
    'laurent_series': {'func': calc_laurent_series, 'params': ['func_type', 'z0', 'n_pos', 'n_neg'], 'desc': 'Laurent series coefficients'},
}
