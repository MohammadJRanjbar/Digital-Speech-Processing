import os.path as path
import scipy.io.wavfile as wav
import scipy.signal as sig
import numpy as np
import ex3_windowing as win
import matplotlib.pyplot as plt


# Read the audio file SX83.WAV and sampling rate
file_path = path.join('.', 'Sounds')
sound_file = path.join(file_path, 'SX83.wav')
Fs, in_sig = wav.read(sound_file) #Read audio file

#  Make sure the sampling rate is 16kHz, resample if necessary
Fs_target = 16000

if not (Fs == Fs_target):
    in_sig = sig.resample_poly(in_sig,Fs_target,Fs)
    Fs = Fs_target

window_types = ['hamming','rect','hann','cosine']
t_frame=0.025
over_lap=0.5
frame_length = int(np.around(t_frame*Fs))
hop_size = int(np.around(t_frame*0.5*Fs))

for window in window_types:

    frame_matrix = win.ex3_windowing(in_sig, frame_length, hop_size, window)

    plt.figure(figsize=(10, 8))
    plt.suptitle(f'Results for {window} window type')
    plt.subplot(3,1,1)
    plt.plot(np.array(range(len(in_sig)))/Fs, in_sig)
    plt.title('Original signal')
    plt.ylabel('Amplitude')
    plt.xlabel('Time')

    plt.subplot(3,1,2)
    plt.plot(np.array(range(frame_length))/(Fs/1000), frame_matrix[:,23])
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.title('25 ms of voiced frame')
    plt.ylabel('Amplitude')
    plt.xlabel('Time')

    plt.subplot(3,1,3)
    Nfft = 1024
    frame_fft = np.fft.rfft(frame_matrix[:,23],n=Nfft)
    f_axis = (np.arange(int(Nfft/2)+1) / (Nfft/2)) * (Fs/2)
    plt.plot(f_axis,20*np.log10(np.absolute(frame_fft)))
    plt.autoscale(enable=True, axis='x', tight=True)
    plt.title('Magnitude spectrum')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency')
    plt.subplots_adjust(hspace=3)  # Adjust vertical spacing between subplots
    plt.savefig(f'{window}_plot.png')
    plt.show()


    plt.suptitle(f'Results for {window} window type')
    frame_matrix_fft = np.fft.rfft(frame_matrix,axis=0,n=Nfft)
    epsilon = 1e-10  # Small constant to avoid zero
    frame_matrix_fft = 20 * np.log10(np.absolute(frame_matrix_fft[::-1]))
    plt.imshow(frame_matrix_fft, aspect='auto')
    ytickpos = [0, int(Nfft/8), int(Nfft/4), int(Nfft*3/8), int(Nfft/2)]
    plt.yticks(ytickpos, f_axis[ytickpos[::-1]])
    plt.title('Spectrogram')
    plt.ylabel('Frequency')
    plt.xlabel('Frame number')
    plt.savefig(f'{window}_spectrogram.png')
    plt.show()



