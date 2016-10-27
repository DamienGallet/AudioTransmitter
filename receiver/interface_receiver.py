import audio_utilities as util 
import constants as const
import goertzel as gz
from listener_driver import *
from tkinter import * 

fenetre = Tk()
fenetre.wm_title("Frequency detector")

# Single frequency detector

singleFreq = LabelFrame(fenetre,text="Single frequency detector")
singleFreq.pack()
label_spinbox = Label(singleFreq,text="Select the frequecy")
spinbox = Spinbox(singleFreq, from_=300, to=20000)
output_field = Label(singleFreq,text="Not started")

listener_driver = None
def output_single(result):
    if list(result.values())[0]:
        output_field['text'] = 'Detected !'
    else:
        output_field['text'] = 'Not detected'


def listen_single():
    global listener_driver
    if listener_driver == None:
        freq = int(spinbox.get())
        print(freq)
        listener_driver = Listener([freq], 8192, const.FREQUENCY, gz.goetzl_driver, output_single, 5*10**19)
        listener_driver.start()

def stop_single():
    global listener_driver
    if listener_driver != None:
        print('stop button')
        listener_driver.stop()
        listener_driver = None
        output_field['text'] = 'Not started'


label_spinbox.pack(side=LEFT,  padx=20)
spinbox.pack(side=LEFT, padx=20)
output_field.pack(side=LEFT, padx=20)

Button(singleFreq, text ='Listen', command= listen_single).pack(side=LEFT, padx=5, pady=5)
Button(singleFreq, text ='Stop', command= stop_single).pack(side=RIGHT, padx=5, pady=5)

# Digit detection
digitFreq = LabelFrame(fenetre,text="Digit detector (single)")
digitFreq.pack()

checked_DG = IntVar()
high_freq_DG = Checkbutton(digitFreq, text="High frequencies", variable=checked_DG).pack(side=LEFT, padx=20)
output_field_sd = Label(digitFreq,text="Not started")
output_field_sd.pack(side=LEFT, padx=20)

def output_single_digit(result):
    detected = 0
    high = bool(checked_DG.get())
    current_max = 0
    for (f,r) in result.items():
        if r>5*10**19 and r>current_max:
            detected = util.number_from_freq(f, high)
            current_max = r

    if detected == 10:
        output_field_sd['text'] = 'Multiple frequencies detected'
    elif detected == 0:
        output_field_sd['text'] = 'No freq detected'
    else :
        output_field_sd['text'] = 'Number : '+str(detected)+' transmitted'



def listen_single_digit():
    global listener_driver
    if listener_driver == None:
        high = bool(checked_DG.get())
        frequencies = util.number_freqs(high)
        listener_driver = Listener(frequencies, 8192, const.FREQUENCY, gz.goetzl_driver_continuous, output_single_digit, 5*10**19)
        listener_driver.start()

def stop_single_digit():
    global listener_driver
    if listener_driver != None:
        print('stop button')
        output_field['text'] = 'Not started'
        listener_driver.stop()
        listener_driver = None

Button(digitFreq, text ='Listen', command= listen_single_digit).pack(side=LEFT, padx=5, pady=5)
Button(digitFreq, text ='Stop', command= stop_single_digit).pack(side=RIGHT, padx=5, pady=5)


# DTMF frequency part
digitFreq_DTMF = LabelFrame(fenetre,text="Digit detector (dtmf)")
digitFreq_DTMF.pack()

checked_DTMF = IntVar()
high_freq_DTMF = Checkbutton(digitFreq_DTMF, text="High frequencies", variable=checked_DG).pack(side=LEFT, padx=20)
output_field_DTMF = Label(digitFreq_DTMF,text="Not started")
output_field_DTMF.pack(side=LEFT, padx=20)

def output_single_digit(result):
    detected = 0
    high = bool(checked_DTMF.get())
    current_max = 0
    for (f,r) in result.items():
        if r>5*10**19 and r>current_max:
            detected = util.number_from_freq(f, high)
            current_max = r

    if detected == 10:
        output_field_sd['text'] = 'Multiple frequencies detected'
    elif detected == 0:
        output_field_sd['text'] = 'No freq detected'
    else :
        output_field_sd['text'] = 'Number : '+str(detected)+' transmitted'



def listen_DTMF_digit():
    global listener_driver
    if listener_driver == None:
        high = bool(checked_DTMF.get())
        frequencies = util.number_freqs(high)
        listener_driver = Listener(frequencies, 8192, const.FREQUENCY, gz.goetzl_driver_continuous, output_single_digit, 5*10**19)
        listener_driver.start()

def stop_DTMF_digit():
    global listener_driver
    if listener_driver != None:
        print('stop button')
        output_field['text'] = 'Not started'
        listener_driver.stop()
        listener_driver = None

Button(digitFreq_DTMF, text ='Listen', command= listen_DTMF_digit).pack(side=LEFT, padx=5, pady=5)
Button(digitFreq_DTMF, text ='Stop', command= stop_DTMF_digit).pack(side=RIGHT, padx=5, pady=5)

# Dual frequency part DTMF
dtmfFreq = LabelFrame(fenetre,text="DTMF frequency generator")
dtmfFreq.pack()
label_spinbox_DT = Label(dtmfFreq,text="Select the number")
spinbox_dtmf = Spinbox(dtmfFreq, from_=1, to=9)
checked = IntVar()
high_freq = Checkbutton(dtmfFreq, text="High frequencies", variable=checked)

label_spinbox_DT.pack(side=LEFT,  padx=20)
spinbox_dtmf.pack(side=LEFT, padx=20)
high_freq.pack(side=LEFT, padx=20)


def generate_dtmf():
    number = int(spinbox_dtmf.get())
    high = bool(checked.get())
    freqs = util.dtmf_freq(number,high)
    spinbox_DA_var.set(freqs[0])
    spinbox_DB_var.set(freqs[1])
    generate_dual()

def stop_dtmf():
    stop_dual()

Button(dtmfFreq, text ='Generate', command= generate_dtmf).pack(side=LEFT, padx=5, pady=5)
Button(dtmfFreq, text ='Stop', command= stop_dtmf).pack(side=RIGHT, padx=5, pady=5)

fenetre.mainloop()

if listener_driver != None:
    listener_driver.stop()

print("End mainloop")
