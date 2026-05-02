"""
Number Theory & Cryptography - Mathematics Computation Module
"""
import math
import random

COMMANDS = {}

# ============================================================
# Divisibility
# ============================================================

def calc_gcd(a: int = 48, b: int = 18) -> dict:
    """Compute GCD using Euclidean algorithm."""
    def euclidean(x, y):
        steps = []
        while y != 0:
            q = x // y
            r = x % y
            steps.append({'a': x, 'b': y, 'quotient': q, 'remainder': r})
            x, y = y, r
        return x, steps
    g, steps = euclidean(abs(a), abs(b))
    return {
        'result': f'GCD({a}, {b}) = {g}',
        'details': {'a': a, 'b': b, 'gcd': g, 'steps': steps},
        'unit': 'dimensionless'
    }

def calc_lcm(a: int = 48, b: int = 18) -> dict:
    """Compute LCM using GCD relationship: lcm(a,b) = |a*b|/gcd(a,b)."""
    g = math.gcd(abs(a), abs(b))
    l = abs(a * b) // g if g != 0 else 0
    return {
        'result': f'LCM({a}, {b}) = {l}',
        'details': {'a': a, 'b': b, 'gcd': g, 'lcm': l},
        'unit': 'dimensionless'
    }

def calc_extended_euclidean(a: int = 48, b: int = 18) -> dict:
    """Extended Euclidean algorithm: find x, y such that ax + by = gcd(a,b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    steps = []
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        steps.append({'quotient': q, 'r': old_r, 's': old_s, 't': old_t})
    g = old_r
    if g < 0:
        g, old_s, old_t = -g, -old_s, -old_t
    return {
        'result': f'{a}({old_s}) + {b}({old_t}) = {g}',
        'details': {'a': a, 'b': b, 'x': old_s, 'y': old_t, 'gcd': g,
                    'verification': a * old_s + b * old_t, 'steps': steps},
        'unit': 'dimensionless'
    }

def calc_divisibility_tests(n: int = 12345) -> dict:
    """Test divisibility of n by numbers 2 through 13."""
    tests = {}
    rules = {
        2: lambda x: x % 2 == 0,
        3: lambda x: sum(int(d) for d in str(abs(x))) % 3 == 0,
        4: lambda x: abs(x) % 100 % 4 == 0,
        5: lambda x: abs(x) % 10 in (0, 5),
        6: lambda x: x % 2 == 0 and sum(int(d) for d in str(abs(x))) % 3 == 0,
        7: lambda x: abs(x) % 7 == 0,
        8: lambda x: abs(x) % 1000 % 8 == 0,
        9: lambda x: sum(int(d) for d in str(abs(x))) % 9 == 0,
        10: lambda x: abs(x) % 10 == 0,
        11: lambda x: abs(x) % 11 == 0,
        12: lambda x: x % 3 == 0 and x % 4 == 0,
        13: lambda x: abs(x) % 13 == 0,
    }
    for d, rule in rules.items():
        tests[f'divisible_by_{d}'] = rule(n)
    divisors = [d for d, v in tests.items() if v]
    return {
        'result': f'{n} is divisible by: {", ".join(d.replace("divisible_by_","") for d in divisors) if divisors else "none"}',
        'details': {'n': n, 'tests': tests},
        'unit': 'dimensionless'
    }

# ============================================================
# Primes
# ============================================================

def calc_prime_trial_division(n: int = 97) -> dict:
    """Check primality using trial division up to sqrt(n)."""
    n_abs = abs(n)
    if n_abs < 2:
        is_prime = False
        factors = []
    else:
        is_prime = True
        factors = []
        limit = int(math.isqrt(n_abs))
        for i in range(2, limit + 1):
            if n_abs % i == 0:
                is_prime = False
                factors.append(i)
                if i != n_abs // i:
                    factors.append(n_abs // i)
                break
        factors = sorted(set(factors))
    return {
        'result': f'{n} is {"prime" if is_prime else "composite"}',
        'details': {'n': n, 'is_prime': is_prime, 'factors_found': factors, 'sqrt_n': int(math.isqrt(n_abs))},
        'unit': 'dimensionless'
    }

def calc_miller_rabin(n: int = 97, k: int = 10) -> dict:
    """Miller-Rabin probabilistic primality test with k witnesses."""
    if n < 2:
        return {'result': f'{n} is composite', 'details': {'n': n, 'is_prime': False, 'witnesses': [], 'certainty': 'N/A'}, 'unit': 'dimensionless'}
    if n == 2:
        return {'result': f'{n} is prime', 'details': {'n': n, 'is_prime': True, 'witnesses': [], 'certainty': 1.0}, 'unit': 'dimensionless'}
    if n % 2 == 0:
        return {'result': f'{n} is composite', 'details': {'n': n, 'is_prime': False, 'witnesses': [2], 'certainty': 'N/A'}, 'unit': 'dimensionless'}
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    witnesses_tested = []
    is_composite = False
    for _ in range(k):
        a = random.randrange(2, min(n - 1, 1000000))
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            witnesses_tested.append({'a': a, 'result': 'probably_prime'})
            continue
        composite_this = True
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite_this = False
                break
        if composite_this:
            is_composite = True
            witnesses_tested.append({'a': a, 'result': 'composite_witness'})
            break
        witnesses_tested.append({'a': a, 'result': 'probably_prime'})
    certainty = 1 - 0.25 ** len(witnesses_tested) if not is_composite else 1.0
    return {
        'result': f'{n} is {"composite" if is_composite else "probably prime"} (certainty: {certainty:.6f})',
        'details': {'n': n, 'is_prime': not is_composite, 's': s, 'd': d,
                    'witnesses': witnesses_tested, 'certainty': certainty},
        'unit': 'dimensionless'
    }

def calc_sieve_eratosthenes(limit: int = 100) -> dict:
    """Sieve of Eratosthenes to find all primes up to limit."""
    if limit < 2:
        return {'result': f'No primes up to {limit}', 'details': {'limit': limit, 'primes': [], 'count': 0}, 'unit': 'dimensionless'}
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    primes = [i for i, is_p in enumerate(sieve) if is_p]
    return {
        'result': f'Found {len(primes)} primes up to {limit}',
        'details': {'limit': limit, 'primes': primes[:50] if len(primes) > 50 else primes,
                    'count': len(primes), 'largest': primes[-1] if primes else None},
        'unit': 'dimensionless'
    }

def calc_prime_counting(x: float = 100.0) -> dict:
    """Prime counting function pi(x) — number of primes <= x, with Liouville approximation."""
    limit = int(x)
    if limit < 2:
        return {'result': f'pi({x}) = 0', 'details': {'x': x, 'pi': 0, 'liouville_approx': 0, 'error': 0}, 'unit': 'dimensionless'}
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    pi = sum(sieve)
    # Liouville approximation: x / (ln(x) - 1.08366)
    if x >= 2:
        liouville = x / (math.log(x) - 1.08366)
    else:
        liouville = 0
    return {
        'result': f'pi({x}) = {pi} (approx: {liouville:.1f})',
        'details': {'x': x, 'pi': pi, 'liouville_approx': round(liouville, 4), 'error': abs(pi - liouville)},
        'unit': 'dimensionless'
    }

def calc_prime_factorization(n: int = 84) -> dict:
    """Prime factorization of integer n."""
    orig = n
    n = abs(n)
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    factor_list = []
    for p, e in sorted(factors.items()):
        factor_list.append({'prime': p, 'exponent': e})
    factorization_str = ' * '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(factors.items()))
    return {
        'result': f'{orig} = {factorization_str}',
        'details': {'n': orig, 'factors': factor_list, 'factor_dict': factors},
        'unit': 'dimensionless'
    }

def calc_next_prime(n: int = 100) -> dict:
    """Find the next prime greater than n."""
    def is_prime(x):
        if x < 2:
            return False
        if x == 2:
            return True
        if x % 2 == 0:
            return False
        limit = int(math.isqrt(x))
        for i in range(3, limit + 1, 2):
            if x % i == 0:
                return False
        return True
    candidate = n + 1
    iterations = 0
    while not is_prime(candidate):
        candidate += 1
        iterations += 1
        if iterations > 100000:
            break
    return {
        'result': f'Next prime after {n} is {candidate}',
        'details': {'input': n, 'next_prime': candidate, 'gap': candidate - n, 'iterations': iterations},
        'unit': 'dimensionless'
    }

# ============================================================
# Congruences / Modular Arithmetic
# ============================================================

def calc_modular_arithmetic(a: int = 7, b: int = 3, mod: int = 11) -> dict:
    """Perform modular arithmetic: add, subtract, multiply, power."""
    return {
        'result': f'Modular ops mod {mod}',
        'details': {
            'a': a, 'b': b, 'modulus': mod,
            'add': (a + b) % mod,
            'subtract': (a - b) % mod,
            'multiply': (a * b) % mod,
            'power': pow(a, b, mod),
            'a_inverse': pow(a, -1, mod) if math.gcd(a, mod) == 1 else None
        },
        'unit': 'dimensionless'
    }

def calc_modular_inverse(a: int = 7, mod: int = 26) -> dict:
    """Compute modular inverse a^{-1} mod m using extended Euclidean algorithm."""
    g = math.gcd(a, mod)
    if g != 1:
        return {
            'result': f'No inverse: gcd({a}, {mod}) = {g} != 1',
            'details': {'a': a, 'modulus': mod, 'inverse': None, 'gcd': g},
            'unit': 'dimensionless'
        }
    inv = pow(a, -1, mod)
    return {
        'result': f'{a}^(-1) mod {mod} = {inv} (check: {a}*{inv} mod {mod} = {(a*inv)%mod})',
        'details': {'a': a, 'modulus': mod, 'inverse': inv, 'verification': (a * inv) % mod},
        'unit': 'dimensionless'
    }

def calc_chinese_remainder(a_list: list = None, m_list: list = None) -> dict:
    """Chinese Remainder Theorem: solve x ≡ a_i (mod m_i) for coprime m_i."""
    if a_list is None:
        a_list = [2, 3, 2]
    if m_list is None:
        m_list = [3, 5, 7]
    if len(a_list) != len(m_list):
        return {'result': 'Error: must have same number of remainders and moduli', 'details': {}, 'unit': 'dimensionless'}
    # Check pairwise coprime
    for i in range(len(m_list)):
        for j in range(i + 1, len(m_list)):
            if math.gcd(m_list[i], m_list[j]) != 1:
                return {
                    'result': f'Moduli not coprime: gcd({m_list[i]}, {m_list[j]}) != 1',
                    'details': {'a': a_list, 'm': m_list, 'coprime': False},
                    'unit': 'dimensionless'
                }
    M = 1
    for m in m_list:
        M *= m
    x = 0
    steps = []
    for i, (a_i, m_i) in enumerate(zip(a_list, m_list)):
        M_i = M // m_i
        y_i = pow(M_i, -1, m_i)
        term = a_i * M_i * y_i
        x += term
        steps.append({'i': i, 'a_i': a_i, 'm_i': m_i, 'M_i': M_i, 'y_i': y_i, 'term': term})
    x %= M
    verification = [x % m for m in m_list]
    return {
        'result': f'x = {x} (mod {M})',
        'details': {'a': a_list, 'm': m_list, 'M': M, 'x': x, 'steps': steps, 'verification': verification},
        'unit': 'dimensionless'
    }

def calc_linear_congruence(a: int = 14, b: int = 30, m: int = 100) -> dict:
    """Solve linear congruence: a*x ≡ b (mod m). Returns all solutions."""
    g = math.gcd(a, m)
    if b % g != 0:
        return {
            'result': f'No solution: gcd({a}, {m}) = {g} does not divide {b}',
            'details': {'a': a, 'b': b, 'm': m, 'gcd': g, 'num_solutions': 0},
            'unit': 'dimensionless'
        }
    a1, b1, m1 = a // g, b // g, m // g
    inv = pow(a1, -1, m1)
    x0 = (inv * b1) % m1
    solutions = [(x0 + k * m1) % m for k in range(g)]
    return {
        'result': f'{g} solution(s): x = {{{", ".join(str(s) for s in solutions)}}} (mod {m})',
        'details': {'a': a, 'b': b, 'm': m, 'gcd': g, 'num_solutions': g,
                    'reduced_a': a1, 'reduced_b': b1, 'reduced_m': m1,
                    'x0': x0, 'solutions': solutions},
        'unit': 'dimensionless'
    }

# ============================================================
# Number-theoretic functions
# ============================================================

def calc_euler_totient(n: int = 36) -> dict:
    """Euler's totient function phi(n): count of numbers <= n coprime to n."""
    orig = n
    result = n
    factors = []
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            factors.append(p)
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1 if p == 2 else 2
    if temp > 1:
        factors.append(temp)
        result -= result // temp
    return {
        'result': f'phi({orig}) = {result}',
        'details': {'n': orig, 'phi': result, 'prime_factors': factors},
        'unit': 'dimensionless'
    }

