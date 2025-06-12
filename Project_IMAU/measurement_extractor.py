import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import raw_file_reader as rfr

reference_mz_index = 0

data = pd.read_csv('extracted_data_176.csv', delimiter=';')
t_times = pd.array(data.iloc[:,1])
t_peaks = pd.array(data.iloc[:,2])
t_left_times = pd.array(data.iloc[:,3])
t_right_times = pd.array(data.iloc[:,4])

times = []
peaks = []
left_times = []
right_times = []
for i,j,k,l in zip(t_times, t_peaks, t_left_times, t_right_times):
    times.append(eval(i))
    peaks.append(eval(j))
    left_times.append(eval(k))
    right_times.append(eval(l))

bounds = np.vstack((left_times[reference_mz_index], right_times[reference_mz_index])).T

for i,j in enumerate(bounds):
    print(f"Starting peak {i}")
    files = rfr.file_list()
    mzs = rfr.get_mzs(rfr.read_file(files[0]))

    cur_output = np.zeros((len(mzs),2))

    for ii,jj in enumerate(mzs):
        print(f"Starting m/z {jj}")
        tot_time = []
        tot_data = []
        for fname in files:
            # print(f"Starting read file {fname}")
            r_data = rfr.read_file(fname)
            times = rfr.get_times(r_data)
            col = r_data.iloc[:, ii]
            for iii, jjj in zip(col, times):
                tot_time.append(jjj)
                tot_data.append(iii)
            # print(f"Finished read file {fname}")

        cur_output[ii] = [mzs[ii], np.mean(tot_data[j[0]:j[1]],axis=0)]
        print(f"Finished m/z {jj}")

    np.savetxt(f'data_files\\peak_{i}.csv', cur_output, delimiter=';')
    print(f"Finished peak {i}. Wrote file data_files\\peak_{i}.csv")