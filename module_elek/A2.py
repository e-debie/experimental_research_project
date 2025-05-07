import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl


mpl.rcParams.update({'font.size': 18})

plot_alias = True
plot_freq_RMS = True
plot_freq_dB = True

figcounter = 0
def fig_title():
    global figcounter
    figcounter += 1
    return f'Figure {figcounter}'

if plot_alias:
    played = [3, 4, 6, 7]
    detected = [3, 4, 4, 3]
    f_s = 10

    func = lambda f : np.abs(f_s*np.round(f/f_s) - f)

    bounds = np.linspace(1, 10, 1000)
    ress = func(bounds)

    plt.plot(bounds, ress, 'k--')
    plt.scatter(played, detected, c='r')
    plt.xlabel('Actual frequency')
    plt.ylabel('Alias frequency')
    plt.title(fig_title())
    plt.show()

if plot_freq_RMS:
    dat = np.genfromtxt('A2_RMS.csv', delimiter=',').T
    plt.plot(dat[0], dat[1], '-', color='orange', linewidth=3)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Amplitude ($\tilde{\text{V}}$)')
    plt.title(fig_title())
    plt.show()

if plot_freq_dB:
    dat = np.genfromtxt('A2_dB.csv', delimiter=',').T
    plt.plot(dat[0], dat[1], '-', color='orange', linewidth=3)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'Amplitude ($\tilde{\text{V}}$)')
    plt.title(fig_title())
    plt.show()