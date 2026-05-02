"""
Nonlinear Physics, Chaos & Fractals - Computation Module
"""
import math
import numpy as np

COMMANDS = {}

def calc_logistic_map(r: float = 3.5, x0: float = 0.5, n_iter: int = 50) -> dict:
    """Logistic map: x_{n+1} = r * x_n * (1 - x_n)."""
    x = x0
    trajectory = [x]
    for i in range(n_iter):
        x = r * x * (1.0 - x)
        trajectory.append(x)
    final = trajectory[-1]
    return {
        'result': f'Logistic map r={r}: final x = {final:.6f} after {n_iter} iterations',
        'details': {'r': r, 'x0': x0, 'n_iter': n_iter, 'final_x': final, 'trajectory': trajectory},
        'unit': 'dimensionless'
    }

def calc_bifurcation_diagram(r_min: float = 2.5, r_max: float = 4.0, n_r: int = 200, n_transient: int = 200, n_sample: int = 100) -> dict:
    """Generate bifurcation diagram data for logistic map."""
    r_values = np.linspace(r_min, r_max, n_r)
    bifurcation_data = []
    for r in r_values:
        x = 0.5
        for _ in range(n_transient):
            x = r * x * (1.0 - x)
        for _ in range(n_sample):
            x = r * x * (1.0 - x)
            bifurcation_data.append({'r': float(r), 'x': float(x)})
    period_doubling = {
        'period_1_to_2': 3.0,
        'period_2_to_4': 3.44949,
        'period_4_to_8': 3.54409,
        'period_8_to_16': 3.56441,
        'onset_of_chaos': 3.569946
    }
    return {
        'result': f'Bifurcation data generated: {len(bifurcation_data)} points, r in [{r_min}, {r_max}]',
        'details': {'r_min': r_min, 'r_max': r_max, 'n_r': n_r, 'n_points': len(bifurcation_data), 'period_doubling_r': period_doubling, 'data_sample': bifurcation_data[:10]},
        'unit': 'dimensionless'
    }

def calc_feigenbaum_constants() -> dict:
    """Feigenbaum constants: delta ~ 4.669, alpha ~ 2.503."""
    delta = 4.669201609102990
    alpha = 2.502907875095892
    return {
        'result': f'Feigenbaum: delta = {delta:.6f}, alpha = {alpha:.6f}',
        'details': {'delta': delta, 'alpha': alpha, 'description': 'delta: ratio of period-doubling intervals, alpha: scaling of bifurcation widths'},
        'unit': 'dimensionless'
    }

def calc_lyapunov_exponent(r: float = 3.9, x0: float = 0.5, n_iter: int = 1000) -> dict:
    """Lyapunov exponent for logistic map: lambda = lim(1/n)*sum(log|r*(1-2*x_i)|)."""
    x = x0
    lyap_sum = 0.0
    for i in range(n_iter):
        derivative = abs(r * (1.0 - 2.0 * x))
        if derivative < 1e-15:
            derivative = 1e-15
        lyap_sum += np.log(derivative)
        x = r * x * (1.0 - x)
    lyap = lyap_sum / n_iter
    behavior = 'chaotic' if lyap > 0 else 'periodic' if lyap < 0 else 'bifurcation'
    return {
        'result': f'Lyapunov exponent lambda = {lyap:.6f} ({behavior})',
        'details': {'r': r, 'x0': x0, 'n_iter': n_iter, 'lyapunov_exponent': lyap, 'behavior': behavior},
        'unit': 'dimensionless'
    }

