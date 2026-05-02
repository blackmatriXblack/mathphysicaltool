"""
Probability & Statistics - Mathematics Computation Module
"""
import math
import numpy as np
from itertools import product, combinations

try:
    from scipy import stats
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

COMMANDS = {}

# ==============================================================================
# COUNTING PROBABILITY
# ==============================================================================

def calc_classical_probability(favorable: int = 3, total: int = 10) -> dict:
    """Calculate classical probability P = favorable/total."""
    if total <= 0:
        return {
            'result': 'Error: total must be positive',
            'details': {'favorable': favorable, 'total': total, 'error': 'invalid total'},
            'unit': 'probability'
        }
    p = favorable / total
    return {
        'result': f'P = {favorable}/{total} = {p:.6f}',
        'details': {'favorable': favorable, 'total': total, 'probability': p},
        'unit': 'probability'
    }

def calc_geometric_probability(area_event: float = 25.0, area_total: float = 100.0) -> dict:
    """Calculate geometric probability P = area_event / area_total."""
    if area_total <= 0:
        return {
            'result': 'Error: total area must be positive',
            'details': {'area_event': area_event, 'area_total': area_total, 'error': 'invalid total'},
            'unit': 'probability'
        }
    p = area_event / area_total
    return {
        'result': f'P = {area_event}/{area_total} = {p:.6f}',
        'details': {'area_event': area_event, 'area_total': area_total, 'probability': p},
        'unit': 'probability'
    }

def calc_conditional_probability(p_a_and_b: float = 0.2, p_b: float = 0.4) -> dict:
    """Calculate conditional probability P(A|B) = P(A n B) / P(B)."""
    if p_b <= 0:
        return {
            'result': 'Error: P(B) must be > 0 for conditional probability',
            'details': {'p_a_and_b': p_a_and_b, 'p_b': p_b, 'error': 'P(B) <= 0'},
            'unit': 'probability'
        }
    p_a_given_b = p_a_and_b / p_b
    return {
        'result': f'P(A|B) = P(A n B)/P(B) = {p_a_and_b}/{p_b} = {p_a_given_b:.6f}',
        'details': {'p_a_and_b': p_a_and_b, 'p_b': p_b, 'p_a_given_b': p_a_given_b},
        'unit': 'probability'
    }

def calc_bayes_theorem(p_b_given_a: float = 0.8, p_a: float = 0.3, p_b: float = 0.5) -> dict:
    """Calculate P(A|B) = P(B|A) * P(A) / P(B) using Bayes' theorem."""
    if p_b <= 0:
        return {
            'result': 'Error: P(B) must be > 0',
            'details': {'p_b_given_a': p_b_given_a, 'p_a': p_a, 'p_b': p_b, 'error': 'P(B) <= 0'},
            'unit': 'probability'
        }
    p_a_given_b = (p_b_given_a * p_a) / p_b
    return {
        'result': f'P(A|B) = ({p_b_given_a} * {p_a}) / {p_b} = {p_a_given_b:.6f}',
        'details': {'p_b_given_a': p_b_given_a, 'p_a': p_a, 'p_b': p_b, 'p_a_given_b': p_a_given_b},
        'unit': 'probability'
    }

def calc_independence_check(p_a: float = 0.3, p_b: float = 0.4, p_a_and_b: float = 0.12) -> dict:
    """Check if events A and B are independent: P(A n B) == P(A) * P(B)."""
    product_p = p_a * p_b
    independent = abs(p_a_and_b - product_p) < 1e-10
    return {
        'result': f'P(A)*P(B) = {product_p:.6f}, P(A n B) = {p_a_and_b:.6f}. Independent: {independent}',
        'details': {'p_a': p_a, 'p_b': p_b, 'p_a_and_b': p_a_and_b, 'p_a_times_p_b': product_p, 'independent': independent},
        'unit': 'boolean'
    }

# ==============================================================================
# RANDOM VARIABLES
# ==============================================================================

def calc_expectation(values: list = None, probabilities: list = None) -> dict:
    """Calculate expectation E[X] = sum x * p(x)."""
    if values is None:
        values = [1, 2, 3, 4, 5, 6]
    if probabilities is None:
        probabilities = [1 / 6] * 6
    if len(values) != len(probabilities):
        return {
            'result': 'Error: values and probabilities must have the same length',
            'details': {'values': values, 'probabilities': probabilities, 'error': 'length mismatch'},
            'unit': 'number'
        }
    exp = sum(v * p for v, p in zip(values, probabilities))
    return {
        'result': f'E[X] = {exp:.6f}',
        'details': {'values': values, 'probabilities': probabilities, 'expectation': exp},
        'unit': 'number'
    }

def calc_variance(values: list = None, probabilities: list = None) -> dict:
    """Calculate variance Var(X) = E[X^2] - (E[X])^2."""
    if values is None:
        values = [1, 2, 3, 4, 5, 6]
    if probabilities is None:
        probabilities = [1 / 6] * 6
    if len(values) != len(probabilities):
        return {
            'result': 'Error: values and probabilities must have the same length',
            'details': {'values': values, 'probabilities': probabilities, 'error': 'length mismatch'},
            'unit': 'number'
        }
    exp = sum(v * p for v, p in zip(values, probabilities))
    exp_sq = sum(v * v * p for v, p in zip(values, probabilities))
    var = exp_sq - exp ** 2
    return {
        'result': f'Var(X) = E[X^2] - (E[X])^2 = {exp_sq:.6f} - {exp:.6f}^2 = {var:.6f}',
        'details': {'values': values, 'probabilities': probabilities, 'E_X': exp, 'E_X2': exp_sq, 'variance': var, 'std_dev': math.sqrt(max(0, var))},
        'unit': 'number'
    }

def calc_covariance(x_values: list = None, y_values: list = None, prob: list = None) -> dict:
    """Calculate covariance Cov(X,Y) = E[XY] - E[X]E[Y]."""
    if x_values is None:
        x_values = [1, 1, 2, 2]
    if y_values is None:
        y_values = [1, 2, 1, 2]
    if prob is None:
        prob = [0.25, 0.25, 0.25, 0.25]
    if len(x_values) != len(y_values) or len(x_values) != len(prob):
        return {
            'result': 'Error: x, y, and prob must have the same length',
            'details': {'x': x_values, 'y': y_values, 'prob': prob, 'error': 'length mismatch'},
            'unit': 'number'
        }
    ex = sum(x * p for x, p in zip(x_values, prob))
    ey = sum(y * p for y, p in zip(y_values, prob))
    exy = sum(x * y * p for x, y, p in zip(x_values, y_values, prob))
    cov = exy - ex * ey
    var_x = sum(x * x * p for x, p in zip(x_values, prob)) - ex ** 2
    var_y = sum(y * y * p for y, p in zip(y_values, prob)) - ey ** 2
    corr = cov / math.sqrt(max(0, var_x) * max(0, var_y)) if max(var_x, var_y) > 1e-12 else 0
    return {
        'result': f'Cov(X,Y) = {cov:.6f}, Correlation = {corr:.6f}',
        'details': {'x': x_values, 'y': y_values, 'prob': prob, 'E_X': ex, 'E_Y': ey, 'E_XY': exy, 'covariance': cov, 'correlation': corr},
        'unit': 'number'
    }

