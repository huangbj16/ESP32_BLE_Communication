import time

# def precise_sleep(duration):
#     start = time.perf_counter()
#     end = start + duration

#     while time.perf_counter() < end:
#         pass

#     actual_sleep_duration = time.perf_counter() - start
#     print(f"{start}, {time.perf_counter()}, Actual sleep duration: {actual_sleep_duration} seconds")

# for i in range(10):
#     precise_sleep(0.1)


# import json
# import numpy as np

# commands = []

# for i in range(10):
#     for j in range(5):
#         commands.append({"time":1.0+i/10, "addr":j+1, "mode":1, "duty":3, "freq":2, "wave":1})

# for i in range(5):
#     commands.append({"time":2.0, "addr":i+1, "mode":0, "duty":3, "freq":2, "wave":1})

# file_path = 'commands_max.json'
# with open(file_path, "w") as file:
#     for command in commands:
#         json.dump(command, file)
#         file.write("\n")


import json
import numpy as np

commands = []

### no phantom

# duration  = 0.4
# vib_step = 1.0
# motor_num = 5
# start_time = 1.0

# for i in range(1, motor_num+1):
#     commands.append({"time":round(start_time+i*vib_step, 2), "addr":2*i-1, "mode":1, "duty":7, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+duration, 2), "addr":2*i-1, "mode":0, "duty":7, "freq":2, "wave":0})

# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":round(start_time+duration*motor_num+3.0, 2), "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})


### linear phantom sensation

# start_time = 1.0
# intensity_level = 15
# duration = 0.1
# motor_num = 5
# for i in range(1, motor_num+1):
#     motor_peak_time = start_time + duration * intensity_level * i
#     for j in range(-intensity_level+1, intensity_level):
#         commands.append({"time":round(motor_peak_time+j*duration, 2), "addr":2*i-1, "mode":1, "duty":min(15-abs(j), 15), "freq":2, "wave":0})
#     commands.append({"time":round(motor_peak_time+intensity_level*duration, 2), "addr":2*i-1, "mode":0, "duty":3, "freq":2, "wave":0})

# for i in range(1, 2*motor_num+1):
#     commands.append({"time":start_time+duration*intensity_level*motor_num+3.0, "addr":i, "mode":0, "duty":3, "freq":2, "wave":1})

# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":start_time+duration*intensity_level*motor_num+3.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

### phantom 2cm
# start_time = 1.0
# vib_duration = 0.5
# duty_num = 15
# motor_num = 5
# motor_addrs = [3, 4, 5, 6, 7]

### phantom 4cm
# start_time = 1.0
# vib_duration = 1.0
# duty_num = 15
# motor_num = 3
# motor_addrs = [15, 17, 19]

### phantom 8cm
# start_time = 1.0
# vib_duration = 2.0
# duty_num = 15
# motor_num = 2
# motor_addrs = [15, 19]

# for i in range(motor_num):
#     timestamps_up = np.linspace(start_time+i*vib_duration, start_time+(i+1)*vib_duration, duty_num, endpoint=False)
#     timestamps_down = np.linspace(start_time+(i+1)*vib_duration, start_time+(i+2)*vib_duration, duty_num, endpoint=False)
#     for j in range(duty_num):
#         commands.append({"time":round(timestamps_up[j], 2), "addr":motor_addrs[i], "mode":1, "duty":j, "freq":2, "wave":0})
#     for j in range(duty_num):
#         commands.append({"time":round(timestamps_down[j], 2), "addr":motor_addrs[i], "mode":1, "duty":duty_num-j, "freq":2, "wave":0})
#     commands.append({"time":start_time+(i+2)*vib_duration, "addr":motor_addrs[i], "mode":0, "duty":0, "freq":2, "wave":0})
    
# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":start_time+vib_duration*(motor_num+1)+2.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

### phantom gaussian

# from scipy.stats import norm

# def gaussian_timestamps(mean, sd, levels):
#     duty_values = np.arange(1, levels+1, 1, dtype=np.float32)
#     gaussian = norm(loc=mean, scale=sd)
#     duty_norms = duty_values*gaussian.pdf(mean)/np.max(duty_values)
#     x_values = np.arange(mean-3*sd, mean+0.01, step=0.01)
#     y_values = gaussian.pdf(x_values)
#     timestamps = np.zeros(levels, dtype=np.float32)
#     for i in range(levels):
#         timestamps[i] = x_values[np.argmin(np.abs(y_values-duty_norms[i]))]
#     print(timestamps)
#     return timestamps.tolist()

