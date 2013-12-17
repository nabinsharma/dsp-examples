# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Dec 15, 2013

import numpy as np
import pylab as pl


def pam_symbols(M, G=1):
  k = np.arange(2**M)
  return G * (-2**M + 1 + 2*k)


def qam_symbols(M, G=1):
  assert M % 2 == 0
  ar = pam_symbols(M / 2)
  ai = pam_symbols(M / 2)
  symbols = np.zeros((len(ar), len(ai)), dtype=np.complex)
  for idx_r, r in enumerate(ar):
    for idx_i, i in enumerate(ai):
      symbols[idx_i, idx_r] = G * (ar[idx_r] + 1j * ai[idx_i])
  return symbols


def plot_constallation(c):
  c = np.squeeze(c.flatten(order = 'F'))
  pl.plot(c.real, c.imag, 'bo', markersize=7)
  pl.xlim(c.real.min() - 2, c.real.max() + 2)
  pl.ylim(c.imag.min() - 2, c.imag.max() + 2)
  pl.title("QAM-{}".format(c.size))
  pl.show()


if __name__ == "__main__":
  s = qam_symbols(2, 1)
  plot_constallation(s)
