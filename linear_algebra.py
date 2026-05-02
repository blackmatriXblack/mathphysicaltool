"""
Linear Algebra - Mathematics Computation Module
"""
import math
import numpy as np
from itertools import combinations

COMMANDS = {}

# ==============================================================================
# DETERMINANTS
# ==============================================================================

def calc_det_2x2(a: float = 3.0, b: float = 1.0, c: float = 2.0, d: float = 4.0) -> dict:
    """Compute determinant of 2x2 matrix [[a,b],[c,d]] = ad - bc."""
    det = a * d - b * c
    return {
        'result': f'det = {a}*{d} - {b}*{c} = {det}',
        'details': {'matrix': [[a, b], [c, d]], 'det': det},
        'unit': 'dimensionless'
    }

def calc_det_3x3(matrix: list = None) -> dict:
    """Compute determinant of 3x3 matrix using Sarrus rule."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    A = np.array(matrix, dtype=float)
    det = A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) \
        - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) \
        + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    return {
        'result': f'det = {det:.4f}',
        'details': {'matrix': matrix, 'det': det},
        'unit': 'dimensionless'
    }

def calc_det_nxn(matrix: list = None, method: str = 'numpy') -> dict:
    """Compute determinant of nxn matrix using Laplace expansion or numpy."""
    if matrix is None:
        matrix = [[1, 0, 2, -1], [3, 0, 0, 5], [2, 1, 4, -3], [1, 0, 5, 0]]
    A = np.array(matrix, dtype=float)
    if method == 'laplace':
        det = _laplace_det(A)
    else:
        det = np.linalg.det(A)
    return {
        'result': f'det = {det:.6f}',
        'details': {'matrix': A.tolist(), 'shape': A.shape, 'method': method, 'det': det},
        'unit': 'dimensionless'
    }

def _laplace_det(A: np.ndarray) -> float:
    """Recursive Laplace expansion along first row."""
    n = A.shape[0]
    if n == 1:
        return A[0, 0]
    if n == 2:
        return A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
    det = 0.0
    for j in range(n):
        sub = np.delete(np.delete(A, 0, axis=0), j, axis=1)
        det += ((-1) ** j) * A[0, j] * _laplace_det(sub)
    return det

def calc_det_properties(matrix: list = None) -> dict:
    """Compute determinant properties: det(A^T) = det(A), det(kA) = k^n det(A), det(A^(-1)) = 1/det(A)."""
    if matrix is None:
        matrix = [[2, 1], [3, 4]]
    A = np.array(matrix, dtype=float)
    det_A = np.linalg.det(A)
    det_AT = np.linalg.det(A.T)
    n = A.shape[0]
    k = 2.0
    det_kA = np.linalg.det(k * A)
    det_kA_expected = (k ** n) * det_A
    props = {
        'det(A)': det_A,
        'det(A^T)': det_AT,
        'det(A^T) == det(A)': abs(det_A - det_AT) < 1e-10,
        f'det({k}A)': det_kA,
        f'{k}^{n} * det(A)': det_kA_expected,
        'det(kA) == k^n det(A)': abs(det_kA - det_kA_expected) < 1e-10,
    }
    if abs(det_A) > 1e-12:
        det_inv = np.linalg.det(np.linalg.inv(A))
        props['det(A^-1)'] = det_inv
        props['1/det(A)'] = 1 / det_A
        props['det(A^-1) == 1/det(A)']: abs(det_inv - 1 / det_A) < 1e-10
    if 'det(A^-1) == 1/det(A)' not in props:
        props['note'] = 'Matrix is singular, A^{-1} does not exist'
    return {
        'result': f'det(A) = {det_A:.6f}, det(A^T) = {det_AT:.6f}',
        'details': {'matrix': A.tolist(), 'properties': {k: v for k, v in props.items() if not isinstance(v, bool)}},
        'unit': 'dimensionless'
    }

# ==============================================================================
# MATRICES
# ==============================================================================

def calc_matrix_add(A: list = None, B: list = None) -> dict:
    """Add two matrices A + B."""
    if A is None:
        A = [[1, 2], [3, 4]]
    if B is None:
        B = [[5, 6], [7, 8]]
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    if A_np.shape != B_np.shape:
        return {
            'result': f'Error: Matrices must have same shape. A={A_np.shape}, B={B_np.shape}',
            'details': {'A': A, 'B': B, 'error': 'shape mismatch'},
            'unit': 'matrix'
        }
    C = A_np + B_np
    return {
        'result': f'A + B = {C.tolist()}',
        'details': {'A': A, 'B': B, 'result': C.tolist()},
        'unit': 'matrix'
    }

def calc_matrix_multiply(A: list = None, B: list = None) -> dict:
    """Multiply two matrices A * B."""
    if A is None:
        A = [[1, 2], [3, 4]]
    if B is None:
        B = [[5, 6], [7, 8]]
    A_np = np.array(A, dtype=float)
    B_np = np.array(B, dtype=float)
    if A_np.shape[1] != B_np.shape[0]:
        return {
            'result': f'Error: Inner dimensions must match. A={A_np.shape}, B={B_np.shape}',
            'details': {'A': A, 'B': B, 'error': 'inner dimension mismatch'},
            'unit': 'matrix'
        }
    C = A_np @ B_np
    return {
        'result': f'A * B = {C.tolist()}',
        'details': {'A': A, 'B': B, 'result': C.tolist()},
        'unit': 'matrix'
    }

def calc_matrix_scalar_mult(matrix: list = None, scalar: float = 3.0) -> dict:
    """Multiply a matrix by a scalar."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6]]
    A = np.array(matrix, dtype=float)
    C = scalar * A
    return {
        'result': f'{scalar} * A = {C.tolist()}',
        'details': {'matrix': matrix, 'scalar': scalar, 'result': C.tolist()},
        'unit': 'matrix'
    }

