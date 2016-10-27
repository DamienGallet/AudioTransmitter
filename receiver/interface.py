from tkinter import * 
from player import Player
import audio_utilities as util
from emission_driver import *


fenetre = Tk()
fenetre.wm_title("Frequency generator")

# Single frequency part

singleFreq = LabelFrame(fenetre,text="Single frequency generator")
singleFreq.pack()
label_spinbox = Label(singleFreq,text="Select the frequecy")
spinbox_var = StringVar()
spinbox = Spinbox(singleFreq, from_=300, to=20000, textvariable=spinbox_var)

player = None
def generate_single():
    global player
    if player == None:
        freq = int(spinbox.get())
        print(freq)
        player = Player([freq], 48000, 48000)
        player.start()

def stop_single():
    global player
    if player != None:
        player.stop()
        player = None

label_spinbox.pack(side=LEFT,  padx=20)
spinbox.pack(side=LEFT, padx=20)

Button(singleFreq, text ='Generate', command= generate_single).pack(side=LEFT, padx=5, pady=5)
Button(singleFreq, text ='Stop', command= stop_single).pack(side=RIGHT, padx=5, pady=5)

# 1 digit transmission
digitFreq = LabelFrame(fenetre,text="One digit transmission")
digitFreq.pack()
label_spinbox_DG = Label(digitFreq,text="Select the number")
spinbox_DG = Spinbox(digitFreq, from_=1, to=9)
checked_DG = IntVar()
high_freq_DG = Checkbutton(digitFreq, text="High frequencies", variable=checked_DG)

label_spinbox_DG.pack(side=LEFT,  padx=20)
spinbox_DG.pack(side=LEFT, padx=20)
high_freq_DG.pack(side=LEFT, padx=20)


def generate_DG():
    number = int(spinbox_DG.get())
    high = bool(checked_DG.get())
    freq = util.number_freq(number,high)
    spinbox_var.set(freq)
    generate_single()

def stop_DG():
    stop_single()

Button(digitFreq, text ='Generate', command= generate_DG).pack(side=LEFT, padx=5, pady=5)
Button(digitFreq, text ='Stop', command= stop_DG).pack(side=RIGHT, padx=5, pady=5)


# Dual frequency part
dualFreq = LabelFrame(fenetre,text="Dual frequency generator")
dualFreq.pack()
label_spinbox_D = Label(dualFreq,text="Select the frequecies")
spinbox_DA_var = StringVar()
spinbox_DB_var = StringVar()
spinbox_DA = Spinbox(dualFreq, from_=300, to=20000, textvariable=spinbox_DA_var)
spinbox_DB = Spinbox(dualFreq, from_=300, to=20000, textvariable=spinbox_DB_var)

playerDual = None
def generate_dual():
    global playerDual
    if playerDual == None:
        freqA = int(spinbox_DA.get())
        freqB = int(spinbox_DB.get())
        playerDual = Player([freqA, freqB], 48000, 48000)
        playerDual.start()

def stop_dual():
    global playerDual
    if playerDual != None:
        playerDual.stop()
        playerDual = None

label_spinbox_D.pack(side=LEFT,  padx=20)
spinbox_DA.pack(side=LEFT, padx=20)
spinbox_DB.pack(side=LEFT, padx=20)

Button(dualFreq, text ='Generate', command= generate_dual).pack(side=LEFT, padx=5, pady=5)
Button(dualFreq, text ='Stop', command= stop_dual).pack(side=RIGHT, padx=5, pady=5)

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



# Data emission
dataFreq = LabelFrame(fenetre,text="Data emitter")
dataFreq.pack()
checkedData = IntVar()
high_freq_data = Checkbutton(dataFreq, text="High frequencies", variable=checkedData).pack(side=LEFT, padx=20)

dataString = StringVar()
input_field_data = Entry(dataFreq,text="Not started", textvariable=dataString).pack(side=LEFT, padx=20)



emission_driver = None
def emit_data():
    global emission_driver
    high = bool(checked.get())
    toTransmit = dataString.get()
    if emission_driver == None:
        emission_driver = Emission_Driver(high, [1,1,0,1,1,1,0,1])
        emission_driver.start()

def stop_data():
    global emission_driver
    if emission_driver != None:
        emission_driver.stop()
        emission_driver = None

Button(dataFreq, text ='Emit', command= emit_data).pack(side=LEFT, padx=5, pady=5)
Button(dataFreq, text ='Stop', command= stop_data).pack(side=RIGHT, padx=5, pady=5)

fenetre.mainloop()

if player != None:
    player.stop()

if playerDual != None:
    playerDual.stop()

if emission_driver != None:
    emission_driver.stop()