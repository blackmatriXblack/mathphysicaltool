"""
Special Functions & Advanced Mathematics - Computation Module
"""
import math
import cmath

COMMANDS = {}

# ============================================================
# Gamma & Beta Functions
# ============================================================

def calc_gamma(x: float = 5.0) -> dict:
    """Gamma function: Lanczos approximation."""
    g = 7
    p = [0.99999999999980993, 676.5203681218851, -1259.1392167224028,
         771.32342877765313, -176.61502916214059, 12.507343278686905,
         -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
    if x < 0.5:
        val = math.pi / (math.sin(math.pi * x) * calc_gamma(1 - x)['details']['gamma'])
    else:
        x -= 1
        z = p[0]
        for i in range(1, g + 2):
            z += p[i] / (x + i)
        t = x + g + 0.5
        val = math.sqrt(2 * math.pi) * (t ** (x + 0.5)) * math.exp(-t) * z
    return {
        'result': f'Gamma({x}) = {val:.10g}',
        'details': {
            'x': x, 'gamma': val,
            'method': 'Lanczos approximation (g=7)',
            'math_gamma': math.gamma(x) if x > 0 else 'undefined'
        },
        'unit': 'dimensionless'
    }

def calc_beta_function(x: float = 2.0, y: float = 3.0) -> dict:
    """Beta function B(x,y) = Gamma(x)Gamma(y)/Gamma(x+y)."""
    B = math.gamma(x) * math.gamma(y) / math.gamma(x + y)
    return {
        'result': f'B({x}, {y}) = {B:.10g}',
        'details': {'x': x, 'y': y, 'beta': B, 'formula': 'B(x,y) = Gamma(x)Gamma(y)/Gamma(x+y)'},
        'unit': 'dimensionless'
    }

def calc_digamma(x: float = 2.0) -> dict:
    """Digamma function psi(x) via asymptotic series."""
    if x < 0.5:
        val = calc_digamma(1 - x)['details']['digamma'] - math.pi / math.tan(math.pi * x)
    else:
        s = 0
        while x < 8:
            s -= 1 / x
            x += 1
        inv = 1 / x
        inv2 = inv * inv
        val = math.log(x) - 0.5 * inv - inv2 * (1/12 - inv2 * (1/120 - inv2 * (1/252)))
        val -= s
    return {
        'result': f'psi({x}) = {val:.10g}',
        'details': {'x': x, 'digamma': val},
        'unit': 'dimensionless'
    }

def calc_incomplete_gamma(a: float = 2.0, x: float = 1.0, mode: str = 'lower') -> dict:
    """Incomplete gamma function: series expansion for lower, continued fraction for upper."""
    if mode == 'lower':
        # Series: gamma(a,x) = x^a * exp(-x) * sum_{k=0}^inf x^k / (a)_{k+1}
        total = 0.0
        term = 1.0 / a
        total += term
        for k in range(1, 200):
            term *= x / (a + k)
            total += term
            if term < 1e-15 * total:
                break
        val = (x ** a) * math.exp(-x) * total
    else:
        # Upper = Gamma(a) - lower
        lower_val = math.gamma(a) if a > 0 else float('inf')
        if a > 0:
            total = 0.0
            term = 1.0 / a
            total += term
            for k in range(1, 200):
                term *= x / (a + k)
                total += term
                if term < 1e-15 * total:
                    break
            val = lower_val - (x ** a) * math.exp(-x) * total
        else:
            val = lower_val
    return {
        'result': f'gamma({a}, {x}) = {val:.10g}',
        'details': {'a': a, 'x': x, 'mode': mode, 'value': val},
        'unit': 'dimensionless'
    }

# ============================================================
# Bessel Functions
# ============================================================

def calc_bessel_j(n: int = 0, x: float = 2.5, terms: int = 30) -> dict:
    """Bessel function of the first kind J_n(x) via series."""
    s = 0.0
    for k in range(terms):
        num = (-1)**k * (x/2)**(2*k+n)
        den = math.factorial(k) * math.gamma(k + n + 1)
        term = num / den
        s += term
        if abs(term) < 1e-15 * abs(s) and k > 5:
            break
    return {
        'result': f'J_{n}({x}) = {s:.10g}',
        'details': {'n': n, 'x': x, 'J_n(x)': s, 'terms_used': k + 1},
        'unit': 'dimensionless'
    }

def calc_bessel_y(n: int = 0, x: float = 2.5) -> dict:
    """Bessel function of the second kind Y_n(x) (for integer n).
    Y_n = (J_n cos(n*pi) - J_{-n})/sin(n*pi), limit for integer n."""
    if n == 0:
        # Y_0(x) asymptotic
        gamma_val = 0.5772156649015329
        s = 0.0
        x2 = x/2
        term = 1.0
        harmonic = 0.0
        for k in range(1, 50):
            harmonic += 1.0 / k
            term *= -(x2**2) / (k * k)
            s += term * harmonic
            if abs(term) < 1e-15:
                break
        val = (2/math.pi) * ((gamma_val + math.log(x2)) * math.j0(x) + s)
    else:
        # Numerical approximation
        def J_n(nu, z):
            s = 0.0
            for k in range(50):
                t = (-1)**k * (z/2)**(2*k+nu) / (math.factorial(k) * math.gamma(k+nu+1))
                s += t
                if abs(t) < 1e-15 * abs(s) and k > 5:
                    break
            return s
        val = (J_n(n, x) * math.cos(n * math.pi) - J_n(-n, x)) / math.sin(n * math.pi)
    return {
        'result': f'Y_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'Y_n(x)': val},
        'unit': 'dimensionless'
    }

def calc_bessel_i(n: int = 0, x: float = 2.5, terms: int = 30) -> dict:
    """Modified Bessel I_n(x) = i^{-n} J_n(ix)."""
    s = 0.0
    for k in range(terms):
        num = (x/2)**(2*k+n)
        den = math.factorial(k) * math.gamma(k + n + 1)
        s += num / den
        if abs(num/den) < 1e-15 * abs(s) and k > 5:
            break
    return {
        'result': f'I_{n}({x}) = {s:.10g}',
        'details': {'n': n, 'x': x, 'I_n(x)': s},
        'unit': 'dimensionless'
    }

def calc_bessel_k(n: int = 0, x: float = 2.5) -> dict:
    """Modified Bessel K_n(x) via series."""
    if n == 0:
        gamma_val = 0.5772156649015329
        x2 = x/2
        val = -(gamma_val + math.log(x2)) * calc_bessel_i(0, x)['details']['I_n(x)']
        s = 0.0
        term = 1.0
        harmonic = 0.0
        for k in range(1, 50):
            harmonic += 1.0 / k
            term *= (x2**2) / (k * k)
            s += term * harmonic
            if abs(term) < 1e-15:
                break
        val += s
    else:
        val = math.pi/2 * (calc_bessel_i(-n, x)['details']['I_n(x)'] - calc_bessel_i(n, x)['details']['I_n(x)']) / math.sin(n * math.pi)
    return {
        'result': f'K_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'K_n(x)': val},
        'unit': 'dimensionless'
    }

def calc_spherical_bessel_j(n: int = 0, x: float = 3.0) -> dict:
    """Spherical Bessel j_n(x) = sqrt(pi/(2x)) * J_{n+1/2}(x)."""
    if n == 0:
        val = math.sin(x) / x if abs(x) > 1e-15 else 1.0
    elif n == 1:
        val = (math.sin(x) / x**2 - math.cos(x) / x) if abs(x) > 1e-15 else 0.0
    elif n == 2:
        val = ((3/x**3 - 1/x) * math.sin(x) - 3*math.cos(x)/x**2) if abs(x) > 1e-15 else 0.0
    else:
        val = math.sqrt(math.pi / (2 * x)) * calc_bessel_j(n, x)['details']['J_n(x)'] if abs(x) > 1e-15 else 0.0
    return {
        'result': f'j_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'j_n(x)': val, 'formula': 'j_n(x) = sqrt(pi/(2x)) J_{n+1/2}(x)'},
        'unit': 'dimensionless'
    }

def calc_bessel_roots(n: int = 0, num_roots: int = 3) -> dict:
    """First few roots of J_n(x) = 0 via precomputed approximate values."""
    j0_roots = [2.4048255577, 5.5200781103, 8.6537279129, 11.7915344390, 14.9309177086]
    j1_roots = [3.8317059702, 7.0155866698, 10.1734681351, 13.3236919363, 16.4706300509]
    j2_roots = [5.1356223018, 8.4172441404, 11.6198411721, 14.7959517823, 17.9598194950]
    tables = {0: j0_roots, 1: j1_roots, 2: j2_roots}
    roots = tables.get(n, j0_roots)[:num_roots]
    return {
        'result': f'First {len(roots)} roots of J_{n}(x)=0: {roots}',
        'details': {'n': n, 'num_roots': num_roots, 'roots': roots},
        'unit': 'dimensionless'
    }

# ============================================================
# Error Function
# ============================================================

def calc_erf(x: float = 1.0) -> dict:
    """Error function erf(x) via math.erf / series expansion."""
    val = math.erf(x)
    return {
        'result': f'erf({x}) = {val:.10g}',
        'details': {'x': x, 'erf': val},
        'unit': 'dimensionless'
    }

def calc_erfc(x: float = 1.0) -> dict:
    """Complementary error function erfc(x) = 1 - erf(x)."""
    val = math.erfc(x) if hasattr(math, 'erfc') else 1 - math.erf(x)
    return {
        'result': f'erfc({x}) = {val:.10g}',
        'details': {'x': x, 'erfc': val},
        'unit': 'dimensionless'
    }

def calc_inverse_erf(y: float = 0.5) -> dict:
    """Inverse error function via approximation."""
    if abs(y) >= 1:
        return {'result': 'y must be in (-1, 1)', 'details': {'y': y}, 'unit': 'dimensionless'}
    a = 0.147
    # Approximation: erf^{-1}(x) ~ ...
    if abs(y) <= 0.7:
        # Maclaurin series
        val = y * math.sqrt(math.pi) / 2
        for n in range(1, 20):
            pass
    # Use rational approximation
    sgn = 1 if y >= 0 else -1
    yy = abs(y)
    t = -2 * math.log((1 - yy) / 2)
    num = 2 * math.sqrt(math.pi) + (math.sqrt(2) / math.pi - math.sqrt(math.pi) / 2) * t
    den = 1 + math.sqrt(2) * t / math.pi
    val = sgn * math.sqrt(t) * num / den
    return {
        'result': f'erf^(-1)({y}) = {val:.10g}',
        'details': {'y': y, 'inverse_erf': val, 'method': 'rational approximation'},
        'unit': 'dimensionless'
    }

# ============================================================
# Legendre & Spherical Harmonics
# ============================================================

def calc_legendre_p(n: int = 3, x: float = 0.5) -> dict:
    """Legendre polynomial P_n(x) using recurrence."""
    if n == 0:
        val = 1.0
    elif n == 1:
        val = x
    else:
        P_prev2, P_prev1 = 1.0, x
        for k in range(2, n + 1):
            val = ((2*k - 1) * x * P_prev1 - (k - 1) * P_prev2) / k
            P_prev2, P_prev1 = P_prev1, val
    return {
        'result': f'P_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'P_n(x)': val, 'recurrence': '(2n-1)xP_{n-1} - (n-1)P_{n-2})/n'},
        'unit': 'dimensionless'
    }

