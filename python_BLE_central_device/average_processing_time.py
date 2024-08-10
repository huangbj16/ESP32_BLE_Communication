# read a file with 1000 lines of data, each line looks like this:
# 18:55:24.197 -> Timestamp: 62185 ms, Data = 60 bytes, # = 1
# read the Timestamp, and save in a numpy array
# calculate the average processing time

import numpy as np
import re

def average_processing_time(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    time_array = np.zeros(300)
    for i in range(300):
        line = lines[i]
        match = re.search(r'Timestamp: (\d+) ms', line)
        time_array[i] = int(match.group(1))
    # print(time_array)
    # calculate the difference between each timestamp, and calculate the average
    diff_array = np.diff(time_array)
    print(diff_array)
    return np.mean(diff_array), np.std(diff_array)

if __name__ == '__main__':
    file_name = 'processing_time.txt'
    print(f'Average processing time = {average_processing_time(file_name)} ms')