import matplotlib.pyplot as plt
import re
import json
import numpy as np

experiment_round_total = 0
stimuli_array = []
data_array = []

addr_array = [1,2,3,4,5,10,9,8,7,6,31,32,33,34,35,40,39,38,37,36]

# read stimuli file

file_path = "study_data/commands_infotransfer_body_P8.json"

with open(file_path, "r") as file:
    lines = file.readlines()
    experiment_round_total = len(lines)
    for line in lines:
        command_strs = re.findall(r'{[^{}]*}', line)
        print(command_strs[1])
        command_json = json.loads(command_strs[1])
        id = command_json["addr"]
        diff_json = json.loads(command_strs[2])
        offset = 1 if diff_json["time"] == 1.2 else 0
        stimuli_array.append(addr_array.index(id)*2+offset) # if low then original id-1, if high then id

# read data file

file_path = "study_data/data_infotransfer_body_P8.json"

with open(file_path, "r") as file:
    lines = file.readlines()
    assert experiment_round_total == len(lines)
    for line in lines:
        data_json = json.loads(line)
        id = data_json["id"]
        offset = 1 if data_json["isContinuous"] == False else 0
        data_array.append(addr_array.index(id)*2+offset) # if low then original id, if high then id+1

print('experiment length = ', experiment_round_total)

stimuli_array = np.array(stimuli_array)
data_array = np.array(data_array)
print(np.max(stimuli_array), np.min(stimuli_array), stimuli_array)
print(np.max(data_array), np.min(data_array), data_array)
category_num = 40
repeat_num = 5
count_array = np.zeros((category_num), dtype=np.float32)

for i in range(experiment_round_total):
    # if (stimuli_array[i]>>1) == (data_array[i]>>1):
    #     count_array[stimuli_array[i]>>1] += 1
    if stimuli_array[i] == data_array[i]:
        count_array[stimuli_array[i]] += 1

# count_array /= repeat_num

# data_array -= stimuli_array
# num_zeros = np.count_nonzero(data_array == 0)
# num_minus = np.count_nonzero(data_array == -2)
# num_plus = np.count_nonzero(data_array == 2)
# print(num_zeros, num_minus, num_plus, np.sum(count_array))
# print(np.sum(count_array), np.sum(num_zeros), np.sum(num_minus), np.sum(num_plus))
print("accuracy = ", np.sum(count_array)/experiment_round_total)

plt.plot(count_array)
plt.show()

# exit()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Create the confusion matrix using NumPy
conf_matrix = confusion_matrix(stimuli_array, data_array)

# Plot the confusion matrix as a heatmap using Matplotlib
plt.figure(figsize=(10, 8))
plt.imshow(conf_matrix, cmap='Blues', interpolation='nearest')
plt.title('Confusion Matrix')
plt.colorbar()

# Label the axes and set tick marks
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.xticks(np.arange(category_num))
plt.yticks(np.arange(category_num))

# Add text annotations in each cell
for i in range(conf_matrix.shape[0]):
    for j in range(conf_matrix.shape[1]):
        plt.text(j, i, str(conf_matrix[i, j]), ha='center', va='center', color='white')

plt.tight_layout()
plt.show()


### calculate information transfer

# stimuli_array = stimuli_array
# data_array = data_array
# print(data_array)

from scipy.stats import entropy

# Calculate the probability distribution of the stimuli array
stimuli_distribution = np.bincount(stimuli_array) / len(stimuli_array)

# Calculate the probability distribution of the data array
data_distribution = np.bincount(data_array) / len(data_array)

# Calculate the joint probability distribution
joint_distribution = np.histogram2d(stimuli_array, data_array, bins=(category_num, category_num))[0] / len(stimuli_array)

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



################ calculate info for position and pattern


stimuli_array_position = stimuli_array >> 1
data_array_position = data_array >> 1
print(stimuli_array[:10], stimuli_array_position[:10])
category_num = 20

# Calculate the probability distribution of the stimuli array
stimuli_distribution = np.bincount(stimuli_array_position) / len(stimuli_array_position)

# Calculate the probability distribution of the data array
data_distribution = np.bincount(data_array_position) / len(data_array_position)

# Calculate the joint probability distribution
joint_distribution = np.histogram2d(stimuli_array_position, data_array_position, bins=(category_num, category_num))[0] / len(stimuli_array_position)

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









stimuli_array_pattern = stimuli_array % 2
data_array_pattern = data_array % 2
print(stimuli_array[:10], stimuli_array_pattern[:10])
category_num = 2

# Calculate the probability distribution of the stimuli array
stimuli_distribution = np.bincount(stimuli_array_pattern) / len(stimuli_array_pattern)

# Calculate the probability distribution of the data array
data_distribution = np.bincount(data_array_pattern) / len(data_array_pattern)

# Calculate the joint probability distribution
joint_distribution = np.histogram2d(stimuli_array_pattern, data_array_pattern, bins=(category_num, category_num))[0] / len(stimuli_array_pattern)

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