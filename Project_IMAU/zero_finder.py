import numpy as np
import pandas as pd

sb_file = 'data_files/peak_0.csv'

data_files = ['data_files/peak_1.csv','data_files/peak_2.csv','data_files/peak_3.csv']

sb_dat = pd.DataFrame(0, index=np.arange(796), columns=(1,1))

mzs = pd.read_csv('data_files/peak_0.csv').iloc[:,0]
sb_avg = sb_dat.iloc[:,1]
sb_std = .1*sb_avg #We do not have two system blanks to find the std, so we assume the std is 10% of the blank

c0_dat = pd.read_csv('data_files/peak_0.csv')
c1_dat = pd.read_csv('data_files/peak_2.csv')
c2_dat = pd.read_csv('data_files/peak_3.csv')

c0_avg = c0_dat.iloc[:,1]
c1_avg = c1_dat.iloc[:,1]
c2_avg = c2_dat.iloc[:,1]

c0_fin = np.zeros(c0_avg.shape)
c1_fin = np.zeros(c1_avg.shape)
c2_fin = np.zeros(c2_avg.shape)

for i,(j,k,l,m,n) in enumerate(zip(c0_avg,c1_avg,c2_avg,sb_avg,sb_std)): # if it's not bigger than avg+3*std, then j>(m+3*n) is 0 so the whole thing is 0
    c0_fin[i] = j * (j>(m+3*n))
    c1_fin[i] = k * (k > (m + 3 * n))
    c2_fin[i] = l * (l > (m + 3 * n))


np.savetxt('zeroed_files/c0_fin.csv', np.vstack((mzs, c0_fin)).T, delimiter=',')
np.savetxt('zeroed_files/c1_fin.csv', np.vstack((mzs, c1_fin)).T, delimiter=',')
np.savetxt('zeroed_files/c2_fin.csv', np.vstack((mzs, c2_fin)).T, delimiter=',')

import matchingTest_wrapper

results = matchingTest_wrapper.get_results()

print(results)

c0_amounts = results['zeroed_files/c0_fin.csv']
c1_amounts = results['zeroed_files/c1_fin.csv']
c2_amounts = results['zeroed_files/c2_fin.csv']

