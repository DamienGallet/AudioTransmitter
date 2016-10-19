import utilities as util
import record as rec

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
    
    for freq in range(10,10000,10):
        magn1 = rec.goetzl([data],freq)
        magn[freq] = [magn1]
        
        print(str(freq)+":"+str(magn1))
    util.write_file(magn,"bifreq100_155.csv")

def threshold_gen():
    magn = {}
    out=[]
    data = util.generate_frequency([300,125,700,740])
    for freq in range(10,1000,5):
        value = rec.goetzl([data],float(freq))
        print(value)
        magn[freq] = [value]
        out.append(value)

    plot2D(range(10,1000,5), out)

#data = util.generate_frequency([400])
#util.play_sound(data)
#bi_freq()
threshold_gen()