def calc_lyapunov_spectrum(r_value: float = 3.9, n_iter: int = 500, n_transient: int = 100) -> dict:
    """Lyapunov exponent over transient-removed trajectory."""
    x = 0.5
    for _ in range(n_transient):
        x = r_value * x * (1.0 - x)
    lyap_sum = 0.0
    for _ in range(n_iter):
        derivative = abs(r_value * (1.0 - 2.0 * x))
        if derivative < 1e-15:
            derivative = 1e-15
        lyap_sum += np.log(derivative)
        x = r_value * x * (1.0 - x)
    lyap = lyap_sum / n_iter
    return {
        'result': f'lambda = {lyap:.6f} (after {n_transient} transient steps)',
        'details': {'r': r_value, 'lyapunov': lyap, 'n_transient': n_transient, 'n_iter': n_iter},
        'unit': 'dimensionless'
    }

def calc_lorenz_system(sigma: float = 10.0, rho: float = 28.0, beta: float = 8.0/3.0, x0: float = 1.0, y0: float = 1.0, z0: float = 1.0, dt: float = 0.01, n_steps: int = 500) -> dict:
    """Lorenz attractor simulation via RK4 method."""
    def lorenz_derivs(state, s, r, b):
        x, y, z = state
        dx = s * (y - x)
        dy = x * (r - z) - y
        dz = x * y - b * z
        return np.array([dx, dy, dz])

    state = np.array([x0, y0, z0])
    trajectory = [state.copy()]
    t_vals = [0.0]
    for i in range(n_steps):
        k1 = lorenz_derivs(state, sigma, rho, beta)
        k2 = lorenz_derivs(state + 0.5 * dt * k1, sigma, rho, beta)
        k3 = lorenz_derivs(state + 0.5 * dt * k2, sigma, rho, beta)
        k4 = lorenz_derivs(state + dt * k3, sigma, rho, beta)
        state = state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        trajectory.append(state.copy())
        t_vals.append((i + 1) * dt)
    final_state = trajectory[-1]
    return {
        'result': f'Lorenz final state: x={final_state[0]:.4f}, y={final_state[1]:.4f}, z={final_state[2]:.4f}',
        'details': {'sigma': sigma, 'rho': rho, 'beta': beta, 'dt': dt, 'n_steps': n_steps, 'final_state': final_state.tolist(), 't_end': t_vals[-1], 'trajectory_sample': [t.tolist() for t in trajectory[:5]]},
        'unit': 'dimensionless'
    }

def calc_lorenz_fixed_points(sigma: float = 10.0, rho: float = 28.0, beta: float = 8.0/3.0) -> dict:
    """Fixed points of Lorenz system: C0=(0,0,0), C+,-=(+/-, +/-sqrt(beta*(rho-1)), rho-1)."""
    fp1 = np.array([0.0, 0.0, 0.0])
    if rho > 1.0:
        val = np.sqrt(beta * (rho - 1.0))
        fp2 = np.array([val, val, rho - 1.0])
        fp3 = np.array([-val, -val, rho - 1.0])
    else:
        val = 0.0
        fp2 = fp3 = None
    return {
        'result': f'Fixed points: C0=(0,0,0), C+/- = ({val:.4f}, {val:.4f}, {rho-1:.4f})' if rho > 1 else 'Only trivial fixed point C0=(0,0,0)',
        'details': {'sigma': sigma, 'rho': rho, 'beta': beta, 'C0': [0,0,0], 'Cplus': fp2.tolist() if fp2 is not None else None, 'Cminus': fp3.tolist() if fp3 is not None else None},
        'unit': 'dimensionless'
    }

def calc_mandelbrot(width: int = 80, height: int = 60, x_min: float = -2.0, x_max: float = 1.0, y_min: float = -1.5, y_max: float = 1.5, max_iter: int = 100) -> dict:
    """Mandelbrot set computation."""
    xs = np.linspace(x_min, x_max, width)
    ys = np.linspace(y_min, y_max, height)
    mandel = np.zeros((height, width))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            c = complex(x, y)
            z = 0.0 + 0.0j
            for k in range(max_iter):
                if abs(z) > 2.0:
                    mandel[i, j] = k
                    break
                z = z * z + c
            else:
                mandel[i, j] = max_iter
    in_set = np.sum(mandel >= max_iter)
    return {
        'result': f'Mandelbrot set: {in_set}/{width*height} points in set',
        'details': {'width': width, 'height': height, 'x_range': [x_min, x_max], 'y_range': [y_min, y_max], 'max_iter': max_iter, 'points_in_set': int(in_set), 'fractal_pct': float(in_set/(width*height)*100)},
        'unit': 'dimensionless'
    }

