"""
Optimization & Operations Research - Mathematics Computation Module
"""
import math
import random

COMMANDS = {}

# ============================================================
# Linear Programming
# ============================================================

def calc_simplex_2var(c1: float = 3.0, c2: float = 2.0,
                      a11: float = 1.0, a12: float = 1.0, b1: float = 4.0,
                      a21: float = 1.0, a22: float = 3.0, b2: float = 6.0,
                      maximize: bool = True) -> dict:
    """Solve 2-variable LP graphically: max/min Z = c1*x + c2*y subject to constraints.
    Constraints: a11*x + a12*y <= b1, a21*x + a22*y <= b2, x>=0, y>=0."""
    # Find all intersection points
    points = [(0, 0)]
    # x-intercept constraint 1
    if a11 != 0:
        x_int = b1 / a11
        if x_int >= 0:
            points.append((x_int, 0))
    # y-intercept constraint 1
    if a12 != 0:
        y_int = b1 / a12
        if y_int >= 0:
            points.append((0, y_int))
    # x-intercept constraint 2
    if a21 != 0:
        x_int = b2 / a21
        if x_int >= 0:
            points.append((x_int, 0))
    # y-intercept constraint 2
    if a22 != 0:
        y_int = b2 / a22
        if y_int >= 0:
            points.append((0, y_int))
    # Intersection of the two lines
    det = a11 * a22 - a12 * a21
    if abs(det) > 1e-10:
        x_int = (b1 * a22 - b2 * a12) / det
        y_int = (a11 * b2 - a21 * b1) / det
        if x_int >= -1e-10 and y_int >= -1e-10:
            points.append((x_int, y_int))
    # Filter feasible points
    feasible = []
    for x, y in points:
        x = max(0, x)
        y = max(0, y)
        if (a11 * x + a12 * y <= b1 + 1e-10 and
            a21 * x + a22 * y <= b2 + 1e-10):
            feasible.append((x, y))
    # Remove duplicates
    feasible = list(set((round(x, 10), round(y, 10)) for x, y in feasible))
    if not feasible:
        return {
            'result': 'No feasible solution found',
            'details': {'constraints': f'{a11}x+{a12}y<={b1}, {a21}x+{a22}y<={b2}',
                        'feasible': False},
            'unit': 'dimensionless'
        }
    # Evaluate objective
    best_val = float('-inf') if maximize else float('inf')
    best_pt = None
    evaluations = []
    for x, y in feasible:
        z = c1 * x + c2 * y
        evaluations.append({'x': x, 'y': y, 'Z': z})
        if maximize and z > best_val:
            best_val, best_pt = z, (x, y)
        if not maximize and z < best_val:
            best_val, best_pt = z, (x, y)
    return {
        'result': f'Optimal {"max" if maximize else "min"} Z = {best_val:.4f} at (x={best_pt[0]:.4f}, y={best_pt[1]:.4f})',
        'details': {
            'objective': f'Z = {c1}x + {c2}y',
            'maximize': maximize,
            'optimal_point': {'x': round(best_pt[0], 6), 'y': round(best_pt[1], 6)},
            'optimal_value': round(best_val, 6),
            'all_feasible': evaluations,
            'corner_points': feasible
        },
        'unit': 'dimensionless'
    }

def calc_standard_form(c: list = None, A: list = None, b: list = None) -> dict:
    """Convert LP to standard form: min c^T x s.t. Ax = b, x >= 0."""
    if c is None:
        c = [3, 2]
    if A is None:
        A = [[1, 1], [2, 1]]
    if b is None:
        b = [4, 5]
    n_vars = len(c)
    n_constraints = len(A)
    num_slack = n_constraints
    # Add slack variables
    new_c = c + [0] * num_slack
    new_A = [row + [0] * num_slack for row in A]
    for i in range(num_slack):
        new_A[i][n_vars + i] = 1
    return {
        'result': f'Standard form: min c^T x, {n_constraints} constraints, {n_vars + num_slack} variables',
        'details': {
            'original_vars': n_vars, 'slack_vars': num_slack,
            'total_vars': n_vars + num_slack, 'num_constraints': n_constraints,
            'c': new_c[:10],
            'A': [row[:10] for row in new_A],
            'b': b,
            'form': 'min c^T x subject to Ax = b, x >= 0'
        },
        'unit': 'dimensionless'
    }

def calc_basic_feasible_solution(A: list = None, b: list = None, basis: list = None) -> dict:
    """Find a basic feasible solution given A, b, and basis indices."""
    if A is None:
        A = [[2, 1, 1, 0], [1, 1, 0, 1]]
    if b is None:
        b = [8, 6]
    if basis is None:
        basis = [2, 3]
    m = len(A)
    n = len(A[0]) if A else 0
    # Extract basis matrix
    B = [[A[i][j] for j in basis] for i in range(m)]
    # Solve B*x_B = b using Cramer's rule for small systems
    det = B[0][0] * B[1][1] - B[0][1] * B[1][0] if m == 2 else None
    if det is not None and abs(det) > 1e-10:
        xB1 = (b[0] * B[1][1] - b[1] * B[0][1]) / det
        xB2 = (B[0][0] * b[1] - B[1][0] * b[0]) / det
        xB = [xB1, xB2]
        feasible = all(v >= -1e-10 for v in xB)
        x_full = [0.0] * n
        for idx, val in zip(basis, xB):
            x_full[idx] = val
        return {
            'result': f'{"Feasible" if feasible else "Infeasible"} basic solution: x = {[round(v,4) for v in x_full]}',
            'details': {
                'A': A, 'b': b, 'basis': basis, 'x_B': [round(v, 6) for v in xB],
                'x': [round(v, 6) for v in x_full], 'feasible': feasible
            },
            'unit': 'dimensionless'
        }
    return {
        'result': 'Could not solve basis system',
        'details': {'A': A, 'b': b, 'basis': basis},
        'unit': 'dimensionless'
    }

def calc_shadow_prices(c: list = None, A: list = None, b: list = None, basis: list = None) -> dict:
    """Compute shadow prices (dual variables) y = c_B^T * B^{-1} for LP."""
    if c is None:
        c = [3, 2, 0, 0]
    if A is None:
        A = [[2, 1, 1, 0], [1, 1, 0, 1]]
    if b is None:
        b = [8, 6]
    if basis is None:
        basis = [0, 1]
    m = len(A)
    cB = [c[j] for j in basis]
    B = [[A[i][j] for j in basis] for i in range(m)]
    det = B[0][0] * B[1][1] - B[0][1] * B[1][0]
    if abs(det) > 1e-10:
        B_inv = [[B[1][1] / det, -B[0][1] / det],
                  [-B[1][0] / det, B[0][0] / det]]
        y = [cB[0] * B_inv[0][0] + cB[1] * B_inv[1][0],
             cB[0] * B_inv[0][1] + cB[1] * B_inv[1][1]]
        return {
            'result': f'Shadow prices: y = [{y[0]:.4f}, {y[1]:.4f}]',
            'details': {
                'c': c, 'A': A, 'b': b, 'basis': basis, 'c_B': cB,
                'B': B, 'B_inv': B_inv, 'shadow_prices': y,
                'interpretation': 'Marginal value of relaxing each constraint'
            },
            'unit': 'dimensionless'
        }
    return {'result': 'Could not compute shadow prices', 'details': {}, 'unit': 'dimensionless'}

