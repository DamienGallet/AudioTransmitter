import pyaudio
import wave
import math

#CHUNK = 9000
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
N = 44100

def goetzl(datas, f):
    #print(f)
    k = round(0.5+(N*f)/RATE)
    #print(k)
    CHUNK = len(datas[0])
    w = (2*math.pi/CHUNK)*k
    cosine = math.cos(w)
    goetrl_param = {
        'cosine' : cosine,
        'sine' : math.sin(w),
        'coeff' : 2.0*cosine
    }

    print("* start goetzl")
    #print(goetrl_param)

    for data in datas:
        currentMagnitude = computeFrame(data,goetrl_param)
    
    return currentMagnitude    

    print("* end goetzl")

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
