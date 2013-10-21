# Nabin Sharma
# Oct 19, 2013
#
# You might need pygame installed to run this program. I worked on
# python 3.3 and there was no imread support using standard PIL
# based modules. So I used pygame to read images.
#
# If you are using Python 2.x, you should be good. Just use
# pylab.imread().
#
# TODO (Nabin): Don't import and use pygame if PIL is installed.

import numpy
import pygame
import pygame.surfarray
import pylab

import haar


def read_image(filename):
    surf = pygame.image.load(filename)
    im = numpy.asmatrix(pygame.surfarray.pixels_red(surf)).T
    return im


def display_image(im, title=None):
    pylab.figure()
    pylab.imshow(im, cmap='gray')
    pylab.axis('image')
    pylab.xticks([])
    pylab.yticks([])
    pylab.title(title)


def main():
    I = read_image('camera.jpg')
    display_image(I, "Original image")

    # Arrange image in column vector.
    I = I.flatten(1).T

    # Generate Haar basis vector (rows of H).
    H = numpy.asmatrix(haar.haar(len(I)))

    # Project image on the new basis.
    I_haar = H * I

    # Remove the second half of the coefficient.
    I_haar[len(I_haar)/2:, 0] = 0

    # Recover the image by inverting change of basis.
    I_haar = H.T * I_haar
    error = I - I_haar
    distance = numpy.sqrt(error.T * error)

    # Rearrange pixels of the image.
    I_haar = numpy.reshape(I_haar, (64, 64), 'F')
    display_image(I_haar, "Recoevered image, distance = {}".format(distance))

    pylab.show()


if __name__ == "__main__":
    main()