def calc_julia_set(c_real: float = -0.7, c_imag: float = 0.27, width: int = 80, height: int = 60, max_iter: int = 100) -> dict:
    """Julia set for given complex parameter c."""
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    xs = np.linspace(x_min, x_max, width)
    ys = np.linspace(y_min, y_max, height)
    c = complex(c_real, c_imag)
    julia = np.zeros((height, width))
    for i, y in enumerate(ys):
        for j, x in enumerate(xs):
            z = complex(x, y)
            for k in range(max_iter):
                if abs(z) > 2.0:
                    julia[i, j] = k
                    break
                z = z * z + c
            else:
                julia[i, j] = max_iter
    in_set = np.sum(julia >= max_iter)
    return {
        'result': f'Julia set c={c}: {in_set}/{width*height} points bounded',
        'details': {'c': str(c), 'width': width, 'height': height, 'max_iter': max_iter, 'points_bounded': int(in_set)},
        'unit': 'dimensionless'
    }

def calc_box_counting_dimension(points: list = None, box_sizes: list = None) -> dict:
    """Box-counting fractal dimension: D = -d(log(N))/d(log(epsilon))."""
    if points is None:
        np.random.seed(42)
        points = np.random.rand(500, 2).tolist()
    pts = np.array(points)
    if box_sizes is None:
        box_sizes = [0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625]
    counts = []
    for eps in box_sizes:
        if eps <= 0:
            continue
        grid = {}
        for pt in pts:
            gx = int(pt[0] / eps)
            gy = int(pt[1] / eps)
            grid[(gx, gy)] = True
        counts.append(len(grid))
    if len(counts) > 1:
        log_eps = np.log(1.0 / np.array(box_sizes[:len(counts)]))
        log_counts = np.log(np.array(counts))
        D, intercept = np.polyfit(log_eps, log_counts, 1)
    else:
        D = 0.0
    return {
        'result': f'Box-counting dimension D = {D:.4f}',
        'details': {'n_points': len(points), 'box_sizes': box_sizes, 'counts': counts, 'fractal_dimension': D},
        'unit': 'dimensionless'
    }

def calc_sierpinski_triangle(depth: int = 5, size: float = 1.0) -> dict:
    """Generate Sierpinski triangle via chaos game."""
    vertices = np.array([[0.0, 0.0], [size, 0.0], [size/2.0, size * np.sqrt(3.0)/2.0]])
    current = np.array([size/4.0, size/4.0])
    n_points = 2000
    points = []
    for _ in range(n_points):
        v = vertices[np.random.randint(0, 3)]
        current = (current + v) / 2.0
        points.append(current.copy())
    pts_arr = np.array(points)
    return {
        'result': f'Sierpinski triangle: {n_points} points generated, depth {depth}',
        'details': {'depth': depth, 'size': size, 'n_points': n_points, 'vertices': vertices.tolist(), 'point_sample': pts_arr[:5].tolist()},
        'unit': 'dimensionless'
    }

def calc_koch_curve(order: int = 3, length: float = 1.0) -> dict:
    """Koch snowflake perimeter: P_n = P_0 * (4/3)^n."""
    P_0 = 3.0 * length
    P_n = P_0 * (4.0/3.0)**order
    fractal_dimension = np.log(4.0) / np.log(3.0)
    area = (2.0 * np.sqrt(3.0) / 5.0) * length**2
    return {
        'result': f'Koch snowflake order {order}: perimeter = {P_n:.6f}, D = {fractal_dimension:.4f}',
        'details': {'order': order, 'initial_length': length, 'perimeter': P_n, 'area_limit': area, 'fractal_dimension': fractal_dimension},
        'unit': 'dimensionless'
    }

