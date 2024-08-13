
import numpy as np

def compute_dtft(x, n, w):
    if x.shape != n.shape:
        raise ValueError('x and n must have same shape')

    X = np.zeros_like(w, dtype=complex)
    for k, wk in enumerate(w):
        X[k] = np.sum(x * np.exp(-1j * wk * n))

    return X