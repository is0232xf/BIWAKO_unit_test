# make a time series of instantaneous electric power consumption graph from a csv file

import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from statistics import mean

# define variables
timestep = 0.01

# import csv format file
path = "test.csv"
data = pd.read_csv(path, index_col=0, skipinitialspace=True)
# comvert csv data to a list format data
current = np.array(data['current'].values.tolist())
count_max_value = len(current)*timestep
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