def calc_duffing_oscillator(alpha: float = -1.0, beta: float = 1.0, gamma: float = 0.3, delta: float = 0.2, omega: float = 1.0, x0: float = 1.0, v0: float = 0.0, dt: float = 0.05, n_steps: int = 400) -> dict:
    """Duffing equation: x'' + gamma*x' + alpha*x + beta*x^3 = delta*cos(omega*t) via RK4."""
    def duffing_derivs(state, t, a, b, g, d, w):
        x, v = state
        dx = v
        dv = d * np.cos(w * t) - g * v - a * x - b * x**3
        return np.array([dx, dv])

    state = np.array([x0, v0])
    for i in range(n_steps):
        t_i = i * dt
        k1 = duffing_derivs(state, t_i, alpha, beta, gamma, delta, omega)
        k2 = duffing_derivs(state + 0.5 * dt * k1, t_i + 0.5 * dt, alpha, beta, gamma, delta, omega)
        k3 = duffing_derivs(state + 0.5 * dt * k2, t_i + 0.5 * dt, alpha, beta, gamma, delta, omega)
        k4 = duffing_derivs(state + dt * k3, t_i + dt, alpha, beta, gamma, delta, omega)
        state = state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    x_final, v_final = state
    return {
        'result': f'Duffing final: x={x_final:.4f}, v={v_final:.4f}',
        'details': {'alpha': alpha, 'beta': beta, 'gamma': gamma, 'delta': delta, 'omega': omega, 'n_steps': n_steps, 'final_x': float(x_final), 'final_v': float(v_final)},
        'unit': 'dimensionless'
    }

def calc_van_der_pol(mu: float = 2.0, x0: float = 1.0, v0: float = 0.0, dt: float = 0.05, n_steps: int = 500) -> dict:
    """Van der Pol oscillator: x'' - mu*(1-x^2)*x' + x = 0 via RK4."""
    def vdp_derivs(state, m):
        x, v = state
        dx = v
        dv = m * (1.0 - x**2) * v - x
        return np.array([dx, dv])

    state = np.array([x0, v0])
    for i in range(n_steps):
        k1 = vdp_derivs(state, mu)
        k2 = vdp_derivs(state + 0.5 * dt * k1, mu)
        k3 = vdp_derivs(state + 0.5 * dt * k2, mu)
        k4 = vdp_derivs(state + dt * k3, mu)
        state = state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return {
        'result': f'Van der Pol final: x={state[0]:.4f}, v={state[1]:.4f}',
        'details': {'mu': mu, 'x0': x0, 'v0': v0, 'n_steps': n_steps, 'final_x': float(state[0]), 'final_v': float(state[1])},
        'unit': 'dimensionless'
    }

def calc_nonlinear_pendulum(theta0: float = np.pi/3, omega0: float = 0.0, L: float = 1.0, g: float = 9.81, dt: float = 0.01, n_steps: int = 300) -> dict:
    """Nonlinear pendulum: theta'' + (g/L)*sin(theta) = 0 via RK4."""
    def pendulum_derivs(state, length, grav):
        theta, omega = state
        dtheta = omega
        domega = -(grav / length) * np.sin(theta)
        return np.array([dtheta, domega])

    state = np.array([theta0, omega0])
    for i in range(n_steps):
        k1 = pendulum_derivs(state, L, g)
        k2 = pendulum_derivs(state + 0.5 * dt * k1, L, g)
        k3 = pendulum_derivs(state + 0.5 * dt * k2, L, g)
        k4 = pendulum_derivs(state + dt * k3, L, g)
        state = state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    T_linear = 2.0 * np.pi * np.sqrt(L / g)
    T_nonlinear = T_linear * (1.0 + theta0**2 / 16.0)
    return {
        'result': f'Pendulum: T_linear={T_linear:.4f}s, T_nonlinear~{T_nonlinear:.4f}s',
        'details': {'theta0_rad': theta0, 'omega0': omega0, 'L_m': L, 'g': g, 'linear_period_s': T_linear, 'nonlinear_period_s': T_nonlinear, 'final_theta': float(state[0]), 'final_omega': float(state[1])},
        'unit': 's'
    }

