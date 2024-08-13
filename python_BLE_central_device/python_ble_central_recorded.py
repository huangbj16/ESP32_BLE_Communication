import asyncio
from bleak import BleakScanner, BleakClient
import json
import time
import threading

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e410'

# file_commands = 'commands/commands_gradual_rise_and_fall.json'
file_commands = 'commands_meta_haptic/v-09-12-2-17/v-09-12-2-17.json'


'''
commands_arm_collection
'''
'''
commands_side_center.json
commands_linear_stroke.json
commands_vertical_stroke.jsonpow
commands_cross_pattern.json
'''

# import pygame

# def play_wav_file():
#     audio_file = "haps_files/drum.wav"
#     pygame.init()
#     pygame.mixer.init()

#     try:
#         sound = pygame.mixer.Sound(audio_file)
#         sound.play()
#         pygame.time.wait(int(sound.get_length() * 1000))  # Wait for the sound to finish
#     except pygame.error as e:
#         print(f"An error occurred: {e}")
#     finally:
#         pygame.quit()


def create_command(addr, mode, duty, freq, wave):
    serial_group = addr // 30
    serial_addr = addr % 30
    byte1 = (serial_group << 2) | (mode & 0x01)
    byte2 = 0x40 | (serial_addr & 0x3F)  # 0x40 represents the leading '01'
    byte3 = 0x80 | ((duty & 0x0F) << 3) | ((freq & 0x03) << 1) | (wave & 0x01)  # 0x80 represents the leading '1'
    return bytearray([byte1, byte2, byte3])

async def sendCommands(client):
    # audio_thread = threading.Thread(target=play_wav_file)
    # audio_thread.start()

    with open(file_commands) as f:
        commands = f.readlines()
        command_idx = 0
        time_offset = time.perf_counter() # record the starting time
        while command_idx < len(commands):
            # collect commands that are at the same time and form the output
            command_parsed = json.loads(commands[command_idx])
            command_output = bytearray([])
            command_output = command_output + create_command(command_parsed['addr'], command_parsed['mode'], command_parsed['duty'], command_parsed['freq'], command_parsed['wave'])
            ts = float(command_parsed['time'])
            command_idx += 1
            command_count = 1 # max allowed in one command is 7
            while True:
                if command_count == 7:
                    break
                if command_idx < len(commands):
                    command_parsed = json.loads(commands[command_idx])
                    if (ts+1e-6) > float(command_parsed['time']): # basically two commands are at the same time
                        command_output = command_output + create_command(command_parsed['addr'], command_parsed['mode'], command_parsed['duty'], command_parsed['freq'], command_parsed['wave'])
                        command_idx += 1
                        command_count += 1
                    else:
                        break
                else:
                    break
            command_output = command_output + bytearray([0xFF, 0xFF, 0xFF]) * (20-command_count)
            # wait for the send time
            print('command time = ', ts)
            start = time.perf_counter()
            # await asyncio.sleep(ts-current_time)
            while (time.perf_counter()-time_offset) < ts:
                pass
            # actual_sleep_duration = time.perf_counter() - start
            # print(f"{start}, Actual sleep duration: {actual_sleep_duration} seconds")
            # print('commands = \n', command_output)
            # print('command len = ', len(command_output))
            await client.write_gatt_char(MOTOR_UUID,  command_output)
            

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'QT Py ESP32-S3':
                print('central unit BLE found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    print('mtu_size = ', client.mtu_size)
                    val = await client.read_gatt_char(MOTOR_UUID)
                    print('Motor read = ', val)
                    await sendCommands(client)

asyncio.run(main())