def calc_mobius(n: int = 30) -> dict:
    """Mobius function mu(n): 0 if n has squared prime factor, 1 if even number of prime factors, -1 if odd."""
    orig = n
    if n == 1:
        return {'result': 'mu(1) = 1', 'details': {'n': 1, 'mu': 1}, 'unit': 'dimensionless'}
    # Factorize
    n_abs = abs(n)
    prime_count = 0
    d = 2
    temp = n_abs
    while d * d <= temp:
        if temp % d == 0:
            count = 0
            while temp % d == 0:
                temp //= d
                count += 1
            if count > 1:
                return {'result': f'mu({orig}) = 0 (has squared factor {d}^2)', 'details': {'n': orig, 'mu': 0, 'reason': f'{d}^2 divides {orig}'}, 'unit': 'dimensionless'}
            prime_count += 1
        d += 1 if d == 2 else 2
    if temp > 1:
        prime_count += 1
    mu = -1 if prime_count % 2 == 1 else 1
    return {
        'result': f'mu({orig}) = {mu}',
        'details': {'n': orig, 'mu': mu, 'num_distinct_primes': prime_count},
        'unit': 'dimensionless'
    }

def calc_divisor_sigma(n: int = 12, k: int = 1) -> dict:
    """Divisor function sigma_k(n) = sum of d^k over divisors d of n."""
    total = 0
    divisors = []
    limit = int(math.isqrt(n))
    for d in range(1, limit + 1):
        if n % d == 0:
            divisors.append(d)
            other = n // d
            if other != d:
                divisors.append(other)
    divisors.sort()
    for d in divisors:
        total += d ** k
    return {
        'result': f'sigma_{k}({n}) = {total}',
        'details': {'n': n, 'k': k, 'divisors': divisors, 'sigma': total,
                    'tau': len(divisors), 'sigma_0': len(divisors), 'sigma_1': sum(divisors)},
        'unit': 'dimensionless'
    }

