"""
Differential Equations & Dynamical Systems — ODEs, PDEs, Phase Portraits
"""
import math
import numpy as np

COMMANDS = {}


def euler_ode(dydx: float = 0.5, y0: float = 1, x0: float = 0, xf: float = 2, h: float = 0.1) -> dict:
    """Euler method y_{n+1}=y_n+h*f(x_n,y_n) for dy/dx=y (f(x,y)=y)"""
    y = y0
    x = x0
    steps = int((xf-x0)/h)
    for _ in range(steps):
        y = y + h * y
        x += h
    exact = y0 * math.exp(xf)
    return {'result': f'y({xf})={y:.6f} (Euler), exact={exact:.6f}', 'details': {'method': 'Euler', 'y_final': y, 'exact': exact, 'h': h, 'steps': steps}, 'unit': ''}


def rk4_ode(y0: float = 1, x0: float = 0, xf: float = 2, h: float = 0.1) -> dict:
    """Runge-Kutta 4 for dy/dx=y"""
    y = y0
    x = x0
    steps = int((xf-x0)/h)
    for _ in range(steps):
        k1 = h * y
        k2 = h * (y + k1/2)
        k3 = h * (y + k2/2)
        k4 = h * (y + k3)
        y = y + (k1 + 2*k2 + 2*k3 + k4)/6
        x += h
    exact = y0 * math.exp(xf)
    return {'result': f'y({xf})={y:.8f} (RK4), exact={exact:.8f}', 'details': {'method': 'RK4', 'y_final': y, 'exact': exact, 'h': h, 'steps': steps}, 'unit': ''}


def second_order_ode(y0: float = 1, yp0: float = 0, x0: float = 0, xf: float = 10, h: float = 0.05) -> dict:
    """y''+y=0 (harmonic oscillator) via RK4 reduction to first-order system"""
    def f(t, Y):
        return np.array([Y[1], -Y[0]])
    Y = np.array([y0, yp0], dtype=float)
    t = x0
    steps = int((xf-x0)/h)
    for _ in range(steps):
        k1 = h * f(t, Y)
        k2 = h * f(t + h/2, Y + k1/2)
        k3 = h * f(t + h/2, Y + k2/2)
        k4 = h * f(t + h, Y + k3)
        Y = Y + (k1 + 2*k2 + 2*k3 + k4)/6
        t += h
    return {'result': f'x={t:.6f}, y={Y[0]:.6f}, y\'={Y[1]:.6f}', 'details': {'x_final': t, 'y': float(Y[0]), 'y_prime': float(Y[1]), 'steps': steps}, 'unit': ''}


def lotka_volterra(prey: float = 40, predator: float = 9, alpha: float = 0.1, beta: float = 0.02, gamma: float = 0.3, delta: float = 0.01, dt: float = 0.01, steps: float = 1000) -> dict:
    """dx/dt=alpha*x-beta*x*y, dy/dt=delta*x*y-gamma*y (one Euler step)"""
    x, y = prey, predator
    for _ in range(int(steps)):
        x_new = x + dt * (alpha*x - beta*x*y)
        y_new = y + dt * (delta*x*y - gamma*y)
        x, y = x_new, y_new
    return {'result': f'Prey={x:.4f}, Predator={y:.4f} at t={dt*steps:.2f}', 'details': {'prey_final': x, 'predator_final': y, 'time': dt*steps, 'steps': int(steps)}, 'unit': ''}


def pendulum(theta0: float = 0.5, omega0: float = 0, dt: float = 0.01, steps: float = 500, L: float = 1, g: float = 9.81) -> dict:
    """theta''=-(g/L)*sin(theta) solved with RK2 (midpoint)"""
    theta, omega = theta0, omega0
    for _ in range(int(steps)):
        k1_theta = dt * omega
        k1_omega = dt * (-g/L * math.sin(theta))
        k2_theta = dt * (omega + k1_omega/2)
        k2_omega = dt * (-g/L * math.sin(theta + k1_theta/2))
        theta += k2_theta
        omega += k2_omega
    return {'result': f'theta={theta:.6f} rad, omega={omega:.6f} rad/s', 'details': {'theta': theta, 'omega': omega, 'L': L, 'g': g, 'time': dt*steps}, 'unit': ''}