### 2cm
# start_time = 1.0
# vib_duration = 0.5
# duty_num = 15
# motor_num = 5
# motor_addrs = [3, 4, 5, 6, 7]

### 4cm
# start_time = 1.0
# vib_duration = 1.0
# duty_num = 15
# motor_num = 3
# motor_addrs = [3, 5, 7]

### 8cm
# start_time = 1.0
# vib_duration = 2.0
# duty_num = 15
# motor_num = 2
# motor_addrs = [3, 7]

# for i in range(motor_num):
#     mid_time = start_time+(i+1)*vib_duration
#     sd = 0.6*vib_duration
#     timestamps_up = gaussian_timestamps(mid_time, sd, duty_num)
#     for j in range(duty_num): ## raming up
#         commands.append({"time":round(timestamps_up[j], 2), "addr":motor_addrs[i], "mode":1, "duty":j+1, "freq":2, "wave":0})
#     for j in np.arange(duty_num-1, 0, step=-1): ## raming down
#         commands.append({"time":round(2*mid_time-timestamps_up[j-1], 2), "addr":motor_addrs[i], "mode":1, "duty":int(j), "freq":2, "wave":0})
#     commands.append({"time":round(2*mid_time-timestamps_up[0]+0.1, 2), "addr":motor_addrs[i], "mode":0, "duty":0, "freq":2, "wave":0})
    
# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":start_time+vib_duration*(motor_num+1)+2.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

### funneling illusion in experiment format

# start_time = 0.0
# duration = 0.4
# vib_step = 1.0
# motor_num = 5
# for i in range(1, motor_num+1):
#     commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":2*i-1, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":2*i+1, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":2*i-1, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":2*i+1, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":start_time+vib_step+3.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

### funneling study two motor condition

# start_time = 0.0
# duration = 0.5
# vib_step = 1.0
# motor_addr = 5
# duty_num = 3
# for i in range(duty_num):
#     commands.append({"time":0, "addr":0, "mode":1, "duty":(i+1)*5, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":4, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":6, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":4, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":6, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":start_time+vib_step+2.0, "addr":0, "mode":0, "duty":(i+1)*5, "freq":3, "wave":1})

### funneling study one motor condition

# start_time = 0.0
# duration = 0.5
# vib_step = 1.0
# duty_num = 3
# for i in range(duty_num):
#     # intensity 1
#     commands.append({"time":0, "addr":0, "mode":1, "duty":(i+1)*5, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":5, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":5, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":start_time+vib_step+2.0, "addr":0, "mode":0, "duty":(i+1)*5, "freq":3, "wave":1})

### cutaneous rabbit

# start_time = 0.0
# vib_step = 5.0
# motor_num = 5
# for i in range(1, motor_num+1):
#     # normal
#     commands.append({"time":round(start_time+i*vib_step+0.0, 2), "addr":i, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.20, 2), "addr":i, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.40, 2), "addr":i, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.50, 2), "addr":i, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.50, 2), "addr":i+1, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.70, 2), "addr":i+1, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.70, 2), "addr":i+2, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+0.80, 2), "addr":i+2, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+1.00, 2), "addr":i+2, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+1.20, 2), "addr":i+2, "mode":0, "duty":15, "freq":2, "wave":0})
#     # illusion
#     commands.append({"time":round(start_time+i*vib_step+2.0, 2), "addr":i, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+2.20, 2), "addr":i, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+2.40, 2), "addr":i, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+2.60, 2), "addr":i, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+2.60, 2), "addr":i+2, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+2.80, 2), "addr":i+2, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+3.00, 2), "addr":i+2, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+i*vib_step+3.20, 2), "addr":i+2, "mode":0, "duty":15, "freq":2, "wave":0})
    

### phantom sensation outside stimuli

# DutyMax = 15
# DutyBase = 5
# dtime = 1.0
# start_time = 1.0
# time_step = 0.1
# step = int(round(dtime / time_step))
# duty_step = 5/float(step)

