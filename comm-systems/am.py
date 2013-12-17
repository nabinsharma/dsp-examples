# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Dec 15, 2013

import numpy as np
import pylab as pl


def am():
  num_samples = 200000
  sampling_freq = 50e3

  t = np.arange(num_samples) / sampling_freq

  # Message and carrier parameters.
  amp_msg = 1
  freq_msg = 440
  amp_car = 1
  freq_car = 5000
  
  # Modulation index.
  mod_index = 0.5

  # Message, carrier and modulated signals.
  sig_msg = amp_msg * np.sin(2 * np.pi * freq_msg * t)
  sig_car = amp_car * np.sin(2 * np.pi * freq_car * t)
  sig_mod = (1 + mod_index * sig_msg) * sig_car

  # Spectrums.
  SIG_MSG = np.fft.fft(sig_msg)
  SIG_CAR = np.fft.fft(sig_car)
  SIG_MOD = np.fft.fft(sig_mod)
  f = (np.arange(len(SIG_MSG)) / len(SIG_MSG))* sampling_freq

  # Plots.
  selection = np.arange(0, 500, dtype=np.int)
  pl.figure()
  pl.subplot(311)
  pl.plot(t[selection], sig_msg[selection])
  pl.title("message")
  pl.subplot(312)
  pl.plot(t[selection], sig_car[selection])
  pl.title("carrier")
  pl.subplot(313)
  pl.plot(t[selection], sig_mod[selection])
  pl.title("am")
  pl.xlabel("time (s)")

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
  pl.xlabel("frequency (Hz)")
  

if __name__ == "__main__":
  am()
  pl.show()