# ============================================================
# Nonlinear Optimization
# ============================================================

def calc_gradient_descent_1d(f_expr: str = 'x**2 + 2*x + 1', x0: float = 5.0,
                             lr: float = 0.1, max_iter: int = 100) -> dict:
    """Gradient descent for 1D function minimization."""
    x = x0
    history = [{'iter': 0, 'x': x, 'f': None}]
    for i in range(max_iter):
        # Numerical gradient
        h = 1e-6
        fx_ph = eval(f_expr, {'x': x + h, 'math': math, 'sin': math.sin, 'cos': math.cos,
                               'exp': math.exp, 'log': math.log})
        fx_mh = eval(f_expr, {'x': x - h, 'math': math, 'sin': math.sin, 'cos': math.cos,
                               'exp': math.exp, 'log': math.log})
        grad = (fx_ph - fx_mh) / (2 * h)
        x_new = x - lr * grad
        fx = eval(f_expr, {'x': x, 'math': math, 'sin': math.sin, 'cos': math.cos,
                          'exp': math.exp, 'log': math.log})
        history.append({'iter': i + 1, 'x': x_new, 'f': fx, 'grad': grad})
        if abs(x_new - x) < 1e-8:
            x = x_new
            break
        x = x_new
    fx_final = eval(f_expr, {'x': x, 'math': math, 'sin': math.sin, 'cos': math.cos,
                              'exp': math.exp, 'log': math.log})
    return {
        'result': f'Minimum at x = {x:.6f}, f(x) = {fx_final:.6f}',
        'details': {
            'f': f_expr, 'x0': x0, 'lr': lr, 'iterations': len(history) - 1,
            'final_x': x, 'final_f': fx_final, 'converged': len(history) <= max_iter
        },
        'unit': 'dimensionless'
    }

def calc_gradient_descent_2d(x0: float = 3.0, y0: float = 3.0,
                             lr: float = 0.1, max_iter: int = 200) -> dict:
    """Gradient descent for 2D Rosenbrock function f(x,y)=(1-x)^2+100(y-x^2)^2."""
    x, y = x0, y0
    history = []
    for i in range(max_iter):
        # Rosenbrock function and gradient
        f_val = (1 - x)**2 + 100 * (y - x**2)**2
        df_dx = -2 * (1 - x) - 400 * x * (y - x**2)
        df_dy = 200 * (y - x**2)
        history.append({'iter': i, 'x': x, 'y': y, 'f': f_val,
                        'grad_norm': math.sqrt(df_dx**2 + df_dy**2)})
        if math.sqrt(df_dx**2 + df_dy**2) < 1e-6:
            break
        x_new = x - lr * df_dx
        y_new = y - lr * df_dy
        if abs(x_new - x) < 1e-10 and abs(y_new - y) < 1e-10:
            break
        x, y = x_new, y_new
    return {
        'result': f'Minimum at ({x:.6f}, {y:.6f}), f = {f_val:.6f}',
        'details': {
            'function': 'Rosenbrock: (1-x)^2 + 100(y-x^2)^2',
            'x0': x0, 'y0': y0, 'lr': lr,
            'final_x': x, 'final_y': y, 'final_f': f_val,
            'iterations': len(history), 'converged': len(history) < max_iter
        },
        'unit': 'dimensionless'
    }

def calc_newton_optimization(f_expr: str = 'x**4 - 3*x**3 + 2',
                             x0: float = 2.0, max_iter: int = 50) -> dict:
    """Newton's method for optimization: find stationary point of f."""
    x = x0
    history = []
    for i in range(max_iter):
        h = 1e-6
        ctx = {'x': x, 'math': math, 'sin': math.sin, 'cos': math.cos,
               'exp': math.exp, 'log': math.log}
        f_ph = eval(f_expr, {**ctx, 'x': x + h})
        f_mh = eval(f_expr, {**ctx, 'x': x - h})
        f0 = eval(f_expr, ctx)
        f_prime = (f_ph - f_mh) / (2 * h)
        f_double = (f_ph - 2 * f0 + f_mh) / (h * h)
        history.append({'iter': i, 'x': x, 'f': f0, 'f_prime': f_prime, 'f_double': f_double})
        if abs(f_prime) < 1e-8:
            break
        if abs(f_double) < 1e-12:
            break
        x_new = x - f_prime / f_double
        if abs(x_new - x) < 1e-10:
            break
        x = x_new
    return {
        'result': f'Stationary point at x = {x:.6f}, f(x) = {f0:.6f}',
        'details': {
            'f': f_expr, 'x0': x0, 'final_x': x, 'final_f': f0,
            'f_prime': f_prime, 'f_double': f_double,
            'iterations': len(history),
            'nature': 'minimum' if f_double > 0 else ('maximum' if f_double < 0 else 'inflection/saddle')
        },
        'unit': 'dimensionless'
    }

def calc_golden_section(f_expr: str = 'x**2 + 2*x', a: float = -5.0, b: float = 5.0,
                        tol: float = 1e-6, max_iter: int = 100) -> dict:
    """Golden-section search for 1D function minimum on interval [a,b]."""
    phi = (1 + math.sqrt(5)) / 2
    inv_phi = 1.0 / phi
    x1 = b - (b - a) / phi
    x2 = a + (b - a) / phi
    ctx_template = {'math': math, 'sin': math.sin, 'cos': math.cos,
                    'exp': math.exp, 'log': math.log}
    f1 = eval(f_expr, {**ctx_template, 'x': x1})
    f2 = eval(f_expr, {**ctx_template, 'x': x2})
    history = [{'iter': 0, 'a': a, 'b': b, 'x1': x1, 'x2': x2, 'f1': f1, 'f2': f2}]
    for i in range(max_iter):
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = b - (b - a) / phi
            f1 = eval(f_expr, {**ctx_template, 'x': x1})
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + (b - a) / phi
            f2 = eval(f_expr, {**ctx_template, 'x': x2})
        history.append({'iter': i + 1, 'a': a, 'b': b})
        if abs(b - a) < tol:
            break
    x_min = (a + b) / 2
    f_min = eval(f_expr, {**ctx_template, 'x': x_min})
    return {
        'result': f'Minimum at x = {x_min:.6f}, f(x) = {f_min:.6f}',
        'details': {
            'f': f_expr, 'interval': [a, b], 'final_x': x_min, 'final_f': f_min,
            'final_interval': [a, b], 'iterations': len(history), 'tolerance': tol
        },
        'unit': 'dimensionless'
    }

