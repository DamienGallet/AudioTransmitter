import utilities as util
import record as rec
import listener as listener

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

def bi_freq():
    freq1 = 1000
    freq2 = 1550
    magn = {}
    data = util.generate_frequency([freq1, freq2])
    
    for freq in range(600,1400,1):
        magn1 = rec.goetzl([data],freq)
        magn[freq] = [magn1]
        
        print(str(freq)+":"+str(magn1))
    util.write_file(magn,"bifreq100_155.csv")

def threshold_gen():
    magn = {}
    out=[]
    rangeData = range(100,3000,1)
    data = util.generate_frequency([900,1000,1100,1200,1300,1400])
    for freq in rangeData:
        value = rec.goetzl([data],float(freq))
        print(value)
        magn[freq] = [value]
        out.append(value)

    plot2D(rangeData, out)

def listen_and_speak():
    #frames = util.listen(1000)
    frames = util.listen_and_raw_record()
    plot2D(range(len(frames)), frames)
    out=[]
    anabeg =100
    anaend = 10000
    for freq in range(anabeg,anaend,10):
        value = rec.goetzl([frames],float(freq))
        print(value)
        out.append(value)

    plot2D(range(anabeg,anaend,10), out)

def result_callback(magns):
    threshold = 100000000000
    for key in magns.keys:
        current_magn = magns[key]
        if magn > threshold:
            print('Frequency '+key+'Hz detected ('+magn+')')
        else:
            print('Frequency '+key+'Hz NOT detected ('+magn+')')

def generate_standard_dtmf(nb):

    freq = [[0,0],
            [1209,697],
            [1336,697],
            [1477,697],
            [1209,770],
            [1336,770],
            [1477,770],
            [1209,852],
            [1336,852],
            [1477,852]]
    util.generate_and_emit_frequency(freq[nb])

def detect_frequencies(frequencies, result):
    util.listen_continuously(rec.goertzel_driver, 44100, 100, frequencies, result)

def compute_frequencies(frequencies):
    util.listen_continuously(compute_detected, 44100, 100, frequencies, result_callback)

def compute_detected(data,frequencies,toto):
    plot2D(range(len(data)), data)
    out=[]
    anabeg =100
    anaend = 10000
    for freq in range(anabeg,anaend,10):
        value = rec.goetzl(data,freq)
        print(freq)
        print(value)
        out.append(value)

    plot2D(range(anabeg,anaend,10), out)

#util.listen_and_raw_record()
#listen_and_speak()
#data = util.generate_frequency([400])
#util.play_sound(data)
#bi_fr
#compute_frequencies([1000])




##############################################################################
#                        LET'S BEGIN NOW !!                                  #
##############################################################################

current_listener = listener.Listener(rec.goetzl,1000)
util.listen_continuously(current_listener, 48000, 10000)
