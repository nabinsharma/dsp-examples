# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 07, 2013

from __future__ import division
import numpy
import pylab
import scipy.signal as signal

F0 = 697.0
FS = 2000.0
T = 0.1
LMB = 0.98


def dt_signal(f1, f2):
    t = numpy.arange(0.0, T + 1/FS, 1/FS)
    x = numpy.sin(2*numpy.pi*f1*t) + numpy.sin(2*numpy.pi*f2*t)
    pylab.figure()
    pylab.plot(t, x)
    pylab.title('x')
    return x


def example_iir(x):
    w0 = 2*numpy.pi*F0/FS
    poles = LMB*numpy.array([numpy.exp(1j*w0), numpy.exp(-1j*w0)])

    # Plot pole diagram of the filter.
    pylab.figure()
    pylab.hold(True)
    pylab.grid(True)
    for pole in poles:
        pylab.plot(pole.real, pole.imag, "xr", markersize=10)
    unit_circ = numpy.exp(1j*numpy.arange(0.0, 1.0, 0.01)*2*numpy.pi)
    pylab.plot(unit_circ.real, unit_circ.imag, 'b')
    pylab.xlabel("real")
    pylab.ylabel("imag")
    pylab.axis("equal")

    # Filter signal.
    b = numpy.array([1.0])
    a = numpy.array([1.0, -2*LMB*numpy.cos(w0), LMB**2])
    y = signal.lfilter(b, a, x)

    # Plot the filtered signal.
    pylab.figure()
    pylab.grid(True)
    pylab.plot(y)
    pylab.title("y, using iir")

    # Plot the magnitude of the DFT/DFS of the filtered signal.
    Y = numpy.fft.fft(y);
    pylab.figure()
    pylab.grid(True)
    pylab.plot(numpy.arange(len(Y))/len(Y), numpy.abs(Y))
    pylab.title("|Y|, using iir")


def example_fir(x):
    bands = (1/FS) * numpy.array([0, F0-130, F0-30, F0+30, F0+130, FS/2])
    desired = [0, 1, 0]
    df, dp, ds  = bands[2] - bands[1], 0.1, 0.05
    numtaps = int(numpy.ceil(1 - (10*numpy.log10(dp*ds) + 13) /
                             (2.324*2*numpy.pi*df)) + 1)
    b = signal.remez(numtaps, bands, desired, weight=[1, ds/dp, 1])

    # Filter signal.
    y = signal.lfilter(b, [1], x)

    # Plot the filtered signal.
    pylab.figure()
    pylab.grid(True)
    pylab.plot(y)
    pylab.title("y, using fir")

    # Plot the magnitude of the DFT/DFS of the filtered signal.
    Y = numpy.fft.fft(y);
    pylab.figure()
    pylab.grid(True)
    pylab.plot(numpy.arange(len(Y))/len(Y), numpy.abs(Y))
    pylab.title("|Y|, using fir")


if __name__ == "__main__":
    x = dt_signal(697.0, 1209.0)
    example_iir(x)
    example_fir(x)
    pylab.show()
