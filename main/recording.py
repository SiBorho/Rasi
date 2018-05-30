#recording
"""
Created on 2018.05.24

@author: S.Borho
"""

import pyaudio
import math
import struct
import wave
import time
import os
import speech_to_text as stt

Threshold = 10

SHORT_NORMALIZE = (1.0/200)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2
TIMEOUT_LENGTH = 3


class Recorder:
    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
            rms = math.pow(sum_squares / count, 0.5)

            return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        print('**** start recording ****')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        filename = os.path.join('output.wav')
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()

    def listen(self, rec):
        while rec:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                rec = False
                self.record()
def start():
    rec = True
    a = Recorder()
    a.listen(rec)
    stt.sendIBM()
