# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 20, 2013

from __future__ import division
import numpy
import os
import pylab as pl
import scipy.signal as signal
from scipy.io import loadmat, wavfile


def quantize(x, R, A=1):
    D = 2*A / 2**R
    xQuant = D * (numpy.floor(x/D) + 0.5)
    errQuant = x - xQuant
    return xQuant, errQuant


def write_and_play(fs, x, filename):
    # Write wav file.
    wavfile.write(filename+".wav", fs, x)
    try:
        # Only for Mac.
        print(filename)
        os.system("afplay {}.wav".format(filename))
    except:
        pass


def example1():
    # Two period sawtooth signal between -A and A.
    A = 1
    x = numpy.arange(-A+0.02, 1+0.02, 0.04)
    x = numpy.hstack((x, x))
    numberBits = (3, 2)
    for R in numberBits:
        xQuant, errQuant = quantize(x, R)
        pl.figure()
        pl.subplot(211)
        pl.title("numberBits = {}".format(R))
        pl.plot(x,label='x')
        pl.hold(True)
        pl.plot(xQuant, linestyle='o', marker='o', color='r',
                fillstyle="none", label="xQuant")
        pl.legend()
        pl.subplot(212)
        pl.plot(errQuant, linestyle='o', marker='o', color='r',
                fillstyle="none")
        pl.xlabel("samples")
        pl.ylabel("errorQuant")
        pl.ylim(-0.2, 0.2)


def example2():
    # Two period sinusoid between -A and A.
    A = 1
    x = numpy.sin(2*numpy.pi*numpy.arange(0, 100, 2)/100)
    x = numpy.hstack((x, x))
    numberBits = (3, 2)
    for R in numberBits:
        xQuant, errQuant = quantize(x, R)
        pl.figure()
        pl.subplot(211)
        pl.title("numberBits = {}".format(R))
        pl.plot(x,label='x')
        pl.hold(True)
        pl.plot(xQuant, linestyle='o', marker='o', color='r',
                fillstyle="none", label="xQuant")
        pl.legend()
        pl.subplot(212)
        pl.plot(errQuant, linestyle='o', marker='o', color='r',
                fillstyle="none")
        pl.xlabel("samples")
        pl.ylabel("errorQuant")
        pl.ylim(-0.2, 0.2)

    # Generate a 1000 period sinusoid between -1 and 1.
    x = numpy.sin(2*numpy.pi*numpy.arange(10000)/10)
    # Quantize with 3 bits.
    xQuant, _ = quantize(x, 3)
    write_and_play(8192, x, "sine_orig")
    write_and_play(8192, xQuant, "sine_quantized_3-bits".format(R))


def example3():
    jingle = loadmat("jingle.mat")
    fs = jingle['Fs'][0][0]
    jingle = jingle['jingle'][0]
    
    max_value = numpy.max(jingle)
    min_value = numpy.min(jingle)
    dyn_range = max_value - min_value
    scaling_factor = 2 / dyn_range
    offset = -1 - scaling_factor * min_value
    
    jingle_normalized = scaling_factor * jingle + offset
    write_and_play(fs, jingle_normalized, "jingle")
    # Quantize with 3 bits
    jingleQuant, _ = quantize(jingle_normalized, 3)
    write_and_play(fs, jingleQuant, "jingle_quantized_3-bits")
    # Quantize with 2 bits
    jingleQuant, _ = quantize(jingle_normalized, 2)
    write_and_play(fs, jingleQuant, "jingle_quantized_2-bits")


if __name__ == "__main__":
    example1()
    example2()
    example3()
    pl.show()