def calc_matrix_transpose(matrix: list = None) -> dict:
    """Compute transpose of a matrix."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6]]
    A = np.array(matrix, dtype=float)
    AT = A.T
    return {
        'result': f'A^T = {AT.tolist()}',
        'details': {'matrix': matrix, 'transpose': AT.tolist(), 'original_shape': A.shape, 'transpose_shape': AT.shape},
        'unit': 'matrix'
    }

def calc_matrix_trace(matrix: list = None) -> dict:
    """Compute trace of a square matrix (sum of diagonal entries)."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {
            'result': 'Error: Trace is only defined for square matrices',
            'details': {'matrix': matrix, 'shape': A.shape, 'error': 'not square'},
            'unit': 'number'
        }
    tr = np.trace(A)
    return {
        'result': f'tr(A) = {tr:.4f}',
        'details': {'matrix': matrix, 'trace': tr, 'diagonal': np.diag(A).tolist()},
        'unit': 'number'
    }

def calc_matrix_inverse(matrix: list = None, method: str = 'numpy') -> dict:
    """Compute inverse of a square matrix A^(-1)."""
    if matrix is None:
        matrix = [[4, 7], [2, 6]]
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {
            'result': 'Error: Inverse requires a square matrix',
            'details': {'matrix': matrix, 'shape': A.shape, 'error': 'not square'},
            'unit': 'matrix'
        }
    det = np.linalg.det(A)
    if abs(det) < 1e-12:
        return {
            'result': 'Error: Matrix is singular (det = 0), no inverse exists',
            'details': {'matrix': matrix, 'det': det, 'error': 'singular'},
            'unit': 'matrix'
        }
    if method == 'adjugate' and A.shape[0] == 2:
        inv = np.array([[A[1, 1], -A[0, 1]], [-A[1, 0], A[0, 0]]]) / det
    elif method == 'adjugate' and A.shape[0] == 3:
        inv = _adjugate_3x3(A) / det
    else:
        try:
            inv = np.linalg.inv(A)
        except np.linalg.LinAlgError:
            return {
                'result': 'Error: Matrix inversion failed',
                'details': {'matrix': matrix, 'det': det, 'error': 'LinAlgError'},
                'unit': 'matrix'
            }
    check = A @ inv
    return {
        'result': f'det(A) = {det:.6f}, A^(-1) = {inv.tolist()}',
        'details': {'matrix': matrix, 'det': det, 'inverse': inv.tolist(), 'check_A_times_Ainv': check.tolist()},
        'unit': 'matrix'
    }

def _adjugate_3x3(A: np.ndarray) -> np.ndarray:
    C = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            sub = np.delete(np.delete(A, i, axis=0), j, axis=1)
            C[i, j] = ((-1) ** (i + j)) * (sub[0, 0] * sub[1, 1] - sub[0, 1] * sub[1, 0])
    return C.T

