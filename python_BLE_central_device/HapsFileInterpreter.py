import json
import numpy as np

'''
m_vibration
    m_melodies
        [0]m_notes (transient)
            [0]m_startingPoint
            [0]m_gain
            [1]m_startingPoint
            [1]m_gain
        [2]m_notes (vibrations)
            [0]m_hapticEffect
                m_amplitudeModulation
                    m_keyframes
                        m_time
                        m_value
            
'''

def extract_vibration_commands(json_data):
    # Check if 'm_vibration' and 'm_melodies' keys are in the json_data
    transient_array = []
    vibration_array = []
    if 'm_vibration' in json_data and 'm_melodies' in json_data['m_vibration']:
        melodies = json_data['m_vibration']['m_melodies']
        print("transient # = ", len(melodies[0]["m_notes"]))
        for t_data in melodies[0]["m_notes"]:
            transient_array.append({"time": np.round(t_data["m_startingPoint"], 2), "duty": np.round(t_data["m_gain"]*16)})
        print("vibration # = ", len(melodies[2]["m_notes"][0]["m_hapticEffect"]["m_amplitudeModulation"]["m_keyframes"]))
        for v_data in melodies[2]["m_notes"][0]["m_hapticEffect"]["m_amplitudeModulation"]["m_keyframes"]:
            vibration_array.append({"time": np.round(v_data["m_time"], 2), "duty": np.round(v_data["m_value"] * 16)})
    else:
        print("The provided JSON does not contain the required structure.")
    print(transient_array)
    print(vibration_array)
    return transient_array, vibration_array

# Load the JSON data from a file or a string
json_file_path = 'haps_files/Shotgun.haps'  # Replace with your JSON file path
with open(json_file_path, 'r') as file:
    data = json.load(file)
    transient_array, vibration_array = extract_vibration_commands(data)

# combine transient into vibration
for t_data in transient_array:
    t_data["time"] = np.round(t_data["time"]+0.01, 2)
    vibration_array.append(t_data)
vibration_array.sort(key=lambda x: x['time'])

print("combined vibration\n", vibration_array)

unique_entries = {}
for entry in vibration_array:
    time = entry['time']
    duty = entry['duty']
    if time not in unique_entries or duty > unique_entries[time]['duty']:
        unique_entries[time] = entry

vibration_array = list(unique_entries.values())

print("cleaned vibration\n", vibration_array)

# turn into our command types, also add interpolation.

import numpy as np

# Given array of vibration commands
commands = [
    {'time': 0, 'duty': 4.0}, {'time': 0.01, 'duty': 16.0}, {'time': 0.02, 'duty': 15.0},
    {'time': 0.07, 'duty': 13.0}, {'time': 0.11, 'duty': 8.0}, {'time': 0.18, 'duty': 3.0},
    {'time': 0.22, 'duty': 3.0}, {'time': 0.28, 'duty': 1.0}, {'time': 0.32, 'duty': 1.0},
    {'time': 0.42, 'duty': 0.0}, {'time': 0.57, 'duty': 14.0}, {'time': 0.72, 'duty': 0.0},
    {'time': 0.82, 'duty': 0.0}, {'time': 0.88, 'duty': 15.0}, {'time': 1.17, 'duty': 0},
    {'time': 2.35, 'duty': 0}
]

# Interpolation function
def interpolate_commands(commands, interval=0.05, motor_addr = 15):
    # Convert the commands to a numpy array for easier processing
    times = np.array([cmd['time'] for cmd in commands])
    duties = np.array([cmd['duty'] for cmd in commands])
    
    # Prepare the output list
    interpolated_commands = []
    
    # Starting time for interpolation
    current_time = 0
    
    # Iterate over the commands
    for i in range(len(times) - 1):
        # Add the current command to the output list
        # {"time": 1.0, "addr": 17, "mode": 1, "duty": 15, "freq": 2, "wave": 0}
        if duties[i] == 0:
            interpolated_commands.append({'time': times[i], 'addr': motor_addr, 'mode': 0, 'duty': int(duties[i]), 'freq': 2, 'wave':0})
        else:
            interpolated_commands.append({'time': times[i], 'addr': motor_addr, 'mode': 1, 'duty': int(duties[i]), 'freq': 2, 'wave':0})
        
        # Calculate the time difference to the next command
        time_diff = times[i+1] - times[i]

        if duties[i] == duties[i+1]: # no need for interpolation
            continue
        
        # If the time difference is larger than the interval, perform interpolation
        if time_diff > interval:
            # Calculate the number of interpolations needed
            num_interpolations = int(np.floor(time_diff / interval))
            
            # Linear interpolation for each step
            for j in range(1, num_interpolations + 1):
                current_time = times[i] + j * interval
                # Interpolated duty based on the linear interpolation formula
                interpolated_duty = np.interp(current_time, times[i:i+2], duties[i:i+2])
                if np.round(interpolated_duty) == 0:
                    interpolated_commands.append({'time': np.round(current_time, 2), 'addr': motor_addr, 'mode': 0, 'duty': int(interpolated_duty), 'freq': 2, 'wave':0})
                else:
                    interpolated_commands.append({'time': np.round(current_time, 2), 'addr': motor_addr, 'mode': 1, 'duty': int(interpolated_duty), 'freq': 2, 'wave':0})
    
    # Add the last command
    interpolated_commands.append({'time': times[-1], 'addr': motor_addr, 'mode': 0, 'duty': int(duties[-1]), 'freq': 2, 'wave':0})
    
    return interpolated_commands

# Interpolate the commands
commands = interpolate_commands(vibration_array)

print(commands)

file_path = 'commands/commands_Shotgun.json'
with open(file_path, "w") as file:
    counter = 0
    for command in commands:
        json.dump(command, file)
        file.write('\n')