def calc_carmichael(n: int = 36) -> dict:
    """Carmichael function lambda(n): smallest m such that a^m ≡ 1 (mod n) for all a coprime to n."""
    def lambda_prime_power(p, e):
        if p == 2:
            if e == 1:
                return 1
            elif e == 2:
                return 2
            else:
                return 2 ** (e - 2)
        else:
            return (p - 1) * (p ** (e - 1))
    def lcm_list(nums):
        if not nums:
            return 1
        res = nums[0]
        for num in nums[1:]:
            res = res * num // math.gcd(res, num)
        return res
    if n == 1:
        return {'result': 'lambda(1) = 1', 'details': {'n': 1, 'lambda': 1}, 'unit': 'dimensionless'}
    orig = n
    factors = {}
    temp = n
    p = 2
    while p * p <= temp:
        while temp % p == 0:
            factors[p] = factors.get(p, 0) + 1
            temp //= p
        p += 1 if p == 2 else 2
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    lambdas = [lambda_prime_power(p, e) for p, e in factors.items()]
    lam = lcm_list(lambdas)
    return {
        'result': f'lambda({orig}) = {lam}',
        'details': {'n': orig, 'lambda': lam, 'factorization': factors, 'component_lambdas': dict(zip(factors.keys(), lambdas))},
        'unit': 'dimensionless'
    }

# ============================================================
# Diophantine Equations
# ============================================================

def calc_linear_diophantine(a: int = 14, b: int = 21, c: int = 35) -> dict:
    """Solve linear Diophantine equation: a*x + b*y = c."""
    g = math.gcd(a, b)
    if c % g != 0:
        return {
            'result': f'No solution: gcd({a}, {b}) = {g} does not divide {c}',
            'details': {'a': a, 'b': b, 'c': c, 'gcd': g, 'solvable': False},
            'unit': 'dimensionless'
        }
    a1, b1, c1 = a // g, b // g, c // g
    # Find particular solution using extended Euclidean
    old_r, r = a1, b1
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    x0 = old_s * c1
    y0 = old_t * c1
    # General solution: x = x0 + (b/g)*t, y = y0 - (a/g)*t
    dx = b // g
    dy = -a // g
    return {
        'result': f'General solution: x = {x0} + {dx}t, y = {y0} + {dy}t',
        'details': {
            'a': a, 'b': b, 'c': c, 'gcd': g,
            'x0': x0, 'y0': y0,
            'dx': dx, 'dy': dy,
            'general_form': f'x = {x0} + {dx}t, y = {y0} + {dy}t',
            'verification': a * x0 + b * y0
        },
        'unit': 'dimensionless'
    }