# for i in range(2*step):
#     commands.append({"time":round(start_time+i*time_step, 1), "addr":5, "mode":1, "duty":int(round(DutyBase+duty_step*i)), "freq":2, "wave":0})
# for i in range(3*step+1):
#     commands.append({"time":round(start_time+time_step*2*step+i*time_step, 1), "addr":5, "mode":1, "duty":int(round(DutyMax-duty_step*i)), "freq":2, "wave":0})
# for i in range(3*step):
#     commands.append({"time":round(start_time+i*time_step, 1), "addr":6, "mode":1, "duty":int(round(duty_step*i)), "freq":2, "wave":0})
# for i in range(2*step+1):
#     commands.append({"time":round(start_time+time_step*3*step+i*time_step, 1), "addr":6, "mode":1, "duty":int(round(DutyMax-duty_step*i)), "freq":2, "wave":0})

# commands.append({"time":round(start_time+time_step*5*step+1.0, 1), "addr":5, "mode":0, "duty":15, "freq":2, "wave":0})
# commands.append({"time":round(start_time+time_step*5*step+1.0, 1), "addr":6, "mode":0, "duty":15, "freq":2, "wave":0})

# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":round(start_time+time_step*5*step+2.0, 1), "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})


### info transfer body
# ids = [1,2,3,4,5,10,9,8,7,6,31,32,33,34,35,40,39,38,37,36]
# start_time = 0.0
# duration = 1.0
# vib_step = 1.0
# duty_num = 3
# for id in ids:
#     # intensity 1
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":1, "duty":1, "freq":0, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":1, "duty":1, "freq":0, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":7, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":7, "freq":2, "wave":0})
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":0, "duty":1, "freq":0, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":0, "duty":1, "freq":0, "wave":1})
#     # intensity 2
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":1, "duty":3, "freq":0, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":1, "duty":3, "freq":0, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":7, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":7, "freq":2, "wave":0})
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":0, "duty":3, "freq":0, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":0, "duty":3, "freq":0, "wave":1})

# for id in ids:
#     # pattern 1: continuous
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":1, "duty":1, "freq":1, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":1, "duty":1, "freq":1, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":0, "duty":1, "freq":1, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":0, "duty":1, "freq":1, "wave":1})
#     # pattern 2: discrete
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":1, "duty":1, "freq":1, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":1, "duty":1, "freq":1, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.2, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.4, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.6, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.8, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     if id < 30:
#         commands.append({"time":0, "addr":0, "mode":0, "duty":1, "freq":1, "wave":1})
#     else:
#         commands.append({"time":0, "addr":30, "mode":0, "duty":1, "freq":1, "wave":1})

### info transfer arm

# ids = [92,94,96,98,100,109,107,105,103,101,62,64,66,68,70,79,77,75,73,71]
# start_time = 0.0
# duration = 1.0
# vib_step = 1.0
# duty_num = 3
# for id in ids:
#     # intensity 1
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":1, "duty":1, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":1, "duty":1, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":0, "duty":1, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":0, "duty":1, "freq":3, "wave":1})

# for id in ids:
#     # pattern 1: continuous
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":1, "duty":3, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":1, "duty":3, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":0, "duty":3, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":0, "duty":3, "freq":3, "wave":1})
#     # pattern 2: discrete
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":1, "duty":3, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":1, "duty":3, "freq":3, "wave":1})
#     commands.append({"time":round(start_time+vib_step, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.2, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.4, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.6, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+0.8, 2), "addr":id, "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+vib_step+duration, 2), "addr":id, "mode":0, "duty":15, "freq":2, "wave":0})
#     if id < 90:
#         commands.append({"time":0, "addr":60, "mode":0, "duty":3, "freq":3, "wave":1})
#     else:
#         commands.append({"time":0, "addr":90, "mode":0, "duty":3, "freq":3, "wave":1})


# commands.append({"time":0, "addr":0, "mode":1, "duty":1, "freq":1, "wave":1})
# for i in range(50):
#     for j in range(5):
#         commands.append({"time":round(i*0.10, 2), "addr":j, "mode":1, "duty":15, "freq":2, "wave":0})
#     for j in range(5):
#         commands.append({"time":round(i*0.10+0.05, 2), "addr":j, "mode":0, "duty":15, "freq":2, "wave":0})
# commands.append({"time":10.0, "addr":0, "mode":0, "duty":1, "freq":1, "wave":1})

