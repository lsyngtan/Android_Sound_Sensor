import urllib.request
import scipy.io.wavfile
from scipy.fftpack import fft, fftfreq
import scipy.signal
import wave
import numpy as np
from pprint import pprint 
import struct
import matplotlib.pyplot as plt

size_audio = 268237

x = wave.open("C:/Users/Leeam/Documents/example.wav", 'rb')
print(x.getparams())

temp = x.readframes(size_audio)

format_float = '<' + str(size_audio) + 'i'

testResult = struct.unpack(format_float, temp)

nb = np.array(testResult)   
nm = np.max(np.abs(nb))
nsigf32 = (nb/nm).astype(np.float32)
pprint(nsigf32)
scipy.io.wavfile.write("C:/Users/Leeam/Documents/newexample.wav", 8000, nsigf32)

datafft = fft(nsigf32)
fftabs = abs(datafft)

freqs = fftfreq(nsigf32.shape[0], 1/8000)

peak = scipy.signal.find_peaks(fftabs)

plt.plot(nsigf32)
plt.show()

plt.plot(fftabs[:int(freqs.size/2)])
plt.show()

plt.plot(freqs, fftabs)
plt.show()

plt.xlim( [10, 8000/2] )
plt.xscale( 'log' )
plt.grid( True )
plt.xlabel( 'Frequency (Hz)' )
plt.plot(freqs[:int(freqs.size/2)],fftabs[:int(freqs.size/2)])
plt.show()