def calc_pythagorean_triples(max_c: int = 50) -> dict:
    """Generate primitive Pythagorean triples (a, b, c) with c <= max_c using Euclid's formula."""
    triples = []
    limit = int(math.isqrt(max_c)) + 1
    for m in range(2, limit):
        for n_ in range(1, m):
            if (m - n_) % 2 == 1 and math.gcd(m, n_) == 1:
                a = m * m - n_ * n_
                b = 2 * m * n_
                c = m * m + n_ * n_
                if c <= max_c:
                    triples.append({'a': min(a, b), 'b': max(a, b), 'c': c,
                                    'm': m, 'n': n_, 'primitive': True})
    triples.sort(key=lambda t: t['c'])
    return {
        'result': f'Found {len(triples)} primitive Pythagorean triples with c <= {max_c}',
        'details': {'max_c': max_c, 'count': len(triples), 'triples': triples},
        'unit': 'dimensionless'
    }

def calc_pell_equation(D: int = 2, max_iter: int = 10) -> dict:
    """Solve Pell's equation x^2 - D*y^2 = 1 using continued fraction method."""
    if int(math.isqrt(D)) ** 2 == D:
        return {
            'result': f'D={D} is a perfect square, only trivial solution x=±1, y=0',
            'details': {'D': D, 'perfect_square': True},
            'unit': 'dimensionless'
        }
    # Continued fraction of sqrt(D)
    a0 = int(math.isqrt(D))
    m = 0
    d_val = 1
    a = a0
    # Convergents
    h_prev, h_cur = 0, 1
    k_prev, k_cur = 1, 0
    period = []
    convergents = []
    for i in range(max_iter * 10):
        h_prev, h_cur = h_cur, a * h_cur + h_prev
        k_prev, k_cur = k_cur, a * k_cur + k_prev
        convergents.append({'h': h_cur, 'k': k_cur, 'value': h_cur / k_cur if k_cur != 0 else float('inf')})
        # Check if fundamental solution found
        if h_cur * h_cur - D * k_cur * k_cur == 1:
            x1, y1 = h_cur, k_cur
            # Generate multiple solutions using (x1 + y1*sqrt(D))^n
            solutions = []
            x_n, y_n = x1, y1
            for n in range(1, min(max_iter + 1, 10)):
                solutions.append({'n': n, 'x': x_n, 'y': y_n})
                x_next = x_n * x1 + D * y_n * y1
                y_next = x_n * y1 + y_n * x1
                x_n, y_n = x_next, y_next
            return {
                'result': f'Fundamental solution: x={x1}, y={y1} for D={D}',
                'details': {'D': D, 'fundamental_x': x1, 'fundamental_y': y1,
                            'solutions': solutions, 'convergents': convergents[-10:]},
                'unit': 'dimensionless'
            }
        m = d_val * a - m
        d_val = (D - m * m) // d_val
        a = (a0 + m) // d_val
        period.append(a)
    return {
        'result': f'Could not find solution within iteration limit for D={D}',
        'details': {'D': D, 'convergents': convergents[-3:]},
        'unit': 'dimensionless'
    }

# ============================================================
# Finite Fields
# ============================================================

def calc_finite_field_ops(p: int = 7, a: int = 3, b: int = 5) -> dict:
    """Basic operations in GF(p): add, sub, mult, div."""
    if not (p > 1):
        return {'result': 'p must be > 1', 'details': {}, 'unit': 'dimensionless'}
    a, b = a % p, b % p
    inv_b = pow(b, -1, p) if b % p != 0 and math.gcd(b, p) == 1 else None
    return {
        'result': f'GF({p}) operations on {a}, {b}',
        'details': {
            'field': f'GF({p})',
            'a': a, 'b': b,
            'add': f'{a} + {b} = {(a + b) % p}',
            'sub': f'{a} - {b} = {(a - b) % p}',
            'mul': f'{a} * {b} = {(a * b) % p}',
            'div': f'{a} / {b} = {(a * inv_b) % p}' if inv_b is not None else 'division by 0',
            'neg_a': (-a) % p,
            'inv_a': pow(a, -1, p) if math.gcd(a, p) == 1 else None
        },
        'unit': 'dimensionless'
    }