def calc_rank(matrix: list = None) -> dict:
    """Compute rank of a matrix (via row echelon form)."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    A = np.array(matrix, dtype=float)
    rank = np.linalg.matrix_rank(A)
    return {
        'result': f'rank(A) = {rank} (shape = {A.shape})',
        'details': {'matrix': matrix, 'shape': A.shape, 'rank': rank},
        'unit': 'dimensionless'
    }

def calc_condition_number(matrix: list = None) -> dict:
    """Compute condition number of a matrix."""
    if matrix is None:
        matrix = [[1, 2], [2, 4.001]]
    A = np.array(matrix, dtype=float)
    cond = np.linalg.cond(A)
    return {
        'result': f'cond(A) = {cond:.6f}',
        'details': {'matrix': matrix, 'condition_number': cond, 'ill_conditioned': cond > 1000},
        'unit': 'dimensionless'
    }

def calc_lu_decomposition(matrix: list = None) -> dict:
    """Compute LU decomposition: A = L * U."""
    if matrix is None:
        matrix = [[4, 3], [6, 3]]
    A = np.array(matrix, dtype=float)
    n = A.shape[0]
    L = np.eye(n)
    U = A.copy().astype(float)
    for i in range(n):
        for j in range(i + 1, n):
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    check = L @ U
    return {
        'result': f'LU: L = {L.tolist()}, U = {U.tolist()}',
        'details': {'matrix': matrix, 'L': L.tolist(), 'U': U.tolist(), 'check': check.tolist()},
        'unit': 'decomposition'
    }

def calc_qr_decomposition(matrix: list = None) -> dict:
    """Compute QR decomposition using Gram-Schmidt."""
    if matrix is None:
        matrix = [[1, -1], [1, 1]]
    A = np.array(matrix, dtype=float)
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for j in range(n):
        v = A[:, j].copy().astype(float)
        for i in range(j):
            R[i, j] = Q[:, i] @ A[:, j]
            v -= R[i, j] * Q[:, i]
        R[j, j] = np.linalg.norm(v)
        if R[j, j] > 1e-12:
            Q[:, j] = v / R[j, j]
    check = Q @ R
    return {
        'result': f'QR: Q = {np.round(Q, 4).tolist()}, R = {np.round(R, 4).tolist()}',
        'details': {'matrix': matrix, 'Q': Q.tolist(), 'R': R.tolist(), 'check': check.tolist()},
        'unit': 'decomposition'
    }

def calc_svd(matrix: list = None) -> dict:
    """Compute Singular Value Decomposition A = U * S * V^T."""
    if matrix is None:
        matrix = [[1, 2], [3, 4], [5, 6]]
    A = np.array(matrix, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    S = np.diag(s)
    check = U @ S @ Vt
    return {
        'result': f'SVD: singular values = {np.round(s, 4).tolist()}',
        'details': {'matrix': matrix, 'U': U.tolist(), 'S': S.tolist(), 'Vt': Vt.tolist(), 'singular_values': s.tolist(), 'check': np.round(check, 6).tolist()},
        'unit': 'decomposition'
    }

# ==============================================================================
# VECTORS
# ==============================================================================

def calc_dot_product(v1: list = None, v2: list = None) -> dict:
    """Compute dot product of two vectors."""
    if v1 is None:
        v1 = [1, 2, 3]
    if v2 is None:
        v2 = [4, 5, 6]
    v1_np = np.array(v1, dtype=float)
    v2_np = np.array(v2, dtype=float)
    if len(v1_np) != len(v2_np):
        return {
            'result': f'Error: Vectors must have same dimension',
            'details': {'v1': v1, 'v2': v2, 'error': 'dimension mismatch'},
            'unit': 'number'
        }
    dot = np.dot(v1_np, v2_np)
    angle = math.acos(np.clip(dot / (np.linalg.norm(v1_np) * np.linalg.norm(v2_np)), -1, 1))
    return {
        'result': f'v1 · v2 = {dot:.4f}, angle = {math.degrees(angle):.2f}°',
        'details': {'v1': v1, 'v2': v2, 'dot_product': dot, 'angle_rad': angle, 'angle_deg': math.degrees(angle)},
        'unit': 'number'
    }

def calc_cross_product(v1: list = None, v2: list = None) -> dict:
    """Compute cross product v1 x v2 (3D vectors)."""
    if v1 is None:
        v1 = [1, 0, 0]
    if v2 is None:
        v2 = [0, 1, 0]
    v1_np = np.array(v1, dtype=float)
    v2_np = np.array(v2, dtype=float)
    if len(v1_np) != 3 or len(v2_np) != 3:
        return {
            'result': 'Error: Cross product is defined in 3D only',
            'details': {'v1': v1, 'v2': v2, 'error': 'not 3D'},
            'unit': 'vector'
        }
    cross = np.cross(v1_np, v2_np)
    magnitude = np.linalg.norm(cross)
    area = magnitude
    return {
        'result': f'v1 x v2 = ({cross[0]:.4f}, {cross[1]:.4f}, {cross[2]:.4f}), magnitude = {magnitude:.4f}',
        'details': {'v1': v1, 'v2': v2, 'cross_product': cross.tolist(), 'magnitude': magnitude, 'area_parallelogram': area},
        'unit': 'vector'
    }

def calc_vector_norm(v: list = None, norm_type: str = 'L2') -> dict:
    """Compute vector norm: L1, L2 (Euclidean), Linf."""
    if v is None:
        v = [3, 4]
    v_np = np.array(v, dtype=float)
    if norm_type == 'L1':
        n = np.sum(np.abs(v_np))
    elif norm_type == 'Linf':
        n = np.max(np.abs(v_np))
    else:
        n = np.linalg.norm(v_np)
    return {
        'result': f'||v||_{norm_type} = {n:.4f}',
        'details': {'v': v, 'norm_type': norm_type, 'norm': n},
        'unit': 'number'
    }

def calc_angle_between_vectors(v1: list = None, v2: list = None) -> dict:
    """Compute the angle between two vectors."""
    if v1 is None:
        v1 = [1, 0]
    if v2 is None:
        v2 = [1, 1]
    v1_np = np.array(v1, dtype=float)
    v2_np = np.array(v2, dtype=float)
    n1 = np.linalg.norm(v1_np)
    n2 = np.linalg.norm(v2_np)
    if n1 < 1e-12 or n2 < 1e-12:
        return {
            'result': 'Error: Cannot compute angle (zero vector)',
            'details': {'v1': v1, 'v2': v2, 'error': 'zero vector'},
            'unit': 'radian'
        }
    cos_theta = np.clip(np.dot(v1_np, v2_np) / (n1 * n2), -1, 1)
    angle = math.acos(cos_theta)
    return {
        'result': f'angle = {angle:.6f} rad = {math.degrees(angle):.4f}°',
        'details': {'v1': v1, 'v2': v2, 'cos_angle': cos_theta, 'angle_rad': angle, 'angle_deg': math.degrees(angle)},
        'unit': 'radian'
    }

def calc_projection(v: list = None, onto: list = None) -> dict:
    """Project vector v onto vector u."""
    if v is None:
        v = [3, 4]
    if onto is None:
        onto = [1, 0]
    v_np = np.array(v, dtype=float)
    u_np = np.array(onto, dtype=float)
    u_norm_sq = np.dot(u_np, u_np)
    if u_norm_sq < 1e-12:
        return {
            'result': 'Error: Cannot project onto zero vector',
            'details': {'v': v, 'onto': onto, 'error': 'zero vector'},
            'unit': 'vector'
        }
    scalar = np.dot(v_np, u_np) / u_norm_sq
    proj = scalar * u_np
    reject = v_np - proj
    return {
        'result': f'proj_u(v) = ({proj[0]:.4f}, {proj[1]:.4f})' + (f', ({proj[2]:.4f})' if len(proj) > 2 else ''),
        'details': {'v': v, 'onto': onto, 'scalar': scalar, 'projection': proj.tolist(), 'rejection': reject.tolist()},
        'unit': 'vector'
    }

def calc_gram_schmidt(vectors: list = None) -> dict:
    """Orthogonalize a set of vectors using Gram-Schmidt process."""
    if vectors is None:
        vectors = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    A = np.array(vectors, dtype=float).T
    m, n = A.shape
    Q = np.zeros((m, n))
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            v -= np.dot(Q[:, i], A[:, j]) * Q[:, i]
        norm_v = np.linalg.norm(v)
        if norm_v > 1e-12:
            Q[:, j] = v / norm_v
    orthonormal = Q.T.tolist()
    # Check orthonormality
    is_orthonormal = True
    for i in range(n):
        for j in range(n):
            if i != j and abs(np.dot(Q[:, i], Q[:, j])) > 1e-10:
                is_orthonormal = False
            if i == j and abs(np.dot(Q[:, i], Q[:, j]) - 1) > 1e-10:
                is_orthonormal = False
    return {
        'result': f'Orthonormal basis: {[np.round(v, 4).tolist() for v in orthonormal]}. Orthonormal: {is_orthonormal}',
        'details': {'input_vectors': vectors, 'orthonormal': orthonormal, 'is_orthonormal': is_orthonormal},
        'unit': 'vectors'
    }

def calc_basis_check(vectors: list = None) -> dict:
    """Check if vectors form a basis (linear independence test)."""
    if vectors is None:
        vectors = [[1, 0], [0, 1], [1, 1]]
    A = np.array(vectors, dtype=float)
    rank = np.linalg.matrix_rank(A)
    n_vectors = A.shape[0]
    dim = A.shape[1] if len(A.shape) > 1 else 1
    is_basis = rank == n_vectors and n_vectors == dim
    is_independent = rank == n_vectors
    span_dim = rank
    return {
        'result': f'Linearly independent: {is_independent}, Is basis: {is_basis}, Span dimension: {span_dim} (rank = {rank}, vectors = {n_vectors})',
        'details': {'vectors': vectors, 'rank': rank, 'n_vectors': n_vectors, 'dimension': dim, 'linearly_independent': is_independent, 'is_basis': is_basis, 'span_dim': span_dim},
        'unit': 'boolean'
    }

# ==============================================================================
# EIGENVALUES
# ==============================================================================

def calc_char_polynomial(matrix: list = None) -> dict:
    """Compute characteristic polynomial det(A - lambda*I) coefficients."""
    if matrix is None:
        matrix = [[2, 1], [1, 2]]
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {
            'result': 'Error: Characteristic polynomial requires a square matrix',
            'details': {'matrix': matrix, 'error': 'not square'},
            'unit': 'polynomial'
        }
    coeffs = np.poly(A)
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        power = n - i
        if abs(c) < 1e-12:
            continue
        sign = '' if (c >= 0 and len(terms) > 0) else ''
        if power == 0:
            terms.append(f'{sign}{c:.4f}')
        elif power == 1:
            terms.append(f'{sign}{c:.4f}*lambda')
        else:
            terms.append(f'{sign}{c:.4f}*lambda^{power}')
    poly_str = ' + '.join(terms).replace('+ -', '- ')
    if n % 2 == 0:
        poly_str = 'det(A - lambda*I) = ' + poly_str
    else:
        poly_str = 'det(A - lambda*I) = -' + poly_str if not poly_str.startswith('-') else 'det(A - lambda*I) = ' + poly_str
    return {
        'result': poly_str,
        'details': {'matrix': matrix, 'coefficients': coeffs.tolist(), 'degree': n},
        'unit': 'polynomial'
    }

def calc_eigenvalues(matrix: list = None, method: str = 'numpy') -> dict:
    """Compute eigenvalues of a square matrix."""
    if matrix is None:
        matrix = [[4, 1], [2, 3]]
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {
            'result': 'Error: Eigenvalues require a square matrix',
            'details': {'matrix': matrix, 'error': 'not square'},
            'unit': 'eigenvalues'
        }
    if method == 'power_iteration':
        # Power iteration for dominant eigenvalue
        v = np.random.rand(A.shape[0])
        for _ in range(100):
            v_new = A @ v
            v_new = v_new / np.linalg.norm(v_new)
            if np.linalg.norm(v_new - v) < 1e-10:
                break
            v = v_new
        dominant_eig = (v @ (A @ v)) / (v @ v)
        vals = [dominant_eig]
        vecs = [v.tolist()]
    elif method == 'qr_algorithm':
        vals, vecs = np.linalg.eig(A)
    else:
        vals, vecs = np.linalg.eig(A)
    trace = np.trace(A)
    det = np.linalg.det(A)
    sum_eig = np.sum(vals)
    prod_eig = np.prod(vals)
    return {
        'result': f'Eigenvalues: {np.round(vals, 6).tolist()}',
        'details': {
            'matrix': matrix, 'eigenvalues': vals.tolist(),
            'trace': trace, 'det': det,
            'sum_eigenvalues': sum_eig, 'product_eigenvalues': prod_eig,
            'trace_matches': abs(trace - sum_eig) < 1e-10 if not any(isinstance(v, complex) for v in vals) else 'complex',
            'det_matches': abs(det - prod_eig) < 1e-10 if not any(isinstance(v, complex) for v in vals) else 'complex'
        },
        'unit': 'eigenvalues'
    }

def calc_eigenvectors(matrix: list = None) -> dict:
    """Compute eigenvalues and eigenvectors. Returns (eigenvalue, eigenvector) pairs."""
    if matrix is None:
        matrix = [[4, 1], [2, 3]]
    A = np.array(matrix, dtype=float)
    if A.shape[0] != A.shape[1]:
        return {
            'result': 'Error: Eigenvectors require a square matrix',
            'details': {'matrix': matrix, 'error': 'not square'},
            'unit': 'eigenvectors'
        }
    vals, vecs = np.linalg.eig(A)
    pairs = []
    for i in range(len(vals)):
        pairs.append({
            'eigenvalue': complex(vals[i]),
            'eigenvector': [complex(v) for v in vecs[:, i]]
        })
    return {
        'result': f'Eigenvalues: {np.round(vals, 4).tolist()}',
        'details': {'matrix': matrix, 'eigenvalues': vals.tolist(), 'eigenvectors': vecs.tolist(), 'pairs': pairs},
        'unit': 'eigenvectors'
    }

def calc_diagonalization(matrix: list = None) -> dict:
    """Check if a matrix is diagonalizable and compute P, D."""
    if matrix is None:
        matrix = [[4, 1], [2, 3]]
    A = np.array(matrix, dtype=float)
    n = A.shape[0]
    vals, vecs = np.linalg.eig(A)
    P = vecs
    if np.linalg.matrix_rank(P) < n:
        return {
            'result': 'Matrix is NOT diagonalizable (defective - eigenvectors are linearly dependent)',
            'details': {'matrix': matrix, 'eigenvalues': vals.tolist(), 'diagonalizable': False},
            'unit': 'boolean'
        }
    D = np.diag(vals)
    try:
        P_inv = np.linalg.inv(P)
    except np.linalg.LinAlgError:
        P_inv = np.linalg.pinv(P)
    check = P @ D @ P_inv
    diag = abs(np.sum(np.diag(check) - np.diag(A))) < 1e-8
    return {
        'result': f'Diagonalizable: {diag}, D = {np.round(np.diag(D), 4).tolist()}',
        'details': {'matrix': matrix, 'diagonalizable': diag, 'P': P.tolist(), 'D': D.tolist(), 'P_inv': P_inv.tolist(), 'check': check.tolist()},
        'unit': 'boolean'
    }

def calc_spectral_radius(matrix: list = None) -> dict:
    """Compute spectral radius rho(A) = max|lambda|."""
    if matrix is None:
        matrix = [[2, 1], [1, 2]]
    A = np.array(matrix, dtype=float)
    vals = np.linalg.eigvals(A)
    rho = max(abs(v) for v in vals)
    return {
        'result': f'rho(A) = {rho:.6f}',
        'details': {'matrix': matrix, 'eigenvalues': vals.tolist(), 'spectral_radius': rho},
        'unit': 'number'
    }

# ==============================================================================
# QUADRATIC FORMS
# ==============================================================================

def calc_quadratic_form_matrix(coeffs: list = None) -> dict:
    """Express quadratic form as x^T A x. E.g., x^2 + 4xy + y^2 => A = [[1,2],[2,1]]."""
    if coeffs is None:
        coeffs = [1, 4, 1]
    a, b, c = coeffs
    A = np.array([[a, b / 2], [b / 2, c]])
    return {
        'result': f'Q(x,y) = {a}x^2 + {b}xy + {c}y^2, matrix A = {A.tolist()}',
        'details': {'coeffs': coeffs, 'matrix': A.tolist()},
        'unit': 'matrix'
    }

def calc_definiteness(matrix: list = None) -> dict:
    """Check definiteness using Sylvester's criterion (leading principal minors)."""
    if matrix is None:
        matrix = [[2, -1], [-1, 2]]
    A = np.array(matrix, dtype=float)
    if not np.allclose(A, A.T):
        return {
            'result': 'Error: Matrix must be symmetric for definiteness check',
            'details': {'matrix': matrix, 'error': 'not symmetric'},
            'unit': 'classification'
        }
    n = A.shape[0]
    minors = []
    for k in range(1, n + 1):
        minors.append(np.linalg.det(A[:k, :k]))
    all_positive = all(m > 0 for m in minors)
    signs_alternate = all(True if i == 0 else (minors[i] * ((-1) ** i) > 0 or abs(minors[i]) < 1e-12) for i in range(n))
    if all_positive:
        definiteness = 'positive definite'
    elif all(m >= 0 for m in minors) and any(abs(m) < 1e-10 for m in minors):
        definiteness = 'positive semidefinite'
    elif all(True if i == 0 else ((-1) ** i * minors[i] > 0 or abs(minors[i]) < 1e-12) for i in range(n)):
        definiteness = 'negative definite' if all(m != 0 for m in minors) else 'negative semidefinite'
    else:
        definiteness = 'indefinite'
    vals = np.linalg.eigvalsh(A)
    all_positive_vals = all(v > -1e-10 for v in vals) and any(v > 1e-10 for v in vals)
    return {
        'result': f'Matrix is {definiteness}. Leading minors: {minors}',
        'details': {'matrix': matrix, 'leading_minors': minors, 'eigenvalues': vals.tolist(), 'definiteness': definiteness},
        'unit': 'classification'
    }

