# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 06, 2013

from __future__ import division
import numpy
import pylab
import scipy.signal as signal
from scipy.io import loadmat, wavfile


def leaky_integrator(M, N):
    lmb = (M - 1) / M
    return (1 - lmb) * lmb**numpy.arange(N)


def example1():
    x1 = numpy.sin(2*numpy.pi*40*numpy.arange(1000)/1000)
    x2 = numpy.sin(2*numpy.pi*80*numpy.arange(1000)/1000)
    x = numpy.hstack((x1, x2))

    # Power of the noise.
    sigma2 = 0.1 
    # Gaussian noise.
    noise = numpy.sqrt(sigma2)*numpy.random.randn(2000)
   
    # Noisy version of x.
    xNoisy = noise + x

    h = leaky_integrator(10, 100)
    y = signal.convolve(xNoisy, h, mode="valid")

    pylab.figure()
    pylab.subplot(211)
    pylab.hold(True)
    pylab.plot(xNoisy, 'r', label="noisy")
    pylab.plot(x, label="clean")
    pylab.legend()
    pylab.subplot(212)
    pylab.hold(True)
    pylab.plot(y)
    pylab.title("filtered")

    nfft = len(xNoisy) - len(h) + 1
    XNoisy = numpy.fft.fft(xNoisy, nfft)
    H = numpy.fft.fft(h, nfft)
    Y = numpy.fft.fft(y, nfft)
    wn = numpy.arange(nfft) / nfft
    pylab.figure()
    pylab.subplot(311)
    pylab.plot(wn, numpy.abs(XNoisy))
    pylab.title("|XNoisy|")
    pylab.subplot(312)
    pylab.plot(wn, numpy.abs(H))
    pylab.title("|H|")
    pylab.subplot(313)
    pylab.plot(wn, numpy.abs(Y))
    pylab.title("|Y|")
    pylab.xlabel("normalized frequencies")
    pylab.show()


def example2():
    jingle = loadmat("jingle.mat")
    fs = jingle['Fs'][0][0]
    jingle = jingle['jingle'][0]
    wavfile.write("jingle_orig.wav", fs, jingle)

    sigma2 = 0.01
    noise = numpy.sqrt(sigma2)*numpy.random.randn(len(jingle))
    jingleNoisy = jingle + noise
    wavfile.write("jingle_noisy.wav", fs, jingleNoisy)

    h = leaky_integrator(10, 100)
    y = signal.convolve(jingleNoisy, h, mode="valid")
    wavfile.write("jingle_filtered.wav", fs, y)

    
    nfft = len(jingle) - len(h) + 1
    Jingle = numpy.fft.fft(jingle, nfft)
    Y = numpy.fft.fft(y, nfft)
    wn = numpy.arange(50000) / nfft
    pylab.figure()
    pylab.subplot(211)
    pylab.plot(wn, numpy.abs(Jingle[:50000]))
    pylab.title("|Jingle|")
    pylab.subplot(212)
    pylab.plot(wn, numpy.abs(Y[:50000]))
    pylab.title("|Y|")
    pylab.xlabel("normalized frequencies")
    pylab.show()


def example3():
    M = numpy.arange(10, 51, 10)
    x = numpy.random.randn(100)
    
    pylab.figure()
    pylab.plot(x)
    pylab.title("x")
    
    for m in M:
        h = (1 / m) * numpy.ones(m)
        y = signal.convolve(x, h, mode="valid")
        pylab.figure()
        pylab.plot(y)
        pylab.title("y, M = %d" % m)
    pylab.show()


if __name__ == "__main__":
    example1()
    example2()
    example3()
