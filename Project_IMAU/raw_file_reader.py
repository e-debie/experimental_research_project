import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


filepath_read = r"D:\all_sediments\\"


def file_list():
    global filepath_read
    outputs = []
    filenames = os.listdir(filepath_read)
    for i in filenames:
        if i[-4:] == '.csv':
            outputs.append(i)

    return outputs


def read_file(fname, plot_axis=None, plot_index = None):
    global filepath_read
    data = pd.read_csv(filepath_read + fname)

    match plot_axis:
        case 0:
            total_mzs = pd.array(data.iloc[0])
            concs = pd.array(data.iloc[plot_index])

            plt.plot(total_mzs, concs, '-')

        case 1:
            total_columns = data.columns

            times = pd.array(data.iloc[:,0])
            concs = pd.array(data.iloc[:,plot_index])

            plt.plot(times, concs, '-')

        case _:
            pass

    return data


def get_times(data):
    times = pd.array(data.iloc[:, 0])[1:]

    return times

def get_mzs(data):
    total_mzs = pd.array(data.iloc[0])[1:]

    return total_mzs


if __name__=='__main__':
    files = file_list()
    r_data = read_file(files[0])
    get_mzs(r_data)

    plt.show()