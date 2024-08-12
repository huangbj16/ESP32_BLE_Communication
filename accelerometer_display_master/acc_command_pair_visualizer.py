'''
read acc and command pair data from the folder,
and visualize the data in a plot.

each line of acc data is in the format of:
{"time": "1.6956172", "acc": [0.16, 0.24, 10.04]}

each line of command data is in the format of:
{"time": 2.02, "addr": 1, "mode": 1, "duty": 2, "freq": 2, "wave": 0}

in a plot, x-axis is time, y-axis plots the acc data in 2-norm acceleration and the command data in duty (0-15).

Since the acc data and command data are not synchronized, we need to align the data by time.

the alignment is done by selecting the first acc data that has acceleration over 1.00, and the first command data time.
'''
import json
import os
import numpy as np
import matplotlib.pyplot as plt

folder_name = 'acc_command_pairs'
acc_data = 'acc_triangles.txt'
command_data = 'command_triangles.json'

acc_data_path = os.path.join(folder_name, acc_data)
command_data_path = os.path.join(folder_name, command_data)

acc_data_list = []
command_data_list = []

with open(acc_data_path, 'r') as f:
    for line in f:
        acc_data_list.append(json.loads(line))

with open(command_data_path, 'r') as f:
    for line in f:
        command_data_list.append(json.loads(line))

# compute 2-norm for acc
acc_data_norm = []
for acc_data in acc_data_list:
    # acc = acc_data['acc']
    acc = acc_data['acc'][0] # only X-axis
    acc_norm = np.linalg.norm(acc)
    acc_data_norm.append({'time': acc_data['time'], 'acc': acc_norm})
# sort
acc_data_norm = sorted(acc_data_norm, key=lambda x: x['time'])
# print min, max and mean for acc
acc_norm_list = [acc_data['acc'] for acc_data in acc_data_norm]
print('min acc = ', min(acc_norm_list))
print('max acc = ', max(acc_norm_list))
print('mean acc = ', np.mean(acc_norm_list))

### average every 10 ms
# acc_data_norm_avg = []
# acc_data_norm_avg.append(acc_data_norm[0])
# acc_data_norm_avg_index = 0
# avg_count = 1
# for i in range(1, len(acc_data_norm)):
#     if acc_data_norm[i]['time'] - acc_data_norm_avg[acc_data_norm_avg_index]['time'] < 0.01:
#         acc_data_norm_avg[acc_data_norm_avg_index]['acc'] = (acc_data_norm_avg[acc_data_norm_avg_index]['acc'] + acc_data_norm[i]['acc'])
#         avg_count += 1
#     else:
#         acc_data_norm_avg[acc_data_norm_avg_index]['acc'] = acc_data_norm_avg[acc_data_norm_avg_index]['acc'] / avg_count
#         acc_data_norm_avg.append(acc_data_norm[i])
#         acc_data_norm_avg_index += 1
#         avg_count = 1
# acc_data_norm = acc_data_norm_avg

### sort command list
command_data_list = sorted(command_data_list, key=lambda x: x['time'])

# find the alignment point
align_time_acc = 0
align_acc_index = 0
for acc_data in acc_data_norm:
    if acc_data['acc'] > 5.00:
        align_time_acc = acc_data['time']
        align_acc_index = acc_data_norm.index(acc_data)
        break
acc_data_norm = acc_data_norm[align_acc_index:]
align_time_command = command_data_list[0]['time']
print('align_time_acc = ', align_time_acc)
print('align_time_command = ', align_time_command)
align_time_diff = align_time_command - align_time_acc

for i in range(len(acc_data_norm)):
    acc_data_norm[i]['time'] = acc_data_norm[i]['time'] + align_time_diff

# plot acc_data_norm and command_data_list in the same plot, with left y-axis for acc and right y-axis for command
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot([acc_data['time'] for acc_data in acc_data_norm], [acc_data['acc'] for acc_data in acc_data_norm], 'r.-')
ax2.plot([command_data['time'] for command_data in command_data_list], [command_data['duty'] for command_data in command_data_list], 'b.-')
# set x range
plt.xlim(command_data_list[0]['time'], command_data_list[-1]['time'])
plt.show()