def calc_correlation(x_values: list = None, y_values: list = None) -> dict:
    """Calculate Pearson correlation coefficient from paired data."""
    if x_values is None:
        x_values = [1, 2, 3, 4, 5]
    if y_values is None:
        y_values = [2, 4, 5, 4, 5]
    if len(x_values) != len(y_values):
        return {
            'result': 'Error: x and y must have the same length',
            'details': {'x': x_values, 'y': y_values, 'error': 'length mismatch'},
            'unit': 'number'
        }
    n = len(x_values)
    mx = np.mean(x_values)
    my = np.mean(y_values)
    cov = sum((x - mx) * (y - my) for x, y in zip(x_values, y_values)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in x_values) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in y_values) / n)
    if sx < 1e-12 or sy < 1e-12:
        corr = 0
    else:
        corr = cov / (sx * sy)
    return {
        'result': f'Correlation r = {corr:.6f}',
        'details': {'x': x_values, 'y': y_values, 'mean_x': mx, 'mean_y': my, 'covariance': cov, 'std_x': sx, 'std_y': sy, 'correlation': corr},
        'unit': 'number'
    }

def calc_moments(values: list = None, probabilities: list = None, order: int = 3) -> dict:
    """Calculate raw and central moments up to a given order."""
    if values is None:
        values = [1, 2, 3, 4, 5, 6]
    if probabilities is None:
        probabilities = [1 / 6] * 6
    if len(values) != len(probabilities):
        return {
            'result': 'Error: values and probabilities must have the same length',
            'details': {'values': values, 'probabilities': probabilities, 'error': 'length mismatch'},
            'unit': 'number'
        }
    mean = sum(v * p for v, p in zip(values, probabilities))
    moments_raw = []
    moments_central = []
    for k in range(1, order + 1):
        raw = sum((v ** k) * p for v, p in zip(values, probabilities))
        central = sum(((v - mean) ** k) * p for v, p in zip(values, probabilities))
        moments_raw.append(raw)
        moments_central.append(central)
    return {
        'result': f'E[X] = {mean:.6f}, raw moments up to order {order}: {[f"{m:.4f}" for m in moments_raw]}, central moments: {[f"{m:.4f}" for m in moments_central]}',
        'details': {'values': values, 'probabilities': probabilities, 'mean': mean, 'raw_moments': moments_raw, 'central_moments': moments_central},
        'unit': 'number'
    }

# ==============================================================================
# DISCRETE DISTRIBUTIONS
# ==============================================================================