def calc_diagonalize_quadratic(coeffs: list = None) -> dict:
    """Diagonalize quadratic form: find P such that P^T A P = D."""
    if coeffs is None:
        coeffs = [1, 4, 1]
    a, b, c = coeffs
    A = np.array([[a, b / 2], [b / 2, c]])
    vals, vecs = np.linalg.eigh(A)
    D = np.diag(vals)
    P = vecs
    eq = f'{vals[0]:.4f} * u^2 + {vals[1]:.4f} * v^2'
    return {
        'result': f'Diagonal form: {eq}',
        'details': {'coeffs': coeffs, 'A': A.tolist(), 'eigenvalues': vals.tolist(), 'D': D.tolist(), 'P': P.tolist()},
        'unit': 'expression'
    }

# ==============================================================================
# TENSOR BASICS
# ==============================================================================

def calc_tensor_product(v1: list = None, v2: list = None) -> dict:
    """Compute tensor (Kronecker/outer) product v1 tensor v2."""
    if v1 is None:
        v1 = [1, 2]
    if v2 is None:
        v2 = [3, 4, 5]
    v1_np = np.array(v1)
    v2_np = np.array(v2)
    T = np.outer(v1_np, v2_np)
    rank = np.linalg.matrix_rank(T)
    return {
        'result': f'v1 (x) v2 = {T.tolist()} (rank = {rank})',
        'details': {'v1': v1, 'v2': v2, 'tensor_product': T.tolist(), 'shape': T.shape, 'rank': rank},
        'unit': 'tensor'
    }