def heat_equation_1d(initial: str = '100,0,0,0,0', alpha: float = 0.4, dt: float = 0.01, steps: float = 50) -> dict:
    """Explicit FTCS scheme: du/dt=alpha*d^2u/dx^2, fixed boundaries"""
    u = np.array([float(v) for v in initial.split(',')], dtype=float)
    n = len(u)
    for _ in range(int(steps)):
        u_new = u.copy()
        for i in range(1, n-1):
            u_new[i] = u[i] + alpha*dt*(u[i+1] - 2*u[i] + u[i-1])
        u = u_new
    u_list = [f'{v:.2f}' for v in u]
    return {'result': f'u = [{", ".join(u_list)}]', 'details': {'final_state': u.tolist(), 'alpha': alpha, 'dt': dt, 'steps': int(steps)}, 'unit': ''}


def wave_equation_1d(initial: str = '0,0.5,1,0.5,0', c: float = 1, dt: float = 0.1, steps: float = 20) -> dict:
    """1D wave u_i^{n+1}=2*u_i^n-u_i^{n-1}+(c*dt)^2*(u_{i+1}^n-2*u_i^n+u_{i-1}^n)"""
    u0 = np.array([float(v) for v in initial.split(',')], dtype=float)
    u_prev = u0.copy()
    u_curr = u0.copy()
    n = len(u0)
    r = (c*dt)**2
    for _ in range(int(steps)):
        u_next = u_curr.copy()
        for i in range(1, n-1):
            u_next[i] = 2*u_curr[i] - u_prev[i] + r*(u_curr[i+1] - 2*u_curr[i] + u_curr[i-1])
        u_prev, u_curr = u_curr, u_next
    u_list = [f'{v:.4f}' for v in u_curr]
    return {'result': f'u = [{", ".join(u_list)}]', 'details': {'final_state': u_curr.tolist(), 'c': c, 'dt': dt, 'steps': int(steps)}, 'unit': ''}


def phase_portrait(dxdt_type: str = 'saddle', x: float = 1, y: float = 0) -> dict:
    """Compute (dx/dt, dy/dt) for saddle/center/spiral/node"""
    if dxdt_type == 'saddle':
        dx, dy = x, -y
    elif dxdt_type == 'center':
        dx, dy = y, -x
    elif dxdt_type == 'spiral':
        dx, dy = -x + y, -x - y
    elif dxdt_type == 'node':
        dx, dy = -x, -y
    else:
        dx, dy = 0.0, 0.0
    mag = math.sqrt(dx*dx + dy*dy)
    return {'result': f'({dxdt_type}) dx/dt={dx:.4f}, dy/dt={dy:.4f}, |v|={mag:.4f}', 'details': {'type': dxdt_type, 'dx/dt': dx, 'dy/dt': dy, 'magnitude': mag}, 'unit': ''}


COMMANDS['euler'] = {'func': euler_ode, 'params': ['dydx', 'y0', 'x0', 'xf', 'h'], 'desc': 'Euler method for dy/dx=y'}
COMMANDS['rk4'] = {'func': rk4_ode, 'params': ['y0', 'x0', 'xf', 'h'], 'desc': 'Runge-Kutta 4 for dy/dx=y'}
COMMANDS['ode2'] = {'func': second_order_ode, 'params': ['y0', 'yp0', 'x0', 'xf', 'h'], 'desc': "Solve y''+y=0 via RK4 reduction"}
COMMANDS['lotka-volterra'] = {'func': lotka_volterra, 'params': ['prey', 'predator', 'alpha', 'beta', 'gamma', 'delta', 'dt', 'steps'], 'desc': 'Lotka-Volterra predator-prey'}
COMMANDS['pendulum'] = {'func': pendulum, 'params': ['theta0', 'omega0', 'dt', 'steps', 'L', 'g'], 'desc': 'Pendulum theta''=-(g/L)sin(theta) RK2'}
COMMANDS['heat1d'] = {'func': heat_equation_1d, 'params': ['initial', 'alpha', 'dt', 'steps'], 'desc': '1D heat equation FTCS scheme'}
COMMANDS['wave1d'] = {'func': wave_equation_1d, 'params': ['initial', 'c', 'dt', 'steps'], 'desc': '1D wave equation explicit scheme'}
COMMANDS['phase'] = {'func': phase_portrait, 'params': ['dxdt_type', 'x', 'y'], 'desc': 'Phase portrait (dx/dt,dy/dt) for saddle/center/spiral/node'}
