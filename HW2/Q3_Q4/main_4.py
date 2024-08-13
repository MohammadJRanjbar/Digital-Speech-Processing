import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from compute_lowpass_impulse_response import compute_lowpass_impulse_response,compute_lowpass_impulse_response_with_scipy
# a) 

parameters = [
    (10, np.pi / 4),
    (15, np.pi / 4),
    (100, np.pi / 4),
    (10000, np.pi / 4),
    (10, np.pi / 2),
    (15, np.pi / 2),
    (100, np.pi / 2),
    (10000, np.pi / 2),
    (10, 3* np.pi / 4),
    (15, 3* np.pi / 4),
    (100, 3* np.pi / 4),
    (10000, 3* np.pi / 4),
]

for idx, (N, wc) in enumerate(parameters, start=1):
    wc_pi = wc / np.pi  # Express wc in terms of pi
    h = compute_lowpass_impulse_response(wc, N)
    h_lib = compute_lowpass_impulse_response_with_scipy(wc, N)
    w, freq_response = signal.freqz(h, 1)
    w_lib, freq_response_lib = signal.freqz(h_lib, 1)

    plt.figure(figsize=(16, 12))  # Adjust the overall figure size here
    plt.subplot(2, 2, 1)
    plt.plot(w / np.pi, 20 * np.log10(np.abs(freq_response)))
    plt.title(f"Freqz Magnitude of the DTFT, Custom Implementation (N={N}, wc={wc_pi:.2f}pi)")
    plt.xlabel("w/pi")
    plt.ylabel("|X(e^{jw})|")

    plt.subplot(2, 2, 2)
    plt.plot(w / np.pi, np.unwrap(np.angle(freq_response)))  # Convert phase to degrees
    plt.title(f"Freqz Phase of the DTFT, Custom Implementation (N={N}, wc={wc_pi:.2f}pi)")
    plt.xlabel("w/pi (radians)")
    plt.ylabel(r"$\angle X(e^{jw})$ (radians)")

    plt.subplot(2, 2, 3)
    plt.plot(w_lib / np.pi, 20 * np.log10(np.abs(freq_response_lib)))
    plt.title(f"Freqz Magnitude of the DTFT, SciPy Implementation (N={N}, wc={wc_pi:.2f}pi)")
    plt.xlabel("w/pi")
    plt.ylabel("|X(e^{jw})|")

    plt.subplot(2, 2, 4)
    plt.plot(w_lib / np.pi, np.unwrap(np.angle(freq_response_lib)))  # Convert phase to degrees
    plt.title(f"Freqz Phase of the DTFT, SciPy Implementation (N={N}, wc={wc_pi:.2f}pi)")
    plt.xlabel("w/pi (radians)")
    plt.ylabel(r"$\angle X(e^{jw})$ (radians)")

    plt.subplots_adjust(hspace=0.5, wspace=0.5)  # Adjust the spacing between subplots here
    plt.show()

########################################################################################################################################
# b) 
import numpy as np
import scipy.io.wavfile as wav
import time
import pygame
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

fs, x = wav.read('PSO_B1short.wav')
# Convert to mono
x = np.mean(x, axis=1)

# Lowpass filter parameters
wc = np.pi * 0.35 
N = int((7+3)/2)
h = compute_lowpass_impulse_response(wc, N)
# Apply convolution
y = np.convolve(x, h, mode='same')

# Assuming x contains the audio data and fs is the sampling rate
segment_length = 2 * fs  # Length of the segment to save
segment_data = x[:segment_length]  # Extracting the segment
wav.write("Original.wav", fs, segment_data.astype(np.int16))  # Save the segment as a WAV file with filename default

pygame.mixer.init()
# Play lowpass filtered audio
pygame.mixer.music.load("Original.wav")
pygame.mixer.music.play()
# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(2)
# Pause for 2 seconds


# Assuming x contains the audio data and fs is the sampling rate
segment_length = 2 * fs  # Length of the segment to save
segment_data = y[:segment_length]  # Extracting the segment
wav.write("low_pass.wav", fs, segment_data.astype(np.int16))  # Save the segment as a WAV file with filename low_pass
# Initialize Pygame mixer
pygame.mixer.init()

# Play lowpass filtered audio
pygame.mixer.music.load("low_pass.wav")
pygame.mixer.music.play()
# Wait for the audio to finish playing
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(2)
# Plot spectrograms with custom colormap
plt.figure()
plt.subplot(2, 1, 1)
plt.specgram(x[:2 * fs], Fs=fs, cmap='plasma')
plt.title('Spectrogram of the original sound file')

plt.subplot(2, 1, 2)
plt.specgram(y[:2 * fs], Fs=fs, cmap='plasma')
plt.title('Spectrogram of the lowpass filtered sound file')
plt.subplots_adjust(hspace=0.35, wspace=0.35)

plt.show()