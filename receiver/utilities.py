try:
    xrange
except NameError:
    xrange = range

import math
import pyaudio
import wave
import sys

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio

BITRATE = 44100

def write_file(datas, file):
    file = open(file, "w")
    for key in datas:
        content = str(key)+","
        for single in datas[key]:
            content+=str(single)+","
        content+="\n"
        file.write(content)
    file.close()

def generate_frequency(freqs):
    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    #number of frames per second/frameset.      

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    LENGTH = 1 #seconds to play sound

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = []  

    for x in xrange(NUMBEROFFRAMES):
        level = 0
        for freq in freqs :
            level += int(math.sin(x/((BITRATE/freq)/math.pi))*127+128)

        WAVEDATA.append(level)

    return WAVEDATA
def array_to_sound(data):
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1, 
                    rate = BITRATE, 
                    output = True)
    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return stream
def play_sound(data):
    p = PyAudio()
    stream = p.open(format = p.get_format_from_width(1), 
                    channels = 1,
                    rate = BITRATE, 
                    output = True)
    stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def record_sound(file, data):
    p = PyAudio()
    CHUNK = 100
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    BITRATE = 44100

    waveFile = wave.open(file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(pyaudio.get_sample_size(FORMAT))
    waveFile.setframerate(BITRATE)
    waveFile.write(data)
    waveFile.close()

def read_file(file):
    chunk = 1024

    if len(sys.argv) < 2:
        print("Error file" +\
              "Usage: %s.was" % file)
        sys.exit(-1)

    # open the file for reading.
    wf = wave.open(file, 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read
    data = wf.readframes(chunk)