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


class Emission_Driver(Thread):

    def __init__(self, high, input_array):
        Thread.__init__(self)
        self.bit_remaining = 8
        self.bytes = input_array
        self.byte_counter = 0
        self.state = protocol.States.NOT_READY
        self.high = high
        self.frequencies = protocol.CHANNELS.values()
        self.channels = {}
        self.player = None
        self.cycle_counter = 3
        self.stop_event = threading.Event()
        for channel in protocol.CHANNELS.keys():
            self.channels[channel] = False

        self.listener_driver = Listener(self.frequencies, const.NB_FRAMES_RECPT, 48000, gz.goetzl_driver, self.handle_result,const.THRESHOLD)
        self.listener_driver.start()
        print('init')

    def run(self):
        toto = None

    def step(self):
        print(self.state)
        if self.state == protocol.States.NOT_READY:
            self.player = Player([protocol.CHANNELS['TRANSMISSION_DEMAND']], const.NB_FRAMES, 48000)
            self.player.start()
            self.state = protocol.States.WAITING_ACKNOWLEDGEMENT
        elif self.state == protocol.States.WAITING_ACKNOWLEDGEMENT:
            self.bits = self.bytes[0]
            if self.channels['ACKNOWLEDGEMENT']:
                self.cycle_counter = 2
                self.player.stop()
                self.state = protocol.States.DATA_EMISSION
        elif self.state == protocol.States.DATA_EMISSION:
            self.cycle_counter -= 1
            print(self.cycle_counter)
            if self.cycle_counter >= 0:
                return
            else:
                self.player.stop()
                self.cycle_counter = 3
                if self.bit_remaining>0:
                    if self.bits[8-self.bit_remaining] == 0:
                        bit = 'BIT_0'
                    else:
                        bit = 'BIT_1'

                    self.player = Player([protocol.CHANNELS[bit]], const.NB_FRAMES, 48000)
                    self.player.start()
                    self.bit_remaining -= 1
                else :
                    self.state = protocol.States.DATA_END
                    print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")

        elif self.state == protocol.States.DATA_END:
            self.player = Player([protocol.CHANNELS['TRANSMISSION_DEMAND']], const.NB_FRAMES, 48000)
            self.player.start()
            self.state = protocol.States.WAITING_CONFIRMATION

        elif self.state == protocol.States.WAITING_CONFIRMATION:
            if self.channels['ACKNOWLEDGEMENT']:
                self.player.stop()
                self.byte_counter += 1
                if self.byte_counter >= len(self.bytes):
                    self.state = protocol.States.TRANSMISSION_END
                    self.player = Player([protocol.CHANNELS['TRANSMISSION_END']], const.NB_FRAMES, 48000)
                    self.player.start()
                    time.sleep(3)
                    print('TRANSMISSION_END')
                    self.player.stop()
                    self.stop()
                else:
                    print(self.byte_counter)
                    self.cycle_counter = 2
                    self.bit_remaining = 8
                    self.bits = self.bytes[self.byte_counter]
                    self.state = protocol.States.DATA_EMISSION


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
        if self.player != None:
            self.player.stop()
        self.stop_event.set()
        self.listener_driver.stop()
        
