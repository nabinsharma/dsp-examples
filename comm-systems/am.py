# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Dec 15, 2013

import numpy as np
import pylab as pl
import scipy.io as sio


def am(sig_msg, sig_car, mod_index, sampling_freq,
       selected_time_samples=None, selected_freq_samples=None):
  sig_mod = (1 + mod_index * sig_msg) * sig_car

  # Spectrums.
  SIG_MSG = np.fft.fft(sig_msg)
  SIG_CAR = np.fft.fft(sig_car)
  SIG_MOD = np.fft.fft(sig_mod)
  f = np.arange(len(SIG_MSG)) / len(SIG_MSG)

  # Plots.
  if selected_time_samples is None:
    selected_time_samples = (0, len(sig_msg) - 1)
  selection = np.arange(
    selected_time_samples[0], selected_time_samples[1], dtype=np.int)
  pl.figure()
  pl.subplot(311)
  pl.plot(sig_msg[selection])
  pl.title("message")
  pl.subplot(312)
  pl.plot(sig_car[selection])
  pl.title("carrier")
  pl.subplot(313)
  pl.plot(sig_mod[selection])
  pl.title("am")
  pl.xlabel("samples")

  pl.figure()
  pl.subplot(311)
  pl.plot(f, np.abs(SIG_MSG))
  pl.title("message spectrum")
  pl.subplot(312)
  pl.plot(f, np.abs(SIG_CAR))
  pl.title("carrier spectrum")
  pl.subplot(313)
  pl.plot(f, np.abs(SIG_MOD))
  pl.title("am spectrum")
  pl.xlabel("normalized frequencies)")

  if selected_freq_samples:
    selection = np.arange(
      selected_freq_samples[0], selected_freq_samples[1], dtype=np.int)
    pl.figure()
    pl.subplot(311)
    pl.plot(f[selection], np.abs(SIG_MSG[selection]))
    pl.title("message spectrum")
    pl.subplot(312)
    pl.plot(f[selection], np.abs(SIG_CAR[selection]))
    pl.title("carrier spectrum")
    pl.subplot(313)
    pl.plot(f[selection], np.abs(SIG_MOD[selection]))
    pl.title("am spectrum")
    pl.xlabel("normalized frequencies)")


def example1():
  num_samples = 200000
  sampling_freq = 50e3
  mod_index = 0.5

  t = np.arange(num_samples) / sampling_freq

  # Message, carrier and modulated signals.
  sig_msg = np.sin(2 * np.pi * 440 * t)
  sig_car = np.sin(2 * np.pi * 5000 * t)
  am(sig_msg, sig_car, mod_index, sampling_freq, (0, 500))


def example2():
  jingleLP = sio.loadmat("jingleLP.mat")
  sig_msg = jingleLP["jingleLP"][0]
  sampling_freq = jingleLP["Fs"][0]
  mod_index = 0.5

  t = np.arange(len(sig_msg)) / sampling_freq

  # Message, carrier and modulated signals.
  sig_msg = 100 * sig_msg / np.abs(sig_msg).max()
  sig_car = np.sin(2 * np.pi * 8000 * t)
  am(sig_msg, sig_car, mod_index, sampling_freq,
     selected_time_samples=(63700, 64401),
     selected_freq_samples=(0, int(0.1*len(sig_msg))))


if __name__ == "__main__":
  example1()
  example2()
  pl.show()