def calc_primitive_root(p: int = 7) -> dict:
    """Find a primitive root modulo prime p."""
    if p < 2:
        return {'result': f'p={p} must be >= 2', 'details': {}, 'unit': 'dimensionless'}
    # Check if p has a primitive root
    if p == 2:
        return {'result': 'Primitive root mod 2 is 1', 'details': {'p': 2, 'root': 1, 'phi': 1}, 'unit': 'dimensionless'}
    phi = p - 1
    # Find prime factors of phi
    factors = set()
    temp = phi
    d = 2
    while d * d <= temp:
        while temp % d == 0:
            factors.add(d)
            temp //= d
        d += 1 if d == 2 else 2
    if temp > 1:
        factors.add(temp)
    roots = []
    for g in range(2, p):
        ok = True
        for q in factors:
            if pow(g, phi // q, p) == 1:
                ok = False
                break
        if ok:
            roots.append(g)
            if len(roots) >= 5:
                break
    if roots:
        return {
            'result': f'Primitive root(s) mod {p}: {roots}',
            'details': {'p': p, 'phi': phi, 'phi_factors': list(factors),
                        'primitive_roots': roots, 'count_total': phi if len(roots) > 0 else 0},
            'unit': 'dimensionless'
        }
    return {
        'result': f'No primitive root found for p={p}',
        'details': {'p': p, 'phi': phi, 'factors': list(factors)},
        'unit': 'dimensionless'
    }

def calc_discrete_log(g: int = 2, h: int = 3, p: int = 7) -> dict:
    """Discrete logarithm: find x such that g^x ≡ h (mod p) using baby-step giant-step."""
    g, h = g % p, h % p
    # Baby-step giant-step
    m = int(math.isqrt(p)) + 1
    # Baby steps: g^j mod p
    baby_steps = {}
    val = 1
    for j in range(m):
        if val not in baby_steps:
            baby_steps[val] = j
        val = (val * g) % p
    # Giant steps: h * (g^{-m})^i mod p
    factor = pow(g, -m, p)
    val = h
    x = None
    for i in range(m):
        if val in baby_steps:
            x = i * m + baby_steps[val]
            break
        val = (val * factor) % p
    if x is not None:
        return {
            'result': f'discrete_log_{g}({h}) mod {p} = {x} (check: {g}^{x} mod {p} = {pow(g,x,p)})',
            'details': {'g': g, 'h': h, 'p': p, 'm': m, 'x': x, 'verification': pow(g, x, p)},
            'unit': 'dimensionless'
        }
    return {
        'result': f'No discrete logarithm found for g={g}, h={h} mod {p}',
        'details': {'g': g, 'h': h, 'p': p, 'm': m},
        'unit': 'dimensionless'
    }

# ============================================================
# RSA
# ============================================================

def calc_rsa_keygen(p: int = 61, q: int = 53) -> dict:
    """RSA key generation: given primes p, q, compute n, phi, e, d."""
    n = p * q
    phi = (p - 1) * (q - 1)
    # Choose e: commonly 65537, or small coprime to phi
    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d = pow(e, -1, phi)
    return {
        'result': f'RSA keys: n={n}, e={e}, d={d}',
        'details': {
            'p': p, 'q': q, 'n': n, 'phi': phi, 'e': e, 'd': d,
            'public_key': (n, e), 'private_key': (n, d),
            'check': (e * d) % phi == 1
        },
        'unit': 'dimensionless'
    }

def calc_rsa_encrypt(message: int = 42, n: int = 3233, e: int = 17) -> dict:
    """RSA encryption: c = m^e mod n."""
    if message >= n:
        return {
            'result': f'Message {message} >= n={n}, cannot encrypt',
            'details': {'message': message, 'n': n, 'error': 'message >= modulus'},
            'unit': 'dimensionless'
        }
    c = pow(message, e, n)
    return {
        'result': f'Encrypted: c = {message}^{e} mod {n} = {c}',
        'details': {'plaintext': message, 'n': n, 'e': e, 'ciphertext': c},
        'unit': 'dimensionless'
    }

def calc_rsa_decrypt(ciphertext: int = 2557, n: int = 3233, d: int = 2753) -> dict:
    """RSA decryption: m = c^d mod n."""
    m = pow(ciphertext, d, n)
    return {
        'result': f'Decrypted: m = {ciphertext}^{d} mod {n} = {m}',
        'details': {'ciphertext': ciphertext, 'n': n, 'd': d, 'plaintext': m},
        'unit': 'dimensionless'
    }

def calc_rsa_sign(message: int = 42, n: int = 3233, d: int = 2753) -> dict:
    """RSA digital signature: s = m^d mod n."""
    s = pow(message, d, n)
    return {
        'result': f'Signature: s = {message}^{d} mod {n} = {s}',
        'details': {'message': message, 'n': n, 'd': d, 'signature': s,
                    'verify_with_public': f'm = s^e mod n = {pow(s, 0x10001, n) if n > 0 else "N/A"}'},
        'unit': 'dimensionless'
    }

# ============================================================
# Elliptic Curves
# ============================================================

def calc_elliptic_point_add(x1: float = 2.0, y1: float = 3.0, x2: float = 2.0,
                            y2: float = 3.0, a: float = 0.0, b: float = 7.0,
                            p: int = None) -> dict:
    """Point addition on elliptic curve y^2 = x^3 + ax + b. If p given, works mod p."""
    if p is not None:
        x1, y1, x2, y2, a, b = x1 % p, y1 % p, x2 % p, y2 % p, a % p, b % p
    # Identity element check
    if x1 is None and y1 is None:
        return {
            'result': f'P + Q = ({x2}, {y2})',
            'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'result_x': x2, 'result_y': y2},
            'unit': 'dimensionless'
        }
    if x2 is None and y2 is None:
        return {
            'result': f'P + Q = ({x1}, {y1})',
            'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'result_x': x1, 'result_y': y1},
            'unit': 'dimensionless'
        }
    # Check if inverse
    if x1 == x2 and (y1 == (-y2 if p is None else (-y2) % p)):
        return {
            'result': f'P + Q = O (point at infinity)',
            'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'result': 'O'},
            'unit': 'dimensionless'
        }
    # Compute slope
    if p is not None:
        if x1 == x2 and y1 == y2:
            # Point doubling
            if y1 == 0:
                return {'result': 'Point doubling gives O', 'details': {'result': 'O'}, 'unit': 'dimensionless'}
            num = (3 * x1 * x1 + a) % p
            den = (2 * y1) % p
            slope = (num * pow(den, -1, p)) % p
        else:
            num = (y2 - y1) % p
            den = (x2 - x1) % p
            slope = (num * pow(den, -1, p)) % p
        x3 = (slope * slope - x1 - x2) % p
        y3 = (slope * (x1 - x3) - y1) % p
    else:
        if x1 == x2 and y1 == y2:
            if y1 == 0:
                return {'result': 'Point doubling gives O', 'details': {'result': 'O'}, 'unit': 'dimensionless'}
            slope = (3 * x1 * x1 + a) / (2 * y1)
        else:
            slope = (y2 - y1) / (x2 - x1)
        x3 = slope * slope - x1 - x2
        y3 = slope * (x1 - x3) - y1
    return {
        'result': f'P + Q = ({x3}, {y3})',
        'details': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'a': a, 'b': b, 'p': p,
                    'slope': slope, 'result_x': x3, 'result_y': y3},
        'unit': 'dimensionless'
    }

