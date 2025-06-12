import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import raw_file_reader as rfr
import scipy as sp


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
    output_left_times = []
    output_right_times = []
    for i in range(len(peaks)):
        output_time.append(tot_time[round(peak_details['left_ips'][i]):round(peak_details['right_ips'][i])])
        output_data.append(tot_data[round(peak_details['left_ips'][i]):round(peak_details['right_ips'][i])])
        output_left_times.append(round(peak_details['left_ips'][i]))
        output_right_times.append(round(peak_details['right_ips'][i]))


    return output_time, output_data, output_left_times, output_right_times



if __name__=='__main__':
    all_files = rfr.file_list()
    first_file = rfr.read_file(all_files[0])
    all_mzs = rfr.get_mzs(first_file)
    all_times = []
    all_left_times = []
    all_right_times = []
    all_data = []
    for i in range(len(all_mzs)):
        current_times, current_data, current_left_times, current_right_times = main(i)
        all_times.append(current_times)
        all_data.append(current_data)
        all_left_times.append(current_left_times)
        all_right_times.append(current_right_times)



    final_times = []
    final_left_times = []
    final_right_times = []
    final_data = []
    for i,(j,k,l,m) in enumerate(zip(all_times,all_data,all_left_times,all_right_times)):
        current_final_times = []
        for jj in j:
            current_final_times.append(np.mean(jj))
        current_final_data = []
        for kk in k:
            current_final_data.append(np.mean(kk))
        current_final_left_times = []
        for ll in l:
            current_final_left_times.append(ll)
        current_final_right_times = []
        for mm in m:
            current_final_right_times.append(mm)

        final_times.append(current_final_times)
        final_data.append(current_final_data)
        final_left_times.append(current_final_left_times)
        final_right_times.append(current_final_right_times)

    file_data = open('extracted_data.csv', 'w')
    file_data.writelines('#m/z;time;mean;left_times;right_times\n')
    file_data.close()

    for i,j,k,l,m in zip(all_mzs, final_times, final_data, final_left_times, final_right_times):
        file_data = open('extracted_data.csv', 'a')
        file_data.writelines(f'{i};{j};{k};{l};{m}\n')
        file_data.close()

    plt.show()