try:
    xrange
except NameError:
    xrange = range

import math
import pyaudio
import wave
import sys
import time
import struct

import constants as const

#sudo apt-get install python-pyaudio
PyAudio = pyaudio.PyAudio

def write_file(datas, file):
    file = open(file, "w")
    for key in datas:
        content = str(key)+","
        for single in datas[key]:
            content+=str(single)+","
        content+="\n"
        file.write(content)
    file.close()
def listen_and_raw_record():
    import pyaudio
    import wave
    import struct

     
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    CHUNK = 1024
    RECORD_SECONDS = 1
    WAVE_OUTPUT_FILENAME = "file.wav"
     
    audio = pyaudio.PyAudio()
     
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print ("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        print()
        data = []
        chuck = stream.read(CHUNK)
        for c in chuck:
            data.append(c - 128)
        #data = struct.unpack('b', stream.read(CHUNK))
        print('beg chunck')
        print(data)
        print('end chunk')
        #frames.append(data)
    print ("finished recording")
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
     
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    return(data)

def listen_continuously(listener, bitrate, record_time):
    data = []
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=bitrate,
                        input=True,
                        frames_per_buffer=const.NB_FRAMES,
                        stream_callback=listener.handle)

    time.sleep(record_time)

    print('Listener shut down')
    stream.stop_stream()
    stream.close()
    audio.terminate()

def generate_continuously(frequencies, bitrate,chunck):

    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 48000 #number of frames per second/frameset.      

    nbOfFreq = len(frequencies)
    values = []

    for x in range(chunck):
        level = 0
        for freq in frequencies:
            level += math.sin(x/((bitrate/freq)/math.pi))/nbOfFreq
        values.append(struct.pack('f', level))
    WAVEDATA = b''.join(values)
    print(WAVEDATA)

    p = PyAudio()
    stream = p.open(format = pyaudio.paFloat32, 
                    channels = 2, 
                    rate = BITRATE, 
                    output = True)
    while(generate):
        stream.write(WAVEDATA)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def listen(time):
    frames = []
    CHUNK = 7500
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    BITRATE = 44100

    audio = pyaudio.PyAudio()
     
    # start Recording
    print("recording...")
 
    import numpy
    stream = audio.open(format=FORMAT,channels=1,rate=BITRATE,input=True,frames_per_buffer=CHUNK)
    data = stream.read(time*CHUNK)
    decoded = numpy.fromstring(data, 'Float32');

    print("finish recording")

    stream.stop_stream()
    stream.close()
    audio.terminate()
    print (decoded)

    return decoded

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
    waveFile.writeframes(b''.join(data))
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