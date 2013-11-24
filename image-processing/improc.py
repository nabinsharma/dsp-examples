# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 23, 2013
#
# You might need pygame installed to run this program. I worked on
# python 3.3 and there was no imread support using standard PIL
# based modules. So I used pygame to read images.
#
# If you are using Python 2.x, you should be good. Just use
# pylab.imread().
#
# TODO (Nabin): Don't import and use pygame if PIL is installed.

import numpy as np
import pygame
import pygame.surfarray
import pylab as pl
import scipy.signal as signal


def read_image(filename):
  surf = pygame.image.load(filename)
  # For grayscale images, R, G and B values
  # are same in the surf.
  im = np.asmatrix(pygame.surfarray.pixels_red(surf)).T
  return im


def display_image(im, title=""):
  pl.figure()
  pl.imshow(im, cmap=pl.cm.gray)
  pl.axis('image')
  pl.xticks([])
  pl.yticks([])
  pl.title(title)


def gauss2d(sigma=1.0, N=5):
  h = np.zeros((2*N + 1, 2*N + 1))
  for n1 in range(-N, N+1):
    for n2 in range(-N, N+1):
      h[n1 + N, n2 + N] = (1 / (2 * np.pi * sigma**2) *
                           np.exp(-(n1**2 + n2**2) / (2 * sigma**2)))
  return h


def get_dct2_vectors(N, M):
  """Compute normalized DCT2 vectors."""
  basis = np.zeros((N*M, N*M))
  X, Y = np.meshgrid(np.arange(M), np.arange(N))
  for k1 in range(N):
    for k2 in range(M):
      vector = (np.cos(np.pi/N*(X + 0.5) * (k1 - 1)) *
                np.cos(np.pi/M*(Y + 0.5) * (k2 - 1)))
      vector = vector.flatten(1)
      basis[k1*N + k2, :] = vector/np.linalg.norm(vector)
  return np.asmatrix(basis)


def example1():
  S = 0.3
  
  # Construct and display the original image.
  im_orig = np.zeros((64, 64))
  im_orig[24, 16:48] = 1
  im_orig[39, 16:48] = 1
  im_orig[24:56, 16] = 1
  im_orig[8:40, 47] = 1
  display_image(im_orig)

  # Compute transformation matrices
  A = np.array([[1, S], [0, 1]])
  d = np.array([0, 0])

  # Initialization.
  nb_row, nb_col = im_orig.shape
  I = np.zeros_like(im_orig)

  for y1 in range(nb_row):
    for y2 in range(nb_col):
      x = np.linalg.pinv(np.asmatrix(A)) * np.asmatrix(
        np.array([y1, y2]) + d).T
      x = np.squeeze(np.asarray(x))
      eta = np.floor(x)
      theta = x - eta
      if eta[0] >= 0 and eta[0] < nb_row:
        if eta[1] >= 0 and eta[1] < nb_col:
          I[y1, y2] = (I[y1, y2] + (1 - theta[0]) * (1 - theta[1]) *
                       im_orig[eta[0], eta[1]])
        if eta[1] >= 0 and eta[1] < (nb_col - 1):
          I[y1, y2] = (I[y1, y2] + (1 - theta[0]) * theta[1] * 
                       im_orig[eta[0], eta[1] + 1])
      if eta[0] >= 0 and eta[0] < nb_row -1:
        if eta[1] >= 1 and eta[1] < nb_col - 1:
          I[y1, y2] = (I[y1, y2] + theta[0] * (1 - theta[1]) * 
                       im_orig[eta[0] + 1, eta[1]])
        if eta[1] >= 0 and eta[1] < nb_col - 1:
          I[y1, y2] = (I[y1, y2] + theta[0] * theta[1] *
                       im_orig[eta[0] + 1, eta[1] + 1])
  display_image(I, "shear")


def example2():
  I = read_image("cameraman.jpg")
  display_image(I, "cameraman")

  # Gaussian blur.
  I_blurred = signal.convolve2d(I, gauss2d(12, 10), mode="same")
  I_sharpened = I - I_blurred
  display_image(I_sharpened, "cameraman: unsharp mask-ed")


def example3():
  # Read downsampled cameraman.
  I = read_image("camera.jpg")
  display_image(I, "camera")
  nb_row, nb_col = I.shape
  I = I.flatten(1)
  basis_matrix = get_dct2_vectors(nb_row, nb_col)
  I_projected = np.squeeze(np.asarray(basis_matrix * np.asmatrix(I).T))
  I_projected[2048:] = 0
  I_approx = np.squeeze(np.asarray(
    np.linalg.pinv(basis_matrix) * np.asmatrix(I_projected).T))
  I_approx = np.reshape(I_approx, (nb_row, nb_col), order='F')
  display_image(I_approx, "camera: \'compressed\' and recovered")


if __name__ == "__main__":
  example1()
  example2()
  example3()
  pl.show()
