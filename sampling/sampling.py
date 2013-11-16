# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 15, 2013

from __future__ import division
import numpy as np
import os
import pylab as pl
import scipy.signal as signal
from scipy.io import loadmat, wavfile
import time


def tone(f, L):
    return np.sin(2*np.pi*f*np.arange(L)/L)


def downsample(x, M):
    return x[::M]


def reconstruct(L, Y):
    N = len(Y)
    YY = np.hstack((Y[:N//2], np.zeros(L-N),
                    Y[(N//2):]))
    scaling = L/len(Y)
    return scaling*np.real(np.fft.ifft(YY))


def plot_pairs(x, X, signame="", orig=None, M=1):
    k = np.arange(len(X)) / len(X)
    pl.figure()
    pl.subplot(211)
    if orig is None:
        pl.plot(x)
        pl.ylabel(signame)
    else:
        missed = M - (len(orig) % M) - 1
        n = np.linspace(0, len(x)-1, len(orig)-missed)
        pl.plot(n, orig[:len(n)], label=signame[0])
        pl.hold(True)
        pl.plot(x, linestyle='o', marker='o', color='r', fillstyle="none",
                label=signame)
        pl.legend()
    pl.xlabel("samples")
    pl.subplot(212)
    pl.plot(k, np.abs(X))
    pl.xlabel("normalized frequencies")
    pl.ylabel("|{}|".format(signame.upper()))


def write_and_listen(fs, x, filename, signame="", plot_fft=True):
    # Write wav file.
    wavfile.write(filename+".wav", fs, x)
    try:
        # Only for Mac.
        os.system("afplay {}.wav".format(filename))
        print("Wait ...")
        time.sleep(2)
    except:
        pass
    # FFT.
    X = np.fft.fft(x)
    if plot_fft:
        pl.figure()
        pl.plot(np.arange(len(X))/len(X), np.abs(X))
        pl.xlabel("normalized frequencies")
        pl.ylabel("|{}|".format(signame).upper())
    return X


def example1():
    # Squared sinc.
    x = np.arange(-499, 501) / 20
    y = np.sinc(x)**2
    # FFT of squared sinc.
    Y = np.fft.fft(y)
    plot_pairs(y, Y, "y")

    # Downsample by 5.
    y5 = downsample(y, 5)
    Y5 = np.fft.fft(y5)
    plot_pairs(y5, Y5, signame="y5", orig=y, M=5)

    # Downsample by 10.
    y10 = downsample(y, 10)
    Y10= np.fft.fft(y10)
    plot_pairs(y10, Y10, signame="y10", orig=y, M=10)

    # Downsample by 20.
    y20 = downsample(y, 20)
    Y20= np.fft.fft(y20)
    plot_pairs(y20, Y20, signame="y20", orig=y, M=20)

    # Reconstruct.
    yy5 = reconstruct(len(Y), Y5)
    yy10 = reconstruct(len(Y), Y10)
    yy20 = reconstruct(len(Y), Y20)
    pl.figure()
    pl.subplot(311)
    pl.plot(yy5, label='yy5')
    pl.hold(True)
    pl.plot(y, "r--", label="y")
    pl.legend()
    pl.subplot(312)
    pl.plot(yy10, label='yy10')
    pl.hold(True)
    pl.plot(y, "r--", label="y")
    pl.legend()
    pl.subplot(313)
    pl.plot(yy20, label='yy20')
    pl.hold(True)
    pl.plot(y, "r--", label="y")
    pl.legend()
    pl.xlabel("samples")


def example2():
    L = 1000
    x = np.hstack((tone(40, L), np.zeros(L),
                   tone(80, L), np.zeros(L),
                   tone(160, L)))
    print("Original tones")
    _ = write_and_listen(9000, x, "tones", "x")

    # Downsample by 2.
    x2 = downsample(x, 2)
    print("Downsampled by 2")
    X2 = write_and_listen(9000, x2, "tones_ds2", "x2")
    # Reconstruct.
    xx2 = reconstruct(len(x), X2)
    print("Reconstructed (2)")
    _ = write_and_listen(9000, xx2, "tones_rc2", "xx2", plot_fft=False)

    # Downsample by 10.
    print("Downsampled by 10")
    x10 = downsample(x, 10)
    X10 = write_and_listen(9000, x10, "tones_ds10", "x10")
    # Reconstruct.
    xx10 = reconstruct(len(x), X10)
    print("Reconstructed (10)")
    _ = write_and_listen(9000, xx10, "tones_rc10", "xx10", plot_fft=False)


def example3():
    jingle = loadmat("jingle.mat")
    fs = jingle['Fs'][0][0]
    jingle = jingle['jingle'][0]

    print("Jingle")
    JINGLE = write_and_listen(fs, jingle, "jingle", "jingle")

    # Downsample by 2.
    jingle2 = downsample(jingle, 2)
    print("Jingle downsampled by 2")
    JINGLE2 = write_and_listen(fs, jingle2, "jingle_ds2", plot_fft=False)
    # Reconstruct.
    jjingle2 = reconstruct(len(JINGLE), JINGLE2)
    print("Reconstructed (2)")
    _ = write_and_listen(fs, jjingle2, "jingle_rc2", plot_fft=False)

    # Downsample by 10.
    jingle10 = downsample(jingle, 10)
    print("Jingle downsampled by 10")
    JINGLE10 = write_and_listen(fs, jingle10, "jingle_ds10", plot_fft=False)
    # Reconstruct.
    jjingle10 = reconstruct(len(JINGLE), JINGLE10)
    print("Reconstructed (10)")
    _ = write_and_listen(fs, jjingle10, "jingle_rc10", plot_fft=False)

    # Low pass filter jingle (cutoff 0.05).
    N1 = np.int(0.05 * len(JINGLE))
    N2 = np.int(0.95 * len(JINGLE))
    JINGLE_LP = JINGLE
    JINGLE_LP[N1:N2+1] = 0
    # Low pass version of the jingle.
    jingle_lp = np.real(np.fft.ifft(JINGLE_LP))
    print("Lowpass filtered jingle")
    _ = write_and_listen(fs, jingle_lp, "jingle_lp", "jingle_lp")

    # Downsample lowpass version by 10.
    jingle_lp10 = downsample(jingle_lp, 10)
    print("Lowpass filtered jingle downsampled by 10")
    JINGLE_LP10 = write_and_listen(
        fs, jingle_lp10, "jingle_lp_ds10", plot_fft=False)
    # Reconstruct.
    jjingle_lp10 = reconstruct(len(JINGLE), JINGLE_LP10)
    print("Reconstructed (10 lowpass version)")
    _ = write_and_listen(fs, jjingle_lp10, "jingle_lp_rc10", plot_fft=False)


if __name__ == "__main__":
    print("--> First example (see the aliasing)")
    example1()
    print("    Wait until end for the figures!")
    time.sleep(1)
    print("--> Second example (hear the aliasing)")
    example2()
    time.sleep(1)
    print("--> Third  example (jingle)")
    example3()
    pl.show()
