CHANNELS = {
    'BIT_0' : 1200,
    'BIT_1' : 700,
    'TRANSMISSION_DEMAND' : 1300,
    'ACKNOWLEDGEMENT' : 500,
    'ERROR' : 1500,
    'TRANSMISSION_END' : 600,
    'CLOCK' : 1600
    }

def define_reversed_channels() :
    reverted = {}
    for key in CHANNELS.keys():
        value = CHANNELS[key]
        reverted[value] = key

    return reverted

REVERTED_CHANNELS = define_reversed_channels()


STATES = {
    'NOT_READY',
    'WAITING_INCOMING',
    'WAITING_ACKNOWLEDGEMENT',
    'WAITING_DATA',
    'DATA_EMISSION',
    'DATA_RECEPTION',
    'WAITING_CONFIRMATION',
    'ERROR_STATE',
    'TRANSMISSION_END'
}

TRANSITIONS = {'NOT_READY' : {},
               'WAITING_INCOMING' : {'TRANSMISSION_DEMAND', 'ERROR'},
               'WAITING_ACKNOWLEDGEMENT' : {'ACKNOWLEDGEMENT', 'ERROR'},
               'WAITING_DATA' : {'BIT_0', 'BIT_1'},
               'DATA_EMISSION' : {'ERROR'},
               'DATA_RECEPTION' : {'ERROR'},
               'WAITING_CONFIMATION' : {'ACKNOWLEDEGEMENT', 'ERROR'},
               'ERROR_STATE' : {},
               'TRANSMISSION_END' : {'BIT_0', 'BIT_1'}}