def calc_kronecker_product(A: list = None, B: list = None) -> dict:
    """Compute Kronecker product A kron B."""
    if A is None:
        A = [[1, 2], [3, 4]]
    if B is None:
        B = [[0, 5], [6, 7]]
    A_np = np.array(A)
    B_np = np.array(B)
    K = np.kron(A_np, B_np)
    return {
        'result': f'A kron B = {K.tolist()} (shape = {K.shape})',
        'details': {'A': A, 'B': B, 'kronecker': K.tolist(), 'shape': K.shape},
        'unit': 'tensor'
    }

def calc_tensor_contraction(tensor: list = None, indices: list = None) -> dict:
    """Contract a tensor over specified indices (trace for matrix)."""
    if tensor is None:
        tensor = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    T = np.array(tensor)
    if len(T.shape) == 2:
        contracted = np.trace(T)
        note = 'Matrix trace (contraction over both indices)'
    else:
        contracted = np.sum(T)
        note = 'Sum of all elements'
    return {
        'result': f'Tensor contraction = {contracted:.4f} ({note})',
        'details': {'tensor': tensor, 'shape': T.shape, 'contracted': contracted},
        'unit': 'number'
    }

def calc_cp_decomposition(tensor: list = None, rank: int = 2) -> dict:
    """Basic CP decomposition for a 2D matrix (SVD-based). Full CP for 3D is approximate."""
    if tensor is None:
        tensor = [[1, 2], [3, 4]]
    T = np.array(tensor)
    U, s, Vt = np.linalg.svd(T)
    components = []
    for r in range(min(rank, len(s))):
        components.append({
            'factor': round(s[r], 6),
            'u': U[:, r].tolist(),
            'v': Vt[r, :].tolist()
        })
    return {
        'result': f'CP decomposition (rank {rank} approximation): {len(components)} components',
        'details': {'tensor': tensor, 'rank': rank, 'components': components, 'singular_values': s.tolist()},
        'unit': 'decomposition'
    }

