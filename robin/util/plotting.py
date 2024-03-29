import numpy as np
import matplotlib.pyplot as plt


def plot_samples(*samples):
    for s in samples:
        plt.plot(s)
    plt.show()


def plot_spectrum(spectrum, rate):
    time_step = 1.0 / rate
    ps = np.abs(spectrum) ** 2
    freqs = np.fft.fftfreq(spectrum.size, time_step)
    idx = np.argsort(freqs)
    plt.plot(freqs[idx], ps[idx])


def plot_stereo(time, left, right):
    f, axes = plt.subplots(2, sharex=True)
    axes[0].plot(time, left)
    axes[0].set_title("Left")
    axes[1].plot(time, right)
    axes[1].set_title("Right")
    plt.show()


def plot_here(x, y):
    plt.plot(x, y)
    plt.show()