def calc_binomial(n: int = 10, p: float = 0.5, k: int = 5) -> dict:
    """Calculate binomial probability P(X=k) = C(n,k) * p^k * (1-p)^(n-k)."""
    if not 0 <= p <= 1:
        return {
            'result': 'Error: p must be in [0, 1]',
            'details': {'n': n, 'p': p, 'k': k, 'error': 'invalid p'},
            'unit': 'probability'
        }
    if k < 0 or k > n:
        return {
            'result': f'Error: k must be in [0, {n}]',
            'details': {'n': n, 'p': p, 'k': k, 'error': 'k out of range'},
            'unit': 'probability'
        }
    prob = math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))
    mean = n * p
    var = n * p * (1 - p)
    cdf = 0
    for i in range(k + 1):
        cdf += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return {
        'result': f'P(X={k}) = C({n},{k}) * {p}^{k} * {1-p}^{n - k} = {prob:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
        'details': {'n': n, 'p': p, 'k': k, 'probability': prob, 'cdf': cdf, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_poisson(lmbda: float = 4.0, k: int = 3) -> dict:
    """Calculate Poisson probability P(X=k) = lambda^k * e^(-lambda) / k!."""
    if lmbda <= 0:
        return {
            'result': 'Error: lambda must be > 0',
            'details': {'lambda': lmbda, 'k': k, 'error': 'invalid lambda'},
            'unit': 'probability'
        }
    prob = (lmbda ** k) * math.exp(-lmbda) / math.factorial(k)
    cdf = sum((lmbda ** i) * math.exp(-lmbda) / math.factorial(i) for i in range(k + 1))
    mean = lmbda
    var = lmbda
    return {
        'result': f'P(X={k}) = {lmbda}^{k} * e^(-{lmbda}) / {k}! = {prob:.6f}. Mean = Var = {mean:.4f}',
        'details': {'lambda': lmbda, 'k': k, 'probability': prob, 'cdf': cdf, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_geometric(p: float = 0.3, k: int = 4) -> dict:
    """Calculate geometric probability P(X=k) = (1-p)^(k-1) * p (number of trials until 1st success)."""
    if not 0 < p <= 1:
        return {
            'result': 'Error: p must be in (0, 1]',
            'details': {'p': p, 'k': k, 'error': 'invalid p'},
            'unit': 'probability'
        }
    prob = ((1 - p) ** (k - 1)) * p
    mean = 1 / p
    var = (1 - p) / (p ** 2)
    return {
        'result': f'P(X={k}) = (1-{p})^{k - 1} * {p} = {prob:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
        'details': {'p': p, 'k': k, 'probability': prob, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_negative_binomial(r: int = 5, p: float = 0.5, k: int = 10) -> dict:
    """Calculate negative binomial probability P(X=k) = C(k-1, r-1) * p^r * (1-p)^(k-r)."""
    if not 0 < p <= 1:
        return {
            'result': 'Error: p must be in (0, 1]',
            'details': {'r': r, 'p': p, 'k': k, 'error': 'invalid p'},
            'unit': 'probability'
        }
    if k < r:
        return {
            'result': f'Error: k ({k}) must be >= r ({r})',
            'details': {'r': r, 'p': p, 'k': k, 'error': 'k < r'},
            'unit': 'probability'
        }
    prob = math.comb(k - 1, r - 1) * (p ** r) * ((1 - p) ** (k - r))
    mean = r / p
    var = r * (1 - p) / (p ** 2)
    return {
        'result': f'P(X={k}) = C({k - 1},{r - 1}) * {p}^{r} * {1 - p}^{k - r} = {prob:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
        'details': {'r': r, 'p': p, 'k': k, 'probability': prob, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_hypergeometric(N: int = 50, K: int = 10, n: int = 5, k: int = 2) -> dict:
    """Calculate hypergeometric probability P(X=k) = C(K,k) * C(N-K, n-k) / C(N,n)."""
    if k > K or n - k > N - K or k < 0 or n - k < 0:
        return {
            'result': f'Error: invalid parameters. Check k <= K ({K}), n-k <= N-K ({N - K}), k >= 0, n-k >= 0',
            'details': {'N': N, 'K': K, 'n': n, 'k': k, 'error': 'invalid parameters'},
            'unit': 'probability'
        }
    prob = math.comb(K, k) * math.comb(N - K, n - k) / math.comb(N, n)
    mean = n * K / N
    var = n * (K / N) * ((N - K) / N) * ((N - n) / (N - 1))
    return {
        'result': f'P(X={k}) = C({K},{k}) * C({N - K},{n - k}) / C({N},{n}) = {prob:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
        'details': {'N': N, 'K': K, 'n': n, 'k': k, 'probability': prob, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

# ==============================================================================
# CONTINUOUS DISTRIBUTIONS
# ==============================================================================

def calc_normal(x: float = 0.0, mu: float = 0.0, sigma: float = 1.0, calc_type: str = 'pdf') -> dict:
    """Calculate normal distribution PDF or CDF at x with mean mu and std sigma."""
    if sigma <= 0:
        return {
            'result': 'Error: sigma must be > 0',
            'details': {'x': x, 'mu': mu, 'sigma': sigma, 'error': 'invalid sigma'},
            'unit': 'probability'
        }
    z = (x - mu) / sigma
    phi_z = (1 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * z * z)
    pdf_val = phi_z / sigma
    if calc_type.lower() == 'pdf':
        return {
            'result': f'N({mu}, {sigma}^2): f({x}) = {pdf_val:.6f} (z = {z:.4f})',
            'details': {'x': x, 'mu': mu, 'sigma': sigma, 'z_score': z, 'pdf': pdf_val},
            'unit': 'density'
        }
    else:
        if HAS_SCIPY:
            cdf_val = stats.norm.cdf(x, loc=mu, scale=sigma)
        else:
            def erf_approx(t):
                a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
                sign = 1 if t >= 0 else -1
                t = abs(t)
                y = 1.0 / (1.0 + p * t)
                return sign * (1 - (((((a5 * y + a4) * y) + a3) * y + a2) * y + a1) * y * math.exp(-t * t))
            cdf_val = 0.5 * (1 + erf_approx(z / math.sqrt(2)))
        return {
            'result': f'N({mu}, {sigma}^2): P(X <= {x}) = {cdf_val:.6f} (z = {z:.4f})',
            'details': {'x': x, 'mu': mu, 'sigma': sigma, 'z_score': z, 'pdf': pdf_val, 'cdf': cdf_val},
            'unit': 'probability'
        }

def calc_uniform(x: float = 0.5, a: float = 0.0, b: float = 1.0, calc_type: str = 'pdf') -> dict:
    """Calculate uniform distribution U[a,b] PDF or CDF at x."""
    if a >= b:
        return {
            'result': 'Error: a must be < b',
            'details': {'x': x, 'a': a, 'b': b, 'error': 'a >= b'},
            'unit': 'density'
        }
    if x < a or x > b:
        pdf_val = 0
        cdf_val = 0 if x < a else 1
    else:
        pdf_val = 1 / (b - a)
        cdf_val = (x - a) / (b - a)
    mean = (a + b) / 2
    var = (b - a) ** 2 / 12
    if calc_type.lower() == 'pdf':
        return {
            'result': f'U[{a},{b}]: f({x}) = {pdf_val:.6f}',
            'details': {'x': x, 'a': a, 'b': b, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    return {
        'result': f'U[{a},{b}]: P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'a': a, 'b': b, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_exponential_dist(x: float = 2.0, lmbda: float = 0.5, calc_type: str = 'pdf') -> dict:
    """Calculate exponential distribution Exp(lambda) PDF or CDF at x."""
    if lmbda <= 0:
        return {
            'result': 'Error: lambda must be > 0',
            'details': {'x': x, 'lambda': lmbda, 'error': 'invalid lambda'},
            'unit': 'density'
        }
    if x < 0:
        pdf_val = 0
        cdf_val = 0
    else:
        pdf_val = lmbda * math.exp(-lmbda * x)
        cdf_val = 1 - math.exp(-lmbda * x)
    mean = 1 / lmbda
    var = 1 / (lmbda ** 2)
    if calc_type.lower() == 'pdf':
        return {
            'result': f'Exp({lmbda}): f({x}) = {pdf_val:.6f}',
            'details': {'x': x, 'lambda': lmbda, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    return {
        'result': f'Exp({lmbda}): P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'lambda': lmbda, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_gamma_dist(x: float = 3.0, alpha: float = 2.0, beta: float = 1.0, calc_type: str = 'pdf') -> dict:
    """Calculate Gamma(alpha, beta) distribution PDF or CDF at x."""
    if alpha <= 0 or beta <= 0:
        return {
            'result': 'Error: alpha and beta must be > 0',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'error': 'invalid parameters'},
            'unit': 'density'
        }
    if x < 0:
        pdf_val = 0
        cdf_val = 0
    else:
        pdf_val = (beta ** alpha / math.gamma(alpha)) * (x ** (alpha - 1)) * math.exp(-beta * x)
        if HAS_SCIPY:
            cdf_val = stats.gamma.cdf(x, a=alpha, scale=1 / beta)
        else:
            cdf_val = None
    mean = alpha / beta
    var = alpha / (beta ** 2)
    if calc_type.lower() == 'pdf':
        return {
            'result': f'Gamma({alpha},{beta}): f({x}) = {pdf_val:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    if cdf_val is None:
        return {
            'result': f'Gamma({alpha},{beta}): CDF requires scipy. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'mean': mean, 'variance': var, 'note': 'scipy required for CDF'},
            'unit': 'probability'
        }
    return {
        'result': f'Gamma({alpha},{beta}): P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'alpha': alpha, 'beta': beta, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_beta_dist(x: float = 0.5, alpha: float = 2.0, beta: float = 5.0, calc_type: str = 'pdf') -> dict:
    """Calculate Beta(alpha, beta) distribution PDF or CDF at x in [0, 1]."""
    if alpha <= 0 or beta <= 0:
        return {
            'result': 'Error: alpha and beta must be > 0',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'error': 'invalid parameters'},
            'unit': 'density'
        }
    if not 0 <= x <= 1:
        pdf_val = 0
        cdf_val = 0 if x < 0 else 1
    else:
        B = math.gamma(alpha) * math.gamma(beta) / math.gamma(alpha + beta)
        pdf_val = (x ** (alpha - 1)) * ((1 - x) ** (beta - 1)) / B
        if HAS_SCIPY:
            cdf_val = stats.beta.cdf(x, a=alpha, b=beta)
        else:
            cdf_val = None
    mean = alpha / (alpha + beta)
    var = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
    if calc_type.lower() == 'pdf':
        return {
            'result': f'Beta({alpha},{beta}): f({x}) = {pdf_val:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    if cdf_val is None:
        return {
            'result': f'Beta({alpha},{beta}): CDF requires scipy. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'alpha': alpha, 'beta': beta, 'mean': mean, 'variance': var, 'note': 'scipy required for CDF'},
            'unit': 'probability'
        }
    return {
        'result': f'Beta({alpha},{beta}): P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'alpha': alpha, 'beta': beta, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_weibull(x: float = 2.0, shape: float = 2.0, scale: float = 3.0, calc_type: str = 'pdf') -> dict:
    """Calculate Weibull distribution PDF or CDF at x."""
    if shape <= 0 or scale <= 0:
        return {
            'result': 'Error: shape and scale must be > 0',
            'details': {'x': x, 'shape': shape, 'scale': scale, 'error': 'invalid parameters'},
            'unit': 'density'
        }
    if x < 0:
        pdf_val = 0
        cdf_val = 0
    else:
        pdf_val = (shape / scale) * ((x / scale) ** (shape - 1)) * math.exp(-((x / scale) ** shape))
        cdf_val = 1 - math.exp(-((x / scale) ** shape))
    mean = scale * math.gamma(1 + 1 / shape)
    var = scale ** 2 * (math.gamma(1 + 2 / shape) - math.gamma(1 + 1 / shape) ** 2)
    if calc_type.lower() == 'pdf':
        return {
            'result': f'Weibull({shape},{scale}): f({x}) = {pdf_val:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'shape': shape, 'scale': scale, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    return {
        'result': f'Weibull({shape},{scale}): P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'shape': shape, 'scale': scale, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

def calc_lognormal(x: float = 2.0, mu: float = 0.0, sigma: float = 0.5, calc_type: str = 'pdf') -> dict:
    """Calculate lognormal(ln N(mu, sigma^2)) distribution PDF or CDF at x."""
    if sigma <= 0:
        return {
            'result': 'Error: sigma must be > 0',
            'details': {'x': x, 'mu': mu, 'sigma': sigma, 'error': 'invalid sigma'},
            'unit': 'density'
        }
    if x <= 0:
        pdf_val = 0
        cdf_val = 0
    else:
        log_x = math.log(x)
        pdf_val = (1 / (x * sigma * math.sqrt(2 * math.pi))) * math.exp(-((log_x - mu) ** 2) / (2 * sigma ** 2))
        if HAS_SCIPY:
            cdf_val = stats.lognorm.cdf(x, s=sigma, scale=math.exp(mu))
        else:
            z = (log_x - mu) / sigma
            a1, a2, a3, a4, a5, p = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429, 0.3275911
            sign = 1 if z >= 0 else -1
            t = abs(z)
            y = 1.0 / (1.0 + p * t)
            erf_z = sign * (1 - (((((a5 * y + a4) * y) + a3) * y + a2) * y + a1) * y * math.exp(-t * t))
            cdf_val = 0.5 * (1 + erf_z / math.sqrt(2))
    mean = math.exp(mu + sigma ** 2 / 2)
    var = (math.exp(sigma ** 2) - 1) * math.exp(2 * mu + sigma ** 2)
    if calc_type.lower() == 'pdf':
        return {
            'result': f'LogNormal({mu},{sigma}^2): f({x}) = {pdf_val:.6f}. Mean = {mean:.4f}, Var = {var:.4f}',
            'details': {'x': x, 'mu': mu, 'sigma': sigma, 'pdf': pdf_val, 'cdf': cdf_val, 'mean': mean, 'variance': var},
            'unit': 'density'
        }
    return {
        'result': f'LogNormal({mu},{sigma}^2): P(X <= {x}) = {cdf_val:.6f}',
        'details': {'x': x, 'mu': mu, 'sigma': sigma, 'cdf': cdf_val, 'mean': mean, 'variance': var},
        'unit': 'probability'
    }

# ==============================================================================
# DESCRIPTIVE STATISTICS
# ==============================================================================

def calc_descriptive_stats(data: list = None) -> dict:
    """Calculate comprehensive descriptive statistics for a dataset."""
    if data is None:
        data = [2, 4, 4, 4, 5, 5, 7, 9, 10, 12]
    n = len(data)
    data_sorted = sorted(data)
    mean_val = sum(data) / n
    median_val = (data_sorted[n // 2] + data_sorted[(n - 1) // 2]) / 2
    freq = {}
    for val in data:
        freq[val] = freq.get(val, 0) + 1
    max_freq = max(freq.values()) if freq else 0
    mode_vals = [k for k, v in freq.items() if v == max_freq]
    var_pop = sum((x - mean_val) ** 2 for x in data) / n
    var_sample = sum((x - mean_val) ** 2 for x in data) / (n - 1) if n > 1 else 0
    std_pop = math.sqrt(var_pop)
    std_sample = math.sqrt(var_sample)
    m3 = sum((x - mean_val) ** 3 for x in data) / n
    skewness = m3 / (std_pop ** 3) if std_pop > 1e-12 else 0
    m4 = sum((x - mean_val) ** 4 for x in data) / n
    kurtosis = m4 / (std_pop ** 4) - 3 if std_pop > 1e-12 else 0
    def percentile(sorted_data, pct):
        k = (len(sorted_data) - 1) * pct / 100
        f = int(k)
        c = k - f
        if f + 1 < len(sorted_data):
            return sorted_data[f] + c * (sorted_data[f + 1] - sorted_data[f])
        return sorted_data[f]
    q1 = percentile(data_sorted, 25)
    q2 = median_val
    q3 = percentile(data_sorted, 75)
    iqr_val = q3 - q1
    data_range = max(data) - min(data)
    z_scores = [(x - mean_val) / std_pop if std_pop > 1e-12 else 0 for x in data]
    return {
        'result': (
            f'n = {n}, Mean = {mean_val:.6f}, Median = {median_val:.4f}, '
            f'Mode = {mode_vals}, SD(pop) = {std_pop:.6f}, '
            f'Variance(pop) = {var_pop:.6f}, Skewness = {skewness:.4f}, Kurtosis = {kurtosis:.4f}, '
            f'Q1 = {q1:.4f}, Q3 = {q3:.4f}, IQR = {iqr_val:.4f}, Range = {data_range:.4f}'
        ),
        'details': {
            'n': n, 'mean': mean_val, 'median': median_val, 'mode': mode_vals,
            'variance_population': var_pop, 'variance_sample': var_sample,
            'std_population': std_pop, 'std_sample': std_sample,
            'skewness': skewness, 'kurtosis': kurtosis,
            'min': min(data), 'max': max(data), 'range': data_range,
            'q1': q1, 'q2': q2, 'q3': q3, 'iqr': iqr_val,
            'z_scores': [round(z, 4) for z in z_scores]
        },
        'unit': 'statistics'
    }

def calc_mean(data: list = None) -> dict:
    """Calculate arithmetic mean of data."""
    if data is None:
        data = [1, 2, 3, 4, 5]
    mean_val = sum(data) / len(data)
    return {
        'result': f'Mean = {mean_val:.6f}',
        'details': {'data': data, 'n': len(data), 'mean': mean_val},
        'unit': 'number'
    }

def calc_median(data: list = None) -> dict:
    """Calculate median of data."""
    if data is None:
        data = [1, 3, 2, 5, 4]
    sorted_data = sorted(data)
    n = len(sorted_data)
    median_val = (sorted_data[n // 2] + sorted_data[(n - 1) // 2]) / 2
    return {
        'result': f'Median = {median_val:.6f}',
        'details': {'data': data, 'sorted': sorted_data, 'n': n, 'median': median_val},
        'unit': 'number'
    }

def calc_mode(data: list = None) -> dict:
    """Calculate mode of data."""
    if data is None:
        data = [1, 2, 2, 3, 3, 3, 4]
    freq = {}
    for val in data:
        freq[val] = freq.get(val, 0) + 1
    max_freq = max(freq.values()) if freq else 0
    modes = sorted([k for k, v in freq.items() if v == max_freq])
    return {
        'result': f'Mode = {modes} (frequency = {max_freq})',
        'details': {'data': data, 'frequency': freq, 'mode': modes, 'max_frequency': max_freq},
        'unit': 'number'
    }

def calc_variance_stats(data: list = None, pop: bool = True) -> dict:
    """Calculate variance (population or sample)."""
    if data is None:
        data = [1, 2, 3, 4, 5]
    n = len(data)
    mean_val = sum(data) / n
    if pop:
        var = sum((x - mean_val) ** 2 for x in data) / n
    else:
        if n < 2:
            return {
                'result': 'Error: Need at least 2 data points for sample variance',
                'details': {'data': data, 'error': 'n < 2'},
                'unit': 'number'
            }
        var = sum((x - mean_val) ** 2 for x in data) / (n - 1)
    sd = math.sqrt(var)
    return {
        'result': f'Variance ({"" if pop else "un"}biased) = {var:.6f}, SD = {sd:.6f}',
        'details': {'data': data, 'n': n, 'mean': mean_val, 'variance': var, 'std_dev': sd, 'population': pop},
        'unit': 'number'
    }

def calc_skewness(data: list = None) -> dict:
    """Calculate skewness of data."""
    if data is None:
        data = [1, 2, 3, 4, 100]
    n = len(data)
    mean_val = sum(data) / n
    var = sum((x - mean_val) ** 2 for x in data) / n
    sd = math.sqrt(var) if var > 1e-12 else 0
    if sd < 1e-12:
        skew = 0
    else:
        m3 = sum((x - mean_val) ** 3 for x in data) / n
        skew = m3 / (sd ** 3)
    interpretation = 'symmetric' if abs(skew) < 0.5 else ('right-skewed' if skew > 0 else 'left-skewed')
    return {
        'result': f'Skewness = {skew:.6f} ({interpretation})',
        'details': {'data': data, 'mean': mean_val, 'sd': sd, 'skewness': skew, 'interpretation': interpretation},
        'unit': 'number'
    }

def calc_kurtosis(data: list = None) -> dict:
    """Calculate excess kurtosis of data."""
    if data is None:
        data = [1, 2, 3, 4, 5]
    n = len(data)
    mean_val = sum(data) / n
    var = sum((x - mean_val) ** 2 for x in data) / n
    sd = math.sqrt(var) if var > 1e-12 else 0
    if sd < 1e-12:
        kurt = 0
    else:
        m4 = sum((x - mean_val) ** 4 for x in data) / n
        kurt = m4 / (sd ** 4) - 3
    interpretation = 'mesokurtic' if abs(kurt) < 0.5 else ('leptokurtic' if kurt > 0 else 'platykurtic')
    return {
        'result': f'Kurtosis (excess) = {kurt:.6f} ({interpretation})',
        'details': {'data': data, 'mean': mean_val, 'sd': sd, 'kurtosis': kurt, 'interpretation': interpretation},
        'unit': 'number'
    }

def calc_quartiles(data: list = None) -> dict:
    """Calculate quartiles and IQR of data."""
    if data is None:
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    sorted_data = sorted(data)
    n = len(sorted_data)
    def q(p):
        idx = p * (n - 1)
        lo = int(idx)
        hi = min(lo + 1, n - 1)
        frac = idx - lo
        return sorted_data[lo] + frac * (sorted_data[hi] - sorted_data[lo])
    q1_val = q(0.25)
    q2_val = q(0.5)
    q3_val = q(0.75)
    iqr_val = q3_val - q1_val
    return {
        'result': f'Q1 = {q1_val:.4f}, Q2 = {q2_val:.4f}, Q3 = {q3_val:.4f}, IQR = {iqr_val:.4f}',
        'details': {'data': data, 'sorted': sorted_data, 'Q1': q1_val, 'Q2': q2_val, 'Q3': q3_val, 'IQR': iqr_val},
        'unit': 'number'
    }

def calc_zscore(data: list = None, x: float = 0.0) -> dict:
    """Calculate z-score for a specific value x relative to the data."""
    if data is None:
        data = [1, 2, 3, 4, 5]
    n = len(data)
    mean_val = sum(data) / n
    sd = math.sqrt(sum((xi - mean_val) ** 2 for xi in data) / n)
    if sd < 1e-12:
        return {
            'result': 'z-score is undefined (std dev = 0)',
            'details': {'data': data, 'x': x, 'mean': mean_val, 'std_dev': 0, 'error': 'zero variance'},
            'unit': 'number'
        }
    z = (x - mean_val) / sd
    return {
        'result': f'z-score of {x} = ({x} - {mean_val:.4f}) / {sd:.4f} = {z:.6f}',
        'details': {'data': data, 'x': x, 'mean': mean_val, 'std_dev': sd, 'z_score': z},
        'unit': 'number'
    }

# ==============================================================================
# REGRESSION
# ==============================================================================

def calc_linear_regression(x: list = None, y: list = None) -> dict:
    """Calculate linear regression y = a*x + b via least squares."""
    if x is None:
        x = [1, 2, 3, 4, 5]
    if y is None:
        y = [2, 4, 5, 4, 5]
    if len(x) != len(y) or len(x) < 2:
        return {
            'result': 'Error: x and y must have same length >= 2',
            'details': {'x': x, 'y': y, 'error': 'invalid input'},
            'unit': 'regression'
        }
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    a = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    b_val = (sum_y - a * sum_x) / n
    y_mean = sum_y / n
    ss_res = sum((yi - (a * xi + b_val)) ** 2 for xi, yi in zip(x, y))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 0
    predictions = [a * xi + b_val for xi in x]
    rmse = math.sqrt(ss_res / n)
    mae = sum(abs(yi - pi) for yi, pi in zip(y, predictions)) / n
    return {
        'result': f'y = {a:.6f}x + {b_val:.6f}, R^2 = {r2:.6f}, RMSE = {rmse:.6f}, MAE = {mae:.6f}',
        'details': {'x': x, 'y': y, 'slope': a, 'intercept': b_val, 'r_squared': r2, 'rmse': rmse, 'mae': mae, 'predictions': predictions, 'equation': f'y = {a:.4f}x + {b_val:.4f}'},
        'unit': 'regression'
    }

def calc_polynomial_regression(x: list = None, y: list = None, degree: int = 2) -> dict:
    """Polynomial regression using numpy polyfit."""
    if x is None:
        x = [1, 2, 3, 4, 5, 6]
    if y is None:
        y = [2, 8, 18, 32, 50, 72]
    if len(x) != len(y) or len(x) <= degree:
        return {
            'result': f'Error: need more data points ({len(x)}) than degree ({degree})',
            'details': {'x': x, 'y': y, 'degree': degree, 'error': 'insufficient data'},
            'unit': 'regression'
        }
    coeffs = np.polyfit(x, y, degree)
    poly_str = ' + '.join(f'{coeffs[i]:.4f}x^{degree - i}' for i in range(degree + 1))
    predictions = np.polyval(coeffs, x)
    y_mean = np.mean(y)
    ss_res = sum((yi - pi) ** 2 for yi, pi in zip(y, predictions))
    ss_tot = sum((yi - y_mean) ** 2 for yi in y)
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 0
    rmse = math.sqrt(ss_res / len(x))
    mae = sum(abs(yi - pi) for yi, pi in zip(y, predictions)) / len(x)
    return {
        'result': f'Polynomial (deg {degree}): {poly_str}, R^2 = {r2:.6f}, RMSE = {rmse:.6f}',
        'details': {'x': x, 'y': y, 'degree': degree, 'coefficients': coeffs.tolist(), 'polynomial': poly_str, 'r_squared': r2, 'rmse': rmse, 'mae': mae},
        'unit': 'regression'
    }

def calc_multiple_linear_regression(X: list = None, y: list = None) -> dict:
    """Multiple linear regression: y = b0 + b1*x1 + b2*x2 + ... using normal equations."""
    if X is None:
        X = [[1, 2], [2, 1], [3, 4], [4, 3]]
    if y is None:
        y = [5, 7, 15, 19]
    n = len(y)
    if len(X) != n:
        return {
            'result': 'Error: X and y must have same number of rows',
            'details': {'X': X, 'y': y, 'error': 'length mismatch'},
            'unit': 'regression'
        }
    X_mat = np.array(X, dtype=float)
    y_vec = np.array(y, dtype=float)
    X_aug = np.hstack([np.ones((n, 1)), X_mat])
    try:
        coeffs = np.linalg.lstsq(X_aug, y_vec, rcond=None)[0]
    except np.linalg.LinAlgError:
        return {
            'result': 'Error: Cannot solve linear system (singular matrix)',
            'details': {'X': X, 'y': y, 'error': 'singular'},
            'unit': 'regression'
        }
    predictions = X_aug @ coeffs
    y_mean = np.mean(y_vec)
    ss_res = sum((y_vec[i] - predictions[i]) ** 2 for i in range(n))
    ss_tot = sum((y_vec[i] - y_mean) ** 2 for i in range(n))
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 0
    rmse = math.sqrt(ss_res / n)
    mae = sum(abs(y_vec[i] - predictions[i]) for i in range(n)) / n
    coeff_str = ', '.join(f'b{i}={coeffs[i]:.4f}' for i in range(len(coeffs)))
    return {
        'result': f'Regression: {coeff_str}, R^2 = {r2:.6f}, RMSE = {rmse:.6f}',
        'details': {'X': X, 'y': y, 'coefficients': coeffs.tolist(), 'r_squared': r2, 'rmse': rmse, 'mae': mae},
        'unit': 'regression'
    }

# ==============================================================================
# STATISTICAL INFERENCE
# ==============================================================================

def calc_confidence_interval(data: list = None, confidence: float = 0.95, ci_type: str = 'z') -> dict:
    """Calculate confidence interval for mean: z-interval (known sigma) or t-interval."""
    if data is None:
        data = [5, 6, 7, 8, 9, 10, 11, 12, 13]
    n = len(data)
    if n < 2:
        return {
            'result': 'Error: Need at least 2 data points',
            'details': {'data': data, 'error': 'insufficient data'},
            'unit': 'interval'
        }
    mean_val = np.mean(data)
    std_val = np.std(data, ddof=1)
    alpha = 1 - confidence
    if ci_type.lower() == 'z':
        if HAS_SCIPY:
            z_val = stats.norm.ppf(1 - alpha / 2)
        else:
            z_approx = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
            z_val = z_approx.get(confidence, 1.96)
        margin = z_val * std_val / math.sqrt(n)
    else:
        if HAS_SCIPY:
            t_val = stats.t.ppf(1 - alpha / 2, df=n - 1)
        else:
            if n - 1 <= 30:
                t_approx = {0.90: 1.812, 0.95: 2.228, 0.99: 3.169}
                t_val = t_approx.get(confidence, 2.228) if n <= 11 else (z_approx.get(confidence, 1.96))
            else:
                z_approx = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
                t_val = z_approx.get(confidence, 1.96)
        margin = t_val * std_val / math.sqrt(n)
    lower = mean_val - margin
    upper = mean_val + margin
    return {
        'result': f'{int(confidence * 100)}% CI: [{lower:.6f}, {upper:.6f}] (mean = {mean_val:.4f})',
        'details': {'data': data, 'confidence': confidence, 'ci_type': ci_type, 'mean': mean_val, 'std': std_val, 'margin': margin, 'lower': lower, 'upper': upper, 'n': n},
        'unit': 'interval'
    }

def calc_one_sample_ttest(data: list = None, mu0: float = 0.0) -> dict:
    """One-sample t-test: H0: mu = mu0."""
    if data is None:
        data = [1.5, 2.0, 2.5, 1.8, 2.2, 1.9, 2.1, 2.3]
    n = len(data)
    if n < 2:
        return {
            'result': 'Error: Need at least 2 data points',
            'details': {'data': data, 'error': 'insufficient data'},
            'unit': 'test'
        }
    mean_val = np.mean(data)
    std_val = np.std(data, ddof=1)
    t_stat = (mean_val - mu0) / (std_val / math.sqrt(n)) if std_val > 1e-12 else 0
    if HAS_SCIPY:
        p_val = 2 * stats.t.sf(abs(t_stat), df=n - 1)
    else:
        p_val = 2 * math.exp(-0.717 * abs(t_stat) - 0.416 * abs(t_stat) ** 2) if abs(t_stat) < 5 else 0
    return {
        'result': f't = {t_stat:.6f}, p-value = {p_val:.6f}' + (f' {"(significant)" if p_val < 0.05 else "(not significant)"} at alpha=0.05'),
        'details': {'data': data, 'mu0': mu0, 'mean': mean_val, 'std': std_val, 'n': n, 't_statistic': t_stat, 'p_value': p_val},
        'unit': 'test'
    }

def calc_two_sample_ttest(data1: list = None, data2: list = None, paired: bool = False) -> dict:
    """Two-sample t-test (independent or paired)."""
    if data1 is None:
        data1 = [2.0, 3.0, 4.0, 5.0, 6.0]
    if data2 is None:
        data2 = [3.0, 4.0, 5.0, 6.0, 7.0]
    n1, n2 = len(data1), len(data2)
    if n1 < 2 or n2 < 2:
        return {
            'result': 'Error: Need at least 2 data points in each group',
            'details': {'data1': data1, 'data2': data2, 'error': 'insufficient data'},
            'unit': 'test'
        }
    if paired:
        if n1 != n2:
            return {
                'result': 'Error: Paired test requires equal sample sizes',
                'details': {'data1': data1, 'data2': data2, 'error': 'unequal sizes for paired test'},
                'unit': 'test'
            }
        diffs = [data1[i] - data2[i] for i in range(n1)]
        return calc_one_sample_ttest(diffs, 0.0)
    mean1, mean2 = np.mean(data1), np.mean(data2)
    var1 = np.var(data1, ddof=1)
    var2 = np.var(data2, ddof=1)
    se = math.sqrt(var1 / n1 + var2 / n2)
    t_stat = (mean1 - mean2) / se if se > 1e-12 else 0
    if HAS_SCIPY:
        df_num = (var1 / n1 + var2 / n2) ** 2
        df_den = ((var1 / n1) ** 2) / (n1 - 1) + ((var2 / n2) ** 2) / (n2 - 1)
        df = df_num / df_den if df_den > 1e-12 else 1
        p_val = 2 * stats.t.sf(abs(t_stat), df=df)
    else:
        p_val = 2 * math.exp(-0.717 * abs(t_stat) - 0.416 * abs(t_stat) ** 2) if abs(t_stat) < 5 else 0
    return {
        'result': f't = {t_stat:.6f}, p-value = {p_val:.6f}' + (f' {"(significant)" if p_val < 0.05 else "(not significant)"} at alpha=0.05'),
        'details': {'data1': data1, 'data2': data2, 'paired': paired, 'mean1': mean1, 'mean2': mean2, 't_statistic': t_stat, 'p_value': p_val},
        'unit': 'test'
    }

def calc_chi_square_test(observed: list = None, expected: list = None) -> dict:
    """Chi-square goodness-of-fit test."""
    if observed is None:
        observed = [25, 30, 20, 25]
    if expected is None:
        expected = [25, 25, 25, 25]
    if len(observed) != len(expected):
        return {
            'result': 'Error: observed and expected must have same length',
            'details': {'observed': observed, 'expected': expected, 'error': 'length mismatch'},
            'unit': 'test'
        }
    chi2 = sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0)
    df = len(observed) - 1
    if HAS_SCIPY:
        p_val = 1 - stats.chi2.cdf(chi2, df)
    else:
        p_val = 1 if chi2 <= 0 else math.exp(-chi2 / 2)
    return {
        'result': f'chi^2 = {chi2:.6f}, df = {df}, p-value = {p_val:.6f}',
        'details': {'observed': observed, 'expected': expected, 'chi_squared': chi2, 'df': df, 'p_value': p_val},
        'unit': 'test'
    }

def calc_anova_one_way(groups: list = None) -> dict:
    """One-way ANOVA test."""
    if groups is None:
        groups = [[5, 6, 7, 8], [7, 8, 9, 10], [9, 10, 11, 12]]
    k = len(groups)
    n_per_group = [len(g) for g in groups]
    N = sum(n_per_group)
    means = [np.mean(g) for g in groups]
    grand_mean = sum(np.sum(g) for g in groups) / N
    ss_between = sum(n_per_group[i] * (means[i] - grand_mean) ** 2 for i in range(k))
    ss_within = sum(sum((x - means[i]) ** 2 for x in groups[i]) for i in range(k))
    ms_between = ss_between / (k - 1) if k > 1 else 0
    ms_within = ss_within / (N - k) if N > k else 1
    f_stat = ms_between / ms_within if ms_within > 1e-12 else 0
    if HAS_SCIPY:
        p_val = 1 - stats.f.cdf(f_stat, k - 1, N - k) if k > 1 else 1
    else:
        p_val = None
    return {
        'result': f'F = {f_stat:.6f}, p-value = {p_val:.6f}' if p_val is not None else f'F = {f_stat:.6f} (scipy needed for p-value)',
        'details': {'groups': groups, 'k': k, 'N': N, 'f_statistic': f_stat, 'p_value': p_val, 'ss_between': ss_between, 'ss_within': ss_within, 'ms_between': ms_between, 'ms_within': ms_within},
        'unit': 'test'
    }

# ==============================================================================
# STOCHASTIC PROCESSES
# ==============================================================================

def calc_markov_chain(transition_matrix: list = None, initial_state: list = None, n_steps: int = 5) -> dict:
    """Compute n-step transition via matrix power."""
    if transition_matrix is None:
        transition_matrix = [[0.7, 0.3], [0.4, 0.6]]
    if initial_state is None:
        initial_state = [1, 0]
    P = np.array(transition_matrix, dtype=float)
    v = np.array(initial_state, dtype=float)
    states_after = [v.tolist()]
    for i in range(n_steps):
        v = v @ P
        states_after.append(v.tolist())
    return {
        'result': f'After {n_steps} steps: state = {v.tolist()}',
        'details': {'transition_matrix': P.tolist(), 'initial_state': initial_state, 'n_steps': n_steps, 'P_n': np.linalg.matrix_power(P, n_steps).tolist(), 'state_evolution': states_after},
        'unit': 'probability'
    }

def calc_stationary_distribution(transition_matrix: list = None) -> dict:
    """Compute stationary distribution pi*P = pi for a Markov chain."""
    if transition_matrix is None:
        transition_matrix = [[0.7, 0.3], [0.4, 0.6]]
    P = np.array(transition_matrix, dtype=float)
    n = P.shape[0]
    A = np.vstack([(P.T - np.eye(n)), np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1
    try:
        pi, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        pi = np.clip(pi, 0, None)
        pi = pi / np.sum(pi)
    except np.linalg.LinAlgError:
        return {
            'result': 'Error: Could not compute stationary distribution',
            'details': {'transition_matrix': P.tolist(), 'error': 'LinAlgError'},
            'unit': 'probability'
        }
    return {
        'result': f'Stationary distribution: pi = {pi.tolist()}',
        'details': {'transition_matrix': P.tolist(), 'stationary': pi.tolist()},
        'unit': 'probability'
    }

def calc_random_walk(n_steps: int = 100, start: int = 0, p: float = 0.5) -> dict:
    """Simulate a 1D random walk. p = probability of step +1, (1-p) = step -1."""
    np.random.seed(42)
    steps = np.random.choice([1, -1], size=n_steps, p=[p, 1 - p])
    path = [start]
    current = start
    for s in steps:
        current += s
        path.append(int(current))
    return {
        'result': f'Random walk ({n_steps} steps): end = {path[-1]}, max = {max(path)}, min = {min(path)}',
        'details': {'n_steps': n_steps, 'start': start, 'p': p, 'end_position': path[-1], 'max_position': max(path), 'min_position': min(path), 'path': path},
        'unit': 'position'
    }

def calc_poisson_process(rate: float = 2.0, time: float = 5.0, n_simulations: int = 3) -> dict:
    """Simulate a Poisson process with given rate over a time interval. Returns count of events."""
    np.random.seed(42)
    counts = []
    for _ in range(n_simulations):
        t = 0
        count = 0
        while t < time:
            t += np.random.exponential(1 / rate)
            if t < time:
                count += 1
        counts.append(count)
    mean_count = np.mean(counts)
    expected = rate * time
    return {
        'result': f'Poisson process (rate={rate}, T={time}): count mean = {mean_count:.2f}, expected = {expected}',
        'details': {'rate': rate, 'time': time, 'simulations': n_simulations, 'counts': counts, 'mean_count': mean_count, 'expected_count': expected},
        'unit': 'count'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    'classical_probability': {'func': calc_classical_probability, 'params': ['favorable', 'total'], 'desc': 'Classical probability P = favorable/total'},
    'geometric_probability': {'func': calc_geometric_probability, 'params': ['area_event', 'area_total'], 'desc': 'Geometric probability'},
    'conditional_probability': {'func': calc_conditional_probability, 'params': ['p_a_and_b', 'p_b'], 'desc': 'Conditional probability P(A|B)'},
    'bayes_theorem': {'func': calc_bayes_theorem, 'params': ['p_b_given_a', 'p_a', 'p_b'], 'desc': "Bayes' theorem"},
    'independence_check': {'func': calc_independence_check, 'params': ['p_a', 'p_b', 'p_a_and_b'], 'desc': 'Check independence of events'},
    'expectation': {'func': calc_expectation, 'params': ['values', 'probabilities'], 'desc': 'Expectation E[X]'},
    'variance': {'func': calc_variance, 'params': ['values', 'probabilities'], 'desc': 'Variance Var(X)'},
    'covariance': {'func': calc_covariance, 'params': ['x_values', 'y_values', 'prob'], 'desc': 'Covariance Cov(X,Y)'},
    'correlation': {'func': calc_correlation, 'params': ['x_values', 'y_values'], 'desc': 'Pearson correlation from data'},
    'moments': {'func': calc_moments, 'params': ['values', 'probabilities', 'order'], 'desc': 'Raw and central moments'},
    'binomial': {'func': calc_binomial, 'params': ['n', 'p', 'k'], 'desc': 'Binomial probability P(X=k)'},
    'poisson': {'func': calc_poisson, 'params': ['lmbda', 'k'], 'desc': 'Poisson probability P(X=k)'},
    'geometric': {'func': calc_geometric, 'params': ['p', 'k'], 'desc': 'Geometric probability P(X=k)'},
    'negative_binomial': {'func': calc_negative_binomial, 'params': ['r', 'p', 'k'], 'desc': 'Negative binomial probability'},
    'hypergeometric': {'func': calc_hypergeometric, 'params': ['N', 'K', 'n', 'k'], 'desc': 'Hypergeometric probability'},
    'normal': {'func': calc_normal, 'params': ['x', 'mu', 'sigma', 'calc_type'], 'desc': 'Normal distribution PDF/CDF'},
    'uniform': {'func': calc_uniform, 'params': ['x', 'a', 'b', 'calc_type'], 'desc': 'Uniform distribution PDF/CDF'},
    'exponential_dist': {'func': calc_exponential_dist, 'params': ['x', 'lmbda', 'calc_type'], 'desc': 'Exponential distribution PDF/CDF'},
    'gamma_dist': {'func': calc_gamma_dist, 'params': ['x', 'alpha', 'beta', 'calc_type'], 'desc': 'Gamma distribution PDF/CDF'},
    'beta_dist': {'func': calc_beta_dist, 'params': ['x', 'alpha', 'beta', 'calc_type'], 'desc': 'Beta distribution PDF/CDF'},
    'weibull': {'func': calc_weibull, 'params': ['x', 'shape', 'scale', 'calc_type'], 'desc': 'Weibull distribution PDF/CDF'},
    'lognormal': {'func': calc_lognormal, 'params': ['x', 'mu', 'sigma', 'calc_type'], 'desc': 'LogNormal distribution PDF/CDF'},
    'descriptive_stats': {'func': calc_descriptive_stats, 'params': ['data'], 'desc': 'Comprehensive descriptive statistics'},
    'mean': {'func': calc_mean, 'params': ['data'], 'desc': 'Arithmetic mean'},
    'median': {'func': calc_median, 'params': ['data'], 'desc': 'Median'},
    'mode': {'func': calc_mode, 'params': ['data'], 'desc': 'Mode'},
    'variance_stats': {'func': calc_variance_stats, 'params': ['data', 'pop'], 'desc': 'Variance (population or sample)'},
    'skewness': {'func': calc_skewness, 'params': ['data'], 'desc': 'Skewness'},
    'kurtosis': {'func': calc_kurtosis, 'params': ['data'], 'desc': 'Excess kurtosis'},
    'quartiles': {'func': calc_quartiles, 'params': ['data'], 'desc': 'Quartiles and IQR'},
    'zscore': {'func': calc_zscore, 'params': ['data', 'x'], 'desc': 'Z-score'},
    'linear_regression': {'func': calc_linear_regression, 'params': ['x', 'y'], 'desc': 'Linear regression y=ax+b'},
    'polynomial_regression': {'func': calc_polynomial_regression, 'params': ['x', 'y', 'degree'], 'desc': 'Polynomial regression'},
    'multiple_linear_regression': {'func': calc_multiple_linear_regression, 'params': ['X', 'y'], 'desc': 'Multiple linear regression'},
    'confidence_interval': {'func': calc_confidence_interval, 'params': ['data', 'confidence', 'ci_type'], 'desc': 'Confidence interval for mean'},
    'one_sample_ttest': {'func': calc_one_sample_ttest, 'params': ['data', 'mu0'], 'desc': 'One-sample t-test'},
    'two_sample_ttest': {'func': calc_two_sample_ttest, 'params': ['data1', 'data2', 'paired'], 'desc': 'Two-sample t-test'},
    'chi_square_test': {'func': calc_chi_square_test, 'params': ['observed', 'expected'], 'desc': 'Chi-square goodness-of-fit'},
    'anova_one_way': {'func': calc_anova_one_way, 'params': ['groups'], 'desc': 'One-way ANOVA'},
    'markov_chain': {'func': calc_markov_chain, 'params': ['transition_matrix', 'initial_state', 'n_steps'], 'desc': 'Markov chain n-step transition'},
    'stationary_distribution': {'func': calc_stationary_distribution, 'params': ['transition_matrix'], 'desc': 'Stationary distribution of Markov chain'},
    'random_walk': {'func': calc_random_walk, 'params': ['n_steps', 'start', 'p'], 'desc': 'Simulate 1D random walk'},
    'poisson_process': {'func': calc_poisson_process, 'params': ['rate', 'time', 'n_simulations'], 'desc': 'Simulate Poisson process'},
}
