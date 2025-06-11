import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import raw_file_reader as rfr
import scipy as sp


'''The idea was to use the peaks in the derivative to find the start and end points of each measurement, 
and to trim the peaks out from there. This does not seem to work.
Scipy peak-finding algorithms cannot find the asymmetrical peak widths as far as I know.
I'll look into it further when I have the time.'''


def derivative(arr, times):
    dt = np.nanmean(np.diff(times))
    out = np.zeros(arr.shape)
    arr = np.nan_to_num(arr, nan=0, posinf=0, neginf=0)
    out[2:-2] = (arr[:-4] - 8*arr[1:-3] + 8*arr[3:-1] - arr[4:]) / (12*dt)
    out[1] = (arr[2]-arr[0]) / (2*dt)
    out[-2] = (arr[-1]-arr[-3]) / (2*dt)
    arr[0] = (arr[1] - arr[0]) / dt
    arr[-1] = (arr[-1] - arr[-2]) / dt

    return out


def main(mz_index, plot=False):
    files = rfr.file_list()
    tot_time = []
    tot_data = []
    for fname in files:
        r_data = rfr.read_file(fname)
        times = rfr.get_times(r_data)
        col = r_data.iloc[:,mz_index]
        for i,j in zip(col,times):
            tot_time.append(j)
            tot_data.append(i)

    tot_mz = rfr.get_mzs(r_data)
    tot_data = np.asarray(tot_data)
    tot_time = np.asarray(tot_time)
    print(f'm/z = {tot_mz[mz_index]}')

    peaks, peak_details = sp.signal.find_peaks(tot_data, prominence=.5, height=.2, width=2, rel_height=.8)

    if plot:
        fig, ax = plt.subplots()
        ax.plot(tot_time, tot_data, '-')
        for i,peak in enumerate(peaks):
            ax.vlines(tot_time[peak], ymin=0, ymax=tot_data[peak], colors='#B00B69')
            ax.fill_betweenx(y=np.linspace(0, tot_data[peak], 1000),
                             x1=tot_time[round(peak_details['left_ips'][i])],
                             x2=tot_time[round(peak_details['right_ips'][i])],
                             alpha=0.5)

    output_time = []
    output_data = []
    for i in range(len(peaks)):
        output_time.append(tot_time[round(peak_details['left_ips'][i]):round(peak_details['right_ips'][i])])
        output_data.append(tot_data[round(peak_details['left_ips'][i]):round(peak_details['right_ips'][i])])

    return output_time, output_data



if __name__=='__main__':
    all_files = rfr.file_list()
    first_file = rfr.read_file(all_files[0])
    all_mzs = rfr.get_mzs(first_file)
    all_times = []
    all_data = []
    for i in range(len(all_mzs)):
        current_times, current_data = main(i)
        all_times.append(current_times)
        all_data.append(current_data)


    final_times = []
    final_data = []
    for i,(j,k) in enumerate(zip(all_times,all_data)):
        current_final_times = []
        for jj in j:
            current_final_times.append(np.mean(jj))
        current_final_data = []
        for kk in k:
            current_final_data.append(np.mean(kk))

        final_times.append(current_final_times)
        final_data.append(current_final_data)

    file_data = open('extracted_data.csv', 'w')
    file_data.write('')
    file_data.close()

    file_time = open('extracted_time.csv', 'w')
    file_time.write('')
    file_time.close()

    for i,j,k in zip(all_mzs, final_data, final_times):
        print(i,j,k)
        file_data = open('extracted_data.csv', 'a')
        file_data.writelines(f'{i};{j}\n')
        file_data.close()

        file_time = open('extracted_time.csv', 'a')
        file_time.writelines(f'{i};{k}\n')
        file_time.close()

    plt.show()