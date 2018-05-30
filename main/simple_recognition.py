# simple_recognition.py
"""
Created on 2018.05.23

@author: S.Borho
"""


import pyaudio
import numpy as np
import scipy.signal as win
import numpy as np
import wave
import recording as rec
import matplotlib.pyplot as plt
import sys


CHANNELS = 1
SAMPLEFREQ = 44100
FORMAT = pyaudio.paInt16
FRAMESIZE = 44100
NOFFRAMES = 2
WOERTER = ['TJ_Record', 'TJ_END']

def save_wav(data, filename, fs=SAMPLEFREQ, ch=CHANNELS, dsize=2):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(dsize)
    wf.setframerate(SAMPLEFREQ)
    wf.writeframes(data)
    wf.close()
    return

def save_numpy_array_wav(decoded, filename, dsize=2):
    data = np.array(decoded, dtype=np.int16).tobytes()
    save_wav(data, filename, dsize)
    return

def my_plot(xData, yData, title='', xLabel='', yLabel='', filename='', grid=True):
    myDpi=100
    fig, ax = plt.subplots(figsize=(800/myDpi, 600/myDpi), dpi=myDpi)
    ax.plot(xData, yData)
    if grid:
        ax.grid()
    if title is not '':
        ax.set_title(title)
    if xLabel is not '':
        ax.set_xlabel(xLabel)
    if yLabel is not '':
        ax.set_ylabel(yLabel)
    ax.autoscale(enable=True, axis='x', tight=True)
    if filename is not '':
        fig.savefig(filename, transparent=True, pad_inches=0, dpi=myDpi)
        plt.close(fig)
    return


def aufnahme(name=''):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=SAMPLEFREQ, input=True,
                    frames_per_buffer=FRAMESIZE)
    data = stream.read(NOFFRAMES * FRAMESIZE)
    decoded = np.fromstring(data, 'Int16');
    if name is not '':
        np.savetxt(name + '.csv', decoded)
    stream.stop_stream()
    stream.close()
    p.terminate()
    return decoded

def trigger(totrigger, name=''):
    LIMIT = 800
    triggered = np.zeros(FRAMESIZE)
    for i in range(totrigger.shape[0]):
        if np.abs(totrigger[i]) > LIMIT:
            break
    for j in range(triggered.shape[0]):
        if i + j < totrigger.shape[0]:
            triggered[j] = totrigger[i + j]
    if name is not '':
        np.savetxt(name + '_triggered.csv', triggered)
    return triggered


def windowing(data, WINSIZE=512):
    spec = np.zeros(WINSIZE)
    lastWinEnd = 2**(len(data) - 1).bit_length()
    window = win.gaussian(WINSIZE, std = WINSIZE/4)
    cnt = 0
    for i in range(0,lastWinEnd-511, 256):
        tmp = data[i:i+WINSIZE]
        if len(tmp) is not WINSIZE:
            vals = tmp
            tmp = np.zeros(WINSIZE, np.float32)
            for i in range(0, len(vals)):
                tmp[i] = vals[i]
        tmp = np.multiply(tmp,window)
        tmp = np.abs(np.fft.fft(tmp))
        spec +=tmp
        cnt += 1
    spec = spec / cnt
    return spec


def kokoeff(f, g):
    sum_fk = 0
    sum_gk = 0
    n = f.shape[0]
    for k in f:
        sum_fk += k
    for k in g:
        sum_gk += k
    my_f = sum_fk / n
    my_g = sum_gk / n
    sum = 0
    for k in range(n):
        sum += (f[k]-my_f)*(g[k]-my_g)
    sigma_fg = sum / n
    sum_sigf = 0
    for k in f:
        sum_sigf += (k - my_f)**2
    sigma_f = np.sqrt(sum_sigf / (n - 1))
    sum_sigg = 0
    for k in g:
        sum_sigg += (k - my_g)**2
    sigma_g = np.sqrt(sum_sigg / (n - 1))
    r_fg = sigma_fg / (sigma_f * sigma_g)
    return r_fg


def recordCommands():
    for wort in WOERTER:
        print(wort)
        for i in range(5):
            print('Aufnahme ' + str(i+1))
            data = aufnahme()
            triggered = trigger(data, 'reference_' + wort + str(i+1))

    spec = {}
    for wort in WOERTER:
        spec[wort] = 0
        n = 0
        for i in range(1):
            win = windowing(np.genfromtxt('reference_'+ wort + str(i+1)
            + '_triggered.csv', delimiter=','))
            spec[wort] = np.add(spec[wort], win)
            n += 1
        mean = spec[wort] / n
        Y = mean
        N = len(Y)/2 + 1
        X = np.linspace(0, SAMPLEFREQ/2, N, endpoint=True)
        my_plot(X[:20], np.abs(Y[:20]/((2**15)-1)), title=wort,
                       xLabel = 'Frequency[$Hz$]', yLabel='Amplitude [$V^{*}$]',
                       filename='referencespectrum_' + wort, grid=True)
        np.savetxt('referencespectrum_' + wort + '.csv', mean)


def recognition(data):
    ref = {}
    max = -1
    for wort in WOERTER:
         ref[wort] = np.genfromtxt('references/referencespectrum_'+ wort + '.csv', delimiter=',')
         koeff = kokoeff(ref[wort], windowing(data))
         if koeff > max:
             max = koeff
             befehl = wort
    if max > 0.95:
        return befehl
    else:
        return "..."


def simple_recognition():
    while True:
        data = aufnahme()
        triggered = trigger(data, 'references/Test')
        for wort in WOERTER:
            totest = np.genfromtxt('references/Test_triggered.csv')
            befehl = recognition(totest)
        print("Befehl: " + befehl)
        if befehl == "TJ_Record":
            rec.start()
        elif befehl == "TJ_END":
            rec.start()