def calc_elliptic_scalar_mult(k: int = 3, x: float = 2.0, y: float = 3.0,
                              a: float = 0.0, b: float = 7.0, p: int = None) -> dict:
    """Scalar multiplication k*P on elliptic curve using double-and-add."""
    if k == 0:
        return {'result': '0*P = O', 'details': {'k': 0, 'result': 'O'}, 'unit': 'dimensionless'}
    if k < 0:
        # Negate point
        y = -y if p is None else (-y) % p
        k = -k
    result_x, result_y = None, None  # Identity
    add_x, add_y = x, y
    steps = []
    while k > 0:
        if k & 1:
            # Add
            if result_x is None:
                result_x, result_y = add_x, add_y
            else:
                if p is not None:
                    if result_x == add_x and result_y == add_y:
                        if add_y == 0:
                            result_x, result_y = None, None
                        else:
                            num = (3 * result_x * result_x + a) % p
                            den = (2 * result_y) % p
                            slope = (num * pow(den, -1, p)) % p
                    else:
                        if result_x == add_x:
                            result_x, result_y = None, None
                        else:
                            num = (add_y - result_y) % p
                            den = (add_x - result_x) % p
                            slope = (num * pow(den, -1, p)) % p
                if result_x is not None and not (result_x == add_x and (result_y == (-add_y if p is None else (-add_y) % p))):
                    if p is not None:
                        x3 = (slope * slope - result_x - add_x) % p
                        y3 = (slope * (result_x - x3) - result_y) % p
                    else:
                        slope = ((3 * result_x * result_x + a) / (2 * result_y)
                                 if (result_x == add_x and result_y == add_y)
                                 else (add_y - result_y) / (add_x - result_x))
                        x3 = slope * slope - result_x - add_x
                        y3 = slope * (result_x - x3) - result_y
                    result_x, result_y = x3, y3
                steps.append(f'bit {k & 1}: added')
        # Double
        if add_y != 0 and add_x is not None:
            if p is not None:
                num = (3 * add_x * add_x + a) % p
                den = (2 * add_y) % p
                slope = (num * pow(den, -1, p)) % p
                add_x = (slope * slope - 2 * add_x) % p
                add_y = (slope * (add_x - (slope * slope - 2 * add_x)) - add_y) % p  # simplified
            # For simplicity, we skip non-modular double steps details
        k >>= 1
    if result_x is None:
        return {'result': f'{k}-fold doubling result = O', 'details': {}, 'unit': 'dimensionless'}
    return {
        'result': f'{k}*P = ({result_x}, {result_y})',
        'details': {'k_base': k, 'x': x, 'y': y, 'a': a, 'b': b, 'p': p,
                    'result_x': result_x, 'result_y': result_y},
        'unit': 'dimensionless'
    }

def calc_ecdh_key_exchange(private_a: int = 5, private_b: int = 7,
                           Gx: int = 2, Gy: int = 3, a: int = 0, b: int = 7, p: int = 97) -> dict:
    """Simplified ECDH key exchange using scalar multiplication on elliptic curve."""
    def scalar_mult_fixed(k, px, py):
        if k == 0:
            return None, None
        rx, ry = None, None
        ax, ay = px, py
        while k > 0:
            if k & 1:
                if rx is None:
                    rx, ry = ax, ay
                else:
                    if rx == ax and ry == ay:
                        if ry == 0:
                            return None, None
                        s = (3 * rx * rx + a) % p
                        s = (s * pow(2 * ry, -1, p)) % p
                    else:
                        if rx == ax:
                            return None, None
                        s = (ay - ry) % p
                        s = (s * pow((ax - rx) % p, -1, p)) % p
                    x3 = (s * s - rx - ax) % p
                    y3 = (s * (rx - x3) - ry) % p
                    rx, ry = x3, y3
            # double
            if ay != 0:
                s = (3 * ax * ax + a) % p
                s = (s * pow(2 * ay, -1, p)) % p
                ax2 = (s * s - 2 * ax) % p
                ay = (s * (ax - ax2) - ay) % p
                ax = ax2
            k >>= 1
        return rx, ry
    pub_a_x, pub_a_y = scalar_mult_fixed(private_a, Gx, Gy)
    pub_b_x, pub_b_y = scalar_mult_fixed(private_b, Gx, Gy)
    shared_a_x, shared_a_y = scalar_mult_fixed(private_a, pub_b_x, pub_b_y)
    shared_b_x, shared_b_y = scalar_mult_fixed(private_b, pub_a_x, pub_a_y)
    return {
        'result': f'Shared secret x-coordinate: {shared_a_x}',
        'details': {
            'curve': f'y^2 = x^3 + {a}x + {b} mod {p}',
            'G': (Gx, Gy),
            'private_A': private_a, 'public_A': (pub_a_x, pub_a_y),
            'private_B': private_b, 'public_B': (pub_b_x, pub_b_y),
            'shared_secret_x': shared_a_x,
            'match': shared_a_x == shared_b_x
        },
        'unit': 'dimensionless'
    }

def calc_point_on_curve(x: float = 2.0, y: float = 3.0, a: float = 0.0, b: float = 7.0,
                        p: int = None) -> dict:
    """Check if point (x,y) lies on elliptic curve y^2 = x^3 + ax + b."""
    if p is not None:
        lhs = (y * y) % p
        rhs = (pow(x, 3, p) + a * x + b) % p
    else:
        lhs = y * y
        rhs = x ** 3 + a * x + b
    on_curve = lhs == rhs
    return {
        'result': f'Point ({x}, {y}) is {"on" if on_curve else "NOT on"} the curve y^2 = x^3 + {a}x + {b}' + (f' mod {p}' if p else ''),
        'details': {'x': x, 'y': y, 'a': a, 'b': b, 'p': p, 'lhs': lhs, 'rhs': rhs, 'on_curve': on_curve},
        'unit': 'dimensionless'
    }

# ============================================================
# Other
# ============================================================

def calc_modular_exponentiation(base: int = 2, exp: int = 100, mod: int = 101) -> dict:
    """Fast modular exponentiation: base^exp mod mod using built-in pow (square-and-multiply)."""
    result = pow(base, exp, mod)
    return {
        'result': f'{base}^{exp} mod {mod} = {result}',
        'details': {'base': base, 'exponent': exp, 'modulus': mod, 'result': result},
        'unit': 'dimensionless'
    }

