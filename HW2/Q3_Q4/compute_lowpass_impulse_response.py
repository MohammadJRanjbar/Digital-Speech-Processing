import numpy as np

def compute_lowpass_impulse_response(wc, N):
    n = np.arange(0, 2*N)
    h = np.sin(wc*(n-N))/(np.pi*(n-N) + np.finfo(float).eps)  # handling division by zero
    h[N] = wc/np.pi  # inserting the solution for the 0/0 case by hand
    return h
from scipy.signal import firwin

def compute_lowpass_impulse_response_with_scipy(wc, N):
    h = firwin(2*N, wc/np.pi)
    return h
