# Nabin Sharma
# Oct 20, 2013

import numpy
import scipy.signal


##### Linearity

# impulse response
alpha = 0.999
# Construct the impulse response of the system of length 100.
h = alpha**numpy.arange(100)

# Two inputs.
x1 = numpy.sin(2*numpy.pi*40*numpy.arange(1000)/1000)
x2 = numpy.sin(2*numpy.pi*80*numpy.arange(1000)/1000)

# Responses to x1 and x2.
y1 = scipy.signal.convolve(x1, h, mode="valid")
y2 = scipy.signal.convolve(x2, h, mode="valid")

# New input as linear combination of x1 and x2.
a, b = 2.0, 10.0
x3 = a*x1 + b*x2

# Response to x3.
y3 = scipy.signal.convolve(x3, h, mode="valid")

# Linear combination of y1 and y2.
yy3 = a*y1 + b*y2

max_error = max(numpy.abs(y3 - yy3))

print("Linearity test: max error = %f" % max_error)


##### Time invarience

# delay by 100 samples
x1_delayed = x1[100:]
y1_delayed_input = scipy.signal.convolve(x1_delayed, h, mode="valid")
y1_delayed = y1[100:901]
max_error = max(numpy.abs(y1_delayed_input - y1_delayed))
print("Time-invarience test: max error = %f" % max_error)
