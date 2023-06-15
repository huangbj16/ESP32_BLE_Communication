import json
import numpy as np

commands = []

for i in range(10):
    for j in range(5):
        commands.append({"time":1.0+i/10, "addr":j+1, "mode":1, "duty":3, "freq":2, "wave":1})

for i in range(5):
    commands.append({"time":2.0, "addr":i+1, "mode":0, "duty":3, "freq":2, "wave":1})

file_path = 'commands_max.json'
with open(file_path, "w") as file:
    for command in commands:
        json.dump(command, file)
        file.write("\n")
