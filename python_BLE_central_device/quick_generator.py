import time

def precise_sleep(duration):
    start = time.perf_counter()
    end = start + duration

    while time.perf_counter() < end:
        pass

    actual_sleep_duration = time.perf_counter() - start
    print(f"{start}, {time.perf_counter()}, Actual sleep duration: {actual_sleep_duration} seconds")

for i in range(10):
    precise_sleep(0.1)


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
