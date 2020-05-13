import json
import http.client
from _util import get_sensor
import urllib.request
import math
import scipy.io.wavfile
from scipy.fftpack import fft, fftfreq
import numpy as np
import struct

framerate = 8000
time_streaming = 5 #seconds
stream_length = time_streaming * 4
nframes = int(stream_length * framerate / 4)
file_location = "C:/Users/Leeam/Documents/audio_example/otherwave.wav"

# Configuration section
UBEAC_URL = 'hub.ubeac.io'
GATEWAY_URL = 'http://myworkspace.hub.ubeac.io/myPC'
DEVICE_FRIENDLY_NAME = 'Android Sound Detector'

with urllib.request.urlopen('http://10.10.10.30:8080/wav') as r:
    audio_start = r.read(44)
    while True:
        audio_add = r.read(framerate)
        for i in range(stream_length - 1):
            audio_add += r.read(framerate)
    
        format_float = '<' + str(nframes) + 'i'
        testResult = struct.unpack(format_float, audio_add)

        nb = np.array(testResult)  
        nm = np.max(np.abs(nb))
        sigf32 = (nb/nm).astype(np.float32)
        scipy.io.wavfile.write(file_location, framerate, sigf32)
        rate, data = scipy.io.wavfile.read(file_location)        

        rms_amp = np.sqrt(np.mean(np.square(data)))
        logrms_amp = 20 * math.log10(rms_amp)
        
        Amplitude = get_sensor("Average Amplitude", {"Amplitude": str(logrms_amp)})

        
        freqs = fftfreq(data.shape[0], 1/rate)
        freqspos = freqs[:int(freqs.size/2)]
        datafft = fft(data)
        fftabs = abs(datafft)[:int(freqs.size/2)]

        peakfreq = np.max(fftabs)
        locmaxfreq = np.argmax(fftabs)  
        freqmax = freqspos[locmaxfreq]     

        Frequency = get_sensor("Frequency", {"Max Frequency" : str(freqmax)})

        Peak = get_sensor("Max Peak", {"Amplitude" : str(locmaxfreq)})

        sensors = []  
        sensors.append(Amplitude)
        sensors.append(Frequency)
        sensors.append(Peak)

        device = [{
            'id': "Android Microphone",
            'sensors': sensors
        }]

        connection = http.client.HTTPSConnection(UBEAC_URL)
        connection.request('POST', GATEWAY_URL, json.dumps(device))
        response = connection.getresponse()
        print(response.read().decode())