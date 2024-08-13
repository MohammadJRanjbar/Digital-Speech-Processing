"""
EX3_WINDOWING Based on the input parameters, generate a n x m matrix of windowed
frames, with n corresponding to frame_length and m corresponding to number
of frames. The first frame starts at the beginning of the data.
"""

import numpy as np

def ex3_windowing(data, frame_length, hop_size, windowing_function):
    frame_window=len(data)-frame_length
    number_of_frames = 1+int(np.floor((frame_window)/hop_size))
    frame_matrix = np.zeros((frame_length,number_of_frames))
    if windowing_function == 'hamming':
        window = np.hamming(frame_length)
    elif windowing_function == 'rect':
        window = np.ones((1,frame_length))
    elif windowing_function == 'cosine':
        window = np.sqrt(np.hanning(frame_length))
    elif windowing_function == 'hann':
        window = np.hanning(frame_length)

    for i in range(number_of_frames):
        start = i * hop_size
        stop = np.minimum(start + frame_length, len(data))
        frame = np.zeros(frame_length)
        frame[0:stop - start] = data[start:stop]
        windowed_frame = window * frame  
        frame_matrix[:, i] = windowed_frame  
    return frame_matrix










