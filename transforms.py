"""
Transforms & Signal Processing — Fourier, Laplace, Z, Wavelets, Filters
"""
import math
import numpy as np

COMMANDS = {}


def fourier_1d(signal: str = '1,2,3,4,5,6,7,8') -> dict:
    """DFT of real signal using numpy.fft, return magnitude spectrum"""
    x = np.array([float(v) for v in signal.split(',')])
    X = np.fft.fft(x)
    mag = np.abs(X)
    mag_list = [f'{v:.2f}' for v in mag]
    return {'result': f'|X| = [{", ".join(mag_list)}]', 'details': {'signal': x.tolist(), 'magnitude': mag.tolist()}, 'unit': ''}


def fft_power_spectrum(signal: str = '1,2,3,2,1,0,-1,-2', dt: float = 0.1) -> dict:
    """Power spectrum from FFT, return max frequency component"""
    x = np.array([float(v) for v in signal.split(',')])
    n = len(x)
    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(n, d=dt)
    power = np.abs(X)**2
    idx = np.argmax(power[:n//2])
    return {'result': f'Peak at f={abs(freqs[idx]):.4f} Hz, power={power[idx]:.2f}', 'details': {'freqs': freqs[:n//2].tolist(), 'power': power[:n//2].tolist(), 'peak_freq': float(abs(freqs[idx])), 'peak_power': float(power[idx])}, 'unit': 'Hz'}


def laplace_transform_basic(s: float = 2, a: float = 1) -> dict:
    """L{e^{-at}} evaluated at s: 1/(s+a)"""
    Fs = 1 / (s + a)
    return {'result': f'L{{e^(-{a}t)}}(s={s}) = {Fs:.6f}', 'details': {'s': s, 'a': a, 'F(s)': Fs, 'transform': 'e^{-at} -> 1/(s+a)'}, 'unit': ''}


def z_transform_basic(z: float = 0.5, a: float = 1) -> dict:
    """Z{a^n} = z/(z-a), |z|>|a|"""
    if abs(z) > abs(a):
        Fz = z / (z - a)
    else:
        Fz = float('inf')
    return {'result': f'Z{{a^n}}(z={z}) = {Fz}', 'details': {'z': z, 'a': a, 'F(z)': Fz, 'converges': abs(z) > abs(a)}, 'unit': ''}


def convolution(signal1: str = '1,2,3', signal2: str = '1,1,1') -> dict:
    """Convolution using numpy.convolve"""
    x = np.array([float(v) for v in signal1.split(',')])
    h = np.array([float(v) for v in signal2.split(',')])
    y = np.convolve(x, h, mode='full')
    y_list = [f'{v:.1f}' for v in y]
    return {'result': f'x * h = [{", ".join(y_list)}]', 'details': {'signal1': x.tolist(), 'signal2': h.tolist(), 'convolution': y.tolist()}, 'unit': ''}


def correlation(signal1: str = '1,2,3,4', signal2: str = '3,4,5,6') -> dict:
    """Cross-correlation using numpy.correlate"""
    x = np.array([float(v) for v in signal1.split(',')])
    y = np.array([float(v) for v in signal2.split(',')])
    r = np.correlate(x, y, mode='full')
    r_list = [f'{v:.1f}' for v in r]
    idx = np.argmax(r)
    return {'result': f'xcorr = [{", ".join(r_list)}], max at lag={idx-(len(x)-1)}', 'details': {'signal1': x.tolist(), 'signal2': y.tolist(), 'correlation': r.tolist(), 'max_lag': int(idx-(len(x)-1))}, 'unit': ''}


def low_pass_filter(signal: str = '1,2,3,2,1', cutoff: float = 0.5) -> dict:
    """Simple moving average filter (window=3) as low-pass"""
    x = np.array([float(v) for v in signal.split(',')])
    n = len(x)
    y = np.zeros(n)
    for i in range(n):
        if i == 0:
            y[i] = (x[0] + x[1]) / 2
        elif i == n - 1:
            y[i] = (x[-2] + x[-1]) / 2
        else:
            y[i] = (x[i-1] + x[i] + x[i+1]) / 3
    y_list = [f'{v:.3f}' for v in y]
    return {'result': f'Low-pass = [{", ".join(y_list)}]', 'details': {'original': x.tolist(), 'filtered': y.tolist(), 'cutoff': cutoff}, 'unit': ''}


def high_pass_filter(signal: str = '1,2,3,2,1') -> dict:
    """High-pass via signal - lowpass (moving avg)"""
    x = np.array([float(v) for v in signal.split(',')])
    n = len(x)
    low = np.zeros(n)
    for i in range(n):
        if i == 0:
            low[i] = (x[0] + x[1]) / 2
        elif i == n - 1:
            low[i] = (x[-2] + x[-1]) / 2
        else:
            low[i] = (x[i-1] + x[i] + x[i+1]) / 3
    y = x - low
    y_list = [f'{v:.3f}' for v in y]
    return {'result': f'High-pass = [{", ".join(y_list)}]', 'details': {'original': x.tolist(), 'filtered': y.tolist()}, 'unit': ''}


def wavelet_haar(signal: str = '1,2,3,4,5,6,7,8') -> dict:
    """Single-level Haar DWT: averages and details"""
    x = np.array([float(v) for v in signal.split(',')])
    n = len(x)
    avg = [float((x[2*i] + x[2*i+1])/2) for i in range(n//2)]
    det = [float((x[2*i] - x[2*i+1])/2) for i in range(n//2)]
    avg_str = ', '.join([f'{v:.2f}' for v in avg])
    det_str = ', '.join([f'{v:.2f}' for v in det])
    return {'result': f'Avg=[{avg_str}], Det=[{det_str}]', 'details': {'averages': avg, 'details': det}, 'unit': ''}


def hilbert_envelope(signal: str = '1,2,3,2,1,0,-1,-2', dt: float = 0.1) -> dict:
    """Analytic signal via FFT, return envelope magnitude"""
    x = np.array([float(v) for v in signal.split(',')])
    n = len(x)
    X = np.fft.fft(x)
    h = np.zeros(n)
    if n % 2 == 0:
        h[0] = 1
        h[n//2] = 1
        h[1:n//2] = 2
    else:
        h[0] = 1
        h[1:(n+1)//2] = 2
    Xa = X * h
    xa = np.fft.ifft(Xa)
    env = np.abs(xa)
    env_list = [f'{v:.3f}' for v in env]
    return {'result': f'Envelope = [{", ".join(env_list)}]', 'details': {'original': x.tolist(), 'envelope': env.tolist()}, 'unit': ''}


COMMANDS['dft'] = {'func': fourier_1d, 'params': ['signal'], 'desc': 'DFT of real signal, magnitude spectrum'}
COMMANDS['fft-power'] = {'func': fft_power_spectrum, 'params': ['signal', 'dt'], 'desc': 'Power spectrum from FFT'}
COMMANDS['laplace'] = {'func': laplace_transform_basic, 'params': ['s', 'a'], 'desc': 'L{e^{-at}} = 1/(s+a)'}
COMMANDS['ztrans'] = {'func': z_transform_basic, 'params': ['z', 'a'], 'desc': 'Z{a^n} = z/(z-a)'}
COMMANDS['conv'] = {'func': convolution, 'params': ['signal1', 'signal2'], 'desc': 'Convolution via numpy.convolve'}
COMMANDS['xcorr'] = {'func': correlation, 'params': ['signal1', 'signal2'], 'desc': 'Cross-correlation via numpy.correlate'}
COMMANDS['lowpass'] = {'func': low_pass_filter, 'params': ['signal', 'cutoff'], 'desc': 'Moving average low-pass filter'}
COMMANDS['highpass'] = {'func': high_pass_filter, 'params': ['signal'], 'desc': 'High-pass = signal - lowpass'}
COMMANDS['haar'] = {'func': wavelet_haar, 'params': ['signal'], 'desc': 'Single-level Haar wavelet transform'}
COMMANDS['hilbert'] = {'func': hilbert_envelope, 'params': ['signal', 'dt'], 'desc': 'Hilbert envelope via analytic signal'}