# ==============================================================================
# LINEAR SYSTEMS
# ==============================================================================

def calc_gaussian_elimination(A: list = None, b: list = None) -> dict:
    """Solve Ax = b using Gaussian elimination with partial pivoting."""
    if A is None:
        A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    if b is None:
        b = [8, -11, -3]
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n = len(b_np)
    Ab = np.hstack([A_np, b_np.reshape(-1, 1)])
    # Forward elimination
    for i in range(n):
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        pivot = Ab[i, i]
        if abs(pivot) < 1e-12:
            continue
        for j in range(i + 1, n):
            factor = Ab[j, i] / pivot
            Ab[j, i:] -= factor * Ab[i, i:]
    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:])) / Ab[i, i]
    check = A_np @ x
    residual = np.linalg.norm(check - b_np)
    return {
        'result': f'x = {np.round(x, 6).tolist()}',
        'details': {'A': A, 'b': b, 'solution': x.tolist(), 'residual': residual},
        'unit': 'vector'
    }

def calc_lu_solve(A: list = None, b: list = None) -> dict:
    """Solve Ax = b using LU decomposition."""
    if A is None:
        A = [[3, 2], [1, 4]]
    if b is None:
        b = [8, 6]
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    n = A_np.shape[0]
    L = np.eye(n)
    U = A_np.copy().astype(float)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(U[i, i]) < 1e-12:
                continue
            factor = U[j, i] / U[i, i]
            L[j, i] = factor
            U[j, i:] -= factor * U[i, i:]
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b_np[i] - np.dot(L[i, :i], y[:i])) / L[i, i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i + 1:], x[i + 1:])) / U[i, i]
    return {
        'result': f'x = {x.tolist()}',
        'details': {'A': A, 'b': b, 'solution': x.tolist(), 'L': L.tolist(), 'U': U.tolist()},
        'unit': 'vector'
    }

