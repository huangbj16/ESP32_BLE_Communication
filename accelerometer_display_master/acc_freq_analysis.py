import json
import numpy as np
import matplotlib.pyplot as plt

# Lists to store the extracted data
times = []
accs = []

# Read the file line by line
with open('acc_data.txt', 'r') as file:
    for line in file:
        data = json.loads(line)
        times.append(float(data['time']))
        accs.append(data['acc'])

# Convert lists to numpy arrays
times_array = np.array(times)
accs_array = np.array(accs)

print(times_array.shape)
print(accs_array.shape)

### Plotting the data
plt.figure(figsize=(10, 6))

# Plot each axis of the acceleration data
plt.xticks(np.arange(round(times_array[0])-1, round(times_array[-1])+1, step=1))
plt.plot(times_array, accs_array[:, 0], color='r', label='X-axis')
plt.plot(times_array, accs_array[:, 1], color='g', label='Y-axis')
plt.plot(times_array, accs_array[:, 2], color='b', label='Z-axis')

# Add legends, labels, and a title
plt.legend()
plt.xlabel('Time')
plt.ylabel('Acceleration')
plt.title('Acceleration Data Over Time')
plt.grid(True)
plt.tight_layout()

plt.show()

### plot frequency spectrum

plt.clf()

ss = [4015, 7091, 10934, 15548]
ee = [4781, 7855, 11699, 16313]

import matplotlib
cc = [matplotlib.cm.Set1(i) for i in np.linspace(0, 0.375, 4)]
labels = ['140Hz', '170Hz', '200Hz', '235Hz']

for i in range(4):
    time_array = times_array[ss[i]:ee[i]]
    acc_array = accs_array[ss[i]:ee[i]]

    acc_len = acc_array.shape[0]
    # acc_abs = np.linalg.norm(acc_array, axis=1)
    acc_z = acc_array[:, 1]
    acc_fft = np.fft.fft(acc_z)[1:acc_len>>1]
    acc_freq = np.fft.fftfreq(acc_len, 1/acc_len)[1:acc_len>>1]

    plt.plot(acc_freq, 2.0 / acc_len * np.abs(acc_fft), color=cc[i], label=labels[i])

plt.legend(fontsize=18)
plt.xlim(95, 305)
# plt.ylim(0, 100)
plt.xticks(np.arange(100, 305, 10))
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title('Frequency Spectrum Of Accelerations At Four Frequency conditions', y=1.05, fontsize=22)
plt.xlabel('Frequency (Hz)', labelpad=15, fontsize=22)
plt.ylabel('Magnitude', labelpad=15, fontsize=22)
plt.tight_layout()
plt.show()