def calc_sandpile_model(grid_size: int = 21, n_grains: int = 200, critical_slope: int = 4) -> dict:
    """Bak-Tang-Wiesenfeld sandpile model (self-organized criticality)."""
    grid = np.zeros((grid_size, grid_size), dtype=int)
    center = grid_size // 2
    avalanche_sizes = []
    for grain in range(n_grains):
        grid[center, center] += 1
        avalanche_size = 0
        while np.any(grid >= critical_slope):
            unstable = np.argwhere(grid >= critical_slope)
            for ui, uj in unstable:
                if grid[ui, uj] >= critical_slope:
                    grid[ui, uj] -= 4
                    avalanche_size += 1
                    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        ni, nj = ui + di, uj + dj
                        if 0 <= ni < grid_size and 0 <= nj < grid_size:
                            grid[ni, nj] += 1
        if avalanche_size > 0:
            avalanche_sizes.append(avalanche_size)
    total_mass = np.sum(grid)
    avg_avalanche = np.mean(avalanche_sizes) if avalanche_sizes else 0
    return {
        'result': f'Sandpile: {len(avalanche_sizes)} avalanches, avg size={avg_avalanche:.2f}, mass={total_mass}',
        'details': {'grid_size': grid_size, 'n_grains': n_grains, 'critical_slope': critical_slope, 'n_avalanches': len(avalanche_sizes), 'avg_avalanche_size': avg_avalanche, 'total_mass': int(total_mass), 'avalanche_sizes': avalanche_sizes[:20]},
        'unit': 'dimensionless'
    }

def calc_ising_model_2d(L: int = 10, T: float = 2.0, n_steps: int = 500) -> dict:
    """2D Ising model Monte Carlo simulation."""
    np.random.seed(42)
    spins = np.random.choice([-1, 1], size=(L, L))
    beta = 1.0 / T if T > 0 else float('inf')
    energy_history = []
    mag_history = []
    for step in range(n_steps):
        for _ in range(L * L):
            i, j = np.random.randint(0, L, 2)
            nb_sum = spins[(i+1)%L, j] + spins[(i-1)%L, j] + spins[i, (j+1)%L] + spins[i, (j-1)%L]
            dE = 2.0 * spins[i, j] * nb_sum
            if dE <= 0 or np.random.random() < np.exp(-beta * dE):
                spins[i, j] *= -1
        if step % 10 == 0:
            E_total = -np.sum(spins * (np.roll(spins, 1, 0) + np.roll(spins, 1, 1)))
            M_total = np.sum(spins)
            energy_history.append(float(E_total))
            mag_history.append(float(M_total))
    avg_mag = np.mean(np.abs(mag_history[-10:])) if mag_history else 0
    T_c = 2.269
    phase = 'ferromagnetic' if T < T_c else 'paramagnetic'
    return {
        'result': f'Ising T={T}: <|M|>={avg_mag:.4f}, T_c={T_c} ({phase})',
        'details': {'L': L, 'T': T, 'n_steps': n_steps, 'avg_abs_magnetization': avg_mag, 'T_c': T_c, 'phase': phase, 'final_energy': energy_history[-1] if energy_history else 0},
        'unit': 'dimensionless'
    }