def calc_least_squares(A: list = None, b: list = None) -> dict:
    """Solve least squares problem min||Ax - b||_2 using normal equations A^T A x = A^T b."""
    if A is None:
        A = [[1, 1], [1, 2], [1, 3]]
    if b is None:
        b = [1, 2, 2]
    A_np = np.array(A, dtype=float)
    b_np = np.array(b, dtype=float)
    ATA = A_np.T @ A_np
    ATb = A_np.T @ b_np
    try:
        x = np.linalg.solve(ATA, ATb)
    except np.linalg.LinAlgError:
        x, residuals, rank, s = np.linalg.lstsq(A_np, b_np, rcond=None)
    residual = np.linalg.norm(A_np @ x - b_np)
    return {
        'result': f'x_hat = {np.round(x, 6).tolist()}, residual norm = {residual:.6f}',
        'details': {'A': A, 'b': b, 'solution': x.tolist(), 'residual_norm': residual, 'ATA': ATA.tolist(), 'ATb': ATb.tolist()},
        'unit': 'vector'
    }

def calc_pseudoinverse(matrix: list = None) -> dict:
    """Compute Moore-Penrose pseudoinverse A^+."""
    if matrix is None:
        matrix = [[1, 2], [3, 4], [5, 6]]
    A = np.array(matrix, dtype=float)
    pinv = np.linalg.pinv(A)
    check1 = A @ pinv @ A
    check2 = pinv @ A @ pinv
    rel_err1 = np.linalg.norm(check1 - A) / max(np.linalg.norm(A), 1e-12)
    rel_err2 = np.linalg.norm(check2 - pinv) / max(np.linalg.norm(pinv), 1e-12)
    return {
        'result': f'A^+ = {np.round(pinv, 4).tolist()} (shape = {pinv.shape})',
        'details': {'matrix': matrix, 'pseudoinverse': pinv.tolist(), 'errors': {'A*A^+*A ~ A': rel_err1, 'A^+*A*A^+ ~ A^+': rel_err2}},
        'unit': 'matrix'
    }

def calc_nullspace(matrix: list = None) -> dict:
    """Compute nullspace basis of A (vectors x such that Ax = 0)."""
    if matrix is None:
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    A = np.array(matrix, dtype=float)
    U, s, Vt = np.linalg.svd(A)
    tol = max(A.shape) * np.spacing(max(s)) if len(s) > 0 else 1e-12
    null_basis = [Vt[i, :] for i in range(len(s), Vt.shape[0])]
    if not null_basis:
        for i in range(len(s)):
            if s[i] < tol:
                null_basis.append(Vt[i, :])
    null_dim = len(null_basis)
    return {
        'result': f'Nullspace dimension = {null_dim}' + (f', basis vectors in details' if null_dim > 0 else ' (trivial nullspace)'),
        'details': {'matrix': matrix, 'singular_values': s.tolist(), 'nullspace_dimension': null_dim, 'nullspace_basis': [v.tolist() for v in null_basis]},
        'unit': 'vectors'
    }

