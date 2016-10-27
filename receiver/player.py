import sys
import pyaudio
import threading
from threading import Thread
import time
import audio_utilities as util

class Player(Thread):
    
    def __init__(self, frequencies, chunck, bitrate):
        Thread.__init__(self)
        self.bitrate = bitrate
        self.stop_event = threading.Event()
        self.wavedata = util.create_audio_chunck(frequencies,chunck,bitrate)

    def run(self):     
        #self.stream = util.get_output_stream(self.bitrate)

        PyAudio = pyaudio.PyAudio
        p = PyAudio()
        self.stream =p.open(format = pyaudio.paFloat32, 
                            channels = 2, 
                            rate = self.bitrate, 
                            output = True)

        while(not self.stop_event.is_set()):
            self.stream.write(self.wavedata)
        
        self.stream.stop_stream()
        self.stream.close()
        p.terminate()

    def stop(self):
        self.stop_event.set()
