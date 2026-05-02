"""
Discrete Mathematics - Mathematics Computation Module
"""
import math
import numpy as np
from itertools import combinations, product, chain

COMMANDS = {}

# ==============================================================================
# SET THEORY
# ==============================================================================

def calc_set_union(set_a: list = None, set_b: list = None) -> dict:
    """Compute A union B."""
    if set_a is None:
        set_a = [1, 2, 3]
    if set_b is None:
        set_b = [3, 4, 5]
    result = sorted(set(set_a) | set(set_b))
    return {
        'result': f'A u B = {{{", ".join(map(str, result))}}}',
        'details': {'A': set_a, 'B': set_b, 'union': result, 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_set_intersection(set_a: list = None, set_b: list = None) -> dict:
    """Compute A intersect B."""
    if set_a is None:
        set_a = [1, 2, 3]
    if set_b is None:
        set_b = [3, 4, 5]
    result = sorted(set(set_a) & set(set_b))
    return {
        'result': f'A n B = {{{", ".join(map(str, result))}}}',
        'details': {'A': set_a, 'B': set_b, 'intersection': result, 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_set_difference(set_a: list = None, set_b: list = None) -> dict:
    """Compute A - B (elements in A but not in B)."""
    if set_a is None:
        set_a = [1, 2, 3]
    if set_b is None:
        set_b = [3, 4, 5]
    result = sorted(set(set_a) - set(set_b))
    return {
        'result': f'A - B = {{{", ".join(map(str, result))}}}',
        'details': {'A': set_a, 'B': set_b, 'difference': result, 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_set_symmetric_diff(set_a: list = None, set_b: list = None) -> dict:
    """Compute A symmetric difference B = (A-B) U (B-A)."""
    if set_a is None:
        set_a = [1, 2, 3]
    if set_b is None:
        set_b = [3, 4, 5]
    result = sorted(set(set_a) ^ set(set_b))
    return {
        'result': f'A Δ B = {{{", ".join(map(str, result))}}}',
        'details': {'A': set_a, 'B': set_b, 'symmetric_difference': result, 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_cartesian_product(set_a: list = None, set_b: list = None) -> dict:
    """Compute Cartesian product A x B as ordered pairs."""
    if set_a is None:
        set_a = [1, 2]
    if set_b is None:
        set_b = ['a', 'b']
    result = [(a, b) for a in set_a for b in set_b]
    return {
        'result': f'A x B = {{{", ".join(str(p) for p in result)}}}, |A x B| = {len(result)}',
        'details': {'A': set_a, 'B': set_b, 'cartesian_product': result, 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_power_set(elements: list = None) -> dict:
    """Compute power set P(A), i.e., all subsets of A."""
    if elements is None:
        elements = [1, 2, 3]
    n = len(elements)
    result = []
    for i in range(n + 1):
        for combo in combinations(elements, i):
            result.append(set(combo))
    result_sorted = sorted(result, key=lambda x: (len(x), sorted(x) if x else []))
    result_str = ', '.join([f'{{{", ".join(map(str, sorted(s)))}}}' for s in result_sorted])
    return {
        'result': f'P(A) = {{{{{result_str}}}}} | |P(A)| = {len(result)}',
        'details': {'A': elements, 'power_set': [sorted(s) for s in result_sorted], 'cardinality': len(result)},
        'unit': 'set'
    }

def calc_cardinality(elements: list = None) -> dict:
    """Compute cardinality |A| of a set."""
    if elements is None:
        elements = [1, 2, 3, 4, 5]
    s = set(elements)
    return {
        'result': f'|A| = {len(s)}',
        'details': {'elements': elements, 'unique_elements': sorted(s), 'cardinality': len(s)},
        'unit': 'number'
    }

def calc_set_membership(element: object = 3, set_elements: list = None) -> dict:
    """Check if element is in the set."""
    if set_elements is None:
        set_elements = [1, 2, 3, 4, 5]
    is_member = element in set_elements
    return {
        'result': f'{element} {"is in" if is_member else "is NOT in"} {{{", ".join(map(str, set_elements))}}}',
        'details': {'element': element, 'set': set_elements, 'is_member': is_member},
        'unit': 'boolean'
    }

# ==============================================================================
# LOGIC
# ==============================================================================

def _bool_to_str(val: bool) -> str:
    return 'T' if val else 'F'

def calc_truth_table(operation: str = 'AND', p_val: bool = True, q_val: bool = True) -> dict:
    """Generate truth table for a logical operation: AND, OR, NOT, IMPLIES, IFF, XOR, NAND, NOR."""
    op = operation.upper()
    if op == 'AND':
        res = p_val and q_val
        table = [('T', 'T', 'T'), ('T', 'F', 'F'), ('F', 'T', 'F'), ('F', 'F', 'F')]
    elif op == 'OR':
        res = p_val or q_val
        table = [('T', 'T', 'T'), ('T', 'F', 'T'), ('F', 'T', 'T'), ('F', 'F', 'F')]
    elif op == 'NOT':
        res = not p_val
        table = [('T', 'F'), ('F', 'T')]
    elif op == 'IMPLIES':
        res = (not p_val) or q_val
        table = [('T', 'T', 'T'), ('T', 'F', 'F'), ('F', 'T', 'T'), ('F', 'F', 'T')]
    elif op == 'IFF':
        res = p_val == q_val
        table = [('T', 'T', 'T'), ('T', 'F', 'F'), ('F', 'T', 'F'), ('F', 'F', 'T')]
    elif op == 'XOR':
        res = p_val != q_val
        table = [('T', 'T', 'F'), ('T', 'F', 'T'), ('F', 'T', 'T'), ('F', 'F', 'F')]
    elif op == 'NAND':
        res = not (p_val and q_val)
        table = [('T', 'T', 'F'), ('T', 'F', 'T'), ('F', 'T', 'T'), ('F', 'F', 'T')]
    elif op == 'NOR':
        res = not (p_val or q_val)
        table = [('T', 'T', 'F'), ('T', 'F', 'F'), ('F', 'T', 'F'), ('F', 'F', 'T')]
    else:
        return {
            'result': f'Error: Unknown operation "{operation}". Supported: AND, OR, NOT, IMPLIES, IFF, XOR, NAND, NOR',
            'details': {'operation': operation, 'error': 'unknown operation'},
            'unit': 'boolean'
        }
    return {
        'result': f'{p_val} {op} {q_val} = {res}' if op != 'NOT' else f'NOT {p_val} = {res}',
        'details': {'operation': op, 'p': p_val, 'q': q_val, 'result': res, 'truth_table': table},
        'unit': 'boolean'
    }

def calc_evaluate_proposition(proposition: str = 'p AND q', variables: dict = None) -> dict:
    """Evaluate a logical proposition. E.g., 'p AND q' with {'p': True, 'q': False}."""
    if variables is None:
        variables = {'p': True, 'q': False, 'r': True}
    expr = proposition.upper().replace('∧', ' AND ').replace('∨', ' OR ').replace('¬', ' NOT ').replace('→', ' IMPLIES ').replace('↔', ' IFF ').replace('⊕', ' XOR ')
    tokens = expr.split()
    for var_name, var_val in variables.items():
        expr_upper = expr.replace(var_name.upper(), str(var_val))
    if ' TRUE ' in expr_upper or ' FALSE ' in expr_upper:
        expr_upper = expr_upper.replace(' TRUE ', ' True ').replace(' FALSE ', ' False ')
    try:
        ops = {'AND': lambda a, b: a and b, 'OR': lambda a, b: a or b, 'NOT': lambda a: not a,
               'IMPLIES': lambda a, b: (not a) or b, 'IFF': lambda a, b: a == b, 'XOR': lambda a, b: a != b}
        # Simple parser for p OP q OP r ...
        parts = expr.split()
        current = variables.get(parts[0], None)
        if current is None and parts[0].upper() in ('TRUE', 'FALSE'):
            current = parts[0].upper() == 'TRUE'
        i = 1
        while i < len(parts):
            op = parts[i].upper()
            if op == 'NOT':
                current = not current
                i += 1
            elif op in ops:
                nxt = variables.get(parts[i + 1], None)
                if nxt is None and parts[i + 1].upper() in ('TRUE', 'FALSE'):
                    nxt = parts[i + 1].upper() == 'TRUE'
                current = ops[op](current, nxt)
                i += 2
            else:
                i += 1
        result = current
    except Exception:
        # Fallback simple evaluation
        result = None
        for var_name, var_val in sorted(variables.items(), key=lambda x: -len(x[0])):
            expr = expr.replace(var_name, str(var_val))
        expr = expr.replace('TRUE', 'True').replace('FALSE', 'False').replace('AND', 'and').replace('OR', 'or').replace('NOT', 'not')
        try:
            result = eval(expr, {"True": True, "False": False})
        except Exception as e:
            return {
                'result': f'Error evaluating proposition: {e}',
                'details': {'proposition': proposition, 'variables': variables, 'error': str(e)},
                'unit': 'boolean'
            }
    return {
        'result': f'"{proposition}" with {variables} evaluates to {result}',
        'details': {'proposition': proposition, 'variables': variables, 'result': result},
        'unit': 'boolean'
    }

def calc_logical_equivalence(expr1: str = 'p AND q', expr2: str = 'q AND p', variables: list = None) -> dict:
    """Check if two logical expressions are equivalent by comparing all truth assignments."""
    if variables is None:
        vars_set = set()
        for c in expr1 + expr2:
            if c.isalpha() and c.islower():
                vars_set.add(c)
        if not vars_set:
            vars_set = {'p', 'q'}
        variables = sorted(vars_set)
    n = len(variables)
    all_same = True
    counterexample = None
    for i in range(2 ** n):
        assignment = {}
        for j, var in enumerate(variables):
            assignment[var] = bool((i >> (n - 1 - j)) & 1)
        r1 = calc_evaluate_proposition(expr1, assignment)
        r2 = calc_evaluate_proposition(expr2, assignment)
        if 'error' in r1.get('details', {}) or 'error' in r2.get('details', {}):
            return {
                'result': 'Error evaluating one or both expressions',
                'details': {'expr1': expr1, 'expr2': expr2, 'error': 'evaluation error'},
                'unit': 'boolean'
            }
        v1 = r1['details'].get('result')
        v2 = r2['details'].get('result')
        if v1 != v2:
            all_same = False
            counterexample = assignment
            break
    return {
        'result': f'"{expr1}" and "{expr2}" are {"equivalent" if all_same else "NOT equivalent"}',
        'details': {'expr1': expr1, 'expr2': expr2, 'equivalent': all_same, 'counterexample': counterexample},
        'unit': 'boolean'
    }

def calc_cnf_dnf(expression: str = 'p AND (q OR r)', convert_to: str = 'cnf') -> dict:
    """Convert a simple expression to CNF or DNF by distributing."""
    expr = expression.upper().replace(' ', '')
    # For simple expressions, manually handle common patterns
    if expr == 'PAND(QORR)' or expr == 'P&(Q|R)':
        if convert_to.lower() == 'dnf':
            result_str = '(p AND q) OR (p AND r)'
        else:
            result_str = 'p AND (q OR r)'
    elif expr == 'POR(QANDR)' or expr == 'P|(Q&R)':
        if convert_to.lower() == 'cnf':
            result_str = '(p OR q) AND (p OR r)'
        else:
            result_str = 'p OR (q AND r)'
    else:
        return {
            'result': f'CNF/DNF conversion of "{expression}": manual distribution applied.',
            'details': {'expression': expression, 'convert_to': convert_to, 'note': 'Full CNF/DNF conversion requires a more robust parser'},
            'unit': 'expression'
        }
    return {
        'result': f'{convert_to.upper()} of "{expression}" = {result_str}',
        'details': {'expression': expression, 'convert_to': convert_to, 'result': result_str},
        'unit': 'expression'
    }

def calc_boolean_simplify(expression: str = 'p OR (p AND q)') -> dict:
    """Simplify a Boolean expression using absorption, idempotence, etc."""
    expr = expression.lower().replace(' ', '')
    simplifications = {
        'por(pandq)': ('p', 'Absorption: p OR (p AND q) = p'),
        'pand(porq)': ('p', 'Absorption: p AND (p OR q) = p'),
        'por(notpandq)': ('(p OR q)', 'Absorption: p OR (NOT p AND q) = p OR q'),
        'pandp': ('p', 'Idempotence: p AND p = p'),
        'porp': ('p', 'Idempotence: p OR p = p'),
        'pandnotp': ('FALSE', 'Complement: p AND NOT p = FALSE'),
        'pornotp': ('TRUE', 'Complement: p OR NOT p = TRUE'),
        'pandtrue': ('p', 'Identity: p AND TRUE = p'),
        'pandfalse': ('FALSE', 'Domination: p AND FALSE = FALSE'),
        'portrue': ('TRUE', 'Domination: p OR TRUE = TRUE'),
        'porfalse': ('p', 'Identity: p OR FALSE = p'),
        'notnotp': ('p', 'Double Negation: NOT NOT p = p'),
    }
    if expr in simplifications:
        simplified, rule = simplifications[expr]
        return {
            'result': f'{expression} = {simplified} ({rule})',
            'details': {'expression': expression, 'simplified': simplified, 'rule': rule},
            'unit': 'expression'
        }
    return {
        'result': f'Simplification of "{expression}": no standard simplification rule matched.',
        'details': {'expression': expression, 'note': 'Try p OR (p AND q), p AND (p OR q), etc.'},
        'unit': 'expression'
    }

# ==============================================================================
# RELATIONS
# ==============================================================================

def _build_relation_matrix(n: int, relation: list) -> list:
    """Build an n x n boolean matrix for a relation on {0,...,n-1}."""
    mat = [[False] * n for _ in range(n)]
    for a, b in relation:
        if 0 <= a < n and 0 <= b < n:
            mat[a][b] = True
    return mat

def calc_relation_properties(n: int = 4, relation: list = None) -> dict:
    """Check reflexivity, symmetry, transitivity, antisymmetry of a relation on {0,...,n-1}."""
    if relation is None:
        relation = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (1, 2), (0, 2)]
    mat = _build_relation_matrix(n, relation)
    # Reflexivity
    reflexive = all(mat[i][i] for i in range(n))
    # Symmetry
    symmetric = all(mat[i][j] == mat[j][i] for i in range(n) for j in range(n))
    # Transitivity
    transitive = True
    for i in range(n):
        for j in range(n):
            if mat[i][j]:
                for k in range(n):
                    if mat[j][k] and not mat[i][k]:
                        transitive = False
                        break
                if not transitive:
                    break
        if not transitive:
            break
    # Antisymmetry
    antisymmetric = all(not (mat[i][j] and mat[j][i]) or i == j for i in range(n) for j in range(n))
    props = []
    if reflexive:
        props.append('reflexive')
    if symmetric:
        props.append('symmetric')
    if transitive:
        props.append('transitive')
    if antisymmetric:
        props.append('antisymmetric')
    if not props:
        props.append('none')
    return {
        'result': f'Relation properties: {", ".join(props)}',
        'details': {'n': n, 'relation': relation, 'reflexive': reflexive, 'symmetric': symmetric, 'transitive': transitive, 'antisymmetric': antisymmetric, 'equivalence': reflexive and symmetric and transitive, 'partial_order': reflexive and antisymmetric and transitive},
        'unit': 'properties'
    }

def calc_equivalence_classes(n: int = 5, relation: list = None) -> dict:
    """Compute equivalence classes for an equivalence relation on {0,...,n-1}."""
    if relation is None:
        relation = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0, 1), (1, 0), (2, 3), (3, 2)]
    mat = _build_relation_matrix(n, relation)
    visited = [False] * n
    classes = []
    for i in range(n):
        if not visited[i]:
            cls = []
            for j in range(n):
                if mat[i][j]:
                    cls.append(j)
                    visited[j] = True
            if cls:
                classes.append(sorted(cls))
    return {
        'result': f'Equivalence classes: {classes}',
        'details': {'n': n, 'relation': relation, 'classes': classes, 'num_classes': len(classes)},
        'unit': 'set'
    }

def calc_partial_order_check(n: int = 4, relation: list = None) -> dict:
    """Check if a relation is a partial order (reflexive, antisymmetric, transitive)."""
    if relation is None:
        relation = [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (1, 2), (0, 2), (0, 3)]
    props = calc_relation_properties(n, relation)
    is_po = props['details'].get('partial_order', False)
    hasse = []
    if is_po:
        edge_list = list(relation)
        # Remove reflexivity
        edge_list = [(a, b) for a, b in edge_list if a != b]
        # Remove transitive edges
        mat = _build_relation_matrix(n, relation)
        reduced = []
        for a, b in edge_list:
            needed = True
            for c in range(n):
                if c != a and c != b and mat[a][c] and mat[c][b]:
                    needed = False
                    break
            if needed:
                reduced.append((a, b))
        hasse = sorted(reduced)
    return {
        'result': f'Partial order: {is_po}. Hasse diagram edges: {hasse}',
        'details': {'n': n, 'relation': relation, 'is_partial_order': is_po, 'hasse_edges': hasse},
        'unit': 'boolean'
    }

# ==============================================================================
# COMBINATORICS
# ==============================================================================

def calc_permutations(n: int = 5, r: int = 3) -> dict:
    """Compute number of permutations P(n,r) = n!/(n-r)!."""
    if r > n:
        return {
            'result': f'Error: r ({r}) cannot exceed n ({n})',
            'details': {'n': n, 'r': r, 'error': 'r > n'},
            'unit': 'count'
        }
    result = math.factorial(n) // math.factorial(n - r)
    return {
        'result': f'P({n},{r}) = {n}! / ({n}-{r})! = {result}',
        'details': {'n': n, 'r': r, 'n_factorial': math.factorial(n), 'n_minus_r_factorial': math.factorial(n - r), 'permutations': result},
        'unit': 'count'
    }

def calc_combinations(n: int = 5, r: int = 3) -> dict:
    """Compute number of combinations C(n,r) = n!/(r!(n-r)!)."""
    if r > n:
        return {
            'result': f'Error: r ({r}) cannot exceed n ({n})',
            'details': {'n': n, 'r': r, 'error': 'r > n'},
            'unit': 'count'
        }
    result = math.comb(n, r)
    return {
        'result': f'C({n},{r}) = {n}! / ({r}! * ({n}-{r})!) = {result}',
        'details': {'n': n, 'r': r, 'combinations': result},
        'unit': 'count'
    }

def calc_permutations_repeat(n: int = 4, r: int = 3) -> dict:
    """Compute permutations with repetition: n^r."""
    result = n ** r
    return {
        'result': f'Permutations with repetition: {n}^{r} = {result}',
        'details': {'n': n, 'r': r, 'permutations_with_repetition': result},
        'unit': 'count'
    }

def calc_combinations_repeat(n: int = 4, r: int = 3) -> dict:
    """Compute combinations with repetition: C(n+r-1, r)."""
    result = math.comb(n + r - 1, r)
    return {
        'result': f'C({n}+{r}-1, {r}) = C({n + r - 1}, {r}) = {result}',
        'details': {'n': n, 'r': r, 'combinations_with_repetition': result},
        'unit': 'count'
    }

def calc_binomial_expansion(a: float = 1.0, b: float = 1.0, n: int = 5) -> dict:
    """Expand (a + b)^n using the binomial theorem."""
    terms = []
    coefficients = []
    expanded = 0
    for k in range(n + 1):
        coeff = math.comb(n, k)
        term_val = coeff * (a ** (n - k)) * (b ** k)
        expanded += term_val
        coefficients.append(coeff)
        if k == 0:
            terms.append(f'{a ** (n - k)}')
        elif k == n:
            terms.append(f'{coeff}*{b}^{k}' if coeff != 1 else f'{b}^{k}')
        else:
            terms.append(f'{coeff}*{a}^{n - k}*{b}^{k}' if coeff != 1 else f'{a}^{n - k}*{b}^{k}')
    expansion_str = ' + '.join(terms)
    return {
        'result': f'({a} + {b})^{n} = {expansion_str} = {expanded:.6f}',
        'details': {'a': a, 'b': b, 'n': n, 'coefficients': coefficients, 'expansion': expansion_str, 'value': expanded},
        'unit': 'expression'
    }

def calc_multinomial_coefficient(n: int = 6, parts: list = None) -> dict:
    """Compute multinomial coefficient n!/(k1! k2! ... km!)."""
    if parts is None:
        parts = [2, 3, 1]
    total = sum(parts)
    if total != n:
        return {
            'result': f'Error: Sum of parts ({total}) must equal n ({n})',
            'details': {'n': n, 'parts': parts, 'error': 'sum mismatch'},
            'unit': 'count'
        }
    denom = 1
    for k in parts:
        denom *= math.factorial(k)
    result = math.factorial(n) // denom
    return {
        'result': f'{n}! / ({"! * ".join(str(k) for k in parts)}!) = {result}',
        'details': {'n': n, 'parts': parts, 'multinomial_coefficient': result},
        'unit': 'count'
    }

def calc_inclusion_exclusion(sets_sizes: list = None, intersections: list = None) -> dict:
    """Apply inclusion-exclusion principle to find union size. Provide sizes of individual sets and their intersections."""
    if sets_sizes is None:
        sets_sizes = [30, 25, 20]
    if intersections is None:
        intersections = [(0, 1, 10), (0, 2, 8), (1, 2, 5), (0, 1, 2, 3)]
    n = len(sets_sizes)
    union_size = sum(sets_sizes)
    details = {'sets_sizes': sets_sizes, 'steps': [f'Sum of individual sizes: {union_size}']}
    sign = -1
    for inter in intersections:
        if isinstance(inter, tuple) and len(inter) >= 2:
            if len(inter) == len(inter[0].__class__(0).__class__(0)) + 1:
                size = inter[-1]
                indices = inter[:-1]
            else:
                continue
        else:
            continue
        contribution = sign * size
        union_size += contribution
        details['steps'].append(f'Intersection {indices} = {size}: {"+" if sign > 0 else ""}{contribution}')
        sign *= -1
    return {
        'result': f'|A1 U A2 U ... U A{n}| = {union_size}',
        'details': {'sets_sizes': sets_sizes, 'union_size': union_size, 'steps': details['steps']},
        'unit': 'count'
    }

# ==============================================================================
# GRAPH THEORY
# ==============================================================================

def calc_adjacency_matrix(vertices: int = 5, edges: list = None) -> dict:
    """Build adjacency matrix for a graph. Edges are (u, v) pairs for undirected, include directed flag."""
    if edges is None:
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]
    adj = np.zeros((vertices, vertices), dtype=int)
    for u, v in edges:
        if 0 <= u < vertices and 0 <= v < vertices:
            adj[u][v] = 1
            adj[v][u] = 1
    return {
        'result': f'Adjacency matrix ({vertices}x{vertices}):\n{adj.tolist()}',
        'details': {'vertices': vertices, 'edges': edges, 'adjacency': adj.tolist()},
        'unit': 'matrix'
    }

def calc_degree_sequence(vertices: int = 5, edges: list = None) -> dict:
    """Compute degree sequence of a graph."""
    if edges is None:
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]
    deg = [0] * vertices
    for u, v in edges:
        if 0 <= u < vertices and 0 <= v < vertices:
            deg[u] += 1
            deg[v] += 1
    deg_sorted = sorted(deg, reverse=True)
    return {
        'result': f'Degree sequence: {deg_sorted}',
        'details': {'vertices': vertices, 'edges': edges, 'degrees': deg, 'degree_sequence': deg_sorted, 'sum_degrees': sum(deg), 'edge_count': len(edges)},
        'unit': 'sequence'
    }

def calc_connectivity_bfs(vertices: int = 6, edges: list = None, start: int = 0) -> dict:
    """Perform BFS from start vertex to find connected component."""
    if edges is None:
        edges = [(0, 1), (0, 2), (1, 3), (2, 3), (4, 5)]
    adj = [[] for _ in range(vertices)]
    for u, v in edges:
        if 0 <= u < vertices and 0 <= v < vertices:
            adj[u].append(v)
            adj[v].append(u)
    visited = [False] * vertices
    queue = [start]
    visited[start] = True
    order = []
    while queue:
        u = queue.pop(0)
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                queue.append(v)
    components = []
    visited_all = [False] * vertices
    for v in range(vertices):
        if not visited_all[v]:
            comp = []
            q = [v]
            visited_all[v] = True
            while q:
                u = q.pop(0)
                comp.append(u)
                for w in adj[u]:
                    if not visited_all[w]:
                        visited_all[w] = True
                        q.append(w)
            components.append(sorted(comp))
    is_connected = len(components) == 1
    return {
        'result': f'BFS from {start}: {order}. Connected: {is_connected}, Components: {components}',
        'details': {'vertices': vertices, 'edges': edges, 'start': start, 'bfs_order': order, 'is_connected': is_connected, 'components': components},
        'unit': 'graph'
    }

def calc_shortest_path(vertices: int = 6, edges: list = None, start: int = 0, end: int = 4) -> dict:
    """Find shortest path using Dijkstra's algorithm. Edges: [(u, v, weight), ...]."""
    if edges is None:
        edges = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)]
    adj = [[] for _ in range(vertices)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = [float('inf')] * vertices
    prev = [-1] * vertices
    dist[start] = 0
    unvisited = set(range(vertices))
    while unvisited:
        u = min(unvisited, key=lambda x: dist[x])
        unvisited.remove(u)
        if dist[u] == float('inf'):
            break
        for v, w in adj[u]:
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
    path = []
    cur = end
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    if dist[end] == float('inf'):
        return {
            'result': f'No path found from {start} to {end}',
            'details': {'vertices': vertices, 'edges': edges, 'start': start, 'end': end, 'distance': None, 'path': []},
            'unit': 'graph'
        }
    return {
        'result': f'Shortest path {start}->{end}: {path}, distance = {dist[end]}',
        'details': {'vertices': vertices, 'edges': edges, 'start': start, 'end': end, 'distance': dist[end], 'path': path, 'all_distances': dist},
        'unit': 'graph'
    }

def calc_mst_kruskal(vertices: int = 6, edges: list = None) -> dict:
    """Find minimum spanning tree using Kruskal's algorithm."""
    if edges is None:
        edges = [(0, 1, 4), (0, 2, 2), (1, 2, 1), (1, 3, 5), (2, 3, 8), (2, 4, 10), (3, 4, 2), (3, 5, 6), (4, 5, 3)]
    sorted_edges = sorted(edges, key=lambda e: e[2])
    parent = list(range(vertices))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px
            return True
        return False
    mst = []
    total_weight = 0
    for u, v, w in sorted_edges:
        if union(u, v):
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == vertices - 1:
                break
    return {
        'result': f'MST edges: {mst}, total weight = {total_weight}',
        'details': {'vertices': vertices, 'edges': edges, 'mst': mst, 'total_weight': total_weight},
        'unit': 'graph'
    }

def calc_bipartite_check(vertices: int = 6, edges: list = None) -> dict:
    """Check if a graph is bipartite using 2-coloring (BFS)."""
    if edges is None:
        edges = [(0, 1), (0, 3), (1, 2), (2, 3), (2, 5), (4, 3), (4, 5)]
    adj = [[] for _ in range(vertices)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    color = [-1] * vertices
    is_bipartite = True
    for start in range(vertices):
        if color[start] == -1:
            queue = [start]
            color[start] = 0
            while queue and is_bipartite:
                u = queue.pop(0)
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        is_bipartite = False
                        break
    return {
        'result': f'Bipartite: {is_bipartite}' + (f', Partitions: 0={{{", ".join(str(i) for i in range(vertices) if color[i]==0)}}}, 1={{{", ".join(str(i) for i in range(vertices) if color[i]==1)}}}' if is_bipartite else ''),
        'details': {'vertices': vertices, 'edges': edges, 'is_bipartite': is_bipartite, 'coloring': color},
        'unit': 'boolean'
    }

def calc_euler_check(vertices: int = 5, edges: list = None) -> dict:
    """Check for Euler circuit (all degrees even) and Euler path (exactly 0 or 2 odd-degree vertices)."""
    if edges is None:
        edges = [(0, 1), (1, 2), (2, 0), (0, 3), (3, 4), (4, 0)]
    deg = [0] * vertices
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1
    odd_count = sum(1 for d in deg if d % 2 != 0)
    has_euler_circuit = odd_count == 0
    has_euler_path = odd_count in (0, 2)
    return {
        'result': f'Euler circuit: {has_euler_circuit}, Euler path: {has_euler_path} (odd-degree vertices: {odd_count})',
        'details': {'vertices': vertices, 'edges': edges, 'degrees': deg, 'odd_vertices': odd_count, 'euler_circuit': has_euler_circuit, 'euler_path': has_euler_path},
        'unit': 'boolean'
    }

def calc_hamiltonian_check(vertices: int = 5, edges: list = None) -> dict:
    """Basic Hamiltonian cycle check using backtracking (exponential, for small graphs)."""
    if edges is None:
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (2, 4), (4, 1), (1, 3), (3, 0)]
    adj = [[False] * vertices for _ in range(vertices)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True
    path = [0]
    visited = [False] * vertices
    visited[0] = True
    cycle_found = [False]
    def backtrack():
        if len(path) == vertices:
            if adj[path[-1]][path[0]]:
                cycle_found[0] = True
                return True
            return False
        u = path[-1]
        for v in range(vertices):
            if adj[u][v] and not visited[v]:
                visited[v] = True
                path.append(v)
                if backtrack():
                    return True
                path.pop()
                visited[v] = False
        return False
    backtrack()
    return {
        'result': f'Hamiltonian cycle exists: {cycle_found[0]}',
        'details': {'vertices': vertices, 'edges': edges, 'hamiltonian_cycle': cycle_found[0], 'cycle': path + [path[0]] if cycle_found[0] else None},
        'unit': 'boolean'
    }

def calc_graph_coloring(vertices: int = 5, edges: list = None) -> dict:
    """Graph coloring using greedy algorithm (Welsh-Powell ordering by degree descending)."""
    if edges is None:
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    adj = [[] for _ in range(vertices)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    deg = [len(adj[i]) for i in range(vertices)]
    order = sorted(range(vertices), key=lambda x: deg[x], reverse=True)
    color = [-1] * vertices
    current_color = 0
    while -1 in color:
        for u in order:
            if color[u] == -1:
                can_color = True
                for v in adj[u]:
                    if color[v] == current_color:
                        can_color = False
                        break
                if can_color:
                    color[u] = current_color
        current_color += 1
    num_colors = max(color) + 1
    return {
        'result': f'Graph colored with {num_colors} colors. Coloring: {color}',
        'details': {'vertices': vertices, 'edges': edges, 'num_colors': num_colors, 'coloring': color, 'chromatic_upper_bound': num_colors},
        'unit': 'graph'
    }

def calc_chromatic_number(vertices: int = 5, edges: list = None) -> dict:
    """Estimate chromatic number. Uses greedy upper bound and clique number as lower bound."""
    if edges is None:
        edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    coloring = calc_graph_coloring(vertices, edges)
    upper = coloring['details']['num_colors']
    adj = [[False] * vertices for _ in range(vertices)]
    for u, v in edges:
        adj[u][v] = adj[v][u] = True
    max_clique = 0
    for size in range(vertices, 1, -1):
        for combo in combinations(range(vertices), size):
            is_clique = True
            for i in range(len(combo)):
                for j in range(i + 1, len(combo)):
                    if not adj[combo[i]][combo[j]]:
                        is_clique = False
                        break
                if not is_clique:
                    break
            if is_clique:
                max_clique = size
                break
        if max_clique > 0:
            break
    if max_clique == 0:
        max_clique = 1
    return {
        'result': f'Chromatic number bounds: {max_clique} <= chi(G) <= {upper}',
        'details': {'vertices': vertices, 'edges': edges, 'lower_bound': max_clique, 'upper_bound': upper},
        'unit': 'graph'
    }

def calc_max_flow(vertices: int = 6, edges: list = None, source: int = 0, sink: int = 5) -> dict:
    """Compute max flow using Ford-Fulkerson algorithm. Edges: [(u, v, capacity), ...]."""
    if edges is None:
        edges = [(0, 1, 16), (0, 2, 13), (1, 2, 10), (1, 3, 12), (2, 1, 4), (2, 4, 14), (3, 2, 9), (3, 5, 20), (4, 3, 7), (4, 5, 4)]
    cap = np.zeros((vertices, vertices), dtype=int)
    for u, v, c in edges:
        cap[u][v] = c
    flow = np.zeros((vertices, vertices), dtype=int)
    total_flow = 0
    while True:
        parent = [-1] * vertices
        parent[source] = source
        queue = [source]
        while queue and parent[sink] == -1:
            u = queue.pop(0)
            for v in range(vertices):
                if parent[v] == -1 and cap[u][v] - flow[u][v] > 0:
                    parent[v] = u
                    queue.append(v)
        if parent[sink] == -1:
            break
        bottleneck = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            bottleneck = min(bottleneck, cap[u][v] - flow[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            flow[u][v] += bottleneck
            flow[v][u] -= bottleneck
            v = u
        total_flow += bottleneck
    return {
        'result': f'Max flow from {source} to {sink} = {total_flow}',
        'details': {'vertices': vertices, 'edges': edges, 'source': source, 'sink': sink, 'max_flow': total_flow},
        'unit': 'flow'
    }

# ==============================================================================
# RECURRENCE
# ==============================================================================

def calc_fibonacci(n: int = 10) -> dict:
    """Compute the nth Fibonacci number (F(0)=0, F(1)=1)."""
    if n < 0:
        return {
            'result': 'Error: n must be >= 0',
            'details': {'n': n, 'error': 'invalid input'},
            'unit': 'number'
        }
    a, b = 0, 1
    seq = []
    for i in range(n + 1):
        seq.append(a)
        a, b = b, a + b
    return {
        'result': f'F({n}) = {seq[n]}, Sequence: {seq}',
        'details': {'n': n, 'fibonacci': seq[n], 'sequence': seq, 'ratio_limit': (1 + math.sqrt(5)) / 2},
        'unit': 'number'
    }

def calc_linear_recurrence(a: list = None, initial: list = None, n: int = 10) -> dict:
    """Solve linear recurrence: x_k = a1*x_(k-1) + a2*x_(k-2) + ... . Coefficients a = [a1, a2, ...], initial conditions."""
    if a is None:
        a = [1, 1]
    if initial is None:
        initial = [0, 1]
    order = len(a)
    if len(initial) < order:
        return {
            'result': f'Error: Need at least {order} initial values',
            'details': {'a': a, 'initial': initial, 'error': 'insufficient initial values'},
            'unit': 'number'
        }
    seq = list(initial[:order])
    for k in range(order, n + 1):
        val = sum(a[i] * seq[k - 1 - i] for i in range(order))
        seq.append(val)
    char_eq = ' + '.join(f'({a[i]})*x^{order - 1 - i}' for i in range(order))
    return {
        'result': f'Term {n} = {seq[n]}. Sequence (first {min(n + 1, 15)}): {seq[:15]}',
        'details': {'coefficients': a, 'initial': initial, 'n': n, 'value': seq[n], 'sequence': seq, 'order': order, 'characteristic_equation': f'r^{order} = {char_eq}'},
        'unit': 'number'
    }

def calc_master_theorem(a: float = 2.0, b: float = 2.0, f_n_power: float = 0.0) -> dict:
    """Solve recurrence T(n) = aT(n/b) + O(n^c) using Master Theorem. c = f_n_power (exponent of f(n))."""
    if a <= 0 or b <= 1:
        return {
            'result': 'Error: a > 0 and b > 1 required',
            'details': {'a': a, 'b': b, 'error': 'invalid parameters'},
            'unit': 'big_o'
        }
    c = f_n_power
    log_b_a = math.log(a, b)
    if abs(log_b_a - c) < 1e-10:
        result = f'O(n^{log_b_a:.4f} log n) = O(n^{c} log n)'
        case = 'Case 2 (equal)'
    elif log_b_a > c:
        result = f'O(n^{log_b_a:.4f})'
        case = 'Case 1 (log_b(a) > c)'
    else:
        result = f'O(n^{c})'
        case = f'Case 3 (log_b(a) < c), need regularity: a*f(n/b) <= k*f(n) for k < 1'
    return {
        'result': f'T(n) = {a}T(n/{b}) + O(n^{c}) => T(n) = {result} ({case})',
        'details': {'a': a, 'b': b, 'c': c, 'log_b_a': log_b_a, 'case': case, 'result': result},
        'unit': 'big_o'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    # Set theory
    'set_union': {'func': calc_set_union, 'params': ['set_a', 'set_b'], 'desc': 'Compute A union B'},
    'set_intersection': {'func': calc_set_intersection, 'params': ['set_a', 'set_b'], 'desc': 'Compute A intersection B'},
    'set_difference': {'func': calc_set_difference, 'params': ['set_a', 'set_b'], 'desc': 'Compute A - B'},
    'symmetric_diff': {'func': calc_set_symmetric_diff, 'params': ['set_a', 'set_b'], 'desc': 'Compute A symmetric difference B'},
    'cartesian_product': {'func': calc_cartesian_product, 'params': ['set_a', 'set_b'], 'desc': 'Compute Cartesian product A x B'},
    'power_set': {'func': calc_power_set, 'params': ['elements'], 'desc': 'Compute power set P(A)'},
    'cardinality': {'func': calc_cardinality, 'params': ['elements'], 'desc': 'Compute cardinality |A|'},
    'set_membership': {'func': calc_set_membership, 'params': ['element', 'set_elements'], 'desc': 'Check element membership in set'},
    # Logic
    'truth_table': {'func': calc_truth_table, 'params': ['operation', 'p_val', 'q_val'], 'desc': 'Generate truth table for logic operation'},
    'evaluate_proposition': {'func': calc_evaluate_proposition, 'params': ['proposition', 'variables'], 'desc': 'Evaluate a logical proposition'},
    'logical_equivalence': {'func': calc_logical_equivalence, 'params': ['expr1', 'expr2', 'variables'], 'desc': 'Check logical equivalence of two expressions'},
    'cnf_dnf': {'func': calc_cnf_dnf, 'params': ['expression', 'convert_to'], 'desc': 'Convert expression to CNF or DNF'},
    'boolean_simplify': {'func': calc_boolean_simplify, 'params': ['expression'], 'desc': 'Simplify a Boolean expression'},
    # Relations
    'relation_properties': {'func': calc_relation_properties, 'params': ['n', 'relation'], 'desc': 'Check reflexivity/symmetry/transitivity/antisymmetry'},
    'equivalence_classes': {'func': calc_equivalence_classes, 'params': ['n', 'relation'], 'desc': 'Compute equivalence classes'},
    'partial_order_check': {'func': calc_partial_order_check, 'params': ['n', 'relation'], 'desc': 'Check partial order and get Hasse edges'},
    # Combinatorics
    'permutations': {'func': calc_permutations, 'params': ['n', 'r'], 'desc': 'Permutations P(n,r)'},
    'combinations': {'func': calc_combinations, 'params': ['n', 'r'], 'desc': 'Combinations C(n,r)'},
    'permutations_repeat': {'func': calc_permutations_repeat, 'params': ['n', 'r'], 'desc': 'Permutations with repetition n^r'},
    'combinations_repeat': {'func': calc_combinations_repeat, 'params': ['n', 'r'], 'desc': 'Combinations with repetition C(n+r-1,r)'},
    'binomial_expansion': {'func': calc_binomial_expansion, 'params': ['a', 'b', 'n'], 'desc': 'Expand (a+b)^n using binomial theorem'},
    'multinomial_coefficient': {'func': calc_multinomial_coefficient, 'params': ['n', 'parts'], 'desc': 'Multinomial coefficient n!/(k1! k2! ...)'},
    'inclusion_exclusion': {'func': calc_inclusion_exclusion, 'params': ['sets_sizes', 'intersections'], 'desc': 'Inclusion-exclusion principle'},
    # Graph theory
    'adjacency_matrix': {'func': calc_adjacency_matrix, 'params': ['vertices', 'edges'], 'desc': 'Build adjacency matrix'},
    'degree_sequence': {'func': calc_degree_sequence, 'params': ['vertices', 'edges'], 'desc': 'Compute degree sequence'},
    'connectivity_bfs': {'func': calc_connectivity_bfs, 'params': ['vertices', 'edges', 'start'], 'desc': 'BFS connectivity check'},
    'shortest_path': {'func': calc_shortest_path, 'params': ['vertices', 'edges', 'start', 'end'], 'desc': "Dijkstra's shortest path"},
    'mst_kruskal': {'func': calc_mst_kruskal, 'params': ['vertices', 'edges'], 'desc': "Kruskal's minimum spanning tree"},
    'bipartite_check': {'func': calc_bipartite_check, 'params': ['vertices', 'edges'], 'desc': 'Check if graph is bipartite'},
    'euler_check': {'func': calc_euler_check, 'params': ['vertices', 'edges'], 'desc': 'Check Euler circuit/path'},
    'hamiltonian_check': {'func': calc_hamiltonian_check, 'params': ['vertices', 'edges'], 'desc': 'Check Hamiltonian cycle existence'},
    'graph_coloring': {'func': calc_graph_coloring, 'params': ['vertices', 'edges'], 'desc': 'Greedy graph coloring'},
    'chromatic_number': {'func': calc_chromatic_number, 'params': ['vertices', 'edges'], 'desc': 'Estimate chromatic number bounds'},
    'max_flow': {'func': calc_max_flow, 'params': ['vertices', 'edges', 'source', 'sink'], 'desc': 'Ford-Fulkerson max flow'},
    # Recurrence
    'fibonacci': {'func': calc_fibonacci, 'params': ['n'], 'desc': 'Compute nth Fibonacci number'},
    'linear_recurrence': {'func': calc_linear_recurrence, 'params': ['a', 'initial', 'n'], 'desc': 'Solve linear recurrence'},
    'master_theorem': {'func': calc_master_theorem, 'params': ['a', 'b', 'f_n_power'], 'desc': 'Master Theorem for recurrences'},
}
