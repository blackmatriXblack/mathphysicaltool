"""Abstract algebra: groups, rings, fields, permutations, number theory."""

import math
import numpy as np


def _parse_csv(s, fn=int):
    return [fn(v.strip()) for v in s.split(',')]


def group_z_mod_add(a=3, b=4, n=6):
    val = (a + b) % n
    return {'result': str(val), 'details': {'a': a, 'b': b, 'modulus': n, 'sum': val}, 'unit': ''}


def group_z_mod_mul(a=3, b=2, n=7):
    val = (a * b) % n
    return {'result': str(val), 'details': {'a': a, 'b': b, 'modulus': n, 'product': val}, 'unit': ''}


def group_order(element=3, modulus=7):
    val, k = element % modulus, 1
    cur = val
    while cur != 1 and k < modulus:
        cur = (cur * val) % modulus
        k += 1
    if cur != 1:
        k = None
    return {'result': str(k), 'details': {'element': element, 'modulus': modulus, 'order': k}, 'unit': ''}


def cyclic_group_generator(n=7):
    gens = []
    for g in range(1, n):
        if math.gcd(g, n) != 1:
            continue
        seen = set()
        cur = 1
        for _ in range(n):
            cur = (cur * g) % n
            seen.add(cur)
        if len(seen) == sum(1 for x in range(1, n) if math.gcd(x, n) == 1):
            gens.append(g)
    return {'result': str(gens), 'details': {'n': n, 'generators': gens}, 'unit': ''}


def permutation_sign(p='2,3,1,4'):
    arr = _parse_csv(p)
    inv = sum(1 for i in range(len(arr)) for j in range(i+1, len(arr)) if arr[i] > arr[j])
    sign = 1 if inv % 2 == 0 else -1
    return {'result': str(sign), 'details': {'permutation': arr, 'inversions': inv, 'sign': sign}, 'unit': ''}


def permutation_multiply(p1='2,1,3', p2='1,3,2'):
    a = _parse_csv(p1)
    b = _parse_csv(p2)
    result = [a[b[i]-1] for i in range(len(a))]
    return {'result': str(result), 'details': {'p1': a, 'p2': b, 'p1∘p2': result}, 'unit': ''}


def ring_zn_operations(a=3, b=5, n=7):
    add = (a + b) % n
    mul = (a * b) % n
    return {'result': f'add={add}, mul={mul}', 'details': {'a': a, 'b': b, 'n': n, 'addition': add, 'multiplication': mul}, 'unit': ''}


def euler_totient(n=12):
    val = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            val -= val // p
        p += 1
    if temp > 1:
        val -= val // temp
    return {'result': str(val), 'details': {'n': n, 'phi(n)': val}, 'unit': ''}


def chinese_remainder(a1=2, m1=3, a2=3, m2=5):
    for x in range(m1 * m2):
        if x % m1 == a1 % m1 and x % m2 == a2 % m2:
            return {'result': str(x), 'details': {'a1': a1, 'm1': m1, 'a2': a2, 'm2': m2, 'x': x, 'modulus': m1*m2}, 'unit': ''}
    return {'result': 'None', 'details': {'error': 'no solution'}, 'unit': ''}


def finite_field_gf_p(prime=5):
    table = [[(i * j) % prime for j in range(prime)] for i in range(prime)]
    return {'result': str(table), 'details': {'prime': prime, 'multiplication_table': table}, 'unit': ''}


def subgroup_check(elements='0,2,4', modulus=6):
    elts = _parse_csv(elements)
    closed = all(((a+b) % modulus) in elts for a in elts for b in elts)
    has_id = 0 in elts
    invs = all(((modulus - a) % modulus if a != 0 else 0) in elts for a in elts)
    is_sg = closed and has_id and invs
    return {'result': str(is_sg), 'details': {'elements': elts, 'modulus': modulus, 'closed': closed, 'has_identity': has_id, 'has_inverses': invs, 'is_subgroup': is_sg}, 'unit': ''}


COMMANDS = {
    'mod-add':    {'func': group_z_mod_add,       'params': ['a','b','n'], 'desc': 'Addition modulo n: (a+b) mod n'},
    'mod-mul':    {'func': group_z_mod_mul,       'params': ['a','b','n'], 'desc': 'Multiplication modulo n: (a*b) mod n'},
    'group-order':{'func': group_order,           'params': ['element','modulus'], 'desc': 'Order of element in Z_n*'},
    'generator':  {'func': cyclic_group_generator,'params': ['n'],        'desc': 'Find generators of cyclic group Z_n*'},
    'perm-sign':  {'func': permutation_sign,      'params': ['p'],        'desc': 'Sign of permutation (+1 even, -1 odd)'},
    'perm-mult':  {'func': permutation_multiply,  'params': ['p1','p2'],  'desc': 'Compose permutations p1∘p2'},
    'ring-ops':   {'func': ring_zn_operations,    'params': ['a','b','n'],'desc': 'Addition and multiplication in Z_n ring'},
    'totient':    {'func': euler_totient,         'params': ['n'],        'desc': "Euler's totient φ(n)"},
    'crt':        {'func': chinese_remainder,     'params': ['a1','m1','a2','m2'], 'desc': 'Chinese Remainder Theorem x≡a_i(mod m_i)'},
    'gf-table':   {'func': finite_field_gf_p,     'params': ['prime'],    'desc': 'Multiplication table for GF(p)'},
    'subgroup':   {'func': subgroup_check,        'params': ['elements','modulus'], 'desc': 'Check if subset is subgroup of Z_n under addition'},
}
