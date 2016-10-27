import pyaudio
import wave
import math
import constants as const
from ploting_utilities import *


def goetzl_driver(datas, frequencies, threshold):
    results = {}

    for frequency in frequencies:
        results[frequency] = (goetzl(datas, frequency)>threshold)

    return results

def goetzl_driver_continuous(datas, frequencies, threshold):
    results = {}

    for frequency in frequencies:
        results[frequency] = goetzl(datas, frequency)

    return results

def goetzl_monitoring(datas, frequencies, threshold):
    results = []
    xValues = range(frequencies[0],frequencies[1],frequencies[2])
    for frequency in xValues:
        results.append(goetzl(datas,frequency))

    plot2D(xValues,results)


def goetzl(datas, f):
    #print(f)
    N = len(datas)
    k = int(0.5+(f*N)/const.FREQUENCY)
    w = (2*math.pi/N)*k
    cosine = math.cos(w)
    goetrl_param = {
        'cosine' : cosine,
        'sine' : math.sin(w),
        'coeff' : 2.0*cosine
    }

    currentMagnitude = computeFrame(datas,goetrl_param)
    print (currentMagnitude)
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