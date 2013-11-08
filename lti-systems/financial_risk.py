# Digital Signal Processing by Paolo Prandoni and Martin Vetterli
# Coursera/EPFL

# Nabin Sharma
# Nov 06, 2013

from __future__ import division
import matplotlib.pyplot as plt
import numpy
import scipy.signal as signal
from scipy.io import loadmat


def leaky_integrator(M, N):
    lmb = (M - 1) / M
    return (1 - lmb) * lmb**numpy.arange(N)


def get_xticks(dates_ts, start_idx):
    str2date = lambda strdate: "{}-{}-{}".format(strdate[:4], strdate[4:6],
                                                 strdate[6:])
    pos_xticks = numpy.linspace(start_idx, len(dates_ts)-1, 6)
    label_xticks = [str2date(str(int(dates_ts[p]))) for p in pos_xticks]
    return pos_xticks, label_xticks


def main():
    M = 100
    lmb = 0.94

    data = loadmat("finance-data.mat")
    price_ts = numpy.squeeze(data["price_ts"])
    dates_ts = numpy.squeeze(data["dates_ts"])

    pos_xticks, label_xticks = get_xticks(dates_ts, 0)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.semilogy(price_ts)
    ax.set_ylim(40, 280)
    ax.set_xticks(pos_xticks)
    ax.set_xticklabels(label_xticks)
    ax.set_xlabel("dates")
    ax.set_ylabel("log-price")

    # Compute simple return time-series.
    return_ts = [(p2 - p1)/p2 for p1, p2 in zip(price_ts[1:], price_ts[:-1])]
    # Plot return.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.plot(return_ts, 'x')
    ax.set_xticks(pos_xticks)
    ax.set_xticklabels(label_xticks)
    ax.set_ylim(-0.2, 0.15)
    ax.set_ylabel('return')

    # Compute the M-point volatility.
    length_ts = len(return_ts)
    volatility = numpy.zeros(length_ts)
    h = (1/M)*numpy.ones(M)
    for i in range(M, length_ts):
        temp = return_ts[(i-M):i]
        moving_average = numpy.sum(h*temp)
        volatility[i] = sum(h*(temp - moving_average)**2)
    volatility = numpy.sqrt(volatility)
    pos_xticks, label_xticks = get_xticks(dates_ts, M)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(volatility[M:])
    ax.set_ylabel("M points volatility")
    ax.set_xticks(pos_xticks)
    ax.set_xticklabels(label_xticks)
    ax.grid(True)

    # Compute the exponentially weighted volatility.
    exp_average = 0
    exp_volatility = numpy.zeros(length_ts + 1)
    for i in range(length_ts):
        exp_average = lmb*exp_average + (1 - lmb)*return_ts[i]
        exp_volatility[i+1] = (lmb*exp_volatility[i] + (1 - lmb) *
                               (return_ts[i] - exp_average)**2)
    exp_volatility = numpy.sqrt(exp_volatility[1:])
    pos_xticks, label_xticks = get_xticks(dates_ts, 0)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(exp_volatility)
    ax.set_ylabel("Exponentially weighted volatility")
    ax.set_xticks(pos_xticks)
    ax.set_xticklabels(label_xticks)
    ax.grid(True)

    plt.show()


if __name__ == "__main__":
    main()