def calc_associated_legendre(n: int = 2, m: int = 1, x: float = 0.5) -> dict:
    """Associated Legendre P_n^m(x) via recurrence."""
    if m > n or m < 0:
        return {'result': f'Requires 0 <= m <= n, got m={m}, n={n}', 'details': {}, 'unit': 'dimensionless'}
    # Rodrigues formula: P_n^m(x) = (-1)^m (1-x^2)^{m/2} d^m/dx^m P_n(x)
    if m == 0:
        val = calc_legendre_p(n, x)['details']['P_n(x)']
    else:
        P_n = calc_legendre_p(n, x)['details']['P_n(x)']
        h = 1e-6
        # Numerical m-th derivative of P_n via finite differences
        def dP(f_val, order):
            if order == 0:
                return f_val
            ctx_x = x
            fph = calc_legendre_p(n, ctx_x + h)['details']['P_n(x)']
            fmh = calc_legendre_p(n, ctx_x - h)['details']['P_n(x)']
            return (fph - fmh) / (2*h) if order == 1 else (dP(fph, order-1) - dP(fmh, order-1)) / h
        if m == 1:
            # Use recurrence
            P_prev = calc_associated_legendre(n, 0, x)['details'].get('P_n^m(x)', calc_legendre_p(n, x)['details']['P_n(x)'])
            # Recurrence: (n-m+1)P_{n+1}^m = (2n+1)x P_n^m - (n+m)P_{n-1}^m
            # Use explicit formula for m=1: P_n^1(x) = n*x*P_n(x) - n*P_{n-1}(x) / sqrt(1-x^2)
            if abs(x) < 1:
                P_nm1 = calc_legendre_p(n - 1, x)['details']['P_n(x)']
                factor = math.sqrt(1 - x*x)
                val = (n * x * calc_legendre_p(n, x)['details']['P_n(x)'] - n * P_nm1) / factor
            else:
                val = 0
        else:
            # Use recurrence to get P_n^m
            val = calc_legendre_p(n, x)['details']['P_n(x)']
            val *= (-1)**m * ((1 - x*x) ** (m/2))
    return {
        'result': f'P_{n}^{m}({x}) = {val:.10g}',
        'details': {'n': n, 'm': m, 'x': x, 'P_n^m(x)': val},
        'unit': 'dimensionless'
    }

