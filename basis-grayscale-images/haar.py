# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Oct 19, 2013

import numpy

def haar(N):
    """
    Returns a Haar matrix of size NxN.
    Ref: https://spark-public.s3.amazonaws.com/dsp/num_examples/Module%203/code/haar.m
    """
    # TODO (Nabin): Make sure N is power of 2.
    h = numpy.zeros((N, N))
    h[0, :] = numpy.ones(N) / numpy.sqrt(N)
    for k in range(1, N):
        p = numpy.fix(numpy.log(k)/numpy.log(2))
        q = k - 2**p
        k1 = 2.0**p
        t1 = N / k1 
        k2 = 2.0**(p + 1)
        t2 = N / k2
        for i in numpy.arange(1, t2):
            h[k+1, i+q*t1] = 2**(p/2) / numpy.sqrt(N)
            h[k+1, i+q*t1+t2] = -2**(p/2) / numpy.sqrt(N)
    return h