# commands.sort(key=lambda x: x['addr'])
# commands.sort(key=lambda x: x['time'])


##### create top-down pattern on the sleeve.

# commands.append({"time":1.0, "addr":0, "mode":1, "duty":1, "freq":3, "wave":1})
# commands.append({"time":1.0, "addr":30, "mode":1, "duty":1, "freq":3, "wave":1})
# commands.append({"time":1.0, "addr":60, "mode":1, "duty":1, "freq":3, "wave":1})
# commands.append({"time":1.0, "addr":120, "mode":1, "duty":1, "freq":3, "wave":1})

# start_time = 2.0
# duration_array = [0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02, 0.01]
# # for duration in np.linspace(0.4, 0.02, num=8):
# for duration in duration_array:
#     for i in range(5):
#         motor_addrs = [i+1, 10-i, 31+i, 40-i, 61+2*i, 80-2*i, 121+2*i, 140-2*i]
#         for addr in motor_addrs:
#             commands.append({"time":round(start_time, 2), "addr":addr, "mode":1, "duty":12, "freq":2, "wave":0})
#         for addr in motor_addrs:
#             commands.append({"time":round(start_time+duration, 2), "addr":addr, "mode":0, "duty":12, "freq":2, "wave":0})
#         start_time += duration
# # for i in range(5):
# #     motor_addrs = [i+1, 10-i, 31+i, 40-i, 61+2*i, 80-2*i, 121+2*i, 140-2*i]
# #     for addr in motor_addrs:
# #         commands.append({"time":round(start_time, 2), "addr":addr, "mode":1, "duty":1, "freq":1, "wave":1})
# # start_time += 3.0
# # for i in range(5):
# #     motor_addrs = [i+1, 10-i, 31+i, 40-i, 61+2*i, 80-2*i, 121+2*i, 140-2*i]
# #     for addr in motor_addrs:
# #         commands.append({"time":round(start_time, 2), "addr":addr, "mode":0, "duty":1, "freq":1, "wave":1})

# start_time += 2.0
# commands.append({"time":round(start_time, 2), "addr":0, "mode":0, "duty":1, "freq":1, "wave":1})
# commands.append({"time":round(start_time, 2), "addr":30, "mode":0, "duty":1, "freq":1, "wave":1})
# commands.append({"time":round(start_time, 2), "addr":60, "mode":0, "duty":1, "freq":1, "wave":1})
# commands.append({"time":round(start_time, 2), "addr":120, "mode":0, "duty":1, "freq":1, "wave":1})

# commands.append({"time":8.0, "addr":0, "mode":0, "duty":1, "freq":1, "wave":1})
# commands.append({"time":8.0, "addr":30, "mode":0, "duty":1, "freq":1, "wave":1})


##### create random breathing patterns on the shirt


# motor_ids = [
#     1,
#     2,
#     3,
#     4,
#     5,
#     6,
#     7,
#     8,
#     9,
#     10,
#     31,
#     32,
#     33,
#     34,
#     35,
#     36,
#     37,
#     38,
#     39,
#     40,
#     61,
#     62,
#     63,
#     64,
#     65,
#     66,
#     67,
#     68,
#     69,
#     70,
#     71,
#     72,
#     73,
#     74,
#     75,
#     76,
#     77,
#     78,
#     79,
#     80,
#     121,
#     122,
#     123,
#     124,
#     125,
#     126,
#     127,
#     128,
#     129,
#     130,
#     131,
#     132,
#     133,
#     134,
#     135,
#     136,
#     137,
#     138,
#     139,
#     140
# ]
# motor_ids = np.array(motor_ids)
# start_time = 1.0

# # duration_array = [1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02]
# duration_array = [0.8, 1.1, 1.0, 0.9, 1.2, 0.9, 0.7, 1.0]
# for duration in duration_array:
#     activated_ids = np.random.choice(motor_ids, size=30, replace=False)
#     print(activated_ids)
#     for addr in activated_ids:
#         commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":1, "freq":1, "wave":1})
#     for addr in activated_ids:
#         commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":1, "freq":1, "wave":1})
#     start_time += duration
# for addr in motor_ids:
#     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":1, "freq":1, "wave":1})
# start_time += 3.0
# for addr in motor_ids:
#     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":0, "duty":1, "freq":1, "wave":1})


