import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from compute_lowpass_impulse_response import compute_lowpass_impulse_response

wc = np.pi/4
N = 15
h = compute_lowpass_impulse_response(wc, N)

w, freq_response = signal.freqz(h, 1)
plt.figure()
plt.subplot(2, 2, 3)
plt.plot(w/np.pi, 20*np.log10(np.abs(freq_response)))
plt.title(f"Freqz Magnitude of the DTFT, {1}")
plt.xlabel("w/pi")
plt.ylabel("|X(e^{jw})|")

plt.subplot(2, 2, 4)
plt.plot(w/np.pi, np.unwrap(np.angle(freq_response)) )  # Convert phase to degrees
plt.title(f"Freqz Phase of the DTFT, {1}")
plt.xlabel("w/pi (radians)")
plt.ylabel(r"\angle X(e^{jw}) (degrees)")
plt.subplots_adjust(hspace=0.25, wspace=0.25)
plt.show()