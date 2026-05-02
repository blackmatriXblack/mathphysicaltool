"""
AI/ML Mathematics - Computation Module
"""
import math

COMMANDS = {}

# ============================================================
# Matrix Calculus
# ============================================================

def calc_gradient_affine(A11: float = 1.0, A12: float = 0.0,
                         A21: float = 0.0, A22: float = 1.0,
                         b1: float = 1.0, b2: float = 2.0,
                         x1: float = 1.0, x2: float = 1.0) -> dict:
    """Gradient of f = ||Ax + b||^2: grad = 2 A^T (Ax + b)."""
    A = [[A11, A12], [A21, A22]]
    b = [b1, b2]
    x = [x1, x2]
    # Ax + b
    Axb = [A[0][0]*x[0] + A[0][1]*x[1] + b[0],
           A[1][0]*x[0] + A[1][1]*x[1] + b[1]]
    # A^T (Ax + b)
    grad = [2 * (A[0][0]*Axb[0] + A[1][0]*Axb[1]),
            2 * (A[0][1]*Axb[0] + A[1][1]*Axb[1])]
    f_val = Axb[0]**2 + Axb[1]**2
    return {
        'result': f'grad f at ({x1},{x2}) = [{grad[0]:.4f}, {grad[1]:.4f}]',
        'details': {
            'A': A, 'b': b, 'x': x,
            'f': f_val, 'gradient': grad,
            'formula': 'grad ||Ax+b||^2 = 2 A^T (Ax+b)'
        },
        'unit': 'dimensionless'
    }

def calc_hessian_quadratic(a: float = 1.0, b: float = 0.0, c: float = 1.0) -> dict:
    """Hessian of quadratic form f = ax^2 + 2b xy + cy^2. H = [[2a, 2b], [2b, 2c]]."""
    H = [[2*a, 2*b], [2*b, 2*c]]
    det = H[0][0]*H[1][1] - H[0][1]*H[1][0]
    if det > 0 and H[0][0] > 0:
        nature = 'positive definite (strict local minimum)'
    elif det > 0 and H[0][0] < 0:
        nature = 'negative definite (strict local maximum)'
    elif det < 0:
        nature = 'indefinite (saddle point)'
    else:
        nature = 'semi-definite'
    return {
        'result': f'Hessian: [[{H[0][0]}, {H[0][1]}], [{H[1][0]}, {H[1][1]}]], {nature}',
        'details': {
            'coefficients': {'a': a, 'b': b, 'c': c},
            'hessian': H, 'determinant': det,
            'nature': nature
        },
        'unit': 'dimensionless'
    }