### linear arm pattern

# start_time = 25.0
# duration = 0.2
# for addr in range(1, 21):
#     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration
# for addr in range(31, 51):
#     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration

### downstream

# start_time = 15.0
# duration = 0.2
# for i in range(10):
#     addrs = [10-i, 10+i+1, 40-i, 40+i+1]
#     for addr in addrs:
#         commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     for addr in addrs:
#         commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration
# for i in range(10):
#     addrs = [i+1, 20-i, 30+i+1, 50-i]
#     for addr in addrs:
#         commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     for addr in addrs:
#         commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration
# for i in range(10):
#     addrs = [10-i, 10+i+1, 40-i, 40+i+1]
#     for addr in addrs:
#         commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     for addr in addrs:
#         commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration

##### create random breathing patterns on the shirt

# motor_ids = [
#     1,
#     2,
#     3,
#     4,
#     5,
#     6,
#     7,
#     8,
#     9,
#     10,
#     11,
#     12,
#     13,
#     14,
#     15,
#     16,
#     17,
#     18,
#     19,
#     20,
#     31,
#     32,
#     33,
#     34,
#     35,
#     36,
#     37,
#     38,
#     39,
#     40,
#     41,
#     42,
#     43,
#     44,
#     45,
#     46,
#     47,
#     48,
#     49,
#     50
# ]
# motor_ids = np.array(motor_ids)
# start_time = 1.0

# # duration_array = [1.0, 0.8, 0.6, 0.5, 0.4, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02]
# duration_array = [0.8, 1.1, 1.0, 0.9, 1.2, 0.9, 0.7, 1.0]
# for duration in duration_array:
#     activated_ids = np.random.choice(motor_ids, size=10, replace=False)
#     print(activated_ids)
#     for addr in activated_ids:
#         commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":15, "freq":2, "wave":0})
#     for addr in activated_ids:
#         commands.append({"time":round(start_time+duration, 2), "addr":int(addr), "mode":0, "duty":15, "freq":2, "wave":0})
#     start_time += duration
# # for addr in motor_ids:
# #     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":1, "duty":1, "freq":1, "wave":1})
# # start_time += 3.0
# for addr in motor_ids:
#     commands.append({"time":round(start_time, 2), "addr":int(addr), "mode":0, "duty":1, "freq":1, "wave":1})


### phantom gaussian

from scipy.stats import norm

def gaussian_timestamps(mean, sd, levels):
    duty_values = np.arange(1, levels+1, 1, dtype=np.float32)
    gaussian = norm(loc=mean, scale=sd)
    duty_norms = duty_values*gaussian.pdf(mean)/np.max(duty_values)
    x_values = np.arange(mean-3*sd, mean+0.01, step=0.01)
    y_values = gaussian.pdf(x_values)
    timestamps = np.zeros(levels, dtype=np.float32)
    for i in range(levels):
        timestamps[i] = x_values[np.argmin(np.abs(y_values-duty_norms[i]))]
    print(timestamps)
    return timestamps.tolist()

# ## 2cm
# start_time = 1.0
# vib_duration = 0.5
# duty_num = 15
# motor_num = 5
# motor_addrs = [3, 4, 5, 6, 7]

# ## 4cm
# start_time = 40.0
# vib_duration = 0.4
# duty_num = 15
# motor_num = 10
# motor_addrs = [31, 33, 35, 37, 39, 40, 38, 36, 34, 32]

# for i in range(motor_num):
#     mid_time = start_time+(i+1)*vib_duration
#     sd = 0.6*vib_duration
#     timestamps_up = gaussian_timestamps(mid_time, sd, duty_num)
#     for j in range(duty_num): ## raming up
#         commands.append({"time":round(timestamps_up[j], 2), "addr":motor_addrs[i], "mode":1, "duty":j+1, "freq":2, "wave":0})
#     for j in np.arange(duty_num-1, 0, step=-1): ## raming down
#         commands.append({"time":round(2*mid_time-timestamps_up[j-1], 2), "addr":motor_addrs[i], "mode":1, "duty":int(j), "freq":2, "wave":0})
#     commands.append({"time":round(2*mid_time-timestamps_up[0]+0.1, 2), "addr":motor_addrs[i], "mode":0, "duty":0, "freq":2, "wave":0})

# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":start_time+vib_duration*(motor_num+1)+2.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})




## 4cm
# start_time = 1.0
# vib_duration = 0.2
# duty_num = 15
# motor_num = 10
# motor_addrs_array = [
#     np.arange(1, 11, step=1, dtype=np.int),
#     np.arange(20, 10, step=-1, dtype=np.int),
#     np.arange(31, 41, step=1, dtype=np.int),
#     np.arange(50, 40, step=-1, dtype=np.int)
# ]

# for i in range(2):
#     motor_addrs = motor_addrs_array[i]
#     for i in range(motor_num):
#         mid_time = start_time+(i+1)*vib_duration
#         sd = 0.6*vib_duration
#         timestamps_up = gaussian_timestamps(mid_time, sd, duty_num)
#         for j in range(duty_num): ## raming up
#             commands.append({"time":round(timestamps_up[j], 2), "addr":int(motor_addrs[i]), "mode":1, "duty":j+1, "freq":2, "wave":0})
#         for j in np.arange(duty_num-1, 0, step=-1): ## raming down
#             commands.append({"time":round(2*mid_time-timestamps_up[j-1], 2), "addr":int(motor_addrs[i]), "mode":1, "duty":int(j), "freq":2, "wave":0})
#         commands.append({"time":round(2*mid_time-timestamps_up[0]+0.1, 2), "addr":int(motor_addrs[i]), "mode":0, "duty":0, "freq":2, "wave":0})



start_time = 67.0
vib_duration = 0.2
motor_num = 10
col_num = 4
motor_addrs_array = [
    np.arange(1, 11, step=1, dtype=np.int),
    np.arange(20, 10, step=-1, dtype=np.int),
    np.arange(31, 41, step=1, dtype=np.int),
    np.arange(50, 40, step=-1, dtype=np.int)
]
motor_addrs = np.array(motor_addrs_array)
print(motor_addrs)

for repeat in range(5):
    for i in range(col_num):
        for j in range(3):
            vib_time = start_time+(repeat*col_num+i)*vib_duration
            commands.append({"time":round(vib_time, 2), "addr":int(motor_addrs[i][5+j]), "mode":1, "duty":15, "freq":2, "wave":0})
            commands.append({"time":round(vib_time+vib_duration, 2), "addr":int(motor_addrs[i][5+j]), "mode":0, "duty":15, "freq":2, "wave":0})


# start_time = 50.0
# vib_duration = 0.2
# motor_num = 10
# col_num = 4
# motor_addrs_array = [
#     np.arange(1, 11, step=1, dtype=np.int),
#     np.arange(20, 10, step=-1, dtype=np.int),
#     np.arange(31, 41, step=1, dtype=np.int),
#     np.arange(50, 40, step=-1, dtype=np.int)
# ]
# motor_addrs = np.array(motor_addrs_array)
# print(motor_addrs)

# for repeat in range(5):
#     for i in range(5):
#         motor_ids = motor_addrs[:, i]
#         vib_time = start_time+(repeat*12+i)*vib_duration
#         end_time = start_time+(repeat*12+10-i)*vib_duration
#         for j in motor_ids:
#             commands.append({"time":round(vib_time, 2), "addr":int(j), "mode":1, "duty":15, "freq":2, "wave":0})
#             commands.append({"time":round(end_time, 2), "addr":int(j), "mode":0, "duty":15, "freq":2, "wave":0})                      

commands.sort(key=lambda x: x['addr'])
commands.sort(key=lambda x: x['time'])

file_path = 'commands/commands_arm_temp.json'
with open(file_path, "w") as file:
    counter = 0
    for command in commands:
        json.dump(command, file)
        file.write('\n')
        # counter += 1
        # if counter == 4:
        #     file.write("\n")
        # if counter == 12:
        #     file.write("\n")
        #     counter = 0