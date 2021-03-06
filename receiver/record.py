import pyaudio
import wave
import math
import constants as const

#CHUNK = 9000
FORMAT = pyaudio.paInt16
CHANNELS = 2

def plot2D(x,y):
    import matplotlib.pyplot as plt
    plt.plot(x,y)
    plt.ylabel('Response')
    plt.show()

def plot(data):
    import matplotlib.pyplot as plt
    plt.plot(data)
    plt.ylabel('some numbers')
    plt.show()

def goertzel_driver(data, frequencies,result_callback):
    result_array = {}
    for frequency in frequencies:
        result_array[frequency] = goetzl(data,frequency)
    result_callback(result_array)   

def goertzel_preconf_driver(data):
    plot2D(range(len(data)), data)
    out=[]
    anabeg =100
    anaend = 10000
    for freq in range(anabeg,anaend,10):
        value = goetzl(data,freq)
        print(freq)
        print(value)
        out.append(value)

    plot2D(range(anabeg,anaend,10), out)

def goetzl(datas, f):
    #print(f)
    N = len(datas)
    k = int(0.5+(f/2*N)/const.FREQUENCY)
    w = (2*math.pi/N)*k
    cosine = math.cos(w)
    goetrl_param = {
        'cosine' : cosine,
        'sine' : math.sin(w),
        'coeff' : 2.0*cosine
    }
    #print(goetrl_param)

    currentMagnitude = computeFrame(datas,goetrl_param)
    
    print(int(currentMagnitude))
    return currentMagnitude

def computeSample(sample, q0, q1, q2,goetrl_param):
    coeff = goetrl_param['coeff']
    q0 = coeff*q1 - q2 + sample
    q2 = q1
    q1 = q0
    return (q0,q1,q2)

def computeFrame(data,goetrl_param):
    q0 = 0.0
    q1 = 0.0
    q2 = 0.0

    for sample in data :
        (q0, q1, q2) = computeSample(sample, q0, q1, q2,goetrl_param)

    cosine = goetrl_param['cosine']
    sine = goetrl_param['sine']
    real = (q1 - q2 * cosine)
    imag = (q2 * sine)
    magnitude = real**2 + imag**2
    return magnitude