def calc_jacobian_softmax(z1: float = 1.0, z2: float = 2.0, z3: float = 3.0) -> dict:
    """Jacobian of softmax: dS_i/dz_j = S_i(delta_ij - S_j)."""
    z = [z1, z2, z3]
    max_z = max(z)
    exp_z = [math.exp(zi - max_z) for zi in z]
    total = sum(exp_z)
    S = [e / total for e in exp_z]
    J = [[0.0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            delta = 1.0 if i == j else 0.0
            J[i][j] = S[i] * (delta - S[j])
    return {
        'result': f'Softmax: {[round(s, 4) for s in S]}, Jacobian tr = {sum(J[i][i] for i in range(3)):.4f}',
        'details': {
            'z': z, 'softmax_output': [round(s, 6) for s in S],
            'jacobian': [[round(v, 6) for v in row] for row in J],
            'formula': 'dS_i/dz_j = S_i (delta_ij - S_j)'
        },
        'unit': 'dimensionless'
    }

def calc_gradient_cross_entropy(logits: list = None, target_one_hot: list = None) -> dict:
    """grad of cross-entropy loss w.r.t. logits: grad = softmax(z) - y."""
    if logits is None:
        logits = [1.0, 2.0, 3.0]
    if target_one_hot is None:
        target_one_hot = [0.0, 0.0, 1.0]
    max_z = max(logits)
    exp_z = [math.exp(zi - max_z) for zi in logits]
    total = sum(exp_z)
    softmax_out = [e / total for e in exp_z]
    grad = [softmax_out[i] - target_one_hot[i] for i in range(len(logits))]
    # Loss
    eps = 1e-12
    loss = -sum(target_one_hot[i] * math.log(max(softmax_out[i], eps)) for i in range(len(logits)))
    return {
        'result': f'Cross-entropy loss = {loss:.6f}, grad = {[round(g, 4) for g in grad]}',
        'details': {
            'logits': logits, 'target': target_one_hot,
            'softmax': [round(s, 6) for s in softmax_out],
            'loss': loss, 'gradient': [round(g, 6) for g in grad],
            'formula': 'dL/dz_i = softmax(z)_i - y_i'
        },
        'unit': 'dimensionless'
    }

def calc_backprop_gradients(x: list = None, W1: list = None, W2: list = None,
                            y_true: list = None) -> dict:
    """Backpropagation gradients for a simple 2-layer network."""
    if x is None:
        x = [0.5, -0.3]
    if W1 is None:
        W1 = [[0.2, 0.4], [-0.1, 0.3]]
    if W2 is None:
        W2 = [[0.1, -0.2]]
    if y_true is None:
        y_true = [1.0]
    # Forward pass
    # Hidden layer: h = sigmoid(W1 @ x)
    z1 = [W1[0][0]*x[0] + W1[0][1]*x[1],
          W1[1][0]*x[0] + W1[1][1]*x[1]]
    h = [1/(1 + math.exp(-zi)) for zi in z1]
    # Output: y_pred = sigmoid(W2 @ h)
    z2 = [W2[0][0]*h[0] + W2[0][1]*h[1]]
    y_pred = [1/(1 + math.exp(-z2[0]))]
    # Binary cross-entropy loss
    eps = 1e-12
    loss = -(y_true[0]*math.log(max(y_pred[0], eps)) + (1-y_true[0])*math.log(max(1-y_pred[0], eps)))
    # Backprop
    dL_dy = [y_pred[0] - y_true[0]]
    dL_dz2 = [dL_dy[0]]
    dL_dW2 = [[dL_dz2[0]*h[0], dL_dz2[0]*h[1]]]
    dL_dh = [dL_dz2[0]*W2[0][0], dL_dz2[0]*W2[0][1]]
    dL_dz1 = [dL_dh[0]*h[0]*(1-h[0]), dL_dh[1]*h[1]*(1-h[1])]
    dL_dW1 = [[dL_dz1[0]*x[0], dL_dz1[0]*x[1]],
              [dL_dz1[1]*x[0], dL_dz1[1]*x[1]]]
    return {
        'result': f'Loss = {loss:.6f}, dL/dW1[0][0] = {dL_dW1[0][0]:.6f}',
        'details': {
            'input': x, 'hidden': [round(v, 6) for v in h],
            'output': round(y_pred[0], 6), 'loss': loss,
            'dL_dW1': [[round(v, 6) for v in row] for row in dL_dW1],
            'dL_dW2': [[round(v, 6) for v in row] for row in dL_dW2]
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Dimensionality Reduction
# ============================================================

def calc_pca(data: list = None) -> dict:
    """PCA: eigenvalues of covariance matrix and explained variance ratio."""
    if data is None:
        data = [[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [4.0, 8.0]]
    n = len(data)
    d = len(data[0])
    # Mean
    means = [sum(data[i][j] for i in range(n)) / n for j in range(d)]
    # Centered data
    centered = [[data[i][j] - means[j] for j in range(d)] for i in range(n)]
    # Covariance matrix: (1/(n-1)) Xc^T Xc
    cov = [[0.0] * d for _ in range(d)]
    for i in range(d):
        for j in range(d):
            cov[i][j] = sum(centered[k][i] * centered[k][j] for k in range(n)) / (n - 1)
    # 2x2 eigenvalue decomposition
    if d == 2:
        a, b, c = cov[0][0], cov[0][1], cov[1][1]
        trace = a + c
        det = a * c - b * b
        disc = trace*trace - 4*det
        if disc >= 0:
            sd = math.sqrt(disc)
            evals = [(trace + sd) / 2, (trace - sd) / 2]
        else:
            evals = [trace/2, trace/2]
        evals.sort(reverse=True)
    else:
        evals = [cov[0][0]]
    total_var = sum(evals)
    ratios = [e / total_var for e in evals] if total_var > 0 else [0]*len(evals)
    return {
        'result': f'Explained variance: PC1 = {ratios[0]:.4f}, PC2 = {ratios[1] if len(ratios)>1 else 0:.4f}',
        'details': {
            'data': data,
            'covariance_matrix': [[round(v, 6) for v in row] for row in cov],
            'eigenvalues': [round(e, 6) for e in evals],
            'explained_variance_ratio': [round(r, 6) for r in ratios]
        },
        'unit': 'dimensionless'
    }

def calc_lda(classes: list = None) -> dict:
    """Linear Discriminant Analysis: between-class and within-class scatter."""
    if classes is None:
        classes = {
            'class0': [[1.0, 2.0], [2.0, 3.0], [3.0, 3.0]],
            'class1': [[5.0, 5.0], [6.0, 5.0], [7.0, 6.0]]
        }
    # Overall mean
    all_data = []
    for pts in classes.values():
        all_data.extend(pts)
    n_total = len(all_data)
    d = len(all_data[0])
    overall_mean = [sum(p[j] for p in all_data) / n_total for j in range(d)]
    # Between-class scatter S_B
    S_B = [[0.0]*d for _ in range(d)]
    S_W = [[0.0]*d for _ in range(d)]
    for cls_name, pts in classes.items():
        n_k = len(pts)
        class_mean = [sum(p[j] for p in pts) / n_k for j in range(d)]
        # S_B
        for i in range(d):
            for j in range(d):
                S_B[i][j] += n_k * (class_mean[i] - overall_mean[i]) * (class_mean[j] - overall_mean[j])
                # S_W: sum of outer products of (x_k - mean_k)
                for pt in pts:
                    S_W[i][j] += (pt[i] - class_mean[i]) * (pt[j] - class_mean[j])
    # Fisher criterion: max w^T S_B w / w^T S_W w
    # Generalized eigenvalue: S_W^{-1} S_B w = lambda w
    # For 2x2, analytical solution
    if d == 2:
        det_W = S_W[0][0]*S_W[1][1] - S_W[0][1]*S_W[1][0]
        if abs(det_W) > 1e-10:
            inv_SW = [[S_W[1][1]/det_W, -S_W[0][1]/det_W],
                      [-S_W[1][0]/det_W, S_W[0][0]/det_W]]
            prod = [[inv_SW[0][0]*S_B[0][0] + inv_SW[0][1]*S_B[1][0],
                     inv_SW[0][0]*S_B[0][1] + inv_SW[0][1]*S_B[1][1]],
                    [inv_SW[1][0]*S_B[0][0] + inv_SW[1][1]*S_B[1][0],
                     inv_SW[1][0]*S_B[0][1] + inv_SW[1][1]*S_B[1][1]]]
            trace = prod[0][0] + prod[1][1]
            det = prod[0][0]*prod[1][1] - prod[0][1]*prod[1][0]
            disc = max(0, trace*trace - 4*det)
            evals = [(trace + math.sqrt(disc))/2, (trace - math.sqrt(disc))/2]
            evals.sort(reverse=True)
        else:
            evals = [0, 0]
    else:
        evals = [0]
    return {
        'result': f'LDA: leading eigenvalue = {evals[0]:.4f}',
        'details': {
            'classes': {k: len(v) for k, v in classes.items()},
            'S_B': [[round(v, 6) for v in row] for row in S_B],
            'S_W': [[round(v, 6) for v in row] for row in S_W],
            'eigenvalues': [round(e, 6) for e in evals]
        },
        'unit': 'dimensionless'
    }

def calc_tsne_cost(y: list = None) -> dict:
    """t-SNE cost function: KL divergence between P and Q distributions (simplified)."""
    if y is None:
        y = [[0.1, 0.2], [0.3, 0.1], [0.0, 0.4]]
    n = len(y)
    # Compute pairwise affinities Q in low-dim space
    Q = [[0.0]*n for _ in range(n)]
    dist_sq = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                d2 = sum((y[i][k] - y[j][k])**2 for k in range(len(y[0])))
                dist_sq[i][j] = d2
                Q[i][j] = 1.0 / (1.0 + d2)
    # Normalize Q
    for i in range(n):
        row_sum = sum(Q[i][j] for j in range(n) if j != i)
        if row_sum > 0:
            for j in range(n):
                if j != i:
                    Q[i][j] /= row_sum
    # Simulate P (high-dim) as uniform (simplified)
    P_ij = 1.0 / (n * (n - 1)) if n > 1 else 0
    cost = 0.0
    for i in range(n):
        for j in range(n):
            if i != j:
                if Q[i][j] > 1e-15 and P_ij > 0:
                    cost += P_ij * math.log(P_ij / Q[i][j])
    return {
        'result': f't-SNE cost (KL div) = {cost:.6f}',
        'details': {
            'n_points': n,
            'cost': cost,
            'pairwise_Q': [[round(v, 6) for v in row[:3]] for row in Q[:3]],
            'description': 'KL div between high-dim P and low-dim Q'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Kernels
# ============================================================

def calc_kernel_linear(x: list = None, y: list = None) -> dict:
    """Linear kernel: K(x,y) = x^T y."""
    if x is None:
        x = [1.0, 2.0, 3.0]
    if y is None:
        y = [4.0, 5.0, 6.0]
    K = sum(x[i]*y[i] for i in range(len(x)))
    return {
        'result': f'K_linear(x,y) = {K:.6f}',
        'details': {'x': x, 'y': y, 'kernel': 'linear', 'K': K, 'formula': 'x^T y'},
        'unit': 'dimensionless'
    }

def calc_kernel_polynomial(x: list = None, y: list = None, c: float = 1.0, d: int = 2) -> dict:
    """Polynomial kernel: K(x,y) = (x^T y + c)^d."""
    if x is None:
        x = [1.0, 2.0]
    if y is None:
        y = [3.0, 4.0]
    dot = sum(x[i]*y[i] for i in range(len(x)))
    K = (dot + c) ** d
    return {
        'result': f'K_poly(x,y) = {K:.6f}',
        'details': {'x': x, 'y': y, 'c': c, 'd': d, 'kernel': 'polynomial',
                    'K': K, 'formula': f'(x^T y + {c})^{d}'},
        'unit': 'dimensionless'
    }

def calc_kernel_rbf(x: list = None, y: list = None, gamma: float = 1.0) -> dict:
    """RBF/Gaussian kernel: K(x,y) = exp(-gamma ||x-y||^2)."""
    if x is None:
        x = [0.0, 0.0]
    if y is None:
        y = [1.0, 1.0]
    dist_sq = sum((x[i] - y[i])**2 for i in range(len(x)))
    K = math.exp(-gamma * dist_sq)
    return {
        'result': f'K_rbf(x,y) = {K:.6f}',
        'details': {'x': x, 'y': y, 'gamma': gamma, '||x-y||^2': dist_sq,
                    'kernel': 'RBF', 'K': K, 'formula': 'exp(-gamma ||x-y||^2)'},
        'unit': 'dimensionless'
    }

def calc_kernel_matrix(data: list = None, kernel_type: str = 'rbf', gamma: float = 1.0) -> dict:
    """Compute kernel (Gram) matrix for dataset."""
    if data is None:
        data = [[0, 0], [1, 1], [2, 2], [3, 3]]
    n = len(data)
    K = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if kernel_type == 'linear':
                K[i][j] = sum(data[i][k]*data[j][k] for k in range(len(data[i])))
            elif kernel_type == 'rbf':
                dist_sq = sum((data[i][k]-data[j][k])**2 for k in range(len(data[i])))
                K[i][j] = math.exp(-gamma * dist_sq)
            elif kernel_type == 'polynomial':
                d = 2
                c = 1.0
                dot = sum(data[i][k]*data[j][k] for k in range(len(data[i])))
                K[i][j] = (dot + c) ** d
    # Check Mercer: symmetric positive semi-definite
    is_symmetric = all(abs(K[i][j] - K[j][i]) < 1e-10 for i in range(n) for j in range(n))
    # Simple test: all eigenvalues >= 0 (for 2x2 sub-blocks)
    # Just report symmetry for now
    return {
        'result': f'Kernel matrix ({kernel_type}), symmetric: {is_symmetric}',
        'details': {
            'kernel': kernel_type, 'data': data,
            'kernel_matrix': [[round(v, 4) for v in row] for row in K],
            'symmetric': is_symmetric
        },
        'unit': 'dimensionless'
    }

def calc_mercer_check(K: list = None) -> dict:
    """Check if a 3x3 matrix satisfies Mercer condition (PSD)."""
    if K is None:
        K = [[2.0, 1.0, 0.5], [1.0, 2.0, 0.8], [0.5, 0.8, 2.0]]
    # Check leading principal minors
    minors = []
    for k in range(1, len(K) + 1):
        sub = [[K[i][j] for j in range(k)] for i in range(k)]
        if k == 1:
            det = sub[0][0]
        elif k == 2:
            det = sub[0][0]*sub[1][1] - sub[0][1]*sub[1][0]
        else:
            det = (sub[0][0]*(sub[1][1]*sub[2][2] - sub[1][2]*sub[2][1]) -
                   sub[0][1]*(sub[1][0]*sub[2][2] - sub[1][2]*sub[2][0]) +
                   sub[0][2]*(sub[1][0]*sub[2][1] - sub[1][1]*sub[2][0]))
        minors.append(det)
    psd = all(m >= -1e-10 for m in minors)
    return {
        'result': f'Mercer condition: {"valid PSD" if psd else "NOT PSD"}',
        'details': {
            'kernel_matrix': K,
            'leading_principal_minors': [round(m, 6) for m in minors],
            'psd': psd
        },
        'unit': 'dimensionless'
    }

# ============================================================
# SVM
# ============================================================

def calc_hinge_loss(scores: list = None, labels: list = None) -> dict:
    """Hinge loss: L = max(0, 1 - y_i * score_i)."""
    if scores is None:
        scores = [0.8, -0.3, 1.2, -0.5]
    if labels is None:
        labels = [1, -1, 1, -1]
    losses = [max(0, 1 - labels[i]*scores[i]) for i in range(len(scores))]
    total_loss = sum(losses) / len(losses)
    return {
        'result': f'Hinge loss = {total_loss:.6f}',
        'details': {
            'scores': scores, 'labels': labels,
            'per_sample_loss': [round(l, 6) for l in losses],
            'average_loss': total_loss,
            'formula': 'max(0, 1 - y_i * score_i)'
        },
        'unit': 'dimensionless'
    }

def calc_svm_margin(w: list = None, x_support: list = None) -> dict:
    """Calculate margin for SVM: margin = 2 / ||w||."""
    if w is None:
        w = [1.0, 1.0]
    w_norm = math.sqrt(sum(wi*wi for wi in w))
    margin = 2.0 / w_norm if w_norm > 0 else 0
    if x_support is None:
        x_support = [2.0, 1.0]
    decision_val = sum(w[i]*x_support[i] for i in range(len(w)))
    return {
        'result': f'Margin = {margin:.6f}, Decision value = {decision_val:.6f}',
        'details': {
            'w': w, '||w||': w_norm,
            'margin': margin,
            'x_support': x_support,
            'decision_value': decision_val,
            'formula': 'margin = 2/||w||'
        },
        'unit': 'dimensionless'
    }

def calc_support_vectors(data: list = None, labels: list = None,
                         w: list = None, b: float = 0.0) -> dict:
    """Identify support vectors: points with |w·x + b - y| < epsilon."""
    if data is None:
        data = [[1, 1], [2, 1], [0, 2], [-1, -1], [-2, -2]]
    if labels is None:
        labels = [1, 1, 1, -1, -1]
    if w is None:
        w = [0.5, 0.5]
    sv_indices = []
    eps = 1e-6
    for i, (x, y) in enumerate(zip(data, labels)):
        margin = y * (sum(w[j]*x[j] for j in range(len(w))) + b)
        if abs(margin - 1.0) < 0.1:
            sv_indices.append(i)
    return {
        'result': f'{len(sv_indices)} support vectors found',
        'details': {
            'data': data, 'labels': labels,
            'w': w, 'b': b,
            'support_vector_indices': sv_indices,
            'sv_data': [data[i] for i in sv_indices]
        },
        'unit': 'dimensionless'
    }

def calc_svm_primal_dual(w: list = None, b: float = 0.0,
                         X: list = None, y: list = None) -> dict:
    """Compute SVM primal and dual objective values."""
    if w is None:
        w = [0.5, 0.5]
    if X is None:
        X = [[1, 1], [2, 1], [-1, -1]]
    if y is None:
        y = [1, 1, -1]
    # Primal: 1/2 ||w||^2 + C * sum hinge_loss
    C = 1.0
    w_norm_sq = sum(wi*wi for wi in w)
    primal = 0.5 * w_norm_sq
    for i in range(len(X)):
        xi = sum(w[j]*X[i][j] for j in range(len(w))) + b
        loss = max(0, 1 - y[i]*xi)
        primal += C * loss
    # Dual (simplified, assuming alpha solved)
    # W(alpha) = sum alpha_i - 1/2 sum_{i,j} alpha_i alpha_j y_i y_j K(x_i, x_j)
    alphas = [0.1, 0.15, 0.25]
    dual = sum(alphas)
    for i in range(len(X)):
        for j in range(len(X)):
            K_ij = sum(X[i][k]*X[j][k] for k in range(len(X[i])))
            dual -= 0.5 * alphas[i] * alphas[j] * y[i] * y[j] * K_ij
    return {
        'result': f'Primal = {primal:.6f}, Dual = {dual:.6f}, gap = {primal - dual:.6f}',
        'details': {
            'w': w, 'b': b, 'C': C,
            'primal_objective': primal,
            'dual_objective': dual,
            'duality_gap': primal - dual
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Clustering
# ============================================================

def calc_kmeans(data: list = None, k: int = 2, max_iter: int = 20) -> dict:
    """K-means clustering (Lloyd's algorithm)."""
    if data is None:
        data = [[1.0, 2.0], [1.5, 1.8], [5.0, 8.0], [8.0, 8.0], [1.0, 0.6],
                [9.0, 11.0], [8.0, 2.0], [10.0, 2.0], [9.0, 3.0]]
    n = len(data)
    d = len(data[0])
    # Initialize centroids randomly
    import random
    centroids = [data[i][:] for i in random.sample(range(n), k)]
    clusters = [0] * n
    for iteration in range(max_iter):
        # Assign
        changed = False
        for i in range(n):
            min_dist = float('inf')
            best_c = 0
            for c in range(k):
                dist = sum((data[i][j] - centroids[c][j])**2 for j in range(d))
                if dist < min_dist:
                    min_dist = dist
                    best_c = c
            if clusters[i] != best_c:
                changed = True
                clusters[i] = best_c
        if not changed:
            break
        # Update centroids
        centroids = [[0.0]*d for _ in range(k)]
        counts = [0] * k
        for i in range(n):
            c = clusters[i]
            for j in range(d):
                centroids[c][j] += data[i][j]
            counts[c] += 1
        for c in range(k):
            if counts[c] > 0:
                for j in range(d):
                    centroids[c][j] /= counts[c]
    return {
        'result': f'K-means: {k} clusters, {iteration+1} iterations',
        'details': {
            'k': k, 'iterations': iteration + 1,
            'centroids': [[round(v, 6) for v in c] for c in centroids],
            'cluster_assignments': clusters,
            'cluster_sizes': [clusters.count(i) for i in range(k)]
        },
        'unit': 'dimensionless'
    }

def calc_silhouette_score(data: list = None, labels: list = None) -> dict:
    """Silhouette score for clustering evaluation."""
    if data is None:
        data = [[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6],
                [9, 11], [8, 2], [10, 2], [9, 3]]
    if labels is None:
        labels = [0, 0, 1, 1, 0, 1, 2, 2, 2]
    n = len(data)
    # For each point compute a(i) and b(i)
    silhouettes = []
    for i in range(n):
        # a(i): avg distance to points in same cluster
        same_cluster = [j for j in range(n) if labels[j] == labels[i] and j != i]
        if not same_cluster:
            a_i = 0
        else:
            a_i = sum(math.sqrt(sum((data[i][k]-data[j][k])**2 for k in range(len(data[i]))))
                      for j in same_cluster) / len(same_cluster)
        # b(i): min avg distance to points in other cluster
        b_i = float('inf')
        unique_labels = set(l for l in labels if l != labels[i])
        for other_label in unique_labels:
            other_cluster = [j for j in range(n) if labels[j] == other_label]
            avg_dist = sum(math.sqrt(sum((data[i][k]-data[j][k])**2 for k in range(len(data[i]))))
                           for j in other_cluster) / len(other_cluster)
            if avg_dist < b_i:
                b_i = avg_dist
        if max(a_i, b_i) > 0:
            s = (b_i - a_i) / max(a_i, b_i)
        else:
            s = 0
        silhouettes.append(s)
    avg_s = sum(silhouettes) / n if n > 0 else 0
    return {
        'result': f'Silhouette score = {avg_s:.4f} (range [-1, 1])',
        'details': {
            'per_point_scores': [round(s, 4) for s in silhouettes],
            'average_score': round(avg_s, 6),
            'interpretation': '1=well separated, 0=overlapping, -1=misclassified'
        },
        'unit': 'dimensionless'
    }

def calc_hierarchical_clustering(data: list = None, linkage: str = 'single') -> dict:
    """Hierarchical clustering with single/complete/average linkage."""
    if data is None:
        data = [[1, 2], [2, 3], [3, 1], [7, 8], [8, 7], [9, 8]]
    n = len(data)
    # Distance matrix
    dist_matrix = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist_matrix[i][j] = math.sqrt(sum((data[i][k]-data[j][k])**2 for k in range(len(data[i]))))
    # Initialize clusters
    clusters = [[i] for i in range(n)]
    merge_history = []
    # Merge n-1 times
    for step in range(n - 1):
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                if linkage == 'single':
                    d = min(dist_matrix[a][b] for a in clusters[i] for b in clusters[j])
                elif linkage == 'complete':
                    d = max(dist_matrix[a][b] for a in clusters[i] for b in clusters[j])
                else:  # average
                    pairs = [(a, b) for a in clusters[i] for b in clusters[j]]
                    d = sum(dist_matrix[a][b] for a, b in pairs) / len(pairs)
                if d < min_dist:
                    min_dist = d
                    merge_i, merge_j = i, j
        merge_history.append({
            'step': step, 'merge': (merge_i, merge_j),
            'distance': round(min_dist, 4),
            'new_cluster': clusters[merge_i] + clusters[merge_j]
        })
        clusters[merge_i] = clusters[merge_i] + clusters[merge_j]
        clusters.pop(merge_j)
        if len(clusters) == 1:
            break
    return {
        'result': f'Hierarchical ({linkage} linkage): {n} points merged into 1 cluster',
        'details': {
            'linkage': linkage, 'n_points': n,
            'merge_history': merge_history,
            'initial_data': data
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Neural Network Math
# ============================================================

def calc_sigmoid(x: float = 0.5) -> dict:
    """Sigmoid activation: sigma(x) = 1/(1 + e^{-x})."""
    s = 1.0 / (1.0 + math.exp(-x))
    d = s * (1 - s)
    return {
        'result': f'sigma({x}) = {s:.6f}',
        'details': {'x': x, 'sigmoid': s, 'derivative': d},
        'unit': 'dimensionless'
    }

def calc_relu(x: float = -0.5) -> dict:
    """ReLU activation: max(0, x)."""
    r = max(0.0, x)
    d = 1.0 if x > 0 else 0.0
    return {
        'result': f'ReLU({x}) = {r}',
        'details': {'x': x, 'relu': r, 'derivative': d},
        'unit': 'dimensionless'
    }

def calc_tanh_activation(x: float = 0.5) -> dict:
    """Tanh activation: tanh(x) = (e^x - e^{-x})/(e^x + e^{-x})."""
    t = math.tanh(x)
    d = 1 - t*t
    return {
        'result': f'tanh({x}) = {t:.6f}',
        'details': {'x': x, 'tanh': t, 'derivative': d},
        'unit': 'dimensionless'
    }

def calc_softmax(logits: list = None) -> dict:
    """Softmax: s_i = exp(z_i) / sum exp(z_j)."""
    if logits is None:
        logits = [1.0, 2.0, 3.0]
    max_z = max(logits)
    exp_z = [math.exp(zi - max_z) for zi in logits]
    total = sum(exp_z)
    s = [e / total for e in exp_z]
    return {
        'result': f'Softmax: {[round(v, 4) for v in s]}',
        'details': {
            'logits': logits, 'softmax_output': [round(v, 6) for v in s],
            'sum_check': sum(s)
        },
        'unit': 'dimensionless'
    }

def calc_forward_pass_2layer(x: list = None, W1: list = None, W2: list = None,
                             b1: list = None, b2: list = None) -> dict:
    """Forward pass through a 2-layer neural network."""
    if x is None:
        x = [0.5, -0.3]
    if W1 is None:
        W1 = [[0.2, 0.4], [-0.1, 0.3]]
    if b1 is None:
        b1 = [0.1, -0.2]
    if W2 is None:
        W2 = [[0.5, -0.1]]
    if b2 is None:
        b2 = [0.3]
    # Layer 1
    z1 = [sum(W1[i][j]*x[j] for j in range(len(x))) + b1[i] for i in range(len(W1))]
    h = [1/(1 + math.exp(-zi)) for zi in z1]  # sigmoid
    # Layer 2
    z2 = [sum(W2[i][j]*h[j] for j in range(len(h))) + b2[i] for i in range(len(W2))]
    y_pred = [1/(1 + math.exp(-zi)) for zi in z2]  # sigmoid output
    return {
        'result': f'Prediction: {[round(v, 4) for v in y_pred]}',
        'details': {
            'input': x,
            'hidden_z1': [round(v, 6) for v in z1],
            'hidden_h': [round(v, 6) for v in h],
            'output_z2': [round(v, 6) for v in z2],
            'output_pred': [round(v, 6) for v in y_pred]
        },
        'unit': 'dimensionless'
    }

def calc_loss_functions(pred: list = None, target: list = None) -> dict:
    """Compute MSE and Cross-Entropy loss."""
    if pred is None:
        pred = [0.7, 0.2, 0.1]
    if target is None:
        target = [1.0, 0.0, 0.0]
    # MSE
    mse = sum((pred[i] - target[i])**2 for i in range(len(pred))) / len(pred)
    # Cross-entropy
    eps = 1e-12
    ce = -sum(target[i] * math.log(max(pred[i], eps)) for i in range(len(pred)))
    return {
        'result': f'MSE = {mse:.6f}, Cross-Entropy = {ce:.6f}',
        'details': {
            'prediction': pred, 'target': target,
            'MSE': mse, 'Cross_Entropy': ce
        },
        'unit': 'dimensionless'
    }

def calc_weight_update(w: float = 0.5, grad: float = 0.3, lr: float = 0.01) -> dict:
    """Weight update rule: w_new = w - lr * grad."""
    w_new = w - lr * grad
    return {
        'result': f'w: {w} -> {w_new:.6f}',
        'details': {
            'w_old': w, 'gradient': grad, 'learning_rate': lr,
            'w_new': w_new, 'update': f'w_new = w - {lr} * grad'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Probability Graphs
# ============================================================

def calc_bayesian_joint(joint_probs: dict = None) -> dict:
    """Compute joint probability from Bayesian network factorization."""
    if joint_probs is None:
        joint_probs = {'P(A)': 0.3, 'P(B|A)': 0.8, 'P(B|~A)': 0.2,
                       'P(C|A)': 0.7, 'P(C|~A)': 0.1}
    PA = joint_probs.get('P(A)', 0.3)
    PBgA = joint_probs.get('P(B|A)', 0.8)
    PBgnA = joint_probs.get('P(B|~A)', 0.2)
    PCgA = joint_probs.get('P(C|A)', 0.7)
    PCgnA = joint_probs.get('P(C|~A)', 0.1)
    P_ABC = PA * PBgA * PCgA
    P_nABC = (1-PA) * PBgnA * PCgnA
    P_ABnC = PA * PBgA * (1-PCgA)
    P_nABnC = (1-PA) * PBgnA * (1-PCgnA)
    P_AnBC = PA * (1-PBgA) * PCgA
    P_nAnBC = (1-PA) * (1-PBgnA) * PCgnA
    P_AnBnC = PA * (1-PBgA) * (1-PCgA)
    P_nAnBnC = (1-PA) * (1-PBgnA) * (1-PCgnA)
    total = P_ABC + P_nABC + P_ABnC + P_nABnC + P_AnBC + P_nAnBC + P_AnBnC + P_nAnBnC
    return {
        'result': f'P(A,B,C) = {P_ABC:.6f}, total = {total:.6f}',
        'details': {
            'joint_probabilities': {
                'P(A,B,C)': P_ABC, 'P(~A,B,C)': P_nABC,
                'P(A,B,~C)': P_ABnC, 'P(~A,B,~C)': P_nABnC,
                'P(A,~B,C)': P_AnBC, 'P(~A,~B,C)': P_nAnBC,
                'P(A,~B,~C)': P_AnBnC, 'P(~A,~B,~C)': P_nAnBnC
            },
            'normalization_check': total
        },
        'unit': 'dimensionless'
    }

def calc_variable_elimination(A_prob: float = 0.3, B_given_A: float = 0.7,
                              B_given_notA: float = 0.1) -> dict:
    """Variable elimination for simple 2-node Bayesian network."""
    # P(B) = P(B|A)P(A) + P(B|~A)P(~A)
    PB = B_given_A * A_prob + B_given_notA * (1 - A_prob)
    return {
        'result': f'P(B) = {PB:.6f} (by summing out A)',
        'details': {
            'P(A)': A_prob, 'P(B|A)': B_given_A,
            'P(B|~A)': B_given_notA, 'P(B)': PB,
            'method': f'P(B) = P(B|A)P(A) + P(B|~A)P(~A)'
        },
        'unit': 'dimensionless'
    }

def calc_markov_blanket() -> dict:
    """Describe Markov blanket of node X in Bayesian network."""
    return {
        'result': 'Markov blanket = parents + children + children\'s other parents',
        'details': {
            'definition': 'Minimal set of nodes that makes X independent of the rest',
            'components': {
                'parents': 'Nodes with arcs to X',
                'children': 'Nodes with arcs from X',
                'co_parents': 'Other parents of X\'s children'
            },
            'property': 'P(X | MB(X), rest) = P(X | MB(X))'
        },
        'unit': 'dimensionless'
    }

# ============================================================
# Information Theory
# ============================================================

def calc_entropy(probs: list = None) -> dict:
    """Shannon entropy H(X) = -sum p(x) log2 p(x)."""
    if probs is None:
        probs = [0.5, 0.25, 0.25]
    eps = 1e-15
    H = -sum(p * math.log2(max(p, eps)) for p in probs)
    return {
        'result': f'H(X) = {H:.6f} bits',
        'details': {
            'probabilities': probs, 'entropy_bits': H,
            'max_possible': math.log2(len(probs)),
            'efficiency': H / math.log2(len(probs)) if len(probs) > 1 else 1
        },
        'unit': 'bits'
    }

def calc_joint_entropy(joint_probs: list = None) -> dict:
    """Joint entropy H(X,Y) = -sum p(x,y) log2 p(x,y)."""
    if joint_probs is None:
        joint_probs = [[0.4, 0.1], [0.2, 0.3]]
    flat = []
    for row in joint_probs:
        flat.extend(row)
    eps = 1e-15
    H = -sum(p * math.log2(max(p, eps)) for p in flat if p > 0)
    return {
        'result': f'H(X,Y) = {H:.6f} bits',
        'details': {
            'joint_probs': joint_probs,
            'joint_entropy_bits': H
        },
        'unit': 'bits'
    }

def calc_conditional_entropy(P_X: list = None, P_YgivenX: list = None) -> dict:
    """H(Y|X) = sum P(x) * H(Y|X=x)."""
    if P_X is None:
        P_X = [0.6, 0.4]
    if P_YgivenX is None:
        P_YgivenX = [[0.9, 0.1], [0.3, 0.7]]
    H_YgX = 0.0
    for i, px in enumerate(P_X):
        eps = 1e-15
        H_i = -sum(py * math.log2(max(py, eps)) for py in P_YgivenX[i] if py > 0)
        H_YgX += px * H_i
    return {
        'result': f'H(Y|X) = {H_YgX:.6f} bits',
        'details': {
            'P_X': P_X, 'P_Y_given_X': P_YgivenX,
            'conditional_entropy': H_YgX
        },
        'unit': 'bits'
    }

def calc_mutual_information(P_X: list = None, P_Y: list = None,
                            P_XY: list = None) -> dict:
    """I(X;Y) = sum p(x,y) log2(p(x,y)/(p(x)p(y)))."""
    if P_X is None:
        P_X = [0.6, 0.4]
    if P_Y is None:
        P_Y = [0.7, 0.3]
    if P_XY is None:
        P_XY = [[0.5, 0.1], [0.2, 0.2]]
    I = 0.0
    eps = 1e-15
    for i in range(len(P_X)):
        for j in range(len(P_Y)):
            if P_XY[i][j] > 0 and P_X[i] > 0 and P_Y[j] > 0:
                I += P_XY[i][j] * math.log2(max(P_XY[i][j], eps) / (P_X[i] * P_Y[j]))
    # Also compute from entropies
    H_X = -sum(p * math.log2(max(p, eps)) for p in P_X)
    flat_probs = []
    for i in range(len(P_X)):
        for j in range(len(P_Y)):
            flat_probs.append(P_XY[i][j])
    H_XY = -sum(p * math.log2(max(p, eps)) for p in flat_probs if p > 0)
    H_Y = -sum(p * math.log2(max(p, eps)) for p in P_Y)
    return {
        'result': f'I(X;Y) = {I:.6f} bits',
        'details': {
            'I_X_Y': I,
            'H_X': H_X, 'H_Y': H_Y, 'H_XY': H_XY,
            'I_from_H': H_X + H_Y - H_XY,
            'relationship': 'I(X;Y) = H(X) + H(Y) - H(X,Y) = H(X) - H(X|Y)'
        },
        'unit': 'bits'
    }

def calc_kl_divergence(P: list = None, Q: list = None) -> dict:
    """KL divergence D_KL(P||Q) = sum P(i) * log(P(i)/Q(i))."""
    if P is None:
        P = [0.5, 0.3, 0.2]
    if Q is None:
        Q = [0.33, 0.33, 0.34]
    eps = 1e-15
    D = 0.0
    for i in range(len(P)):
        if P[i] > 0 and Q[i] > 0:
            D += P[i] * math.log2(P[i] / Q[i])
    return {
        'result': f'D_KL(P||Q) = {D:.6f} bits',
        'details': {
            'P': P, 'Q': Q,
            'KL_divergence': D,
            'properties': 'D_KL >= 0, asymmetric (D_KL(P||Q) != D_KL(Q||P))'
        },
        'unit': 'bits'
    }

def calc_cross_entropy_info(P: list = None, Q: list = None) -> dict:
    """Cross-entropy H(P,Q) = -sum P(i) log Q(i)."""
    if P is None:
        P = [1.0, 0.0, 0.0]
    if Q is None:
        Q = [0.7, 0.2, 0.1]
    eps = 1e-15
    H_PQ = -sum(P[i] * math.log2(max(Q[i], eps)) for i in range(len(P)))
    H_P = -sum(p * math.log2(max(p, eps)) for p in P if p > 0)
    D_KL = H_PQ - H_P
    return {
        'result': f'H(P,Q) = {H_PQ:.6f} bits, D_KL = {D_KL:.6f}',
        'details': {
            'P': P, 'Q': Q,
            'cross_entropy': H_PQ,
            'entropy_H_P': H_P,
            'KL_divergence': D_KL,
            'relationship': 'H(P,Q) = H(P) + D_KL(P||Q)'
        },
        'unit': 'bits'
    }


# ============================================================
# COMMANDS Registry
# ============================================================

COMMANDS = {
    'gradient_affine': {'func': calc_gradient_affine, 'params': ['A11', 'A12', 'A21', 'A22', 'b1', 'b2', 'x1', 'x2'], 'desc': 'Gradient of ||Ax+b||^2'},
    'hessian_quadratic': {'func': calc_hessian_quadratic, 'params': ['a', 'b', 'c'], 'desc': 'Hessian of quadratic form'},
    'jacobian_softmax': {'func': calc_jacobian_softmax, 'params': ['z1', 'z2', 'z3'], 'desc': 'Jacobian of softmax'},
    'gradient_cross_entropy': {'func': calc_gradient_cross_entropy, 'params': ['logits', 'target_one_hot'], 'desc': 'Gradient of cross-entropy loss'},
    'backprop_gradients': {'func': calc_backprop_gradients, 'params': ['x', 'W1', 'W2', 'y_true'], 'desc': 'Backprop for 2-layer network'},
    'pca': {'func': calc_pca, 'params': ['data'], 'desc': 'PCA eigenvalues and variance ratios'},
    'lda': {'func': calc_lda, 'params': ['classes'], 'desc': 'LDA between/within-class scatter'},
    'tsne_cost': {'func': calc_tsne_cost, 'params': ['y'], 'desc': 't-SNE cost (KL divergence)'},
    'kernel_linear': {'func': calc_kernel_linear, 'params': ['x', 'y'], 'desc': 'Linear kernel K = x^T y'},
    'kernel_polynomial': {'func': calc_kernel_polynomial, 'params': ['x', 'y', 'c', 'd'], 'desc': 'Polynomial kernel (x^T y + c)^d'},
    'kernel_rbf': {'func': calc_kernel_rbf, 'params': ['x', 'y', 'gamma'], 'desc': 'RBF kernel exp(-gamma||x-y||^2)'},
    'kernel_matrix': {'func': calc_kernel_matrix, 'params': ['data', 'kernel_type', 'gamma'], 'desc': 'Kernel (Gram) matrix'},
    'mercer_check': {'func': calc_mercer_check, 'params': ['K'], 'desc': 'Check Mercer condition (PSD)'},
    'hinge_loss': {'func': calc_hinge_loss, 'params': ['scores', 'labels'], 'desc': 'SVM hinge loss'},
    'svm_margin': {'func': calc_svm_margin, 'params': ['w', 'x_support'], 'desc': 'SVM margin = 2/||w||'},
    'support_vectors': {'func': calc_support_vectors, 'params': ['data', 'labels', 'w', 'b'], 'desc': 'Identify support vectors'},
    'svm_primal_dual': {'func': calc_svm_primal_dual, 'params': ['w', 'b', 'X', 'y'], 'desc': 'SVM primal and dual objectives'},
    'kmeans': {'func': calc_kmeans, 'params': ['data', 'k', 'max_iter'], 'desc': 'K-means clustering (Lloyd algorithm)'},
    'silhouette_score': {'func': calc_silhouette_score, 'params': ['data', 'labels'], 'desc': 'Silhouette score for clustering'},
    'hierarchical_clustering': {'func': calc_hierarchical_clustering, 'params': ['data', 'linkage'], 'desc': 'Hierarchical clustering'},
    'sigmoid': {'func': calc_sigmoid, 'params': ['x'], 'desc': 'Sigmoid activation sigma(x)'},
    'relu': {'func': calc_relu, 'params': ['x'], 'desc': 'ReLU activation max(0,x)'},
    'tanh_activation': {'func': calc_tanh_activation, 'params': ['x'], 'desc': 'Tanh activation'},
    'softmax': {'func': calc_softmax, 'params': ['logits'], 'desc': 'Softmax function'},
    'forward_pass_2layer': {'func': calc_forward_pass_2layer, 'params': ['x', 'W1', 'W2', 'b1', 'b2'], 'desc': 'Forward pass 2-layer NN'},
    'loss_functions': {'func': calc_loss_functions, 'params': ['pred', 'target'], 'desc': 'MSE and Cross-Entropy loss'},
    'weight_update': {'func': calc_weight_update, 'params': ['w', 'grad', 'lr'], 'desc': 'Weight update w = w - lr*grad'},
    'bayesian_joint': {'func': calc_bayesian_joint, 'params': ['joint_probs'], 'desc': 'Bayesian network joint probability'},
    'variable_elimination': {'func': calc_variable_elimination, 'params': ['A_prob', 'B_given_A', 'B_given_notA'], 'desc': 'Variable elimination'},
    'markov_blanket': {'func': calc_markov_blanket, 'params': [], 'desc': 'Markov blanket description'},
    'entropy': {'func': calc_entropy, 'params': ['probs'], 'desc': 'Shannon entropy H(X)'},
    'joint_entropy': {'func': calc_joint_entropy, 'params': ['joint_probs'], 'desc': 'Joint entropy H(X,Y)'},
    'conditional_entropy': {'func': calc_conditional_entropy, 'params': ['P_X', 'P_YgivenX'], 'desc': 'Conditional entropy H(Y|X)'},
    'mutual_information': {'func': calc_mutual_information, 'params': ['P_X', 'P_Y', 'P_XY'], 'desc': 'Mutual information I(X;Y)'},
    'kl_divergence': {'func': calc_kl_divergence, 'params': ['P', 'Q'], 'desc': 'KL divergence D_KL(P||Q)'},
    'cross_entropy_info': {'func': calc_cross_entropy_info, 'params': ['P', 'Q'], 'desc': 'Cross-entropy H(P,Q)'},
}
