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
# intensity_level = 8
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

### funneling study one motor condition

start_time = 0.0
duration = 0.5
vib_step = 1.0
motor_num = 20
for i in range(1, motor_num+1):
    commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
    commands.append({"time":round(start_time+vib_step, 2), "addr":2*i-1, "mode":1, "duty":15, "freq":2, "wave":0})
    commands.append({"time":round(start_time+vib_step+duration, 2), "addr":2*i-1, "mode":0, "duty":15, "freq":2, "wave":0})
    commands.append({"time":start_time+vib_step+2.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

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
    

# commands.append({"time":0, "addr":0, "mode":1, "duty":15, "freq":3, "wave":1})
# commands.append({"time":start_time+vib_step*motor_num+vib_step+3.0, "addr":0, "mode":0, "duty":15, "freq":3, "wave":1})

# commands.sort(key=lambda x: x['addr'])
# commands.sort(key=lambda x: x['time'])

file_path = 'commands/InfoTransfer_one_motor_skip.json'
with open(file_path, "w") as file:
    counter = 0
    for command in commands:
        json.dump(command, file)
        counter += 1
        if counter == 4:
            file.write("\n")
            counter = 0