def calc_critical_exponents() -> dict:
    """Critical exponents for various universality classes."""
    exponents = {
        'Ising_2D': {'beta': 0.125, 'gamma': 1.75, 'nu': 1.0, 'alpha': 0.0, 'delta': 15.0},
        'Ising_3D': {'beta': 0.326, 'gamma': 1.239, 'nu': 0.630, 'alpha': 0.110, 'delta': 4.79},
        'MeanField': {'beta': 0.5, 'gamma': 1.0, 'nu': 0.5, 'alpha': 0.0, 'delta': 3.0},
        'Heisenberg': {'beta': 0.365, 'gamma': 1.386, 'nu': 0.705, 'alpha': -0.115, 'delta': 4.80},
        'XY_model': {'beta': 0.345, 'gamma': 1.316, 'nu': 0.669, 'alpha': -0.007, 'delta': 4.81},
    }
    return {
        'result': f'Critical exponents: Ising 2D beta={exponents["Ising_2D"]["beta"]}, gamma={exponents["Ising_2D"]["gamma"]}',
        'details': exponents,
        'unit': 'dimensionless'
    }

def calc_henon_map(a: float = 1.4, b: float = 0.3, x0: float = 0.0, y0: float = 0.0, n_iter: int = 500) -> dict:
    """Henon map: x_{n+1}=1-a*x_n^2+y_n, y_{n+1}=b*x_n."""
    x, y = x0, y0
    for _ in range(n_iter):
        x_new = 1.0 - a * x**2 + y
        y = b * x
        x = x_new
    return {
        'result': f'Henon map: (x,y)=({x:.6f}, {y:.6f}) after {n_iter} iterations',
        'details': {'a': a, 'b': b, 'n_iter': n_iter, 'final_x': x, 'final_y': y},
        'unit': 'dimensionless'
    }

def calc_rossler_system(a: float = 0.2, b: float = 0.2, c: float = 5.7, x0: float = 1.0, y0: float = 1.0, z0: float = 1.0, dt: float = 0.05, n_steps: int = 400) -> dict:
    """Rossler attractor: dx/dt=-y-z, dy/dt=x+ay, dz/dt=b+z(x-c)."""
    def rossler_derivs(state, aa, bb, cc):
        x, y, z = state
        dx = -y - z
        dy = x + aa * y
        dz = bb + z * (x - cc)
        return np.array([dx, dy, dz])

    state = np.array([x0, y0, z0])
    for i in range(n_steps):
        k1 = rossler_derivs(state, a, b, c)
        k2 = rossler_derivs(state + 0.5 * dt * k1, a, b, c)
        k3 = rossler_derivs(state + 0.5 * dt * k2, a, b, c)
        k4 = rossler_derivs(state + dt * k3, a, b, c)
        state = state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
    return {
        'result': f'Rossler final: x={state[0]:.4f}, y={state[1]:.4f}, z={state[2]:.4f}',
        'details': {'a': a, 'b': b, 'c': c, 'n_steps': n_steps, 'final_state': state.tolist()},
        'unit': 'dimensionless'
    }

def calc_tent_map(r: float = 1.8, x0: float = 0.3, n_iter: int = 50) -> dict:
    """Tent map: x_{n+1} = r*x_n for x_n<0.5, r*(1-x_n) for x_n>=0.5."""
    x = x0
    for _ in range(n_iter):
        if x < 0.5:
            x = r * x
        else:
            x = r * (1.0 - x)
    return {
        'result': f'Tent map r={r}: final x = {x:.6f}',
        'details': {'r': r, 'x0': x0, 'n_iter': n_iter, 'final_x': x},
        'unit': 'dimensionless'
    }

def calc_standard_map(K: float = 1.0, p0: float = 0.0, theta0: float = 0.5, n_iter: int = 100) -> dict:
    """Chirikov standard map: p_{n+1}=p_n+K*sin(theta_n), theta_{n+1}=theta_n+p_{n+1}."""
    p = p0
    theta = theta0
    for _ in range(n_iter):
        p = p + K * np.sin(theta)
        theta = (theta + p) % (2.0 * np.pi)
    return {
        'result': f'Standard map K={K}: (theta,p)=({theta:.4f}, {p:.4f})',
        'details': {'K': K, 'p0': p0, 'theta0': theta0, 'n_iter': n_iter, 'final_theta': theta, 'final_p': p},
        'unit': 'dimensionless'
    }

