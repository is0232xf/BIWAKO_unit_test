# make a time series of instantaneous electric power consumption graph from a csv file

import csv
import glob
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

# define variables
timestep = 0.01

def csv_to_graph(path):
    data = pd.read_csv(path, index_col=0, skipinitialspace=True)
    # comvert csv data to a list format data
    current = np.array(data['current'].values.tolist())
    # find the peak value from the list data
    peak_value_index = np.argmax(current)
    # extract useful values from arround the peak value
    arround_peak_value = current[peak_value_index-100:peak_value_index+500]

    # calucurate const value
    const_value = arround_peak_value[len(arround_peak_value)-400:len(arround_peak_value)]
    avg_const_value = round(mean(const_value),2)
    text_avg_const_value = "mean const value = " + str(avg_const_value)
    # make a time series graph
    count = np.arange(0, len(arround_peak_value)/100, timestep)
    plt.plot(count, arround_peak_value)
    plt.xlim(0.0, 6.0)
    plt.ylim(0.0, 10.0)
    plt.xlabel('t [s]')
    plt.ylabel('current [A]')
    font_dict = dict(style="italic",
                    size=16)
    bbox_dict = dict(facecolor="#ffffff",
                    edgecolor="#000000",
                    fill=True)
    plt.text(2.5, 9, text_avg_const_value, font_dict, bbox=bbox_dict)
    plt.grid()
    plt.show()

def make_result_file(path):
    # define variables
    peak_value = []
    mean_const_value = []
    # make file list
    file_list = glob.glob(path+'*.csv')
    # extract the peak value and average const value of each file
    # and append each value to the list
    for file in file_list:   
        data = pd.read_csv(file, index_col=0, skipinitialspace=True)
        # comvert csv data to a list format data
        current = np.array(data['current'].values.tolist())
        # find the peak value from the list data
        peak_value_index = np.argmax(current)
        # extract useful values from arround the peak value
        arround_peak_value = current[peak_value_index-100:peak_value_index+500]
        # calucurate const value
        const_value = arround_peak_value[len(arround_peak_value)-400:len(arround_peak_value)]
        avg_const_value = round(mean(const_value),2)
        # calcurate mean value of peak value and average const value
        peak_value.append(np.max(current))
        mean_const_value.append(avg_const_value)
    # make a result file(write each value)
    file_name = path + 'result.txt'
    f = open(file_name, 'a')
    for i in range(len(file_list)):
        peak = peak_value[i]
        const = mean_const_value[i]
        f.write("FILE%s: Peak value: %s, Mean const value: %s \n" % (i, peak, const))
    mean_peak = round(mean(peak_value),2)
    mean_const = round(mean(mean_const_value),2)
    f.write("Mean peak value: %s, Mean const value: %s\n" % (mean_peak, mean_const))
    f.close()
if __name__ == "__main__":
    # import csv format file
    # useage: make a time series of power consumption graph
    path = "test.csv"
    csv_to_graph(path)
    
    """
    # useage: make result files
    path = 'C:/Users/is0232xf/OneDrive - 学校法人立命館/ソースコード/BIWAKO_unit_test/csv/diagonal/'
    files = os.listdir(path)
    # get subdirectory list
    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    for subdir in files_dir:
        dir = path + subdir + '/'
        make_result_file(dir)
    """