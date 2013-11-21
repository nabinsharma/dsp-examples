# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 20, 2013

from __future__ import division
import numpy
import os
import pylab as pl
import scipy.signal as signal
from scipy.io import wavfile


def nextpow2(n):
  return int(numpy.ceil(numpy.log2(n)))


def uniform_noise(nr, nc=1, a=0.0, b=1.0):
  return numpy.squeeze(a + (b-a) * numpy.random.rand(nr, nc))


def gaussian_noise(nr, nc=1, m=0.0, sigma2=1.0):
  return numpy.squeeze(m + numpy.sqrt(sigma2) * numpy.random.randn(nr, nc))


def leaky_integrator(K=10, L=100):
  lmb = (K-1) / K
  return (1 - lmb) * lmb**numpy.arange(L)

    
def write_and_play(fs, x, filename):
  # Write wav file.
  wavfile.write(filename+".wav", fs, x)
  try:
    # Only for Mac.
    print(filename)
    os.system("afplay {}.wav".format(filename))
  except:
    pass


def main(N, M=1):
  # Generate uniform noise (each column is a realization).
  noise1 = uniform_noise(N, M, a=-1.7, b=1.7)
  # Generate Gaussian noise (each column is a realization).
  noise2 = gaussian_noise(N, M)
  write_and_play(8192, noise1[:, 0], "noise1")
  write_and_play(8192, noise2[:, 0], "noise2")
  pl.figure()
  pl.subplot(211)
  pl.stem(noise1[:100, 0])
  pl.ylabel("noise1")
  pl.subplot(212)
  pl.stem(noise2[:100, 0])
  pl.ylabel("noise2")
  pl.xlabel("samples")
  
  Noise1 = numpy.fft.fft(noise1, n=2**nextpow2(N), axis=0)
  Noise2 = numpy.fft.fft(noise2, n=2**nextpow2(N), axis=0)
  psdNoise1 = numpy.mean(numpy.abs(Noise1)**2, 1) / N
  psdNoise2 = numpy.mean(numpy.abs(Noise2)**2, 1) / N
  pl.figure()
  pl.subplot(211)
  pl.plot(numpy.arange(len(psdNoise1))/len(psdNoise1), psdNoise1)
  pl.ylim(0, 1.5)
  pl.ylabel("psdNoise1")
  pl.subplot(212)
  pl.plot(numpy.arange(len(psdNoise2))/len(psdNoise2), psdNoise2)
  pl.ylim(0, 1.5)
  pl.ylabel("psdNoise2")
  pl.xlabel("normalized frequencies")
  
  pl.figure()
  pl.subplot(211)
  pl.hist(noise1[:, 0], bins=50)
  pl.ylabel("noise1 recurrences")
  pl.subplot(212)
  pl.hist(noise2[:, 0], bins=50)
  pl.ylabel("noise2 recurrences")
  pl.xlabel("values")
  
  # Leaky integrator (filter).
  h = leaky_integrator()
  H = numpy.fft.fft(h, 2**nextpow2(N))
  absH2 = numpy.abs(H)**2
  
  # Filter noise.
  N2 = N -len(h) + 1
  yy2 = numpy.zeros((N2, M))
  for i in range(M):
    yy2[:, i] = numpy.convolve(noise2[:, i], h, mode="valid")
  write_and_play(8192, yy2[:, 0], "filtered_noise2")
  psdY2 = numpy.mean(numpy.abs(numpy.fft.fft(
    yy2, n=2**nextpow2(N2), axis=0))**2, 1) / N2
  
  pl.figure()
  pl.subplot(311)
  pl.plot(numpy.arange(len(psdNoise2))/len(psdNoise2), psdNoise2)
  pl.ylim(0, 1.5)
  pl.ylabel("psdNoise2")
  pl.subplot(312)
  pl.plot(numpy.arange(len(absH2))/len(absH2), absH2)
  pl.ylim(0, 1.5)
  pl.ylabel("squareMagH")
  pl.subplot(313)
  pl.plot(numpy.arange(len(psdY2))/len(psdY2), psdY2)
  pl.ylim(0, 1.5)
  pl.ylabel("psdY2")
  pl.xlabel("normalized frequencies")
  
  pl.show()
  
if __name__ == "__main__":
  # Number of samples in a realization.
  N = 10000
  # Work with 5000 realizations (M).
  main(N, M=1000)
