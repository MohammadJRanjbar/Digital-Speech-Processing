import numpy as np
from compute_dtft import compute_dtft
import matplotlib.pyplot as plt
from scipy.signal import freqz
def plot_mag_phase(X, w, x, n, pltid):
    plt.figure(figsize=(12, 8))

    # Magnitude of the DTFT
    plt.subplot(2, 2, 1)
    plt.plot(w/np.pi, 20*np.log10(np.abs(X)))
    plt.title(f"Magnitude of the DTFT, {pltid}")
    plt.xlabel("w/\pi")
    plt.ylabel("|X(e^{jw})|")

    # Phase of the DTFT
    plt.subplot(2, 2, 2)
    plt.plot(w/np.pi, np.unwrap(np.angle(X)))
    plt.title(f"Phase of the DTFT, {pltid}")
    plt.xlabel("w/pi (radians)")
    plt.ylabel(r"\angle X(e^{jw})")

    # Freqz Magnitude of the DTFT

    wz,Xz  = freqz(x,worN=len(w))
    plt.subplot(2, 2, 3)
    plt.plot(wz/np.pi, 20*np.log10(np.abs(Xz)))
    plt.title(f"Freqz Magnitude of the DTFT, {pltid}")
    plt.xlabel("w/pi")
    plt.ylabel("|X(e^{jw})|")

    # Freqz Phase of the DTFT
    plt.subplot(2, 2, 4)
    plt.plot(wz/np.pi,np.unwrap(np.angle(Xz))- n[0]*wz)
    plt.title(f"Freqz Phase of the DTFT, {pltid}")
    plt.xlabel("w/pi (radians)")
    plt.ylabel(r"\angle X(e^{jw})")
    plt.subplots_adjust(hspace=0.25, wspace=0.25)
    plt.show()

##################################################################################
# Part (a)
n = np.arange(-20, 20)
x = 3 * (5 ** -np.abs(n.astype(float) - 2))
w = np.arange(0, np.pi + np.pi/100, np.pi/100)

X = compute_dtft(x, n, w)
plot_mag_phase(X, w, x, n, pltid='(a)')

##################################################################################
# Part (b)
n = np.arange(-20, 21)
alpha = 0.8
w0 = 2 * np.pi / 4.5  # period 4.5
phi = np.pi / 4
pltid = '(b)'
x = (alpha ** n) * np.cos((w0 * n) + phi) * (n >= 0)

# Compute and plot DTFT
w = np.arange(0, np.pi + np.pi/100, np.pi/100)
X = compute_dtft(x, n, w)
plot_mag_phase(X, w, x, n, pltid)

##################################################################################
# Part (c)

# Define signal parameters
n = np.arange(-1000, 1000)
pltid = '(c)'
x = 7 * np.ones_like(n)

# Compute frequency vector
w = np.arange(0, np.pi + np.pi/100, np.pi/100)
# Compute and plot DTFT

X = compute_dtft(x, n, w)
plot_mag_phase(X, w, x, n, pltid)

##################################################################################
# Part (d)
# Define parameters
n = np.arange(-20,20)
w0 = 2 * np.pi / 4.5  # Angular frequency corresponding to a period of 4.5
phi = np.pi / 4
A = 5
pltid = ' (d)'

# Generate the signal x[n]
x = A * np.cos(w0 * n + phi)

w = np.arange(0, np.pi + np.pi/100, np.pi/100)

# Compute and plot DTFT
X = compute_dtft(x, n, w)
plot_mag_phase(X, w, x, n, pltid)

##################################################################################
# Part (e)

n = np.arange(-20, 20)
w0 = 2 * np.pi / 4.5  # Angular frequency corresponding to a period of 4.5
phi = np.pi / 4
A = 5
pltid = ' (e)'
w = np.arange(0, np.pi + np.pi/100, np.pi/100)
x = A * np.sin(w0 * n + phi) * ((n >= 0) & (n <= 9))

# Compute and plot DTFT
X = compute_dtft(x, n, w)
plot_mag_phase(X, w, x, n, pltid)