def calc_column_space(matrix: list = None) -> dict:
    """Compute column space basis of A using SVD."""
    if matrix is None:
        matrix = [[1, 2], [3, 4], [5, 6]]
    A = np.array(matrix, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    tol = max(A.shape) * np.spacing(max(s)) if len(s) > 0 else 1e-12
    rank = sum(1 for v in s if v > tol)
    col_basis = [U[:, i] for i in range(rank)]
    return {
        'result': f'Column space dimension (rank) = {rank}',
        'details': {'matrix': matrix, 'singular_values': s.tolist(), 'rank': rank, 'column_basis': [v.tolist() for v in col_basis]},
        'unit': 'vectors'
    }

# ==============================================================================
# COMMANDS
# ==============================================================================

COMMANDS = {
    'det_2x2': {'func': calc_det_2x2, 'params': ['a', 'b', 'c', 'd'], 'desc': '2x2 determinant ad - bc'},
    'det_3x3': {'func': calc_det_3x3, 'params': ['matrix'], 'desc': '3x3 determinant via Sarrus'},
    'det_nxn': {'func': calc_det_nxn, 'params': ['matrix', 'method'], 'desc': 'nxn determinant (Laplace expansion or numpy)'},
    'det_properties': {'func': calc_det_properties, 'params': ['matrix'], 'desc': 'Determinant properties verification'},
    'matrix_add': {'func': calc_matrix_add, 'params': ['A', 'B'], 'desc': 'Matrix addition A + B'},
    'matrix_multiply': {'func': calc_matrix_multiply, 'params': ['A', 'B'], 'desc': 'Matrix multiplication A * B'},
    'matrix_scalar_mult': {'func': calc_matrix_scalar_mult, 'params': ['matrix', 'scalar'], 'desc': 'Scalar multiplication of matrix'},
    'matrix_transpose': {'func': calc_matrix_transpose, 'params': ['matrix'], 'desc': 'Matrix transpose A^T'},
    'matrix_trace': {'func': calc_matrix_trace, 'params': ['matrix'], 'desc': 'Matrix trace tr(A)'},
    'matrix_inverse': {'func': calc_matrix_inverse, 'params': ['matrix', 'method'], 'desc': 'Matrix inverse A^(-1)'},
    'rank': {'func': calc_rank, 'params': ['matrix'], 'desc': 'Matrix rank'},
    'condition_number': {'func': calc_condition_number, 'params': ['matrix'], 'desc': 'Matrix condition number'},
    'lu_decomposition': {'func': calc_lu_decomposition, 'params': ['matrix'], 'desc': 'LU decomposition A = L*U'},
    'qr_decomposition': {'func': calc_qr_decomposition, 'params': ['matrix'], 'desc': 'QR decomposition (Gram-Schmidt)'},
    'svd': {'func': calc_svd, 'params': ['matrix'], 'desc': 'Singular Value Decomposition'},
    'dot_product': {'func': calc_dot_product, 'params': ['v1', 'v2'], 'desc': 'Vector dot product'},
    'cross_product': {'func': calc_cross_product, 'params': ['v1', 'v2'], 'desc': 'Vector cross product (3D)'},
    'vector_norm': {'func': calc_vector_norm, 'params': ['v', 'norm_type'], 'desc': 'Vector norm L1/L2/Linf'},
    'angle_between_vectors': {'func': calc_angle_between_vectors, 'params': ['v1', 'v2'], 'desc': 'Angle between two vectors'},
    'projection': {'func': calc_projection, 'params': ['v', 'onto'], 'desc': 'Project vector v onto u'},
    'gram_schmidt': {'func': calc_gram_schmidt, 'params': ['vectors'], 'desc': 'Gram-Schmidt orthogonalization'},
    'basis_check': {'func': calc_basis_check, 'params': ['vectors'], 'desc': 'Check if vectors form a basis'},
    'char_polynomial': {'func': calc_char_polynomial, 'params': ['matrix'], 'desc': 'Characteristic polynomial'},
    'eigenvalues': {'func': calc_eigenvalues, 'params': ['matrix', 'method'], 'desc': 'Eigenvalues computation'},
    'eigenvectors': {'func': calc_eigenvectors, 'params': ['matrix'], 'desc': 'Eigenvalues and eigenvectors'},
    'diagonalization': {'func': calc_diagonalization, 'params': ['matrix'], 'desc': 'Matrix diagonalization P*D*P^(-1)'},
    'spectral_radius': {'func': calc_spectral_radius, 'params': ['matrix'], 'desc': 'Spectral radius rho(A)'},
    'quadratic_form_matrix': {'func': calc_quadratic_form_matrix, 'params': ['coeffs'], 'desc': 'Quadratic form to symmetric matrix'},
    'definiteness': {'func': calc_definiteness, 'params': ['matrix'], 'desc': "Matrix definiteness (Sylvester's criterion)"},
    'diagonalize_quadratic': {'func': calc_diagonalize_quadratic, 'params': ['coeffs'], 'desc': 'Diagonalize quadratic form'},
    'tensor_product': {'func': calc_tensor_product, 'params': ['v1', 'v2'], 'desc': 'Tensor/outer product v1 (x) v2'},
    'kronecker_product': {'func': calc_kronecker_product, 'params': ['A', 'B'], 'desc': 'Kronecker product A kron B'},
    'tensor_contraction': {'func': calc_tensor_contraction, 'params': ['tensor', 'indices'], 'desc': 'Tensor contraction'},
    'cp_decomposition': {'func': calc_cp_decomposition, 'params': ['tensor', 'rank'], 'desc': 'CP decomposition (rank approximation)'},
    'gaussian_elimination': {'func': calc_gaussian_elimination, 'params': ['A', 'b'], 'desc': 'Solve Ax=b via Gaussian elimination'},
    'lu_solve': {'func': calc_lu_solve, 'params': ['A', 'b'], 'desc': 'Solve Ax=b via LU decomposition'},
    'least_squares': {'func': calc_least_squares, 'params': ['A', 'b'], 'desc': 'Least squares solution'},
    'pseudoinverse': {'func': calc_pseudoinverse, 'params': ['matrix'], 'desc': 'Moore-Penrose pseudoinverse'},
    'nullspace': {'func': calc_nullspace, 'params': ['matrix'], 'desc': 'Nullspace basis of A'},
    'column_space': {'func': calc_column_space, 'params': ['matrix'], 'desc': 'Column space basis of A'},
}