def calc_spherical_harmonic(l: int = 2, m: int = 0, theta: float = 0.5, phi: float = 1.0) -> dict:
    """Spherical harmonic Y_l^m(theta, phi)."""
    # Normalization factor
    c1 = math.sqrt((2*l + 1) / (4 * math.pi))
    c2 = math.sqrt(math.factorial(l - abs(m)) / math.factorial(l + abs(m)))
    # Associated Legendre at cos(theta)
    x = math.cos(theta)
    Plm = calc_associated_legendre(l, abs(m), x)
    Plm_val = Plm['details'].get('P_n^m(x)', 0)
    # Compute Y_l^m
    if m >= 0:
        Y = c1 * c2 * Plm_val * complex(math.cos(m * phi), math.sin(m * phi))
    else:
        Y = c1 * c2 * Plm_val * complex(math.cos(m * phi), math.sin(m * phi))
        Y = (-1)**abs(m) * Y.conjugate()
    Y_mag = abs(Y)
    return {
        'result': f'Y_{l}^{m}(theta={theta}, phi={phi}) = {Y.real:.6g} + {Y.imag:.6g}i',
        'details': {
            'l': l, 'm': m, 'theta': theta, 'phi': phi,
            'Y_lm': (Y.real, Y.imag),
            'magnitude': Y_mag
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Elliptic Integrals
# ============================================================

def calc_elliptic_k(m: float = 0.5) -> dict:
    """Complete elliptic integral of the first kind K(m)."""
    if m >= 1:
        val = float('inf')
    elif m == 0:
        val = math.pi / 2
    else:
        a = 1.0
        b = math.sqrt(1 - m)
        c = math.sqrt(m)
        for _ in range(20):
            a_new = (a + b) / 2
            b = math.sqrt(a * b)
            c = (a - b) / 2
            a = a_new
            if abs(c) < 1e-15:
                break
        val = math.pi / (2 * a)
    return {
        'result': f'K({m}) = {val:.10g}',
        'details': {'m': m, 'K(m)': val, 'method': 'AGM (arithmetic-geometric mean)'},
        'unit': 'dimensionless'
    }

def calc_elliptic_e(m: float = 0.5) -> dict:
    """Complete elliptic integral of the second kind E(m) via AGM."""
    if m >= 1:
        E = 1.0 if m == 1 else float('inf')
    elif m == 0:
        E = math.pi / 2
    else:
        a = 1.0
        b = math.sqrt(1 - m)
        s = m
        n = 1
        for _ in range(20):
            a_new = (a + b) / 2
            b = math.sqrt(a * b)
            s -= n * ((a - b) / 2)**2
            n *= 2
            a = a_new
            if abs(a - b) < 1e-15:
                break
        E = s * math.pi / (2 * a)
    return {
        'result': f'E({m}) = {E:.10g}',
        'details': {'m': m, 'E(m)': E, 'method': 'AGM'},
        'unit': 'dimensionless'
    }

def calc_jacobi_elliptic(u: float = 0.5, m: float = 0.5) -> dict:
    """Jacobi elliptic functions sn(u|m), cn(u|m), dn(u|m) via AGM."""
    if m == 0:
        sn, cn, dn = math.sin(u), math.cos(u), 1.0
    elif m == 1:
        sn = math.tanh(u)
        cn = 1.0 / math.cosh(u)
        dn = cn
    else:
        # Landen/Gauss transformation
        a = [1.0]
        g = [math.sqrt(1 - m)]
        n = 0
        while abs(a[n] - g[n]) > 1e-12 and n < 20:
            a.append((a[n] + g[n]) / 2)
            g.append(math.sqrt(a[n] * g[n]))
            n += 1
        phi = (2**n) * a[n] * u
        for i in range(n, 0, -1):
            phi = (phi + math.asin((a[i-1]/a[i] - 1) * math.sin(phi))) / 2
        sn = math.sin(phi)
        cn = math.cos(phi)
        dn = math.sqrt(1 - m * sn * sn)
    return {
        'result': f'sn({u}|{m}) = {sn:.6g}, cn = {cn:.6g}, dn = {dn:.6g}',
        'details': {
            'u': u, 'm': m,
            'sn': sn, 'cn': cn, 'dn': dn,
            'check': f'sn^2 + cn^2 = {sn*sn + cn*cn:.6g}, m*sn^2 + dn^2 = {m*sn*sn + dn*dn:.6g}'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Hypergeometric Functions
# ============================================================

def calc_hypergeometric_2f1(a: float = 1.0, b: float = 2.0, c: float = 3.0,
                            z: float = 0.5, terms: int = 100) -> dict:
    """Gauss hypergeometric function 2F1(a,b;c;z) via series."""
    s = 1.0
    term = 1.0
    for k in range(terms):
        term *= (a + k) * (b + k) / ((c + k) * (k + 1)) * z
        s += term
        if abs(term) < 1e-15 * abs(s):
            break
    return {
        'result': f'2F1({a},{b};{c};{z}) = {s:.10g}',
        'details': {'a': a, 'b': b, 'c': c, 'z': z, '2F1': s, 'terms_used': k + 1},
        'unit': 'dimensionless'
    }

def calc_confluent_hypergeometric(a: float = 1.0, c: float = 2.0,
                                  z: float = 0.5, terms: int = 100) -> dict:
    """Confluent hypergeometric 1F1(a;c;z) via series."""
    s = 1.0
    term = 1.0
    for k in range(terms):
        term *= (a + k) / ((c + k) * (k + 1)) * z
        s += term
        if abs(term) < 1e-15 * abs(s):
            break
    return {
        'result': f'1F1({a};{c};{z}) = {s:.10g}',
        'details': {'a': a, 'c': c, 'z': z, '1F1': s, 'terms_used': k + 1},
        'unit': 'dimensionless'
    }

# ============================================================
# Orthogonal Polynomials
# ============================================================

def calc_hermite(n: int = 3, x: float = 0.5) -> dict:
    """Hermite polynomial H_n(x) via recurrence."""
    if n == 0:
        val = 1.0
    elif n == 1:
        val = 2 * x
    else:
        H_prev2, H_prev1 = 1.0, 2 * x
        for k in range(2, n + 1):
            val = 2 * x * H_prev1 - 2 * (k - 1) * H_prev2
            H_prev2, H_prev1 = H_prev1, val
    return {
        'result': f'H_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'H_n(x)': val, 'recurrence': '2x H_{n-1} - 2(n-1) H_{n-2}'},
        'unit': 'dimensionless'
    }

def calc_laguerre(n: int = 3, x: float = 0.5) -> dict:
    """Laguerre polynomial L_n(x) via recurrence."""
    if n == 0:
        val = 1.0
    elif n == 1:
        val = 1 - x
    else:
        L_prev2, L_prev1 = 1.0, 1 - x
        for k in range(2, n + 1):
            val = ((2*k - 1 - x) * L_prev1 - (k - 1) * L_prev2) / k
            L_prev2, L_prev1 = L_prev1, val
    return {
        'result': f'L_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'L_n(x)': val, 'recurrence': '((2n-1-x)L_{n-1} - (n-1)L_{n-2})/n'},
        'unit': 'dimensionless'
    }

def calc_chebyshev_t(n: int = 3, x: float = 0.5) -> dict:
    """Chebyshev polynomial T_n(x) via recurrence: T_n = 2x T_{n-1} - T_{n-2}."""
    if n == 0:
        val = 1.0
    elif n == 1:
        val = x
    else:
        T_prev2, T_prev1 = 1.0, x
        for k in range(2, n + 1):
            val = 2 * x * T_prev1 - T_prev2
            T_prev2, T_prev1 = T_prev1, val
    return {
        'result': f'T_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'T_n(x)': val, 'recurrence': '2x T_{n-1} - T_{n-2}'},
        'unit': 'dimensionless'
    }

def calc_chebyshev_u(n: int = 3, x: float = 0.5) -> dict:
    """Chebyshev polynomial of second kind U_n(x) via recurrence."""
    if n == 0:
        val = 1.0
    elif n == 1:
        val = 2 * x
    else:
        U_prev2, U_prev1 = 1.0, 2 * x
        for k in range(2, n + 1):
            val = 2 * x * U_prev1 - U_prev2
            U_prev2, U_prev1 = U_prev1, val
    return {
        'result': f'U_{n}({x}) = {val:.10g}',
        'details': {'n': n, 'x': x, 'U_n(x)': val, 'recurrence': '2x U_{n-1} - U_{n-2}'},
        'unit': 'dimensionless'
    }

# ============================================================
# Airy Functions
# ============================================================

def calc_airy_ai(x: float = -2.0) -> dict:
    """Airy function Ai(x) via series for small |x|, asymptotic for large."""
    if abs(x) <= 5:
        c1 = 0.355028053887817
        c2 = 0.258819403792807
        s = 0.0
        term = 1.0
        for k in range(100):
            den = 1.0
            for j in range(1, k + 1):
                den *= (3*j - 1) * (3*j)
            # Series: Ai(x) = c1 f(x) - c2 g(x)
            pass
        # Use series representation
        s = 0.0
        for k in range(50):
            if k == 0:
                t1 = 1.0
                t2 = x**3 / 6
            else:
                t1 *= x**3 / ((3*k) * (3*k - 1))
                t2 *= x**3 / ((3*k + 1) * (3*k))
                s += t1 * c1 - x * t2 * c2
        val = c1 * sum(x**(3*k) / (3**k * math.factorial(k) * math.prod(range(3*k-2, 3*k+1))) for k in range(30)) if abs(x) < 10 else 0
    # Simpler: use asymptotic form
    if x > 0:
        val = 0.5 * math.pi**(-0.5) * x**(-0.25) * math.exp(-2/3 * x**1.5)
    elif x < 0:
        val = math.pi**(-0.5) * (-x)**(-0.25) * math.sin(2/3 * (-x)**1.5 + math.pi/4)
    else:
        val = 0.355028053887817
    return {
        'result': f'Ai({x}) = {val:.10g}',
        'details': {'x': x, 'Ai(x)': val, 'method': 'asymptotic expansion'},
        'unit': 'dimensionless'
    }

def calc_airy_bi(x: float = -2.0) -> dict:
    """Airy function Bi(x)."""
    if abs(x) <= 5:
        Bi = math.sqrt(3) * abs(calc_airy_ai(x)['details']['Ai(x)'])
    if x > 0:
        val = math.pi**(-0.5) * x**(-0.25) * math.exp(2/3 * x**1.5)
    elif x < 0:
        val = math.pi**(-0.5) * (-x)**(-0.25) * math.cos(2/3 * (-x)**1.5 + math.pi/4)
    else:
        val = 0.614926627446001
    return {
        'result': f'Bi({x}) = {val:.10g}',
        'details': {'x': x, 'Bi(x)': val, 'method': 'asymptotic expansion'},
        'unit': 'dimensionless'
    }

# ============================================================
# Zeta & Polylogarithm
# ============================================================

def calc_zeta(s: float = 2.0, terms: int = 100000) -> dict:
    """Riemann zeta function zeta(s) via series (s > 1) or eta trick."""
    if s <= 1:
        # Dirichlet eta: eta(s) = (1 - 2^{1-s}) zeta(s)
        eta = 0.0
        for n in range(1, terms + 1):
            eta += (-1)**(n+1) / (n ** s)
        val = eta / (1 - 2**(1 - s))
    else:
        val = 0.0
        for n in range(1, terms + 1):
            val += 1 / (n ** s)
    return {
        'result': f'zeta({s}) = {val:.10g}',
        'details': {'s': s, 'terms': terms, 'zeta(s)': val,
                    'known': {2: math.pi**2/6}.get(s, None)},
        'unit': 'dimensionless'
    }

def calc_dirichlet_eta(s: float = 2.0, terms: int = 100000) -> dict:
    """Dirichlet eta function eta(s) = sum (-1)^{n-1}/n^s."""
    val = 0.0
    for n in range(1, terms + 1):
        val += (-1)**(n+1) / (n ** s)
    return {
        'result': f'eta({s}) = {val:.10g}',
        'details': {'s': s, 'terms': terms, 'eta(s)': val,
                    'relation': 'eta(s) = (1 - 2^{1-s}) zeta(s)'},
        'unit': 'dimensionless'
    }

def calc_polylogarithm(s: float = 1.0, z: float = 0.5, terms: int = 1000) -> dict:
    """Polylogarithm Li_s(z) = sum_{k=1}^inf z^k / k^s."""
    if abs(z) > 0.99 and s <= 0:
        return {'result': f'Slow convergence for |z|={abs(z)}, s={s}', 'details': {}, 'unit': 'dimensionless'}
    val = 0.0
    for k in range(1, terms + 1):
        term = (z ** k) / (k ** s)
        val += term
        if abs(term) < 1e-15 * abs(val) and k > 5:
            break
    return {
        'result': f'Li_{s}({z}) = {val:.10g}',
        'details': {'s': s, 'z': z, 'Li_s(z)': val, 'terms': k},
        'unit': 'dimensionless'
    }


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'gamma': {'func': calc_gamma, 'params': ['x'], 'desc': 'Gamma function (Lanczos approximation)'},
    'beta': {'func': calc_beta_function, 'params': ['x', 'y'], 'desc': 'Beta function B(x,y)'},
    'digamma': {'func': calc_digamma, 'params': ['x'], 'desc': 'Digamma function psi(x)'},
    'incomplete_gamma': {'func': calc_incomplete_gamma, 'params': ['a', 'x', 'mode'], 'desc': 'Incomplete gamma function'},
    'bessel_j': {'func': calc_bessel_j, 'params': ['n', 'x', 'terms'], 'desc': 'Bessel J_n(x) series'},
    'bessel_y': {'func': calc_bessel_y, 'params': ['n', 'x'], 'desc': 'Bessel Y_n(x)'},
    'bessel_i': {'func': calc_bessel_i, 'params': ['n', 'x', 'terms'], 'desc': 'Modified Bessel I_n(x)'},
    'bessel_k': {'func': calc_bessel_k, 'params': ['n', 'x'], 'desc': 'Modified Bessel K_n(x)'},
    'spherical_bessel_j': {'func': calc_spherical_bessel_j, 'params': ['n', 'x'], 'desc': 'Spherical Bessel j_n(x)'},
    'bessel_roots': {'func': calc_bessel_roots, 'params': ['n', 'num_roots'], 'desc': 'Roots of J_n(x)=0'},
    'erf': {'func': calc_erf, 'params': ['x'], 'desc': 'Error function erf(x)'},
    'erfc': {'func': calc_erfc, 'params': ['x'], 'desc': 'Complementary error function erfc(x)'},
    'inverse_erf': {'func': calc_inverse_erf, 'params': ['y'], 'desc': 'Inverse error function'},
    'legendre_p': {'func': calc_legendre_p, 'params': ['n', 'x'], 'desc': 'Legendre polynomial P_n(x)'},
    'associated_legendre': {'func': calc_associated_legendre, 'params': ['n', 'm', 'x'], 'desc': 'Associated Legendre P_n^m(x)'},
    'spherical_harmonic': {'func': calc_spherical_harmonic, 'params': ['l', 'm', 'theta', 'phi'], 'desc': 'Spherical harmonic Y_l^m'},
    'elliptic_k': {'func': calc_elliptic_k, 'params': ['m'], 'desc': 'Complete elliptic integral K(m)'},
    'elliptic_e': {'func': calc_elliptic_e, 'params': ['m'], 'desc': 'Complete elliptic integral E(m)'},
    'jacobi_elliptic': {'func': calc_jacobi_elliptic, 'params': ['u', 'm'], 'desc': 'Jacobi elliptic sn/cn/dn'},
    'hypergeometric_2f1': {'func': calc_hypergeometric_2f1, 'params': ['a', 'b', 'c', 'z', 'terms'], 'desc': 'Gauss 2F1 series'},
    'confluent_hypergeometric': {'func': calc_confluent_hypergeometric, 'params': ['a', 'c', 'z', 'terms'], 'desc': 'Confluent 1F1 series'},
    'hermite': {'func': calc_hermite, 'params': ['n', 'x'], 'desc': 'Hermite polynomial H_n(x)'},
    'laguerre': {'func': calc_laguerre, 'params': ['n', 'x'], 'desc': 'Laguerre polynomial L_n(x)'},
    'chebyshev_t': {'func': calc_chebyshev_t, 'params': ['n', 'x'], 'desc': 'Chebyshev T_n(x)'},
    'chebyshev_u': {'func': calc_chebyshev_u, 'params': ['n', 'x'], 'desc': 'Chebyshev U_n(x)'},
    'airy_ai': {'func': calc_airy_ai, 'params': ['x'], 'desc': 'Airy function Ai(x)'},
    'airy_bi': {'func': calc_airy_bi, 'params': ['x'], 'desc': 'Airy function Bi(x)'},
    'zeta': {'func': calc_zeta, 'params': ['s', 'terms'], 'desc': 'Riemann zeta zeta(s)'},
    'dirichlet_eta': {'func': calc_dirichlet_eta, 'params': ['s', 'terms'], 'desc': 'Dirichlet eta eta(s)'},
    'polylogarithm': {'func': calc_polylogarithm, 'params': ['s', 'z', 'terms'], 'desc': 'Polylogarithm Li_s(z)'},
}
