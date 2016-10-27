from enum import Enum

CHANNELS = {
    'BIT_0' : 1200,
    'BIT_1' : 700,
    'TRANSMISSION_DEMAND' : 1300,
    'ACKNOWLEDGEMENT' : 500,
    'ERROR' : 1500,
    'TRANSMISSION_END' : 600,
    'CLOCK' : 1600
    }

FREQUENCIES = {}
for (k,v) in CHANNELS.items():
  FREQUENCIES[v] = k


class States(Enum):
    NOT_READY = 1
    WAITING_INCOMING = 2
    WAITING_ACKNOWLEDGEMENT = 3
    WAITING_DATA = 4
    DATA_EMISSION = 5
    DATA_RECEPTION = 6
    DATA_END = 7
    WAITING_CONFIRMATION = 8
    ERROR_STATE = 9
    TRANSMISSION_END = 10

TRANSITIONS = {'NOT_READY' : {},
               'WAITING_INCOMING' : {'TRANSMISSION_DEMAND', 'ERROR'},
               'WAITING_ACKNOWLEDGEMENT' : {'ACKNOWLEDGEMENT', 'ERROR'},
               'WAITING_DATA' : {'BIT_0', 'BIT_1'},
               'DATA_EMISSION' : {'ERROR'},
               'DATA_RECEPTION' : {'ERROR'},
               'WAITING_CONFIMATION' : {'ACKNOWLEDEGEMENT', 'ERROR'},
               'ERROR_STATE' : {},
               'TRANSMISSION_END' : {'BIT_0', 'BIT_1'}}