def calc_lagrange_multiplier(f_expr: str = 'x**2 + y**2',
                             g_expr: str = 'x + y - 1',
                             guess_xy: list = None) -> dict:
    """Solve constrained optimization using Lagrange multipliers (2 variables).
    Solve: min/max f(x,y) subject to g(x,y) = 0."""
    if guess_xy is None:
        guess_xy = [0.5, 0.5]
    x, y = guess_xy[0], guess_xy[1]
    ctx = {'x': x, 'y': y, 'math': math, 'sin': math.sin, 'cos': math.cos,
           'exp': math.exp, 'log': math.log}
    # Use Newton's method on the Lagrange system
    for i in range(50):
        # f = f(x,y), g = g(x,y) = 0
        lam = 0  # estimate lambda
        h = 1e-6
        # Gradients via finite difference
        f0 = eval(f_expr, ctx)
        g0 = eval(g_expr, ctx)
        fx = (eval(f_expr, {**ctx, 'x': x + h}) - f0) / h
        fy = (eval(f_expr, {**ctx, 'y': y + h}) - f0) / h
        gx = (eval(g_expr, {**ctx, 'x': x + h}) - g0) / h
        gy = (eval(g_expr, {**ctx, 'y': y + h}) - g0) / h
        lam = fx / gx if abs(gx) > 1e-10 else fy / gy if abs(gy) > 1e-10 else 1.0
        # Solve linearized system
        # Hessian approximated
        fxx = (eval(f_expr, {**ctx, 'x': x + h}) - 2 * f0 + eval(f_expr, {**ctx, 'x': x - h})) / (h * h)
        fyy = (eval(f_expr, {**ctx, 'y': y + h}) - 2 * f0 + eval(f_expr, {**ctx, 'y': y - h})) / (h * h)
        fxy = 0  # cross via finite diff
        gxx = (eval(g_expr, {**ctx, 'x': x + h}) - 2 * g0 + eval(g_expr, {**ctx, 'x': x - h})) / (h * h)
        gyy = (eval(g_expr, {**ctx, 'y': y + h}) - 2 * g0 + eval(g_expr, {**ctx, 'y': y - h})) / (h * h)
        # System: [fxx-lam*gxx, fxy-lam*gxy, gx; fxy-lam*gxy, fyy-lam*gyy, gy; gx, gy, 0] * [dx, dy, dlam] = -[fx-lam*gx, fy-lam*gy, g]
        rhs1 = -(fx - lam * gx)
        rhs2 = -(fy - lam * gy)
        rhs3 = -g0
        det = gx * gx + gy * gy
        if abs(det) < 1e-12:
            break
        # Simplified update for 2-variable case
        dx = (rhs3 * gx + rhs1) / (fxx if abs(fxx) > 1e-10 else 1.0)
        dy = (rhs3 * gy + rhs2) / (fyy if abs(fyy) > 1e-10 else 1.0)
        if abs(dx) < 1e-8 and abs(dy) < 1e-8:
            break
        x += 0.1 * dx
        y += 0.1 * dy
        ctx = {**ctx, 'x': x, 'y': y}
    f_final = eval(f_expr, ctx)
    g_final = eval(g_expr, ctx)
    return {
        'result': f'Stationary point at ({x:.6f}, {y:.6f}), f = {f_final:.6f}, g = {g_final:.6f}',
        'details': {
            'f': f_expr, 'constraint': g_expr,
            'x': x, 'y': y, 'f_val': f_final, 'g_val': g_final,
            'lambda': lam
        },
        'unit': 'dimensionless'
    }