def calc_jacobi_symbol(a: int = 2, n: int = 15) -> dict:
    """Compute Jacobi symbol (a/n)."""
    if n <= 0 or n % 2 == 0:
        return {'result': f'Jacobi symbol requires odd positive n, got n={n}', 'details': {}, 'unit': 'dimensionless'}
    a %= n
    result = 1
    steps = []
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                result = -result
                steps.append(f'Factor 2, n%8={r}, flip sign')
            else:
                steps.append(f'Factor 2, n%8={r}, no sign change')
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
            steps.append(f'Swap: both ≡3 mod 4, flip sign')
        else:
            steps.append(f'Swap: no sign change')
        a %= n
    if n == 1:
        return {
            'result': f'Jacobi({a if "a" in dir() else "0"}/{n}) = {result}',
            'details': {'a_orig': a, 'n_orig': n, 'jacobi': result, 'steps': steps[-5:]},
            'unit': 'dimensionless'
        }
    return {
        'result': f'Jacobi symbol = {result}',
        'details': {'a': a, 'n': n, 'jacobi': result, 'legendre': result if n > 2 else None},
        'unit': 'dimensionless'
    }

def calc_jacobi_symbol_corrected(a: int = 2, n: int = 15) -> dict:
    """Compute Jacobi symbol (a/n) — corrected implementation."""
    if n <= 0 or n % 2 == 0:
        return {'result': f'Jacobi symbol requires odd positive n, got n={n}', 'details': {'error': True}, 'unit': 'dimensionless'}
    a_orig, n_orig = a, n
    a = a % n
    t = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            if r == 3 or r == 5:
                t = -t
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            t = -t
        a %= n
    if n == 1:
        return {
            'result': f'Jacobi({a_orig}/{n_orig}) = {t}',
            'details': {'a': a_orig, 'n': n_orig, 'jacobi': t},
            'unit': 'dimensionless'
        }
    return {'result': f'Jacobi({a_orig}/{n_orig}) = 0', 'details': {'a': a_orig, 'n': n_orig, 'jacobi': 0}, 'unit': 'dimensionless'}

