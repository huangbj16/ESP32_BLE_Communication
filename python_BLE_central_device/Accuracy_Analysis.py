import matplotlib.pyplot as plt
import re
import json
import numpy as np

experiment_round_total = 0
stimuli_array = []
data_array = []

# addr_array = [1,2,3,4,5,10,9,8,7,6,31,32,33,34,35,40,39,38,37,36]
addr_array = [92,94,96,98,100,109,107,105,103,101,62,64,66,68,70,79,77,75,73,71]

# read stimuli file

for i in range(1, 9):

    file_path = f"study_data/commands_infotransfer_arm_P{i}.json"

    with open(file_path, "r") as file:
        lines = file.readlines()
        experiment_round_total = len(lines)
        for line in lines:
            command_strs = re.findall(r'{[^{}]*}', line)
            # print(command_strs[1])
            command_json = json.loads(command_strs[1])
            id = command_json["addr"]
            diff_json = json.loads(command_strs[2])
            # offset = 1 if diff_json["time"] == 1.2 else 0
            stimuli_array.append(addr_array.index(id))

    # read data file

    file_path = f"study_data/data_infotransfer_arm_P{i}.json"

    with open(file_path, "r") as file:
        lines = file.readlines()
        assert experiment_round_total == len(lines)
        for line in lines:
            data_json = json.loads(line)
            id = data_json["id"]
            # offset = 1 if data_json["isContinuous"] == False else 0
            data_array.append(addr_array.index(id))

print('experiment length = ', len(stimuli_array))

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

category_num = 20

# Create the confusion matrix using NumPy
conf_matrix = confusion_matrix(stimuli_array, data_array)

conf_matrix = np.round(conf_matrix/80.0, 2)

# Plot the confusion matrix as a heatmap using Matplotlib
plt.figure(figsize=(10, 8))
plt.imshow(conf_matrix, cmap='Blues', interpolation='nearest', vmin=0, vmax=1.0)
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

accuracy_array = np.zeros((category_num), dtype=np.float32)

for i in range(category_num):
    accuracy_array[i] = conf_matrix[i, i]

accuracy_str = ', '.join(map(str, accuracy_array))
print(accuracy_str)

