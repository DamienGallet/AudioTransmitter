import sys
import pyaudio
import threading
from threading import Thread
from ploting_utilities import *
import time
import audio_utilities as util
import constants as const
import protocol as protocol
from listener_driver import *
import goertzel as gz
from player import *


class Reception_Driver(Thread):

    def __init__(self, high, output):
        Thread.__init__(self)
        self.bit_count = 0
        self.bytes = []
        self.bits = []
        self.state = protocol.States.NOT_READY
        self.high = high
        self.frequencies = protocol.CHANNELS.values()
        self.channels = {}
        self.player = None
        self.stop_event = threading.Event()
        self.output = output
        self.cycle_counter = 3
        for channel in protocol.CHANNELS.keys():
            self.channels[channel] = False

        self.listener_driver = Listener(self.frequencies, const.NB_FRAMES_RECPT, 48000, gz.goetzl_driver, self.handle_result, const.THRESHOLD)
        self.listener_driver.start()
        self.state = protocol.States.WAITING_INCOMING
        print('init')

    def run(self):
        toto = None

    def step(self):
        print(self.state)
        if self.state == protocol.States.WAITING_INCOMING:
            if self.channels['TRANSMISSION_DEMAND']:
                self.cycle_counter = 3
                self.player = Player([protocol.CHANNELS['ACKNOWLEDGEMENT']], const.NB_FRAMES, 48000)
                self.player.start()
                self.state = protocol.States.WAITING_DATA
                
        elif self.state == protocol.States.WAITING_DATA:
            if self.cycle_counter != 0:
                self.cycle_counter -= 1
                return
            self.cycle_counter = 3 
            self.bits = []
            self.player.stop()
            if self.channels['BIT_0']:
                self.cycle_counter = 3
                self.state = protocol.States.DATA_RECEPTION
                self.bit_count = 0
            elif self.channels['BIT_1']:
                self.cycle_counter = 3
                self.state = protocol.States.DATA_RECEPTION
                self.bit_count = 0
            elif self.channels['TRANSMISSION_END']:
                self.player.stop()
                self.state = protocol.States.TRANSMISSION_END
                self.stop()
        elif self.state == protocol.States.DATA_RECEPTION:
            print(self.bit_count)
            print(self.cycle_counter)
            self.cycle_counter -= 1
            if self.bit_count >= 8:
                print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                print(self.bits)
                self.bytes.append(self.bits)
                self.output(self.bits)
                self.state = protocol.States.DATA_END
                return
            if self.cycle_counter == 2:
                if self.channels['BIT_0']:
                    self.bit_count += 1
                    self.bits.append(0)
                elif self.channels['BIT_1']:
                    self.bit_count += 1
                    self.bits.append(1)
                elif self.channels['ERROR']:
                    self.state = protocol.States.WAITING_DATA
                    return
            if self.cycle_counter < 0:
                self.cycle_counter = 3
                return
            

        elif self.state == protocol.States.DATA_END:
            self.cycle_counter = 3
            self.player = Player([protocol.CHANNELS['ACKNOWLEDGEMENT']], const.NB_FRAMES, 48000)
            self.player.start()
            self.state = protocol.States.WAITING_DATA
            


    def handle_result(self, data):
        print(data)
        for (f,r) in data.items():
            if r:
                self.channels[protocol.FREQUENCIES[f]] = True
            else :
                self.channels[protocol.FREQUENCIES[f]] = False
        print(self.channels)
        self.step()

    def stop(self):
        self.stop_event.set()
        self.listener_driver.stop()
        if self.player != None:
            self.player.stop()
