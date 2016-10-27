import pyaudio
import math
import struct

def create_audio_chunck(frequencies,chunck_length,bitrate):
    nbOfFreq = len(frequencies)
    values = []

    for x in range(chunck_length):
        level = 0
        for freq in frequencies:
            level += math.sin(x/((bitrate/freq)/math.pi))/nbOfFreq
        values.append(struct.pack('f', level))
    return b''.join(values)

def get_output_stream(bitrate):
    PyAudio = pyaudio.PyAudio
    p = PyAudio()
    stream = p.open(    format = pyaudio.paFloat32, 
                        channels = 2, 
                        rate = bitrate, 
                        output = True)

    return stream

def number_freq(number, high):
    freq =      range(1000,2000,100)

    freq_high = range(17000,18000,100)

    if high:
        return freq_high[number]
    else:
        return freq[number]

def number_freqs(high):
    freq =      range(1000,2000,100)

    freq_high = range(17000,18000,100)

    if high:
        return freq_high
    else:
        return freq

def number_from_freq(freq,high):
    nb = 11
    if high:
        nb = (freq/100) - 170
    else:
        nb = (freq/100) - 10 
    return nb

def dtmf_freqs_only(high):
    freq = [697,770,852,1209,1336,1477]
    freq_high = [13000,13100,13200,13800,13900,14000]

    if high:
        return freq_high
    else:
        return freq

def dtmf_freq(number, high, raw=False):
    freq =      [   [0,0],
                    [697,1209],
                    [697,1336],
                    [697,1477],
                    [770,1209],
                    [770,1336],
                    [770,1477],
                    [852,1209],
                    [852,1336],
                    [852,1477]]

    freq_high = [   [0,0],
                    [13000,13800],
                    [13100,13800],
                    [13200,13800],
                    [13000,13900],
                    [13100,13900],
                    [13200,13900],
                    [13000,14000],
                    [13100,14000],
                    [13200,14000]]
    if raw:
        if high:
            return freq_high
        else:
            return freq

    if high:
        return freq_high[number]
    else:
        return freq[number]

def number_from_dtmf(freqs, high):
    ordered = sorted(freqs)
    dtmf_freqs = dtmf_freq(0,high,True)
    for i in range(len(dtmf_freqs)):
        if dtmf_freqs[i] == ordered:
            return i
    return 11

def convert_recording(in_data, frame_count):
    print(frame_count)
    levels = []
    for _i in range(0,frame_count,4):
        level = struct.unpack('@i', in_data[_i:_i + 4])[0]
        levels.append(level)

    return levels