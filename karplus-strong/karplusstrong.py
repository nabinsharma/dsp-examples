# Nabin Sharma
# Oct 09, 2013

import pylab
import scipy.io.wavfile
import time


def ks_loop(x, alpha=1, D=1):
    # If x is 1d array, convert to list.
    if (not isinstance(x, list)):
        x = x.tolist()

    # Length of the output signal must be larger than the length of the
    # input signal that is, D must be larger than 1.
    D = max(D, 1)
    
    # Number of input samples.
    M = len(x)

    # Number of output samples.
    size_y = D * M

    # Initialize with random input x.
    y = list(x)

    for i in range(M, size_y):
        y.append(alpha * y[i - M])
    
    return pylab.array(y)


def ks(x, alpha=1, D=1):
    # If x is list, convert to 1d array.
    if (isinstance(x, list)):
        x = pylab.array(x)

    # Length of the output signal must be larger than the length of the
    # input signal that is, D must be larger than 1.
    D = max(D, 1)

    # Number of input samples.
    M = len(x)

    # Create a vector of the powers of alpha, [alpha^0 alpha^1 ....].
    size_alphaVector = D;
    alphaVector = (alpha * pylab.ones(
        size_alphaVector)) ** range(size_alphaVector)

    # Create a matrix with M columns, each being the vector of the powers
    # of alpha.
    alphaMatrix = pylab.tile(alphaVector, (M, 1)).T;

    # Create a matrix with D rows filled by the input signal x.
    xMatrix = pylab.tile(x, (D, 1));

    # Multipliy the two
    yMatrix = alphaMatrix * xMatrix

    # Read out the output row by row
    y = yMatrix.flatten(0)

    return y


def generate_cord():
    """
    TODO: Pass the parameters as input arguments.

    Parameters:
      - Fs       : sampling frequency
      - F0       : frequency of the notes forming chord
      - gain     : gains of individual notes in the chord
      - duration : duration of the chord in second
      - alpha    : attenuation in KS algorithm
    """
    Fs = 48000

    # D2, D3, F3, G3, F4, A4, C5, G5
    F0 = 440 * pylab.array(
        [2**-(31.0/12), 2**-(19.0/12), 2**-(16.0/12), 2**(-14.0/12),
         2**-(4.0/12), 1.0, 2**(3.0/12), 2**(10.0/12)])
    gain = [1.2, 3.0, 1.0, 2.2, 1.0, 1.0, 1.0, 3.5]
    duration = 4.0
    alpha = 0.9785

    # Number of samples in the chord.
    nbsample_chord = Fs * duration

    # This is used to correct alpha later, so that all the notes
    # decay together (with the same decay rate).
    first_duration = pylab.ceil(nbsample_chord / pylab.round_(Fs/F0[0]))

    # Initialization.
    chord = pylab.zeros(nbsample_chord)

    for i, f in enumerate(F0):
        print("Working on %g / %g" % (i+1, len(F0)))
        # Get M and duration parameter.
        current_M = pylab.round_(Fs/f)
        current_duration = pylab.ceil(nbsample_chord / current_M)

        # Correct current alpha so that all the notes decay together
        # (with the same decay rate)
        current_alpha = alpha ** (first_duration / current_duration)

        # Let Paul's high D on the bass ring a bit longer.
        if i == 1:
            current_alpha = current_alpha ** 0.8

        # Generate input and output of KS algorithm.
        x = pylab.rand(current_M)
        y = ks(x, current_alpha, int(current_duration))
        y = y[:int(nbsample_chord)]
        
        # Construct the chord by adding the generated note (with the
        # appropriate gain).
        chord = chord + gain[i] * y
        
    return Fs, duration, chord


def main():
    x = pylab.randn(100)
    t0 = time.clock()
    y1 = ks_loop(x, 0.9, 10)
    t_loop = time.clock() - t0
    t0 = time.clock()
    y2 = ks(x, 0.9, 10)
    t_matrix = time.clock() - t0
    print("Loop method took %g seconds." % t_loop)
    print("Matrix method took %g seconds." % t_matrix)
    # Make sure y1 and y2 are same within very small numeric
    # error.
    assert(pylab.sum(pylab.absolute(y1 - y2)) < 1e-10)

    # Plot x and y
    pylab.figure()
    pylab.subplot(211)
    pylab.stem(x)
    pylab.ylabel('x')
    pylab.subplot(212)
    pylab.stem(y2)
    pylab.ylabel('y')
    pylab.xlabel('samples')

    print("Generating the opening chord of Hard day's night by The Beatles ...")
    Fs, T, chord = generate_cord()
    pylab.figure()
    pylab.plot(pylab.arange(0.0, T, 1.0/Fs), chord)
    pylab.xlabel('time (sec)')
    pylab.title('First Chord of Hard Days Night')
    print("Writing the chord to chord.wav ...")
    C = max(pylab.absolute(chord))
    scipy.io.wavfile.write("chord.wav", Fs,
                           pylab.int16((2**15 - 1) * chord / C))
    print("Done.")

    pylab.show()


if __name__ == '__main__':
    main()