def calc_kkt_conditions(x: list = None, lagrange: list = None,
                        f_expr: str = 'x**2 + y**2',
                        g_expr: str = 'x + y - 2') -> dict:
    """Check KKT conditions at point x with multiplier lambda for min f s.t. g=0."""
    if x is None:
        x = [1.0, 1.0]
    if lagrange is None:
        lagrange = 2.0  # lambda
    h = 1e-6
    ctx = {'x': x[0], 'y': x[1], 'math': math}
    f0 = eval(f_expr, ctx)
    fx = (eval(f_expr, {**ctx, 'x': x[0] + h}) - f0) / h
    fy = (eval(f_expr, {**ctx, 'y': x[1] + h}) - f0) / h
    g0 = eval(g_expr, ctx)
    gx = (eval(g_expr, {**ctx, 'x': x[0] + h}) - g0) / h
    gy = (eval(g_expr, {**ctx, 'y': x[1] + h}) - g0) / h
    lam = lagrange
    # Stationarity
    stat1 = abs(fx - lam * gx)
    stat2 = abs(fy - lam * gy)
    stationarity_satisfied = stat1 < 1e-4 and stat2 < 1e-4
    primal_feasible = abs(g0) < 1e-6
    return {
        'result': f'KKT: Stationarity={"OK" if stationarity_satisfied else "FAIL"}, Primal Feasibility={"OK" if primal_feasible else "FAIL"}',
        'details': {
            'x': x, 'lambda': lam,
            'grad_f': [fx, fy], 'grad_g': [gx, gy],
            'stationarity': [stat1, stat2], 'stationarity_ok': stationarity_satisfied,
            'primal_feasibility': g0, 'primal_ok': primal_feasible
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Integer Programming
# ============================================================

def calc_branch_and_bound(c: list = None, A: list = None, b: list = None) -> dict:
    """Simple branch and bound for 2-variable 0-1 integer program."""
    if c is None:
        c = [5, 3]
    if A is None:
        A = [[2, 1]]
    if b is None:
        b = [4]
    best_val = float('-inf')
    best_x = None
    nodes_explored = 0
    # Enumerate all 0/1 combinations for small problems
    for x1 in range(2):
        for x2 in range(2):
            feasible = True
            for i, row in enumerate(A):
                if row[0] * x1 + row[1] * x2 > b[i]:
                    feasible = False
                    break
            if feasible:
                nodes_explored += 1
                val = c[0] * x1 + c[1] * x2
                if val > best_val:
                    best_val = val
                    best_x = [x1, x2]
    return {
        'result': f'Optimal IP solution: x = {best_x}, Z = {best_val}',
        'details': {
            'c': c, 'A': A, 'b': b,
            'optimal_x': best_x, 'optimal_value': best_val,
            'nodes_explored': nodes_explored
        },
        'unit': 'dimensionless'
    }

def calc_knapsack_01(values: list = None, weights: list = None, capacity: float = 10.0) -> dict:
    """0/1 Knapsack problem solved via dynamic programming."""
    if values is None:
        values = [60, 100, 120]
    if weights is None:
        weights = [10, 20, 30]
    n = len(values)
    W = int(capacity)
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - int(weights[i - 1])] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    # Backtrack
    selected = []
    w = W
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            w -= int(weights[i - 1])
    selected.reverse()
    return {
        'result': f'Max value: {dp[n][W]}, selected items: {selected}',
        'details': {
            'values': values, 'weights': weights, 'capacity': capacity,
            'max_value': dp[n][W], 'selected_items': selected,
            'selected_values': [values[i] for i in selected],
            'selected_weights': [weights[i] for i in selected],
            'total_weight': sum(weights[i] for i in selected)
        },
        'unit': 'dimensionless'
    }

def calc_assignment_problem(cost_matrix: list = None) -> dict:
    """Assignment problem solved via Hungarian algorithm (minimization)."""
    if cost_matrix is None:
        cost_matrix = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
    n = len(cost_matrix)
    # Step 1: Subtract row minimum
    matrix = [row[:] for row in cost_matrix]
    for i in range(n):
        min_val = min(matrix[i])
        for j in range(n):
            matrix[i][j] -= min_val
    # Step 2: Subtract column minimum
    for j in range(n):
        min_val = min(matrix[i][j] for i in range(n))
        for i in range(n):
            matrix[i][j] -= min_val
    # Step 3: Cover zeros with minimum lines
    # For simplicity, handle small matrices with brute force
    assignment = [-1] * n
    assigned = [False] * n
    for i in range(n):
        for j in range(n):
            if not assigned[j] and matrix[i][j] == 0:
                assignment[i] = j
                assigned[j] = True
                break
    # Resolve unassigned
    for i in range(n):
        if assignment[i] == -1:
            for j in range(n):
                if not assigned[j]:
                    assignment[i] = j
                    assigned[j] = True
                    break
    total_cost = sum(cost_matrix[i][assignment[i]] for i in range(n))
    return {
        'result': f'Optimal assignment total cost: {total_cost}',
        'details': {
            'cost_matrix': cost_matrix,
            'assignment': {f'worker_{i}': f'task_{assignment[i]}' for i in range(n)},
            'assignment_list': assignment,
            'total_cost': total_cost
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Dynamic Programming
# ============================================================

def calc_shortest_path_dag(edges: list = None, num_nodes: int = 6, source: int = 0) -> dict:
    """Shortest path in DAG using DP topological order."""
    if edges is None:
        edges = [(0, 1, 5), (0, 2, 3), (1, 3, 6), (1, 2, 2), (2, 4, 4),
                 (2, 5, 2), (2, 3, 7), (3, 5, 1), (4, 5, 3)]
    # Build adjacency
    adj = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        adj[u].append((v, w))
    # Topological sort (assuming DAG)
    visited = [False] * num_nodes
    topo = []
    def dfs(u):
        visited[u] = True
        for v, _ in adj[u]:
            if not visited[v]:
                dfs(v)
        topo.append(u)
    for i in range(num_nodes):
        if not visited[i]:
            dfs(i)
    topo.reverse()
    # DP
    INF = float('inf')
    dist = [INF] * num_nodes
    dist[source] = 0
    pred = [-1] * num_nodes
    for u in topo:
        if dist[u] != INF:
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    pred[v] = u
    paths = {}
    for i in range(num_nodes):
        if dist[i] != INF:
            path = []
            curr = i
            while curr != -1:
                path.append(curr)
                curr = pred[curr]
            path.reverse()
            paths[i] = path
    return {
        'result': f'Shortest distances from node {source}: {dist}',
        'details': {
            'edges': edges, 'num_nodes': num_nodes, 'source': source,
            'distances': dist, 'paths': paths, 'topo_order': topo
        },
        'unit': 'dimensionless'
    }

def calc_matrix_chain(dims: list = None) -> dict:
    """Matrix chain multiplication: find optimal parenthesization."""
    if dims is None:
        dims = [10, 30, 5, 60]
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k
    def build_parens(i, j):
        if i == j:
            return f'M{i+1}'
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f'({left} x {right})'
    parens = build_parens(0, n - 1)
    return {
        'result': f'Min scalar multiplications: {dp[0][n-1]}, order: {parens}',
        'details': {
            'dimensions': dims, 'min_cost': dp[0][n - 1],
            'parenthesization': parens, 'dp_table': dp
        },
        'unit': 'dimensionless'
    }

def calc_lcs(s1: str = 'AGGTAB', s2: str = 'GXTXAYB') -> dict:
    """Longest Common Subsequence (LCS) of two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # Backtrack
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            lcs.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    lcs.reverse()
    return {
        'result': f'LCS: "{"".join(lcs)}", length = {len(lcs)}',
        'details': {
            's1': s1, 's2': s2, 'lcs': ''.join(lcs),
            'length': len(lcs), 'lcs_list': lcs, 'dp_shape': [m + 1, n + 1]
        },
        'unit': 'dimensionless'
    }

def calc_edit_distance(s1: str = 'kitten', s2: str = 'sitting') -> dict:
    """Edit distance (Levenshtein) between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return {
        'result': f'Edit distance("{s1}", "{s2}") = {dp[m][n]}',
        'details': {
            's1': s1, 's2': s2, 'distance': dp[m][n],
            'operations': 'insert/delete/substitute'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Queueing Theory
# ============================================================

def calc_mm1_queue(arrival_rate: float = 2.0, service_rate: float = 3.0) -> dict:
    """M/M/1 queue analysis: arrival rate λ, service rate μ."""
    lam, mu = arrival_rate, service_rate
    rho = lam / mu
    if rho >= 1:
        return {
            'result': f'System unstable: rho = {rho:.4f} >= 1',
            'details': {'lambda': lam, 'mu': mu, 'rho': rho, 'unstable': True},
            'unit': 'dimensionless'
        }
    L = rho / (1 - rho)
    Lq = rho * rho / (1 - rho)
    W = 1 / (mu - lam)
    Wq = rho / (mu - lam)
    P0 = 1 - rho
    return {
        'result': f'M/M/1: L={L:.4f}, Lq={Lq:.4f}, W={W:.4f}, Wq={Wq:.4f}',
        'details': {
            'lambda': lam, 'mu': mu, 'rho': rho,
            'L': L, 'Lq': Lq, 'W': W, 'Wq': Wq,
            'P0': P0, 'Pn_formula': f'(1-rho)*rho^n'
        },
        'unit': 'dimensionless'
    }

def calc_mmc_queue(arrival_rate: float = 3.0, service_rate: float = 2.0,
                   num_servers: int = 2) -> dict:
    """M/M/c queue analysis."""
    lam, mu, c = arrival_rate, service_rate, num_servers
    rho = lam / (c * mu)
    if rho >= 1:
        return {
            'result': f'System unstable: rho = {rho:.4f} >= 1',
            'details': {'lambda': lam, 'mu': mu, 'c': c, 'rho': rho, 'unstable': True},
            'unit': 'dimensionless'
        }
    # P0
    sum_term = sum((lam / mu) ** n / math.factorial(n) for n in range(c))
    last_term = ((lam / mu) ** c) / (math.factorial(c) * (1 - rho))
    P0 = 1 / (sum_term + last_term)
    # Lq
    Lq = (P0 * (lam / mu) ** c * rho) / (math.factorial(c) * (1 - rho) ** 2)
    L = Lq + lam / mu
    Wq = Lq / lam
    W = L / lam
    return {
        'result': f'M/M/{c}: L={L:.4f}, Lq={Lq:.4f}, W={W:.4f}, Wq={Wq:.4f}',
        'details': {
            'lambda': lam, 'mu': mu, 'c': c, 'rho': rho,
            'L': L, 'Lq': Lq, 'W': W, 'Wq': Wq, 'P0': P0
        },
        'unit': 'dimensionless'
    }

def calc_mg1_queue(arrival_rate: float = 1.0, mean_service: float = 0.4,
                   var_service: float = 0.02) -> dict:
    """M/G/1 queue: Pollaczek-Khinchine formula."""
    lam = arrival_rate
    ES = mean_service
    ES2 = var_service + ES * ES
    rho = lam * ES
    if rho >= 1:
        return {
            'result': f'System unstable: rho = {rho:.4f} >= 1',
            'details': {'lambda': lam, 'ES': ES, 'rho': rho, 'unstable': True},
            'unit': 'dimensionless'
        }
    Lq = (lam ** 2 * ES2) / (2 * (1 - rho))
    Wq = Lq / lam
    L = Lq + rho
    W = L / lam
    return {
        'result': f'M/G/1: L={L:.4f}, Lq={Lq:.4f}, W={W:.4f}, Wq={Wq:.4f}',
        'details': {
            'lambda': lam, 'ES': ES, 'Var_S': var_service, 'ES2': ES2, 'rho': rho,
            'L': L, 'Lq': Lq, 'W': W, 'Wq': Wq
        },
        'unit': 'dimensionless'
    }

def calc_littles_law(L: float = 10.0, lam: float = 2.0) -> dict:
    """Little's Law: L = lambda * W. Given L and lambda, compute W."""
    W = L / lam if lam > 0 else 0
    return {
        'result': f"Little's Law: L={L}, lambda={lam} => W = {W:.4f}",
        'details': {
            'L': L, 'lambda': lam, 'W': W,
            'formula': 'L = lambda * W',
            'alternate_forms': {
                'W_from_L': W, 'L_from_W': lam * 5
            }
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Inventory
# ============================================================

def calc_eoq(demand_rate: float = 1000.0, ordering_cost: float = 50.0,
             holding_cost: float = 2.5) -> dict:
    """Economic Order Quantity: Q* = sqrt(2DS/H)."""
    D, S, H = demand_rate, ordering_cost, holding_cost
    Q_opt = math.sqrt(2 * D * S / H)
    total_cost = (D / Q_opt) * S + (Q_opt / 2) * H
    return {
        'result': f'EOQ = {Q_opt:.2f} units, Total annual cost = ${total_cost:.2f}',
        'details': {
            'demand_rate_D': D, 'ordering_cost_S': S, 'holding_cost_H': H,
            'EOQ': round(Q_opt, 4), 'order_frequency': D / Q_opt,
            'total_annual_cost': round(total_cost, 4),
            'ordering_cost_component': (D / Q_opt) * S,
            'holding_cost_component': (Q_opt / 2) * H
        },
        'unit': 'units'
    }

def calc_reorder_point(daily_demand: float = 50.0, lead_time_days: float = 7.0,
                       safety_stock: float = 100.0) -> dict:
    """Reorder Point: ROP = d * L + SS."""
    ROP = daily_demand * lead_time_days + safety_stock
    return {
        'result': f'ROP = {ROP:.0f} units (demand during lead time + safety stock)',
        'details': {
            'daily_demand': daily_demand, 'lead_time_days': lead_time_days,
            'safety_stock': safety_stock, 'ROP': ROP,
            'demand_during_lead_time': daily_demand * lead_time_days
        },
        'unit': 'units'
    }

def calc_safety_stock(z_score: float = 1.96, std_dev_lead_time: float = 30.0,
                      avg_lead_time: float = 7.0) -> dict:
    """Safety stock = z * sigma * sqrt(L)."""
    ss = z_score * std_dev_lead_time * math.sqrt(avg_lead_time)
    return {
        'result': f'Safety stock = {ss:.2f} units (service level: {z_score:.2f} sigma)',
        'details': {
            'z_score': z_score, 'std_dev_demand': std_dev_lead_time,
            'lead_time': avg_lead_time, 'safety_stock': round(ss, 4),
            'service_level': f'{z_score} sigma (~{95 if z_score==1.96 else 99 if z_score==2.58 else "?"}% service level)'
        },
        'unit': 'units'
    }

def calc_newsvendor(selling_price: float = 50.0, cost: float = 30.0,
                    salvage: float = 10.0, mean_demand: float = 100.0,
                    std_dev: float = 30.0) -> dict:
    """Newsvendor model: optimal order quantity Q*."""
    Cu = selling_price - cost  # underage cost
    Co = cost - salvage        # overage cost
    critical_ratio = Cu / (Cu + Co)
    # Approximate optimal quantity (using normal distribution)
    # z-score for critical ratio
    def norm_inv_approx(p):
        """Approximate inverse normal CDF."""
        if p <= 0 or p >= 1:
            return 0
        t = math.sqrt(-2 * math.log(min(p, 1 - p)))
        c0 = 2.515517
        c1 = 0.802853
        c2 = 0.010328
        d1 = 1.432788
        d2 = 0.189269
        d3 = 0.001308
        t = t - (c0 + c1 * t + c2 * t * t) / (1 + d1 * t + d2 * t * t + d3 * t * t * t)
        return t if p >= 0.5 else -t
    z = norm_inv_approx(critical_ratio)
    Q_opt = mean_demand + z * std_dev
    expected_profit = (selling_price - cost) * mean_demand - (selling_price - salvage) * std_dev * (
        z * (2 * (0.5 - 0.5 * (1 if z > 0 else 0))) + 0.3989 * math.exp(-z * z / 2)
    )  # simplified
    return {
        'result': f'Optimal order: Q* = {Q_opt:.1f}, Critical ratio = {critical_ratio:.4f}',
        'details': {
            'selling_price': selling_price, 'cost': cost, 'salvage': salvage,
            'Cu': Cu, 'Co': Co, 'critical_ratio': critical_ratio,
            'z_score': round(z, 4), 'Q_opt': round(Q_opt, 4),
            'mean_demand': mean_demand, 'std_dev': std_dev
        },
        'unit': 'units'
    }

# ============================================================
# Game Theory
# ============================================================

def calc_zero_sum_2x2(payoff: list = None) -> dict:
    """2x2 zero-sum game: find minimax/maximin strategies."""
    if payoff is None:
        payoff = [[3, -1], [-2, 4]]
    a, b, c, d = payoff[0][0], payoff[0][1], payoff[1][0], payoff[1][1]
    det = a + d - b - c
    if abs(det) < 1e-10:
        return {
            'result': 'No unique mixed strategy equilibrium',
            'details': {'payoff': payoff, 'det': det},
            'unit': 'dimensionless'
        }
    p = (d - c) / det  # Row player's prob of row 1
    q = (d - b) / det  # Column player's prob of col 1
    v = (a * d - b * c) / det  # Value of the game
    p = max(0, min(1, p))
    q = max(0, min(1, q))
    return {
        'result': f'Game value = {v:.4f}, Row strategy: [{p:.4f}, {1-p:.4f}], Col strategy: [{q:.4f}, {1-q:.4f}]',
        'details': {
            'payoff_matrix': payoff,
            'value': round(v, 6),
            'row_strategy': [round(p, 4), round(1 - p, 4)],
            'col_strategy': [round(q, 4), round(1 - q, 4)],
            'maximin': max(min(payoff[0]), min(payoff[1])),
            'minimax': min(max(payoff[0][0], payoff[1][0]), max(payoff[0][1], payoff[1][1]))
        },
        'unit': 'dimensionless'
    }

def calc_nash_equilibrium_2x2(payoff_row: list = None, payoff_col: list = None) -> dict:
    """Find Nash equilibrium for 2x2 bimatrix game."""
    if payoff_row is None:
        payoff_row = [[3, 0], [5, 1]]
    if payoff_col is None:
        payoff_col = [[3, 5], [0, 1]]
    # Check pure strategy equilibria
    equilibria = []
    for i in range(2):
        for j in range(2):
            # Check if (i,j) is best response
            br_row = payoff_row[i][j] >= payoff_row[1 - i][j]
            br_col = payoff_col[i][j] >= payoff_col[i][1 - j]
            if br_row and br_col:
                equilibria.append({'type': 'pure', 'row': i, 'col': j,
                                   'payoffs': [payoff_row[i][j], payoff_col[i][j]]})
    # Mixed strategy (if no pure found)
    a, b, c, d = payoff_row[0][0], payoff_row[0][1], payoff_row[1][0], payoff_row[1][1]
    e, f, g, h = payoff_col[0][0], payoff_col[0][1], payoff_col[1][0], payoff_col[1][1]
    denom_row = a - c - b + d
    denom_col = e - g - f + h
    if abs(denom_row) > 1e-10 and abs(denom_col) > 1e-10:
        p = (d - c) / denom_row
        q = (h - f) / denom_col
        if 0 <= p <= 1 and 0 <= q <= 1:
            equilibria.append({
                'type': 'mixed',
                'row_strategy': [p, 1 - p],
                'col_strategy': [q, 1 - q],
                'payoffs': [
                    p * q * a + p * (1 - q) * b + (1 - p) * q * c + (1 - p) * (1 - q) * d,
                    p * q * e + p * (1 - q) * f + (1 - p) * q * g + (1 - p) * (1 - q) * h
                ]
            })
    return {
        'result': f'Found {len(equilibria)} Nash equilibria',
        'details': {
            'payoff_row': payoff_row, 'payoff_col': payoff_col,
            'equilibria': equilibria
        },
        'unit': 'dimensionless'
    }

def calc_prisoner_dilemma(defect_row: float = 5.0, defect_col: float = 5.0,
                          both_coop: float = 3.0, both_defect: float = 1.0,
                          sucker: float = 0.0) -> dict:
    """Prisoner's dilemma payoff analysis."""
    payoff = {
        ('C', 'C'): (both_coop, both_coop),
        ('C', 'D'): (sucker, defect_col),
        ('D', 'C'): (defect_row, sucker),
        ('D', 'D'): (both_defect, both_defect)
    }
    nash = ('D', 'D')
    is_dilemma = (defect_row > both_coop and defect_col > both_coop and
                  both_coop > both_defect)
    return {
        'result': f"Nash equilibrium: ({nash[0]}, {nash[1]}), Dilemma: {'Yes' if is_dilemma else 'No'}",
        'details': {
            'payoffs': {str(k): v for k, v in payoff.items()},
            'nash_equilibrium': nash,
            'pareto_optimal': ('C', 'C'),
            'is_prisoner_dilemma': is_dilemma,
            'temptation': defect_row,
            'reward': both_coop,
            'punishment': both_defect,
            'sucker_payoff': sucker
        },
        'unit': 'dimensionless'
    }

def calc_dominated_strategies(payoff_row: list = None) -> dict:
    """Eliminate strictly dominated strategies from payoff matrix."""
    if payoff_row is None:
        payoff_row = [[3, 2, 4], [1, 1, 2], [0, 3, 1]]
    matrix = [row[:] for row in payoff_row]
    num_rows = len(matrix)
    num_cols = len(matrix[0]) if matrix else 0
    dominated = []
    remaining = list(range(num_rows))
    # Check for strictly dominated rows
    for i in range(num_rows):
        for j in range(num_rows):
            if i != j:
                if all(matrix[i][k] < matrix[j][k] for k in range(num_cols)):
                    dominated.append({'row': i, 'dominated_by': j})
    return {
        'result': f'Found {len(dominated)} dominated strategies',
        'details': {
            'original_matrix': payoff_row,
            'dominated_strategies': dominated,
            'surviving_rows': [i for i in range(num_rows) if not any(d['row'] == i for d in dominated)]
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Metaheuristics
# ============================================================

def calc_genetic_algorithm(f_expr: str = 'x**2 + 2*x + 1',
                           x_min: float = -10.0, x_max: float = 10.0,
                           pop_size: int = 20, generations: int = 30,
                           mutation_rate: float = 0.1) -> dict:
    """Genetic algorithm for 1D function minimization."""
    # Initial population
    pop = [random.uniform(x_min, x_max) for _ in range(pop_size)]
    best_history = []
    for gen in range(generations):
        ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
        # Evaluate fitness (negative for minimization)
        fitness = []
        for ind in pop:
            try:
                f_val = eval(f_expr, {**ctx, 'x': ind})
                fitness.append(-f_val if abs(f_val) < 1e10 else -1e10)
            except Exception:
                fitness.append(-1e10)
        # Selection: sort by fitness
        ranked = sorted(zip(fitness, pop), key=lambda t: t[0], reverse=True)
        best_history.append({'gen': gen, 'best_x': ranked[0][1], 'best_f': -ranked[0][0]})
        # Create new population
        new_pop = [ranked[0][1], ranked[1][1]]  # Elitism
        while len(new_pop) < pop_size:
            # Tournament selection
            t1 = random.choice(ranked[:pop_size // 2])
            t2 = random.choice(ranked[:pop_size // 2])
            parent1 = t1[1] if t1[0] > t2[0] else t2[1]
            t1 = random.choice(ranked[:pop_size // 2])
            t2 = random.choice(ranked[:pop_size // 2])
            parent2 = t1[1] if t1[0] > t2[0] else t2[1]
            # Crossover (average)
            child = (parent1 + parent2) / 2
            # Mutation
            if random.random() < mutation_rate:
                child += random.uniform(-1, 1) * (x_max - x_min) * 0.1
            child = max(x_min, min(x_max, child))
            new_pop.append(child)
        pop = new_pop[:pop_size]
    final_f = -max(zip(*[[eval(f_expr, {**{**ctx, 'x': i}}) for i in pop]])[0] if pop else [0])
    best_x = best_history[-1]['best_x']
    return {
        'result': f'GA: Minimum at x = {best_x:.6f}, f(x) = {final_f:.6f}',
        'details': {
            'function': f_expr, 'range': [x_min, x_max],
            'pop_size': pop_size, 'generations': generations,
            'mutation_rate': mutation_rate,
            'best_x': best_x, 'best_f': final_f,
            'history': best_history[-5:]
        },
        'unit': 'dimensionless'
    }

def calc_simulated_annealing(f_expr: str = 'x**2 + 2*x + 1',
                             x_min: float = -10.0, x_max: float = 10.0,
                             T0: float = 100.0, cooling_rate: float = 0.95,
                             max_iter: int = 200) -> dict:
    """Simulated annealing for 1D function minimization."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    x = random.uniform(x_min, x_max)
    f_curr = eval(f_expr, {**ctx, 'x': x})
    best_x, best_f = x, f_curr
    T = T0
    history = [{'iter': 0, 'T': T, 'x': x, 'f': f_curr}]
    for i in range(max_iter):
        x_new = x + random.uniform(-1, 1) * (x_max - x_min) * 0.1 * (T / T0)
        x_new = max(x_min, min(x_max, x_new))
        f_new = eval(f_expr, {**ctx, 'x': x_new})
        delta = f_new - f_curr
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            x, f_curr = x_new, f_new
            if f_curr < best_f:
                best_x, best_f = x, f_curr
        T *= cooling_rate
        if i % 20 == 0:
            history.append({'iter': i, 'T': T, 'x': x, 'f': f_curr, 'best_f': best_f})
    return {
        'result': f'SA: Minimum at x = {best_x:.6f}, f(x) = {best_f:.6f}',
        'details': {
            'function': f_expr, 'range': [x_min, x_max],
            'T0': T0, 'cooling_rate': cooling_rate, 'iterations': max_iter,
            'best_x': best_x, 'best_f': best_f, 'history': history
        },
        'unit': 'dimensionless'
    }

def calc_particle_swarm(f_expr: str = 'x**2 + y**2',
                        x_min: float = -10.0, x_max: float = 10.0,
                        num_particles: int = 30, max_iter: int = 50) -> dict:
    """Particle Swarm Optimization (2D)."""
    ctx = {'math': math, 'sin': math.sin, 'cos': math.cos, 'exp': math.exp, 'log': math.log}
    # Initialize particles
    pos = [[random.uniform(x_min, x_max), random.uniform(x_min, x_max)] for _ in range(num_particles)]
    vel = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(num_particles)]
    pbest = [p[:] for p in pos]
    pbest_f = [eval(f_expr, {**ctx, 'x': p[0], 'y': p[1]}) for p in pos]
    gbest = min(zip(pbest_f, pbest), key=lambda t: t[0])
    gbest_pos, gbest_f = gbest[1], gbest[0]
    w, c1, c2 = 0.5, 1.5, 1.5
    for iteration in range(max_iter):
        for i in range(num_particles):
            for d in range(2):
                r1, r2 = random.random(), random.random()
                vel[i][d] = (w * vel[i][d] +
                             c1 * r1 * (pbest[i][d] - pos[i][d]) +
                             c2 * r2 * (gbest_pos[d] - pos[i][d]))
                pos[i][d] += vel[i][d]
                pos[i][d] = max(x_min, min(x_max, pos[i][d]))
            f_val = eval(f_expr, {**ctx, 'x': pos[i][0], 'y': pos[i][1]})
            if f_val < pbest_f[i]:
                pbest[i] = pos[i][:]
                pbest_f[i] = f_val
                if f_val < gbest_f:
                    gbest_f = f_val
                    gbest_pos = pos[i][:]
    return {
        'result': f'PSO: Minimum at ({gbest_pos[0]:.6f}, {gbest_pos[1]:.6f}), f = {gbest_f:.6f}',
        'details': {
            'function': f_expr, 'range': [x_min, x_max],
            'num_particles': num_particles, 'max_iter': max_iter,
            'best_x': gbest_pos[0], 'best_y': gbest_pos[1],
            'best_f': gbest_f
        },
        'unit': 'dimensionless'
    }

def calc_ant_colony_tsp(cities: list = None, num_ants: int = 20,
                        max_iter: int = 50, alpha: float = 1.0,
                        beta: float = 2.0, evap_rate: float = 0.5) -> dict:
    """Ant Colony Optimization for basic TSP."""
    if cities is None:
        cities = [(0, 0), (1, 2), (3, 1), (5, 3), (2, 4), (4, 0)]
    n = len(cities)
    # Distance matrix
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = cities[i][0] - cities[j][0]
            dy = cities[i][1] - cities[j][1]
            dist[i][j] = math.sqrt(dx * dx + dy * dy)
    # Pheromone matrix
    tau0 = 1.0 / (n * sum(min(row) for row in dist))
    tau = [[tau0] * n for _ in range(n)]
    best_tour, best_len = None, float('inf')
    for iteration in range(max_iter):
        tours = []
        tour_lens = []
        for ant in range(num_ants):
            visited = [False] * n
            start = random.randrange(n)
            tour = [start]
            visited[start] = True
            for step in range(n - 1):
                curr = tour[-1]
                probs = []
                for j in range(n):
                    if not visited[j]:
                        p = (tau[curr][j] ** alpha) * ((1.0 / max(dist[curr][j], 1e-10)) ** beta)
                        probs.append((j, p))
                total = sum(p for _, p in probs)
                if total > 0:
                    r = random.random() * total
                    cum = 0
                    for j, p in probs:
                        cum += p
                        if cum >= r:
                            tour.append(j)
                            visited[j] = True
                            break
                else:
                    for j in range(n):
                        if not visited[j]:
                            tour.append(j)
                            visited[j] = True
                            break
            # Close tour
            tour_len = sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))
            tours.append(tour)
            tour_lens.append(tour_len)
            if tour_len < best_len:
                best_len = tour_len
                best_tour = tour[:]
        # Evaporate pheromones
        for i in range(n):
            for j in range(n):
                tau[i][j] *= (1 - evap_rate)
        # Deposit pheromones
        for tour, tlen in zip(tours, tour_lens):
            delta = 1.0 / max(tlen, 1e-10)
            for i in range(n):
                u, v = tour[i], tour[(i + 1) % n]
                tau[u][v] += delta
                tau[v][u] += delta
    best_coords = [cities[i] for i in best_tour] if best_tour else []
    return {
        'result': f'ACO TSP: Best tour length = {best_len:.4f}',
        'details': {
            'cities': cities, 'n_cities': n,
            'num_ants': num_ants, 'iterations': max_iter,
            'best_tour': best_tour,
            'best_length': round(best_len, 4),
            'best_coords': best_coords
        },
        'unit': 'distance'
    }


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'simplex_2var': {'func': calc_simplex_2var, 'params': ['c1', 'c2', 'a11', 'a12', 'b1', 'a21', 'a22', 'b2', 'maximize'], 'desc': '2-variable LP graphical solution'},
    'standard_form': {'func': calc_standard_form, 'params': ['c', 'A', 'b'], 'desc': 'Convert LP to standard form'},
    'basic_feasible_solution': {'func': calc_basic_feasible_solution, 'params': ['A', 'b', 'basis'], 'desc': 'Basic feasible solution from basis'},
    'shadow_prices': {'func': calc_shadow_prices, 'params': ['c', 'A', 'b', 'basis'], 'desc': 'Compute shadow prices for LP'},
    'gradient_descent_1d': {'func': calc_gradient_descent_1d, 'params': ['f_expr', 'x0', 'lr', 'max_iter'], 'desc': 'Gradient descent 1D minimization'},
    'gradient_descent_2d': {'func': calc_gradient_descent_2d, 'params': ['x0', 'y0', 'lr', 'max_iter'], 'desc': 'Gradient descent 2D (Rosenbrock)'},
    'newton_optimization': {'func': calc_newton_optimization, 'params': ['f_expr', 'x0', 'max_iter'], 'desc': "Newton's method for optimization"},
    'golden_section': {'func': calc_golden_section, 'params': ['f_expr', 'a', 'b', 'tol', 'max_iter'], 'desc': 'Golden-section search 1D'},
    'lagrange_multiplier': {'func': calc_lagrange_multiplier, 'params': ['f_expr', 'g_expr', 'guess_xy'], 'desc': 'Lagrange multiplier method'},
    'kkt_conditions': {'func': calc_kkt_conditions, 'params': ['x', 'lagrange', 'f_expr', 'g_expr'], 'desc': 'Check KKT optimality conditions'},
    'branch_and_bound': {'func': calc_branch_and_bound, 'params': ['c', 'A', 'b'], 'desc': 'Branch and bound for 0-1 IP'},
    'knapsack_01': {'func': calc_knapsack_01, 'params': ['values', 'weights', 'capacity'], 'desc': '0/1 Knapsack dynamic programming'},
    'assignment_problem': {'func': calc_assignment_problem, 'params': ['cost_matrix'], 'desc': 'Assignment problem (Hungarian algorithm)'},
    'shortest_path_dag': {'func': calc_shortest_path_dag, 'params': ['edges', 'num_nodes', 'source'], 'desc': 'Shortest path in DAG'},
    'matrix_chain': {'func': calc_matrix_chain, 'params': ['dims'], 'desc': 'Matrix chain multiplication DP'},
    'lcs': {'func': calc_lcs, 'params': ['s1', 's2'], 'desc': 'Longest Common Subsequence'},
    'edit_distance': {'func': calc_edit_distance, 'params': ['s1', 's2'], 'desc': 'Levenshtein edit distance'},
    'mm1_queue': {'func': calc_mm1_queue, 'params': ['arrival_rate', 'service_rate'], 'desc': 'M/M/1 queue analysis'},
    'mmc_queue': {'func': calc_mmc_queue, 'params': ['arrival_rate', 'service_rate', 'num_servers'], 'desc': 'M/M/c queue analysis'},
    'mg1_queue': {'func': calc_mg1_queue, 'params': ['arrival_rate', 'mean_service', 'var_service'], 'desc': 'M/G/1 queue (Pollaczek-Khinchine)'},
    'littles_law': {'func': calc_littles_law, 'params': ['L', 'lam'], 'desc': "Little's Law: L = lambda*W"},
    'eoq': {'func': calc_eoq, 'params': ['demand_rate', 'ordering_cost', 'holding_cost'], 'desc': 'Economic Order Quantity'},
    'reorder_point': {'func': calc_reorder_point, 'params': ['daily_demand', 'lead_time_days', 'safety_stock'], 'desc': 'Reorder point calculation'},
    'safety_stock': {'func': calc_safety_stock, 'params': ['z_score', 'std_dev_lead_time', 'avg_lead_time'], 'desc': 'Safety stock calculation'},
    'newsvendor': {'func': calc_newsvendor, 'params': ['selling_price', 'cost', 'salvage', 'mean_demand', 'std_dev'], 'desc': 'Newsvendor model'},
    'zero_sum_2x2': {'func': calc_zero_sum_2x2, 'params': ['payoff'], 'desc': '2x2 zero-sum game solution'},
    'nash_equilibrium_2x2': {'func': calc_nash_equilibrium_2x2, 'params': ['payoff_row', 'payoff_col'], 'desc': 'Nash equilibrium for 2x2 bimatrix'},
    'prisoner_dilemma': {'func': calc_prisoner_dilemma, 'params': ['defect_row', 'defect_col', 'both_coop', 'both_defect', 'sucker'], 'desc': "Prisoner's dilemma analysis"},
    'dominated_strategies': {'func': calc_dominated_strategies, 'params': ['payoff_row'], 'desc': 'Eliminate dominated strategies'},
    'genetic_algorithm': {'func': calc_genetic_algorithm, 'params': ['f_expr', 'x_min', 'x_max', 'pop_size', 'generations', 'mutation_rate'], 'desc': 'Genetic algorithm 1D minimization'},
    'simulated_annealing': {'func': calc_simulated_annealing, 'params': ['f_expr', 'x_min', 'x_max', 'T0', 'cooling_rate', 'max_iter'], 'desc': 'Simulated annealing optimization'},
    'particle_swarm': {'func': calc_particle_swarm, 'params': ['f_expr', 'x_min', 'x_max', 'num_particles', 'max_iter'], 'desc': 'Particle Swarm Optimization 2D'},
    'ant_colony_tsp': {'func': calc_ant_colony_tsp, 'params': ['cities', 'num_ants', 'max_iter', 'alpha', 'beta', 'evap_rate'], 'desc': 'Ant Colony Optimization for TSP'},
}
