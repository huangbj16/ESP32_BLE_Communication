import json

def read_haptic_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def map_amplitude_to_duty(amplitude):
    # Assuming amplitude ranges from 0 to 1, map it to an integer from 0 to 15.
    return int(amplitude * 15)

def convert_haptic_to_custom_format(haptic_data):
    envelopes = haptic_data["signals"]["continuous"]["envelopes"]["amplitude"]
    custom_format_data = []
    start_offset = 2.0

    for envelope in envelopes:        
        time = envelope["time"]
        amplitude = envelope["amplitude"]
        print("time: ", time, "amplitude: ", amplitude)
        duty = map_amplitude_to_duty(amplitude)
        mode = 1 if duty > 0 else 0
        # Create the custom formatted dictionary
        custom_entry = {
            "time": round(start_offset+time, 3),
            "addr": 1,  # default as specified
            "mode": mode,  # 1 for start
            "duty": duty,
            "freq": 2,  # default frequency
            "wave": 0   # default wave
        }
        
        custom_format_data.append(custom_entry)
    # add the stop command
    custom_entry = {
        "time": round(start_offset+time+0.1, 3),
        "addr": 1,  # default as specified
        "mode": 0,  # 0 for stop
        "duty": 0,
        "freq": 2,  # default frequency
        "wave": 0   # default wave
    }
    custom_format_data.append(custom_entry)

    return custom_format_data

def write_custom_format_file(custom_data, output_file_path):
    with open(output_file_path, 'w') as file:
        for entry in custom_data:
            file.write(json.dumps(entry) + '\n')

def main():
    input_file_path = 'commands_meta_haptic/v-09-12-2-17/v-09-12-2-17.haptic'  # Example file path
    output_file_path = 'commands_meta_haptic/v-09-12-2-17/v-09-12-2-17.json'
    
    # Reading .haptic file
    haptic_data = read_haptic_file(input_file_path)
    
    # Converting to custom format
    custom_format_data = convert_haptic_to_custom_format(haptic_data)
    
    # Writing custom formatted data to a file
    write_custom_format_file(custom_format_data, output_file_path)
    print(f"Conversion complete. Data written to {output_file_path}")

if __name__ == "__main__":
    main()