def calc_legendre_symbol(a: int = 2, p: int = 7) -> dict:
    """Legendre symbol (a/p) for odd prime p using Euler's criterion: a^{(p-1)/2} mod p."""
    if p < 2:
        return {'result': 'p must be prime >= 2', 'details': {}, 'unit': 'dimensionless'}
    a = a % p
    if a == 0:
        leg = 0
    else:
        leg = pow(a, (p - 1) // 2, p)
        if leg == p - 1:
            leg = -1
        elif leg == 1:
            leg = 1
        else:
            leg = 0
    meaning = {1: 'quadratic residue', -1: 'quadratic non-residue', 0: 'zero (divisible by p)'}
    return {
        'result': f'Legendre({a}/{p}) = {leg} ({meaning.get(leg, "unknown")})',
        'details': {'a': a, 'p': p, 'legendre': leg, 'meaning': meaning.get(leg)},
        'unit': 'dimensionless'
    }

def calc_sqrt_mod_p(a: int = 2, p: int = 7) -> dict:
    """Square root modulo prime p using Tonelli-Shanks algorithm when it applies."""
    a = a % p
    if a == 0:
        return {'result': f'sqrt({a}) mod {p} = 0', 'details': {'a': a, 'p': p, 'roots': [0]}, 'unit': 'dimensionless'}
    # Check Legendre symbol
    if pow(a, (p - 1) // 2, p) != 1:
        return {
            'result': f'{a} is a quadratic non-residue mod {p}, no square root',
            'details': {'a': a, 'p': p, 'is_quadratic_residue': False},
            'unit': 'dimensionless'
        }
    # Simple cases
    if p % 4 == 3:
        root = pow(a, (p + 1) // 4, p)
        return {
            'result': f'sqrt({a}) mod {p} = ±{root} (mod {p})',
            'details': {'a': a, 'p': p, 'roots': [root, p - root],
                        'check': (root * root) % p == a},
            'unit': 'dimensionless'
        }
    if p % 8 == 5:
        v = pow(2 * a, (p - 5) // 8, p)
        root = (a * v * (2 * a * v * v - 1)) % p
        return {
            'result': f'sqrt({a}) mod {p} = ±{root} (mod {p})',
            'details': {'a': a, 'p': p, 'roots': [root, p - root],
                        'check': (root * root) % p == a},
            'unit': 'dimensionless'
        }
    # Tonelli-Shanks for general case
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    # Find a quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    M = S
    c = pow(z, Q, p)
    t = pow(a, Q, p)
    R = pow(a, (Q + 1) // 2, p)
    while t != 1:
        # Find least i such that t^(2^i) ≡ 1
        i = 1
        temp = (t * t) % p
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
        b = pow(c, 1 << (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p
    return {
        'result': f'sqrt({a}) mod {p} = ±{R} (mod {p})',
        'details': {'a': a, 'p': p, 'roots': [R, p - R], 'check': (R * R) % p == a},
        'unit': 'dimensionless'
    }

def calc_continued_fraction(value: float = 3.245, max_terms: int = 10) -> dict:
    """Compute continued fraction expansion of a real number."""
    x = value
    terms = []
    convergents = []
    h_prev2, h_prev1 = 0, 1
    k_prev2, k_prev1 = 1, 0
    for i in range(max_terms):
        a = int(math.floor(x))
        terms.append(a)
        h = a * h_prev1 + h_prev2
        k = a * k_prev1 + k_prev2
        if k != 0:
            convergents.append({'term': a, 'h': h, 'k': k, 'value': h / k})
        else:
            convergents.append({'term': a, 'h': h, 'k': k, 'value': float('inf')})
        h_prev2, h_prev1 = h_prev1, h
        k_prev2, k_prev1 = k_prev1, k
        frac = x - a
        if abs(frac) < 1e-15:
            break
        x = 1.0 / frac
    return {
        'result': f'Continued fraction of {value} = [{"; ".join(str(t) for t in terms)}]',
        'details': {'value': value, 'terms': terms, 'convergents': convergents},
        'unit': 'dimensionless'
    }

def calc_modular_system_congruences() -> dict:
    """Pre-built system of congruences solver (wraps CRT for 3 equations)."""
    # Return the CRT function with default values
    return calc_chinese_remainder([2, 3, 2], [3, 5, 7])


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'gcd': {'func': calc_gcd, 'params': ['a', 'b'], 'desc': 'GCD using Euclidean algorithm'},
    'lcm': {'func': calc_lcm, 'params': ['a', 'b'], 'desc': 'LCM using GCD relationship'},
    'extended_euclidean': {'func': calc_extended_euclidean, 'params': ['a', 'b'], 'desc': 'Extended Euclidean: ax+by=gcd(a,b)'},
    'divisibility_tests': {'func': calc_divisibility_tests, 'params': ['n'], 'desc': 'Test divisibility by 2-13'},
    'trial_division': {'func': calc_prime_trial_division, 'params': ['n'], 'desc': 'Primality via trial division'},
    'miller_rabin': {'func': calc_miller_rabin, 'params': ['n', 'k'], 'desc': 'Miller-Rabin primality test'},
    'sieve_eratosthenes': {'func': calc_sieve_eratosthenes, 'params': ['limit'], 'desc': 'Sieve of Eratosthenes up to limit'},
    'prime_counting': {'func': calc_prime_counting, 'params': ['x'], 'desc': 'Prime counting function pi(x)'},
    'prime_factorization': {'func': calc_prime_factorization, 'params': ['n'], 'desc': 'Prime factorization of n'},
    'next_prime': {'func': calc_next_prime, 'params': ['n'], 'desc': 'Next prime greater than n'},
    'modular_arithmetic': {'func': calc_modular_arithmetic, 'params': ['a', 'b', 'mod'], 'desc': 'Modular add/sub/mult/pow'},
    'modular_inverse': {'func': calc_modular_inverse, 'params': ['a', 'mod'], 'desc': 'Modular inverse a^{-1} mod m'},
    'chinese_remainder': {'func': calc_chinese_remainder, 'params': ['a_list', 'm_list'], 'desc': 'Chinese Remainder Theorem'},
    'linear_congruence': {'func': calc_linear_congruence, 'params': ['a', 'b', 'm'], 'desc': 'Solve ax ≡ b (mod m)'},
    'system_congruences': {'func': calc_modular_system_congruences, 'params': [], 'desc': 'System of congruences (CRT)'},
    'euler_totient': {'func': calc_euler_totient, 'params': ['n'], 'desc': "Euler's totient phi(n)"},
    'mobius': {'func': calc_mobius, 'params': ['n'], 'desc': 'Mobius function mu(n)'},
    'divisor_sigma': {'func': calc_divisor_sigma, 'params': ['n', 'k'], 'desc': 'Divisor function sigma_k(n)'},
    'carmichael': {'func': calc_carmichael, 'params': ['n'], 'desc': 'Carmichael function lambda(n)'},
    'linear_diophantine': {'func': calc_linear_diophantine, 'params': ['a', 'b', 'c'], 'desc': 'Solve ax+by=c'},
    'pythagorean_triples': {'func': calc_pythagorean_triples, 'params': ['max_c'], 'desc': 'Pythagorean triples with c <= max_c'},
    'pell_equation': {'func': calc_pell_equation, 'params': ['D', 'max_iter'], 'desc': "Solve Pell's equation x^2-Dy^2=1"},
    'finite_field_ops': {'func': calc_finite_field_ops, 'params': ['p', 'a', 'b'], 'desc': 'GF(p) field operations'},
    'primitive_root': {'func': calc_primitive_root, 'params': ['p'], 'desc': 'Find primitive root mod p'},
    'discrete_log': {'func': calc_discrete_log, 'params': ['g', 'h', 'p'], 'desc': 'Discrete log via baby-step giant-step'},
    'rsa_keygen': {'func': calc_rsa_keygen, 'params': ['p', 'q'], 'desc': 'RSA key generation'},
    'rsa_encrypt': {'func': calc_rsa_encrypt, 'params': ['message', 'n', 'e'], 'desc': 'RSA encryption'},
    'rsa_decrypt': {'func': calc_rsa_decrypt, 'params': ['ciphertext', 'n', 'd'], 'desc': 'RSA decryption'},
    'rsa_sign': {'func': calc_rsa_sign, 'params': ['message', 'n', 'd'], 'desc': 'RSA digital signature'},
    'elliptic_point_add': {'func': calc_elliptic_point_add, 'params': ['x1', 'y1', 'x2', 'y2', 'a', 'b', 'p'], 'desc': 'Elliptic curve point addition'},
    'elliptic_scalar_mult': {'func': calc_elliptic_scalar_mult, 'params': ['k', 'x', 'y', 'a', 'b', 'p'], 'desc': 'Elliptic curve scalar multiplication'},
    'ecdh_key_exchange': {'func': calc_ecdh_key_exchange, 'params': ['private_a', 'private_b', 'Gx', 'Gy', 'a', 'b', 'p'], 'desc': 'ECDH key exchange'},
    'point_on_curve': {'func': calc_point_on_curve, 'params': ['x', 'y', 'a', 'b', 'p'], 'desc': 'Check if point is on elliptic curve'},
    'modular_exponentiation': {'func': calc_modular_exponentiation, 'params': ['base', 'exp', 'mod'], 'desc': 'Fast modular exponentiation'},
    'jacobi_symbol': {'func': calc_jacobi_symbol_corrected, 'params': ['a', 'n'], 'desc': 'Jacobi symbol (a/n)'},
    'legendre_symbol': {'func': calc_legendre_symbol, 'params': ['a', 'p'], 'desc': 'Legendre symbol (a/p)'},
    'sqrt_mod_p': {'func': calc_sqrt_mod_p, 'params': ['a', 'p'], 'desc': 'Square root modulo prime p'},
    'continued_fraction': {'func': calc_continued_fraction, 'params': ['value', 'max_terms'], 'desc': 'Continued fraction expansion'},
}
