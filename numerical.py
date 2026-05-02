"""
Numerical Methods & Engineering Mathematics - Computation Module
"""
import math
from decimal import Decimal, getcontext
from fractions import Fraction

COMMANDS = {}

# ============================================================
# Root Finding
# ============================================================

def calc_bisection(f_expr: str = 'x**3 - x - 2', a: float = 1.0, b: float = 2.0,
                   tol: float = 1e-6, max_iter: int = 100) -> dict:
    """Bisection method for root finding."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    fa = eval(f_expr, {**ctx, 'x': a})
    fb = eval(f_expr, {**ctx, 'x': b})
    if fa * fb > 0:
        return {
            'result': f'f(a)*f(b) > 0, no sign change in [{a}, {b}]',
            'details': {'a': a, 'b': b, 'f(a)': fa, 'f(b)': fb, 'converged': False},
            'unit': 'dimensionless'
        }
    history = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = eval(f_expr, {**ctx, 'x': c})
        history.append({'iter': i, 'a': a, 'b': b, 'c': c, 'f(c)': fc, 'interval': b - a})
        if abs(fc) < tol or (b - a) / 2 < tol:
            break
        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc
    return {
        'result': f'Root: x = {c:.10f}, f(x) = {fc:.2e}',
        'details': {
            'f': f_expr, 'interval': [a, b], 'root': c, 'f_root': fc,
            'iterations': len(history), 'tolerance': tol, 'converged': abs(fc) < tol or (b - a) < tol
        },
        'unit': 'dimensionless'
    }

def calc_newton_raphson(f_expr: str = 'x**3 - x - 2',
                        fprime_expr: str = '3*x**2 - 1',
                        x0: float = 1.5, tol: float = 1e-8, max_iter: int = 50) -> dict:
    """Newton-Raphson method: x_{n+1} = x_n - f(x_n)/f'(x_n)."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    x = x0
    history = []
    for i in range(max_iter):
        fx = eval(f_expr, {**ctx, 'x': x})
        fpx = eval(fprime_expr, {**ctx, 'x': x})
        history.append({'iter': i, 'x': x, 'f(x)': fx, "f'(x)": fpx})
        if abs(fpx) < 1e-15:
            return {
                'result': f'Derivative near zero at x={x}, method failed',
                'details': {'x': x, 'f(x)': fx, "f'(x)": fpx, 'converged': False},
                'unit': 'dimensionless'
            }
        x_new = x - fx / fpx
        if abs(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    fx_final = eval(f_expr, {**ctx, 'x': x})
    return {
        'result': f'Root: x = {x:.10f}, f(x) = {fx_final:.2e}',
        'details': {
            'f': f_expr, "f'": fprime_expr, 'x0': x0,
            'root': x, 'f_root': fx_final,
            'iterations': len(history), 'tolerance': tol,
            'converged': abs(fx_final) < tol,
            'convergence_order': 2  # Quadratic for simple roots
        },
        'unit': 'dimensionless'
    }

def calc_secant(f_expr: str = 'x**3 - x - 2', x0: float = 1.0, x1: float = 2.0,
                tol: float = 1e-8, max_iter: int = 50) -> dict:
    """Secant method for root finding (no derivative needed)."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    x_prev, x_curr = x0, x1
    f_prev = eval(f_expr, {**ctx, 'x': x_prev})
    history = []
    for i in range(max_iter):
        f_curr = eval(f_expr, {**ctx, 'x': x_curr})
        history.append({'iter': i, 'x': x_curr, 'f(x)': f_curr})
        if abs(f_curr) < tol:
            break
        if abs(f_curr - f_prev) < 1e-15:
            return {
                'result': 'Division by near-zero in secant step',
                'details': {'converged': False},
                'unit': 'dimensionless'
            }
        x_new = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        if abs(x_new - x_curr) < tol:
            x_prev, x_curr = x_curr, x_new
            break
        x_prev, x_curr = x_curr, x_new
        f_prev = f_curr
    return {
        'result': f'Root: x = {x_curr:.10f}, f(x) = {f_curr:.2e}',
        'details': {
            'f': f_expr, 'x0': x0, 'x1': x1,
            'root': x_curr, 'f_root': f_curr,
            'iterations': len(history), 'tolerance': tol,
            'converged': abs(f_curr) < tol,
            'convergence_order': 1.618  # Golden ratio
        },
        'unit': 'dimensionless'
    }

def calc_fixed_point(g_expr: str = 'math.cos(x)', x0: float = 0.5,
                     tol: float = 1e-8, max_iter: int = 100) -> dict:
    """Fixed-point iteration: x_{n+1} = g(x_n)."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    x = x0
    history = []
    for i in range(max_iter):
        x_new = eval(g_expr, {**ctx, 'x': x})
        history.append({'iter': i, 'x': x, 'x_new': x_new, 'diff': abs(x_new - x)})
        if abs(x_new - x) < tol:
            x = x_new
            break
        x = x_new
    return {
        'result': f'Fixed point: x = {x:.10f}, g(x) = {x:.10f}',
        'details': {
            'g': g_expr, 'x0': x0,
            'fixed_point': x,
            'iterations': len(history), 'tolerance': tol,
            'converged': abs(x - eval(g_expr, {**ctx, 'x': x})) < tol
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Numerical Differentiation
# ============================================================

def calc_numerical_derivative(f_expr: str = 'x**3', x: float = 2.0,
                              h: float = 0.01) -> dict:
    """Numerical differentiation: forward, backward, central differences."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    fx = eval(f_expr, {**ctx, 'x': x})
    fx_ph = eval(f_expr, {**ctx, 'x': x + h})
    fx_mh = eval(f_expr, {**ctx, 'x': x - h})
    forward = (fx_ph - fx) / h
    backward = (fx - fx_mh) / h
    central = (fx_ph - fx_mh) / (2 * h)
    return {
        'result': f"f'(x) via central: {central:.6f}, forward: {forward:.6f}, backward: {backward:.6f}",
        'details': {
            'f': f_expr, 'x': x, 'h': h,
            'forward_diff': forward, 'backward_diff': backward,
            'central_diff': central,
            'forward_error_O': 'O(h)',
            'central_error_O': 'O(h^2)'
        },
        'unit': 'dimensionless'
    }

def calc_second_derivative(f_expr: str = 'x**3', x: float = 2.0,
                           h: float = 0.01) -> dict:
    """Second derivative using central finite difference: f''(x) ≈ [f(x+h)-2f(x)+f(x-h)]/h²."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    fx = eval(f_expr, {**ctx, 'x': x})
    fx_ph = eval(f_expr, {**ctx, 'x': x + h})
    fx_mh = eval(f_expr, {**ctx, 'x': x - h})
    d2 = (fx_ph - 2 * fx + fx_mh) / (h * h)
    return {
        'result': f"f''({x}) = {d2:.6f}",
        'details': {
            'f': f_expr, 'x': x, 'h': h,
            'second_derivative': d2,
            'error_O': 'O(h^2)'
        },
        'unit': 'dimensionless'
    }

def calc_richardson_extrapolation(f_expr: str = 'x**2', x: float = 1.0,
                                  h: float = 0.1) -> dict:
    """Richardson extrapolation for derivative: D = (4*D(h/2) - D(h))/3."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    def D(step):
        fx_ph = eval(f_expr, {**ctx, 'x': x + step})
        fx_mh = eval(f_expr, {**ctx, 'x': x - step})
        return (fx_ph - fx_mh) / (2 * step)
    D_h = D(h)
    D_h2 = D(h / 2)
    D_richardson = (4 * D_h2 - D_h) / 3
    return {
        'result': f"f'({x}) = {D_richardson:.10f} (Richardson), D(h)={D_h:.6f}, D(h/2)={D_h2:.6f}",
        'details': {
            'f': f_expr, 'x': x, 'h': h,
            'D_h': D_h, 'D_h2': D_h2,
            'richardson': D_richardson,
            'formula': '(4*D(h/2) - D(h))/3'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Numerical Integration
# ============================================================

def calc_trapezoidal(f_expr: str = 'x**2', a: float = 0.0, b: float = 1.0,
                     n: int = 100) -> dict:
    """Trapezoidal rule for numerical integration."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    h = (b - a) / n
    x_vals = [a + i * h for i in range(n + 1)]
    f_vals = [eval(f_expr, {**ctx, 'x': xi}) for xi in x_vals]
    integral = h * (0.5 * f_vals[0] + sum(f_vals[1:-1]) + 0.5 * f_vals[-1])
    return {
        'result': f'Integral = {integral:.8f} (trapezoidal, n={n})',
        'details': {
            'f': f_expr, 'a': a, 'b': b, 'n': n, 'h': h,
            'integral': integral,
            'error_O': 'O(h^2)'
        },
        'unit': 'dimensionless'
    }

def calc_simpson_13(f_expr: str = 'x**2', a: float = 0.0, b: float = 1.0,
                    n: int = 100) -> dict:
    """Simpson's 1/3 rule (n must be even)."""
    if n % 2 != 0:
        n += 1
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    h = (b - a) / n
    x_vals = [a + i * h for i in range(n + 1)]
    f_vals = [eval(f_expr, {**ctx, 'x': xi}) for xi in x_vals]
    integral = (h / 3) * (f_vals[0] + f_vals[-1] +
                          4 * sum(f_vals[1:-1:2]) +
                          2 * sum(f_vals[2:-1:2]))
    return {
        'result': f'Integral = {integral:.8f} (Simpson 1/3, n={n})',
        'details': {
            'f': f_expr, 'a': a, 'b': b, 'n': n, 'h': h,
            'integral': integral,
            'error_O': 'O(h^4)'
        },
        'unit': 'dimensionless'
    }

def calc_simpson_38(f_expr: str = 'x**2', a: float = 0.0, b: float = 1.0,
                    n: int = 99) -> dict:
    """Simpson's 3/8 rule (n must be multiple of 3)."""
    while n % 3 != 0:
        n += 1
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    h = (b - a) / n
    x_vals = [a + i * h for i in range(n + 1)]
    f_vals = [eval(f_expr, {**ctx, 'x': xi}) for xi in x_vals]
    integral = (3 * h / 8) * (f_vals[0] + f_vals[-1] +
                              3 * sum(f_vals[i] for i in range(1, n) if i % 3 != 0) +
                              2 * sum(f_vals[i] for i in range(3, n - 1, 3)))
    return {
        'result': f'Integral = {integral:.8f} (Simpson 3/8, n={n})',
        'details': {
            'f': f_expr, 'a': a, 'b': b, 'n': n, 'h': h,
            'integral': integral,
            'error_O': 'O(h^4)'
        },
        'unit': 'dimensionless'
    }

def calc_romberg(f_expr: str = 'x**2', a: float = 0.0, b: float = 1.0,
                 max_level: int = 5) -> dict:
    """Romberg integration using Richardson extrapolation."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    R = [[0.0] * (max_level + 1) for _ in range(max_level + 1)]
    # R[0][0]: trapezoidal with 1 interval
    h = b - a
    fa = eval(f_expr, {**ctx, 'x': a})
    fb = eval(f_expr, {**ctx, 'x': b})
    R[0][0] = 0.5 * h * (fa + fb)
    for k in range(1, max_level + 1):
        # Trapezoidal with 2^k intervals
        h /= 2
        n = 2 ** k
        sum_mid = 0.0
        for i in range(1, n, 2):
            xi = a + i * h
            sum_mid += eval(f_expr, {**ctx, 'x': xi})
        R[k][0] = 0.5 * R[k - 1][0] + h * sum_mid
        # Richardson extrapolation
        for j in range(1, k + 1):
            R[k][j] = R[k][j - 1] + (R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)
    return {
        'result': f'Integral = {R[max_level][max_level]:.12f} (Romberg, level {max_level})',
        'details': {
            'f': f_expr, 'a': a, 'b': b,
            'integral': R[max_level][max_level],
            'romberg_table': R,
            'max_level': max_level
        },
        'unit': 'dimensionless'
    }

def calc_gaussian_quadrature(f_expr: str = 'x**2', a: float = -1.0, b: float = 1.0,
                             n: int = 5) -> dict:
    """Gaussian quadrature (Gauss-Legendre) with n points."""
    # Precomputed Gauss-Legendre nodes and weights for n=2,3,4,5
    gauss_data = {
        2: {'nodes': [-0.5773502691896257, 0.5773502691896257],
            'weights': [1.0, 1.0]},
        3: {'nodes': [-0.7745966692414834, 0.0, 0.7745966692414834],
            'weights': [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]},
        4: {'nodes': [-0.8611363115940526, -0.3399810435848563, 0.3399810435848563, 0.8611363115940526],
            'weights': [0.3478548451374538, 0.6521451548625461, 0.6521451548625461, 0.3478548451374538]},
        5: {'nodes': [-0.9061798459386640, -0.5384693101056831, 0.0, 0.5384693101056831, 0.9061798459386640],
            'weights': [0.2369268850561891, 0.4786286704993665, 0.5688888888888889, 0.4786286704993665, 0.2369268850561891]},
    }
    if n not in gauss_data:
        n = 5  # default
    data = gauss_data[n]
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    # Transform from [-1,1] to [a,b]
    mid = (b + a) / 2
    half_len = (b - a) / 2
    integral = 0.0
    for xi, wi in zip(data['nodes'], data['weights']):
        x_mapped = mid + half_len * xi
        integral += wi * eval(f_expr, {**ctx, 'x': x_mapped})
    integral *= half_len
    return {
        'result': f'Integral = {integral:.12f} (Gauss-Legendre, {n} points)',
        'details': {
            'f': f_expr, 'a': a, 'b': b, 'n': n,
            'integral': integral,
            'nodes': data['nodes'], 'weights': data['weights']
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Interpolation
# ============================================================

def calc_lagrange_interpolation(x_points: list = None, y_points: list = None,
                                x_eval: float = None) -> dict:
    """Lagrange polynomial interpolation."""
    if x_points is None:
        x_points = [0, 1, 2, 3]
    if y_points is None:
        y_points = [1, 2, 0, 3]
    if x_eval is None:
        x_eval = 1.5
    n = len(x_points)
    if n != len(y_points):
        return {'result': 'x and y must have same length', 'details': {}, 'unit': 'dimensionless'}
    # Evaluate at x_eval
    result = 0.0
    basis_vals = []
    for i in range(n):
        term = y_points[i]
        basis = 1.0
        for j in range(n):
            if i != j:
                term *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
                basis *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
        result += term
        basis_vals.append(basis)
    return {
        'result': f'P({x_eval}) = {result:.6f}',
        'details': {
            'x_points': x_points, 'y_points': y_points, 'x_eval': x_eval,
            'interpolated': result,
            'basis_values': basis_vals
        },
        'unit': 'dimensionless'
    }

def calc_newton_divided_diff(x_points: list = None, y_points: list = None,
                             x_eval: float = None) -> dict:
    """Newton's divided difference interpolation."""
    if x_points is None:
        x_points = [0, 1, 2, 3]
    if y_points is None:
        y_points = [1, 2, 0, 3]
    if x_eval is None:
        x_eval = 1.5
    n = len(x_points)
    # Build divided difference table
    dd = [[0.0] * n for _ in range(n)]
    for i in range(n):
        dd[i][0] = y_points[i]
    for j in range(1, n):
        for i in range(n - j):
            dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / (x_points[i + j] - x_points[i])
    # Evaluate
    result = dd[0][0]
    product = 1.0
    terms = [dd[0][0]]
    for j in range(1, n):
        product *= (x_eval - x_points[j - 1])
        result += dd[0][j] * product
        terms.append(dd[0][j] * product)
    return {
        'result': f'P({x_eval}) = {result:.6f}',
        'details': {
            'x_points': x_points, 'y_points': y_points, 'x_eval': x_eval,
            'interpolated': result,
            'divided_diff_table': dd,
            'coefficients': [dd[0][j] for j in range(n)]
        },
        'unit': 'dimensionless'
    }

def calc_cubic_spline(x_points: list = None, y_points: list = None,
                      x_eval: float = None) -> dict:
    """Natural cubic spline interpolation."""
    if x_points is None:
        x_points = [0, 1, 2, 3]
    if y_points is None:
        y_points = [1, 2, 0, 3]
    if x_eval is None:
        x_eval = 1.5
    n = len(x_points) - 1
    h = [x_points[i + 1] - x_points[i] for i in range(n)]
    # Solve tridiagonal system for second derivatives
    alpha = [0.0] * (n + 1)
    for i in range(1, n):
        alpha[i] = (3 / h[i]) * (y_points[i + 1] - y_points[i]) - (3 / h[i - 1]) * (y_points[i] - y_points[i - 1])
    l = [1.0] * (n + 1)
    mu = [0.0] * (n + 1)
    z = [0.0] * (n + 1)
    for i in range(1, n):
        l[i] = 2 * (x_points[i + 1] - x_points[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]
    l[n] = 1.0
    z[n] = 0.0
    c = [0.0] * (n + 1)
    b = [0.0] * n
    d = [0.0] * n
    for j in range(n - 1, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b[j] = (y_points[j + 1] - y_points[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
        d[j] = (c[j + 1] - c[j]) / (3 * h[j])
    # Find which interval x_eval belongs to
    idx = 0
    for i in range(n):
        if x_points[i] <= x_eval <= x_points[i + 1]:
            idx = i
            break
    dx = x_eval - x_points[idx]
    result = y_points[idx] + b[idx] * dx + c[idx] * dx * dx + d[idx] * dx * dx * dx
    return {
        'result': f'S({x_eval}) = {result:.6f} (cubic spline)',
        'details': {
            'x_points': x_points, 'y_points': y_points, 'x_eval': x_eval,
            'interpolated': result,
            'coeffs': {'a': y_points, 'b': b, 'c': c, 'd': d},
            'interval': idx
        },
        'unit': 'dimensionless'
    }

def calc_linear_interpolation(x_points: list = None, y_points: list = None,
                              x_eval: float = None) -> dict:
    """Linear (piecewise) interpolation."""
    if x_points is None:
        x_points = [0, 1, 2, 3]
    if y_points is None:
        y_points = [1, 2, 0, 3]
    if x_eval is None:
        x_eval = 1.5
    n = len(x_points)
    if x_eval <= x_points[0]:
        result = y_points[0]
    elif x_eval >= x_points[-1]:
        result = y_points[-1]
    else:
        for i in range(n - 1):
            if x_points[i] <= x_eval <= x_points[i + 1]:
                t = (x_eval - x_points[i]) / (x_points[i + 1] - x_points[i])
                result = y_points[i] + t * (y_points[i + 1] - y_points[i])
                break
    return {
        'result': f'f({x_eval}) = {result:.6f} (linear interpolation)',
        'details': {
            'x_points': x_points, 'y_points': y_points, 'x_eval': x_eval,
            'interpolated': result
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Curve Fitting
# ============================================================

def calc_polynomial_fit(x_data: list = None, y_data: list = None,
                        degree: int = 2) -> dict:
    """Polynomial least-squares fit using Vandermonde matrix (normal equations)."""
    if x_data is None:
        x_data = [0, 1, 2, 3, 4, 5]
    if y_data is None:
        y_data = [1, 2.1, 2.9, 4.2, 5.1, 5.9]
    n = len(x_data)
    m = degree + 1
    # Build Vandermonde-like normal equations: A^T A c = A^T y
    # A_ij = x_i^j
    A = [[x_data[i] ** j for j in range(m)] for i in range(n)]
    # A^T A
    ATA = [[sum(A[k][i] * A[k][j] for k in range(n)) for j in range(m)] for i in range(m)]
    # A^T y
    ATy = [sum(A[k][i] * y_data[k] for k in range(n)) for i in range(m)]
    # Solve linear system using Gaussian elimination
    coeffs = list(ATy)
    mat = [row[:] for row in ATA]
    for col in range(m):
        # Partial pivot
        max_row = max(range(col, m), key=lambda r: abs(mat[r][col]))
        if abs(mat[max_row][col]) < 1e-12:
            continue
        mat[col], mat[max_row] = mat[max_row], mat[col]
        coeffs[col], coeffs[max_row] = coeffs[max_row], coeffs[col]
        pivot = mat[col][col]
        for j in range(col, m):
            mat[col][j] /= pivot
        coeffs[col] /= pivot
        for i in range(m):
            if i != col and abs(mat[i][col]) > 1e-12:
                factor = mat[i][col]
                for j in range(col, m):
                    mat[i][j] -= factor * mat[col][j]
                coeffs[i] -= factor * coeffs[col]
    # Compute R^2
    y_mean = sum(y_data) / n
    ss_res = sum((y_data[i] - sum(coeffs[j] * x_data[i] ** j for j in range(m))) ** 2 for i in range(n))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y_data)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    eq_str = ' + '.join(f'{c:.4f}x^{i}' if i > 0 else f'{c:.4f}' for i, c in enumerate(coeffs))
    return {
        'result': f'y = {eq_str}, R^2 = {r2:.6f}',
        'details': {
            'x': x_data, 'y': y_data, 'degree': degree,
            'coefficients': [round(c, 6) for c in coeffs],
            'r_squared': r2,
            'ss_res': ss_res, 'ss_tot': ss_tot
        },
        'unit': 'dimensionless'
    }

def calc_exponential_fit(x_data: list = None, y_data: list = None) -> dict:
    """Exponential fit: y = a * exp(b*x) via log transform."""
    if x_data is None:
        x_data = [0, 1, 2, 3, 4]
    if y_data is None:
        y_data = [1.0, 2.7, 7.4, 20.1, 54.6]
    # log(y) = log(a) + b*x
    log_y = [math.log(yi) for yi in y_data if yi > 0]
    if len(log_y) < len(y_data):
        return {'result': 'Error: y values must be positive for log transform', 'details': {}, 'unit': 'dimensionless'}
    n = len(x_data)
    # Linear least squares on (x, log(y))
    sx = sum(x_data)
    sy = sum(log_y)
    sxx = sum(xi * xi for xi in x_data)
    sxy = sum(x_data[i] * log_y[i] for i in range(n))
    det = n * sxx - sx * sx
    if abs(det) < 1e-15:
        return {'result': 'Singular matrix, cannot fit', 'details': {}, 'unit': 'dimensionless'}
    b = (n * sxy - sx * sy) / det
    log_a = (sy - b * sx) / n
    a = math.exp(log_a)
    # R^2
    y_pred = [a * math.exp(b * xi) for xi in x_data]
    y_mean = sum(y_data) / n
    ss_res = sum((y_data[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y_data)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return {
        'result': f'y = {a:.4f} * exp({b:.4f}*x), R^2 = {r2:.6f}',
        'details': {
            'x': x_data, 'y': y_data,
            'a': a, 'b': b, 'r_squared': r2,
            'equation': f'y = {a:.6f} * e^({b:.6f} x)'
        },
        'unit': 'dimensionless'
    }

def calc_power_law_fit(x_data: list = None, y_data: list = None) -> dict:
    """Power law fit: y = a * x^b via log-log transform."""
    if x_data is None:
        x_data = [1, 2, 3, 4, 5]
    if y_data is None:
        y_data = [2.0, 5.6, 10.4, 16.0, 22.4]
    log_x = [math.log(xi) for xi in x_data if xi > 0]
    log_y = [math.log(yi) for yi in y_data if yi > 0]
    n = len(log_x)
    sx = sum(log_x)
    sy = sum(log_y)
    sxx = sum(xi * xi for xi in log_x)
    sxy = sum(log_x[i] * log_y[i] for i in range(n))
    det = n * sxx - sx * sx
    if abs(det) < 1e-15:
        return {'result': 'Singular matrix, cannot fit', 'details': {}, 'unit': 'dimensionless'}
    b = (n * sxy - sx * sy) / det
    log_a = (sy - b * sx) / n
    a = math.exp(log_a)
    y_pred = [a * xi ** b for xi in x_data]
    y_mean = sum(y_data) / n
    ss_res = sum((y_data[i] - y_pred[i]) ** 2 for i in range(n))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y_data)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return {
        'result': f'y = {a:.4f} * x^{b:.4f}, R^2 = {r2:.6f}',
        'details': {
            'x': x_data, 'y': y_data,
            'a': a, 'b': b, 'r_squared': r2,
            'equation': f'y = {a:.6f} * x^{b:.6f}'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Error Analysis
# ============================================================

def calc_error_analysis(true_value: float = 3.141592653589793,
                       approx_value: float = 3.14) -> dict:
    """Compute absolute, relative, and percentage errors."""
    abs_err = abs(approx_value - true_value)
    rel_err = abs_err / abs(true_value) if true_value != 0 else abs_err
    pct_err = rel_err * 100
    return {
        'result': f'Abs error = {abs_err:.2e}, Rel error = {rel_err:.2e} ({pct_err:.4f}%)',
        'details': {
            'true': true_value, 'approximation': approx_value,
            'absolute_error': abs_err, 'relative_error': rel_err,
            'percentage_error': pct_err
        },
        'unit': 'dimensionless'
    }

def calc_truncation_error(h: float = 0.1, order: float = 2.0) -> dict:
    """Estimate truncation error for step size h, given method order p: O(h^p)."""
    trunc = h ** order
    return {
        'result': f'Truncation error O(h^{order}) ~ {trunc:.2e} for h = {h}',
        'details': {
            'h': h, 'order': order, 'truncation_error_estimate': trunc,
            'formula': f'O(h^{order})'
        },
        'unit': 'dimensionless'
    }

def calc_error_propagation(vars_dict: dict = None,
                           funcs: dict = None) -> dict:
    """Error propagation: sigma_f^2 = sum((df/dx_i)^2 * sigma_i^2).
    vars_dict: {var_name: (value, uncertainty)}
    funcs: expression as string. Default: f = x*y + z."""
    if vars_dict is None:
        vars_dict = {'x': (10.0, 0.5), 'y': (5.0, 0.2), 'z': (2.0, 0.1)}
    # Default: f = x*y + z
    x, sx = vars_dict.get('x', (0, 0))
    y, sy = vars_dict.get('y', (0, 0))
    z, sz = vars_dict.get('z', (0, 0))
    # For f = x*y + z: df/dx = y, df/dy = x, df/dz = 1
    df_dx = y
    df_dy = x
    df_dz = 1.0
    sigma_f_sq = (df_dx * sx) ** 2 + (df_dy * sy) ** 2 + (df_dz * sz) ** 2
    sigma_f = math.sqrt(sigma_f_sq)
    f_val = x * y + z
    return {
        'result': f'f = {f_val:.4f} ± {sigma_f:.4f}',
        'details': {
            'function': 'f = x*y + z',
            'variables': vars_dict,
            'f_value': f_val,
            'partials': {'df/dx': df_dx, 'df/dy': df_dy, 'df/dz': df_dz},
            'contributions': {'x': (df_dx * sx) ** 2, 'y': (df_dy * sy) ** 2, 'z': (df_dz * sz) ** 2},
            'sigma_f_sq': sigma_f_sq, 'sigma_f': sigma_f
        },
        'unit': 'dimensionless'
    }

def calc_convergence_rate(errors: list = None) -> dict:
    """Estimate convergence rate from sequence of errors: p ≈ log(e_n/e_{n+1})/log(2)."""
    if errors is None:
        errors = [0.1, 0.025, 0.00625, 0.0015625]
    rates = []
    for i in range(len(errors) - 1):
        if errors[i + 1] > 0:
            rate = math.log(errors[i] / errors[i + 1]) / math.log(2)
            rates.append(rate)
    avg_rate = sum(rates) / len(rates) if rates else 0
    return {
        'result': f'Estimated convergence rate: {avg_rate:.2f} (per halving)',
        'details': {
            'errors': errors, 'rates': rates,
            'average_rate': avg_rate,
            'interpretation': f'~O(h^{avg_rate:.1f})'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# FEM Basics
# ============================================================

def calc_fem_bar_stiffness(E: float = 210e9, A: float = 0.01, L: float = 1.0) -> dict:
    """1D bar element stiffness matrix: K = (EA/L) * [[1, -1], [-1, 1]]."""
    k = E * A / L
    K = [[k, -k], [-k, k]]
    return {
        'result': f'Bar stiffness matrix (EA/L = {k:.2e}): [[{K[0][0]:.2e}, {K[0][1]:.2e}], [{K[1][0]:.2e}, {K[1][1]:.2e}]]',
        'details': {
            'E': E, 'A': A, 'L': L, 'EA/L': k,
            'stiffness_matrix': K,
            'formula': 'K = (EA/L) * [[1, -1], [-1, 1]]'
        },
        'unit': 'N/m'
    }

def calc_fem_heat_conduction(k: float = 50.0, L: float = 1.0) -> dict:
    """1D heat conduction element matrix: K = (k/L) * [[1, -1], [-1, 1]]."""
    ke = k / L
    K = [[ke, -ke], [-ke, ke]]
    return {
        'result': f'Heat conduction matrix (k/L = {ke:.2f}): [[{K[0][0]:.2f}, {K[0][1]:.2f}], [{K[1][0]:.2f}, {K[1][1]:.2f}]]',
        'details': {
            'k': k, 'L': L, 'k_over_L': ke,
            'conductivity_matrix': K,
            'formula': 'K = (k/L) * [[1, -1], [-1, 1]]'
        },
        'unit': 'W/(m^2*K)'
    }

def calc_fem_assemble_global(K1: list = None, K2: list = None,
                             num_nodes: int = 3) -> dict:
    """Assemble global stiffness matrix from 2 elements (3 nodes: 1-2, 2-3)."""
    if K1 is None:
        K1 = [[100, -100], [-100, 100]]
    if K2 is None:
        K2 = [[200, -200], [-200, 200]]
    K_global = [[0.0] * num_nodes for _ in range(num_nodes)]
    # Element 1: nodes 0-1
    for i in range(2):
        for j in range(2):
            K_global[i][j] += K1[i][j]
    # Element 2: nodes 1-2
    for i in range(2):
        for j in range(2):
            K_global[1 + i][1 + j] += K2[i][j]
    return {
        'result': f'Global matrix ({num_nodes}x{num_nodes}) assembled',
        'details': {
            'K1': K1, 'K2': K2,
            'element_connections': [[0, 1], [1, 2]],
            'K_global': K_global
        },
        'unit': 'N/m'
    }

# ============================================================
# FDM (Finite Difference Method)
# ============================================================

def calc_fdm_heat_1d(alpha: float = 0.01, L: float = 1.0, T_max: float = 0.1,
                     nx: int = 10, nx_method: int = None) -> dict:
    """1D heat equation du/dt = alpha * d^2u/dx^2, explicit scheme."""
    if nx_method is None:
        nx_method = nx
    dx = L / nx_method
    # CFL condition: dt <= 0.5 * dx^2 / alpha
    dt_max = 0.5 * dx * dx / alpha
    dt = dt_max * 0.9
    nt = int(T_max / dt)
    # Initial condition: u(x,0) = sin(pi*x/L)
    u = [math.sin(math.pi * i * dx / L) for i in range(nx_method + 1)]
    u_new = u[:]
    r = alpha * dt / (dx * dx)
    history = [u[:]]
    for _ in range(min(nt, 100)):
        for i in range(1, nx_method):
            u_new[i] = u[i] + r * (u[i + 1] - 2 * u[i] + u[i - 1])
        u_new[0] = 0  # Boundary
        u_new[nx_method] = 0
        u, u_new = u_new, u
        history.append(u[:])
    analytic = math.sin(math.pi * (L / 2) / L) * math.exp(-alpha * math.pi**2 * T_max / L**2)
    return {
        'result': f'Heat eq: u(L/2, {T_max}) = {u[nx_method // 2]:.6f} (analytic: {analytic:.6f})',
        'details': {
            'alpha': alpha, 'L': L, 'T_max': T_max,
            'nx': nx_method, 'dx': dx, 'dt': dt, 'nt': min(nt, 100),
            'r': r, 'CFL': r, 'CFL_satisfied': r <= 1.0,
            'u_mid_final': u[nx_method // 2],
            'analytic': analytic,
            'error': abs(u[nx_method // 2] - analytic)
        },
        'unit': 'temperature'
    }

def calc_fdm_wave_1d(c: float = 1.0, L: float = 1.0, T_max: float = 0.5,
                     nx: int = 50) -> dict:
    """1D wave equation d^2u/dt^2 = c^2 * d^2u/dx^2, explicit scheme."""
    dx = L / nx
    dt = 0.9 * dx / c  # CFL
    r = (c * dt / dx) ** 2
    nt = int(T_max / dt)
    # Initial conditions
    x_vals = [i * dx for i in range(nx + 1)]
    u_prev = [math.sin(math.pi * xi / L) for xi in x_vals]  # u(x,0)
    u_curr = u_prev[:]  # du/dt(x,0) = 0 => u(x,dt) = u(x,0)
    u_next = u_curr[:]
    for _ in range(min(nt, 200)):
        for i in range(1, nx):
            u_next[i] = 2 * u_curr[i] - u_prev[i] + r * (u_curr[i + 1] - 2 * u_curr[i] + u_curr[i - 1])
        u_next[0] = 0
        u_next[nx] = 0
        u_prev, u_curr, u_next = u_curr, u_next, u_prev
    return {
        'result': f'Wave eq: u(L/2, {T_max}) = {u_curr[nx // 2]:.6f}',
        'details': {
            'c': c, 'L': L, 'T_max': T_max,
            'nx': nx, 'dx': dx, 'dt': dt, 'r': r,
            'CFL': r, 'CFL_satisfied': r <= 1.0,
            'u_mid': u_curr[nx // 2]
        },
        'unit': 'displacement'
    }

def calc_poisson_2d(f_func: str = '-2*(x**2 + y**2 - x - y)', nx: int = 20, ny: int = 20) -> dict:
    """2D Poisson equation: d^2u/dx^2 + d^2u/dy^2 = f(x,y) using 5-point stencil.
    Domain: [0,1]x[0,1], u=0 on boundary, f(x,y) given."""
    hx = 1.0 / nx
    hy = 1.0 / ny
    hx2, hy2 = hx * hx, hy * hy
    u = [[0.0] * (ny + 1) for _ in range(nx + 1)]
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos}
    # Gauss-Seidel iteration
    for iteration in range(500):
        max_diff = 0.0
        for i in range(1, nx):
            for j in range(1, ny):
                x, y = i * hx, j * hy
                f_val = eval(f_func, {**ctx, 'x': x, 'y': y})
                u_new = ((u[i + 1][j] + u[i - 1][j]) / hx2 +
                         (u[i][j + 1] + u[i][j - 1]) / hy2 - f_val) / (2 / hx2 + 2 / hy2)
                max_diff = max(max_diff, abs(u_new - u[i][j]))
                u[i][j] = u_new
        if max_diff < 1e-8:
            break
    mid_val = u[nx // 2][ny // 2]
    return {
        'result': f'Poisson: u(0.5, 0.5) = {mid_val:.6f}',
        'details': {
            'f': f_func, 'nx': nx, 'ny': ny,
            'hx': hx, 'hy': hy,
            'u_center': mid_val,
            'iterations': iteration + 1,
            'stencil': '5-point'
        },
        'unit': 'dimensionless'
    }

def calc_cfl_condition(c: float = 1.0, dx: float = 0.1, scheme: str = 'explicit') -> dict:
    """Check CFL stability condition for explicit FDM schemes."""
    if scheme == 'explicit':
        dt_max = dx / c
    elif scheme == 'explicit_heat':
        dt_max = 0.5 * dx * dx / c
    elif scheme == 'explicit_wave':
        dt_max = dx / c
    else:
        dt_max = dx / c
    return {
        'result': f'CFL condition for {scheme}: dt <= {dt_max:.6f}',
        'details': {
            'c': c, 'dx': dx, 'scheme': scheme,
            'dt_max': dt_max,
            'condition': f'dt <= {dt_max:.6f}'
        },
        'unit': 'time'
    }

# ============================================================
# High Precision
# ============================================================

def calc_decimal_precision(a_str: str = '1.0', b_str: str = '7.0',
                           op: str = 'divide', prec: int = 50) -> dict:
    """Arbitrary precision arithmetic using Python's decimal module."""
    getcontext().prec = prec
    a = Decimal(a_str)
    b = Decimal(b_str)
    if op == 'add':
        r = a + b
    elif op == 'subtract':
        r = a - b
    elif op == 'multiply':
        r = a * b
    elif op == 'divide':
        r = a / b
    else:
        r = a + b
    return {
        'result': f'{a_str} {op} {b_str} = {r}',
        'details': {
            'a': str(a), 'b': str(b), 'operation': op,
            'result': str(r), 'precision': prec
        },
        'unit': 'dimensionless'
    }

def calc_rational_arithmetic(num1: tuple = None, num2: tuple = None,
                             op: str = 'add') -> dict:
    """Arithmetic using exact rational numbers (fractions)."""
    if num1 is None:
        num1 = (1, 3)
    if num2 is None:
        num2 = (1, 6)
    f1 = Fraction(num1[0], num1[1])
    f2 = Fraction(num2[0], num2[1])
    if op == 'add':
        r = f1 + f2
    elif op == 'subtract':
        r = f1 - f2
    elif op == 'multiply':
        r = f1 * f2
    elif op == 'divide':
        r = f1 / f2
    else:
        r = f1 + f2
    return {
        'result': f'{f1} {op} {f2} = {r} = {float(r):.6f}',
        'details': {
            'num1': str(f1), 'num2': str(f2), 'operation': op,
            'result_exact': str(r), 'result_float': float(r)
        },
        'unit': 'dimensionless'
    }

def calc_big_decimal_ops(expr: str = '2**100') -> dict:
    """Arbitrary integer/large number operations."""
    result = eval(expr)
    return {
        'result': f'{expr} = {result}',
        'details': {
            'expression': expr, 'result': str(result),
            'num_digits': len(str(abs(result)))
        },
        'unit': 'dimensionless'
    }


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'bisection': {'func': calc_bisection, 'params': ['f_expr', 'a', 'b', 'tol', 'max_iter'], 'desc': 'Bisection method for root finding'},
    'newton_raphson': {'func': calc_newton_raphson, 'params': ['f_expr', 'fprime_expr', 'x0', 'tol', 'max_iter'], 'desc': 'Newton-Raphson root finding'},
    'secant': {'func': calc_secant, 'params': ['f_expr', 'x0', 'x1', 'tol', 'max_iter'], 'desc': 'Secant method for root finding'},
    'fixed_point': {'func': calc_fixed_point, 'params': ['g_expr', 'x0', 'tol', 'max_iter'], 'desc': 'Fixed-point iteration'},
    'numerical_derivative': {'func': calc_numerical_derivative, 'params': ['f_expr', 'x', 'h'], 'desc': 'Forward/backward/central differences'},
    'second_derivative': {'func': calc_second_derivative, 'params': ['f_expr', 'x', 'h'], 'desc': 'Second derivative via central difference'},
    'richardson_extrapolation': {'func': calc_richardson_extrapolation, 'params': ['f_expr', 'x', 'h'], 'desc': 'Richardson extrapolation for derivative'},
    'trapezoidal': {'func': calc_trapezoidal, 'params': ['f_expr', 'a', 'b', 'n'], 'desc': 'Trapezoidal rule integration'},
    'simpson_13': {'func': calc_simpson_13, 'params': ['f_expr', 'a', 'b', 'n'], 'desc': "Simpson's 1/3 rule"},
    'simpson_38': {'func': calc_simpson_38, 'params': ['f_expr', 'a', 'b', 'n'], 'desc': "Simpson's 3/8 rule"},
    'romberg': {'func': calc_romberg, 'params': ['f_expr', 'a', 'b', 'max_level'], 'desc': 'Romberg integration'},
    'gaussian_quadrature': {'func': calc_gaussian_quadrature, 'params': ['f_expr', 'a', 'b', 'n'], 'desc': 'Gaussian quadrature (Gauss-Legendre)'},
    'lagrange_interpolation': {'func': calc_lagrange_interpolation, 'params': ['x_points', 'y_points', 'x_eval'], 'desc': 'Lagrange polynomial interpolation'},
    'newton_divided_diff': {'func': calc_newton_divided_diff, 'params': ['x_points', 'y_points', 'x_eval'], 'desc': "Newton's divided difference interpolation"},
    'cubic_spline': {'func': calc_cubic_spline, 'params': ['x_points', 'y_points', 'x_eval'], 'desc': 'Natural cubic spline interpolation'},
    'linear_interpolation': {'func': calc_linear_interpolation, 'params': ['x_points', 'y_points', 'x_eval'], 'desc': 'Linear interpolation'},
    'polynomial_fit': {'func': calc_polynomial_fit, 'params': ['x_data', 'y_data', 'degree'], 'desc': 'Polynomial least-squares fit'},
    'exponential_fit': {'func': calc_exponential_fit, 'params': ['x_data', 'y_data'], 'desc': 'Exponential fit via log transform'},
    'power_law_fit': {'func': calc_power_law_fit, 'params': ['x_data', 'y_data'], 'desc': 'Power law fit via log-log transform'},
    'error_analysis': {'func': calc_error_analysis, 'params': ['true_value', 'approx_value'], 'desc': 'Absolute/relative/percentage error'},
    'truncation_error': {'func': calc_truncation_error, 'params': ['h', 'order'], 'desc': 'Truncation error estimate O(h^p)'},
    'error_propagation': {'func': calc_error_propagation, 'params': ['vars_dict', 'funcs'], 'desc': 'Error propagation formula'},
    'convergence_rate': {'func': calc_convergence_rate, 'params': ['errors'], 'desc': 'Estimate convergence rate from errors'},
    'fem_bar_stiffness': {'func': calc_fem_bar_stiffness, 'params': ['E', 'A', 'L'], 'desc': '1D bar element stiffness matrix'},
    'fem_heat_conduction': {'func': calc_fem_heat_conduction, 'params': ['k', 'L'], 'desc': '1D heat conduction element matrix'},
    'fem_assemble_global': {'func': calc_fem_assemble_global, 'params': ['K1', 'K2', 'num_nodes'], 'desc': 'Assemble global stiffness matrix 2-element'},
    'fdm_heat_1d': {'func': calc_fdm_heat_1d, 'params': ['alpha', 'L', 'T_max', 'nx', 'nx_method'], 'desc': '1D heat equation explicit FDM'},
    'fdm_wave_1d': {'func': calc_fdm_wave_1d, 'params': ['c', 'L', 'T_max', 'nx'], 'desc': '1D wave equation explicit FDM'},
    'poisson_2d': {'func': calc_poisson_2d, 'params': ['f_func', 'nx', 'ny'], 'desc': '2D Poisson equation 5-point stencil'},
    'cfl_condition': {'func': calc_cfl_condition, 'params': ['c', 'dx', 'scheme'], 'desc': 'CFL stability condition check'},
    'decimal_precision': {'func': calc_decimal_precision, 'params': ['a_str', 'b_str', 'op', 'prec'], 'desc': 'Arbitrary precision via Decimal'},
    'rational_arithmetic': {'func': calc_rational_arithmetic, 'params': ['num1', 'num2', 'op'], 'desc': 'Exact rational arithmetic via Fractions'},
    'big_decimal_ops': {'func': calc_big_decimal_ops, 'params': ['expr'], 'desc': 'Large number operations'},
}
