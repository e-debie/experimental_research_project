import numpy as np
import matplotlib.pyplot as plt
import scipy
import matplotlib as mpl
    

plot = True
mpl.rcParams.update({'font.size': 18})
figcounter = 0
def fig_title():
    global figcounter
    figcounter += 1
    return f'Figure {figcounter}'

data = np.loadtxt(r"A1_DC.csv",
                  delimiter=',',
                  comments='#')


nbins = 300
spanning = data[:, 1]
tellingen, bins = np.histogram(spanning, bins=nbins)
bins_midden = (bins[1:] + bins[:-1]) / 2
piek_index, _ = scipy.signal.find_peaks(tellingen)
piek_spanning = bins_midden[piek_index]
piek_telling = tellingen[piek_index]

if plot:
        plt.figure()
        plt.hist(spanning, bins=nbins)
        plt.scatter(piek_spanning, piek_telling, c='r')
        plt.xlabel('Spanning (V)')
        plt.ylabel('Tellingen')
        plt.title(fig_title())
        plt.show()


print(f'The mean difference between peaks is {np.mean(np.diff(piek_spanning)):.3e} '
      f'± {np.std(np.diff(piek_spanning)):.3e}')
print(f'Hence, the step size fits into ±25 V a total of {50/np.mean(np.diff(piek_spanning))} times, '
      f'of which the log_2 is {np.log2(50/np.mean(np.diff(piek_spanning)))}')