def calc_poincare_section(trajectory_data: list = None, plane_dim: int = 0, plane_val: float = 0.0) -> dict:
    """Compute Poincare section from trajectory data crossing a plane."""
    if trajectory_data is None:
        t = np.linspace(0, 10, 200)
        trajectory_data = np.column_stack([np.sin(t), np.cos(t), t]).tolist()
    traj = np.array(trajectory_data)
    section_points = []
    for i in range(1, len(traj)):
        if (traj[i-1, plane_dim] - plane_val) * (traj[i, plane_dim] - plane_val) < 0:
            frac = (plane_val - traj[i-1, plane_dim]) / (traj[i, plane_dim] - traj[i-1, plane_dim] + 1e-15)
            pt = traj[i-1] + frac * (traj[i] - traj[i-1])
            section_points.append(pt.tolist())
    return {
        'result': f'Poincare section: {len(section_points)} crossing points found',
        'details': {'plane_dim': plane_dim, 'plane_val': plane_val, 'n_crossings': len(section_points), 'points': section_points[:10]},
        'unit': 'dimensionless'
    }

def calc_correlation_dimension(points: list = None, epsilons: list = None) -> dict:
    """Correlation dimension: C(eps) = (2/(N(N-1))) * sum(H(eps - |x_i - x_j|))."""
    if points is None:
        np.random.seed(123)
        points = np.random.rand(200, 2).tolist()
    pts = np.array(points)
    N = len(pts)
    if epsilons is None:
        epsilons = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
    log_eps = []
    log_C = []
    for eps in epsilons:
        count = 0
        for i in range(N):
            dists = np.linalg.norm(pts[i+1:] - pts[i], axis=1)
            count += 2 * np.sum(dists < eps)
        C = count / (N * (N - 1)) if N > 1 else 0
        if C > 0:
            log_eps.append(np.log(eps))
            log_C.append(np.log(C))
    if len(log_eps) > 1:
        D, intercept = np.polyfit(log_eps, log_C, 1)
    else:
        D = 0.0
    return {
        'result': f'Correlation dimension D = {D:.4f}',
        'details': {'N': N, 'epsilons': epsilons, 'log_C': log_C, 'correlation_dimension': D},
        'unit': 'dimensionless'
    }

def calc_recurrence_plot(time_series: list = None, threshold: float = 0.1) -> dict:
    """Generate recurrence plot data from time series."""
    if time_series is None:
        time_series = np.sin(np.linspace(0, 20, 100)).tolist()
    ts = np.array(time_series)
    N = len(ts)
    recurrence = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            if abs(ts[i] - ts[j]) < threshold:
                recurrence[i, j] = 1
    recurrence_rate = np.sum(recurrence) / (N * N)
    return {
        'result': f'Recurrence rate = {recurrence_rate:.4f} at threshold {threshold}',
        'details': {'N': N, 'threshold': threshold, 'recurrence_rate': recurrence_rate, 'total_recurrences': int(np.sum(recurrence))},
        'unit': 'dimensionless'
    }

