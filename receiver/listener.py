import constants as const

import struct
import pyaudio

class Listener:
    def __init__(self, main_callback,param1,param2=0,param3=0):
        self.main_callback = main_callback
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    def handle(self, in_data, frame_count, time_info, status):
        levels = []
        for _i in range(const.NB_FRAMES):
            level = struct.unpack('<h', in_data[_i:_i + 2])[0]
            levels.append(level)
        
        self.main_callback(levels,self.param1)
        
        return (in_data, pyaudio.paContinue)