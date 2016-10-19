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

def generate_frequency(freqs)
    #See http://en.wikipedia.org/wiki/Bit_rate#Audio
    BITRATE = 44400 #number of frames per second/frameset.      

    #See http://www.phy.mtu.edu/~suits/notefreqs.html
    FREQUENCY = 440 #Hz, waves per second, 261.63=C4-note.
    LENGTH = 10 #seconds to play sound

    NUMBEROFFRAMES = int(BITRATE * LENGTH)
    RESTFRAMES = NUMBEROFFRAMES % BITRATE
    WAVEDATA = ''  

    for x in xrange(NUMBEROFFRAMES):
        level = 0
        for freq in freqs :
            level += int(math.sin(x/((BITRATE/freq)/math.pi))*127+128)
        WAVEDATA = WAVEDATA+chr(level)

    #fill remainder of frameset with silence
    for x in xrange(RESTFRAMES): 
        WAVEDATA = WAVEDATA+chr(128)

    return WAVEDATA

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

def record_sound(file):
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	    data = stream.read(CHUNK)
	    frames.append(data)
	print "finished recording"
	
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

def read_file(file):
	chunk = 1024

	if len(sys.argv) < 2:
	    print "Error file" +\
	          "Usage: %s.was" % file
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