COMMANDS = {
    'logistic_map': {'func': calc_logistic_map, 'params': ['r', 'x0', 'n_iter'], 'desc': 'Logistic map iteration x -> r*x*(1-x)'},
    'bifurcation': {'func': calc_bifurcation_diagram, 'params': ['r_min', 'r_max', 'n_r', 'n_transient', 'n_sample'], 'desc': 'Bifurcation diagram data for logistic map'},
    'feigenbaum': {'func': calc_feigenbaum_constants, 'params': [], 'desc': 'Feigenbaum constants delta and alpha'},
    'lyapunov': {'func': calc_lyapunov_exponent, 'params': ['r', 'x0', 'n_iter'], 'desc': 'Lyapunov exponent for logistic map'},
    'lyapunov_spectrum': {'func': calc_lyapunov_spectrum, 'params': ['r_value', 'n_iter', 'n_transient'], 'desc': 'Lyapunov exponent over transient-removed trajectory'},
    'lorenz': {'func': calc_lorenz_system, 'params': ['sigma', 'rho', 'beta', 'x0', 'y0', 'z0', 'dt', 'n_steps'], 'desc': 'Lorenz attractor RK4 simulation'},
    'lorenz_fixed': {'func': calc_lorenz_fixed_points, 'params': ['sigma', 'rho', 'beta'], 'desc': 'Fixed points of Lorenz system'},
    'mandelbrot': {'func': calc_mandelbrot, 'params': ['width', 'height', 'x_min', 'x_max', 'y_min', 'y_max', 'max_iter'], 'desc': 'Mandelbrot set computation'},
    'julia': {'func': calc_julia_set, 'params': ['c_real', 'c_imag', 'width', 'height', 'max_iter'], 'desc': 'Julia set for complex parameter c'},
    'box_counting': {'func': calc_box_counting_dimension, 'params': ['points', 'box_sizes'], 'desc': 'Box-counting fractal dimension'},
    'sierpinski': {'func': calc_sierpinski_triangle, 'params': ['depth', 'size'], 'desc': 'Sierpinski triangle via chaos game'},
    'koch_curve': {'func': calc_koch_curve, 'params': ['order', 'length'], 'desc': 'Koch snowflake perimeter and dimension'},
    'duffing': {'func': calc_duffing_oscillator, 'params': ['alpha', 'beta', 'gamma', 'delta', 'omega', 'x0', 'v0', 'dt', 'n_steps'], 'desc': 'Duffing oscillator RK4 simulation'},
    'van_der_pol': {'func': calc_van_der_pol, 'params': ['mu', 'x0', 'v0', 'dt', 'n_steps'], 'desc': 'Van der Pol oscillator simulation'},
    'nonlinear_pendulum': {'func': calc_nonlinear_pendulum, 'params': ['theta0', 'omega0', 'L', 'g', 'dt', 'n_steps'], 'desc': 'Nonlinear pendulum RK4 simulation'},
    'sandpile': {'func': calc_sandpile_model, 'params': ['grid_size', 'n_grains', 'critical_slope'], 'desc': 'BTW sandpile model for SOC'},
    'ising_2d': {'func': calc_ising_model_2d, 'params': ['L', 'T', 'n_steps'], 'desc': '2D Ising model Monte Carlo simulation'},
    'critical_exponents': {'func': calc_critical_exponents, 'params': [], 'desc': 'Critical exponents for universality classes'},
    'henon': {'func': calc_henon_map, 'params': ['a', 'b', 'x0', 'y0', 'n_iter'], 'desc': 'Henon map iteration'},
    'rossler': {'func': calc_rossler_system, 'params': ['a', 'b', 'c', 'x0', 'y0', 'z0', 'dt', 'n_steps'], 'desc': 'Rossler attractor simulation'},
    'tent_map': {'func': calc_tent_map, 'params': ['r', 'x0', 'n_iter'], 'desc': 'Tent map iteration'},
    'standard_map': {'func': calc_standard_map, 'params': ['K', 'p0', 'theta0', 'n_iter'], 'desc': 'Chirikov standard map'},
    'poincare': {'func': calc_poincare_section, 'params': ['trajectory_data', 'plane_dim', 'plane_val'], 'desc': 'Poincare section from trajectory'},
    'correlation_dimension': {'func': calc_correlation_dimension, 'params': ['points', 'epsilons'], 'desc': 'Correlation dimension estimation'},
    'recurrence_plot': {'func': calc_recurrence_plot, 'params': ['time_series', 'threshold'], 'desc': 'Recurrence plot from time series'}
}
