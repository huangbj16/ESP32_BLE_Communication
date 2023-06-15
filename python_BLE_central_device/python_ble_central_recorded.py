import asyncio
from bleak import BleakScanner, BleakClient
import json
import time

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e410'

file_commands = 'commands_max.json'

current_time = 0

# async def setMotor(client):
#     while True:
#         motor_addr = int(input('what is the next motor you want to control?'))
#         start_or_stop = int(input('1 for start and 0 for stop?'))
#         # duty = int(input('0-3 for duty?'))
#         command = {
#             'addr':motor_addr,
#             'mode':start_or_stop,
#             'duty':3, # default
#             'freq':2, # default
#             'wave':1, # default
#         }
#         output = bytearray(json.dumps(command), 'utf-8')
#         await client.write_gatt_char(MOTOR_UUID,  output)

async def sendCommands(client):
    global current_time
    with open(file_commands) as f:
        commands = f.readlines()
        for command in commands:
            command_parsed = json.loads(command)
            ts = float(command_parsed['time'])
            if ts > (current_time + 1e-6):
                print('wait for ', ts-current_time)
                await asyncio.sleep(ts-current_time)
            current_time = ts
            print(command.replace('\n', ''))
            output = bytearray(command, 'utf-8')
            print(time.time_ns()/(10**9))
            await client.write_gatt_char(MOTOR_UUID,  output)
            print(time.time_ns()/(10**9))
            

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'FEATHER_ESP32':
                print('feather device found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    val = await client.read_gatt_char(MOTOR_UUID)
                    print('Motor read = ', val)
                    await sendCommands(client)

asyncio.run(main())