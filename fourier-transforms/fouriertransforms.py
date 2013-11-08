# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Oct 20, 2013

import numpy
import pylab

# To read mat file.
import scipy.io


def dftmtx(N):
    """DFT Matrix."""
    M = numpy.asmatrix(numpy.arange(N))
    return numpy.exp((-1j * 2 * numpy.pi / N) * M.T * M)


def unit_step(L, N=0):
    """u[n] = 1 for 0 <= n <= L-1.
            = 0 for L <= n <= max(N-1, L).
    """
    N = max(N, L)
    return numpy.hstack((numpy.ones(L), numpy.zeros(N - L)))


def plot_dt_signal(x, title=None):
    """Plot discrete time signal."""
    pylab.figure()
    pylab.stem(range(len(x)), x)
    pylab.title(title)
    pylab.xlabel("samples")


def plot_dft_samples(X, title=None, hide_phase_errors=False):
    k = numpy.arange(len(X)) / len(X)
    pylab.figure()
    pylab.subplot(2,1,1)
    pylab.title(title)
    pylab.stem(k, numpy.abs(X))
    pylab.ylabel("magnitude")
    pylab.subplot(2,1,2)
    if hide_phase_errors:
        real_parts = numpy.array(
            [n if numpy.abs(n) > 1e3 * numpy.finfo(float).eps \
             else 0.0 for n in numpy.real(X)])
        imag_parts = numpy.array(
            [n if numpy.abs(n) > 1e3 * numpy.finfo(float).eps \
             else 0.0 for n in numpy.imag(X)])
        pylab.stem(k, numpy.arctan2(imag_parts, real_parts))
    else:
        pylab.stem(k, numpy.angle(X))
    pylab.ylabel("phase in rads")
    pylab.xlabel("normalized frequencies")


def plot_dft(X, title=None):
    k = numpy.arange(len(X)) / len(X)
    pylab.figure()
    pylab.title(title)
    pylab.plot(k, numpy.abs(X))
    pylab.ylabel("magnitude")
    pylab.xlabel("normalized frequencies")


def _generate_sin_wave(f, N, A=1.0):
    return A * numpy.sin(2.0 * numpy.pi * f * numpy.arange(N) / N)


def example1():
    # Genreate signal.
    N = 128
    x1 = unit_step(64, N)
    # Get the DFT matrix.
    WN = dftmtx(N)
    # DFT.
    X1 = numpy.squeeze(numpy.asarray(WN * numpy.asmatrix(x1).T))
    plot_dt_signal(unit_step(64, 128), "x1")
    plot_dft_samples(X1, "DFT of x1")
    plot_dft_samples(
        X1, "DFT of x1 with numerical errors in phase hidden", True)
    # Inverse DFT (synthesize x1)
    x1_s = numpy.squeeze(numpy.asarray((
        1.0 / N) * WN.H * numpy.asmatrix(X1).T))
    plot_dt_signal(numpy.real(x1_s), "x1 via inverse DFT")


def example2():
    x = scipy.io.loadmat("frequencyRepresentation.mat")['x'][0]
    pylab.figure()
    pylab.plot(x[:500])
    pylab.xlabel("samples")
    pylab.ylabel("x")
    # DFT.
    X = numpy.squeeze(numpy.asarray(
        dftmtx(4000) * numpy.asmatrix(x).T))
    plot_dft(X, "Two sinusoids")


def example3():
    """Three tones."""
    x1 = _generate_sin_wave(40, 1000)
    x2 = _generate_sin_wave(80, 1000)
    x3 = _generate_sin_wave(160, 1000)
    z = numpy.zeros(1000)
    x = numpy.hstack((x1, z, x2, z, x3))
    N = len(x)
    WN = dftmtx(N)
    X = numpy.squeeze(numpy.asarray(WN * numpy.asmatrix(x).T))
    plot_dft(X, "Three tones")
    # Reduce base.
    WN_reduced = numpy.delete(WN, range(600, 4400), 0)
    X_approx = WN_reduced * numpy.asmatrix(x).T
    x_approx = (1.0 / N) * (WN_reduced.H * X_approx)
    X = numpy.squeeze(numpy.asarray(WN * x_approx))
    plot_dft(X, "Approximating with limited base causes loss of one sinusoid")


def example4():
    """FFT"""
    N = 4000
    x = _generate_sin_wave(40, N) + _generate_sin_wave(80, N)
    M = N
    X = numpy.fft.fft(x, M)
    plot_dft(X, "FFT of input without truncation")
    M = 500
    X = numpy.fft.fft(x, M)
    plot_dft(X, "FFT of input with truncation")
    M = 50
    X = numpy.fft.fft(x, M)
    plot_dft(X, "FFT of input with more truncation")
    xM = numpy.fft.ifft(X, M)
    M = 4000
    X = numpy.fft.fft(xM, M)
    plot_dft(X, "A case where increasing dft size has no other advantage "
             "than nicer plot")


if __name__ == "__main__":
    example1()
    example2()
    example3()
    example4()
    pylab.show()
