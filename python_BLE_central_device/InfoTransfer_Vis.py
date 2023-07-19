import matplotlib.pyplot as plt
import re
import json
import numpy as np

experiment_round_total = 0
stimuli_array = []
data_array = []


# read stimuli file

file_path = "data/InfoTransfer_one_motor_skip_shuffle_100.json"

with open(file_path, "r") as file:
    lines = file.readlines()
    experiment_round_total = len(lines)
    for line in lines:
        command_strs = re.findall(r'{[^{}]*}', line)
        # print(command_strs[1])
        command_json = json.loads(command_strs[1])
        id = command_json["addr"]
        stimuli_array.append(id)

# read data file
file_path = "data/data_bingjian_IT_skip_20230718_2.json"

with open(file_path, "r") as file:
    lines = file.readlines()
    assert experiment_round_total == len(lines)
    for line in lines:
        # print(line.strip())
        data_array.append(int(line))

print('experiment length = ', experiment_round_total)

stimuli_array = np.array(stimuli_array)
data_array = np.array(data_array)
category_num = 20
repeat_num = 5
count_array = np.zeros((category_num), dtype=np.float32)

for i in range(experiment_round_total):
    if stimuli_array[i] == data_array[i]:
        count_array[(stimuli_array[i]>>1)] += 1 # from 1-39 to 0-19

# count_array /= repeat_num

# data_array -= stimuli_array
# num_zeros = np.count_nonzero(data_array == 0)
# num_minus = np.count_nonzero(data_array == -1)
# num_plus = np.count_nonzero(data_array == 1)
# print(num_zeros, num_minus, num_plus, np.sum(count_array))
print(np.sum(count_array))

plt.plot(count_array)
plt.show()

### calculate information transfer

stimuli_array = stimuli_array>>1
data_array = data_array>>1
print(data_array)

from scipy.stats import entropy

# Calculate the probability distribution of the stimuli array
stimuli_distribution = np.bincount(stimuli_array) / len(stimuli_array)

# Calculate the probability distribution of the data array
data_distribution = np.bincount(data_array) / len(data_array)

# Calculate the joint probability distribution
joint_distribution = np.histogram2d(stimuli_array, data_array, bins=(20, 20))[0] / len(stimuli_array)

# Calculate the mutual information
mi = 0
for i in range(len(stimuli_distribution)):
    for j in range(len(data_distribution)):
        if joint_distribution[i, j] != 0 and stimuli_distribution[i] != 0 and data_distribution[j] != 0:
            mi += joint_distribution[i, j] * np.log2(joint_distribution[i, j] / (stimuli_distribution[i] * data_distribution[j]))

# Normalize the mutual information by the maximum entropy of the stimuli array
max_entropy = entropy(stimuli_distribution, base=2)
normalized_mi = mi / max_entropy

print("Mutual Information:", mi)
print("Maximum Information IS:", max_entropy)
print("Normalized Mutual Information:", normalized_mi)
