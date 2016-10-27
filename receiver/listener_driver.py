import sys
import pyaudio
import threading
from threading import Thread
from ploting_utilities import *
import time
import audio_utilities as util
import constants as const

class Listener(Thread):
    
    def __init__(self, frequencies, chunck, bitrate, computing_callback, output_callback, threshold):
        Thread.__init__(self)
        self.bitrate = bitrate
        self.stop_event = threading.Event()
        self.frequencies = frequencies
        self.computing_callback = computing_callback
        self.output_callback = output_callback
        self.threshold = threshold
        self.chunck = chunck

    def run(self):
        data = []
        FORMAT = pyaudio.paInt32
        CHANNELS = 1

        audio = pyaudio.PyAudio()

        self.stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=self.bitrate,
                            input=True,
                            frames_per_buffer=self.chunck,
                            stream_callback=self.handle)

        while(not self.stop_event.is_set()):
            self.stop_event.wait(1000)
            print('Run')

        print('Listener shut down')
        self.stream.stop_stream()
        self.stream.close()
        audio.terminate()

    def handle(self, in_data, frame_count, time_info, status):
        levels = util.convert_recording(in_data, frame_count)
        result = self.computing_callback(levels,self.frequencies,self.threshold)
        self.output_callback(result)
        
        return (in_data, pyaudio.paContinue)

    def stop(self):
        self.stop_event.set()
        self.stream.stop_stream()
        self.stream.close()