import asyncio
from bleak import BleakScanner, BleakClient
import json
from airsim_distance_sensors import AirSim_Module

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e410'

async def setMotor(client):
    # setup airsim connection
    airsim_control = AirSim_Module()
    motor_num = 5
    motor_ids = [3, 8, 33, 5, 1]
    is_trigger_array = [False for _ in range(motor_num)]
    # turn on buck converter
    for i in range(2):
        buck_addr = i*30
        command = {
            'addr':buck_addr, 
            'mode':1,
            'duty':1, # default
            'freq':3, # default
            'wave':1, # default
        }
        data = bytearray(json.dumps(command), 'utf-8')
        print(data)
        await client.write_gatt_char(MOTOR_UUID,  data)
    while True:
        for i in range(motor_num):
            rawDistance = airsim_control.get_distance_by_sensor("Distance"+str(i+1))
            if rawDistance.distance <= 2.0 and not is_trigger_array[i]:
                is_trigger_array[i] = True
                print("distance sensor ", i, "triggered")
                # trigger vibration i
                start_or_stop = 1
                command = {
                    'addr':motor_ids[i],
                    'mode':start_or_stop,
                    'duty':7, # default
                    'freq':2, # default
                    'wave':0, # default
                }
                output = bytearray(json.dumps(command), 'utf-8')
                print(output)
                await client.write_gatt_char(MOTOR_UUID,  output)              
            if rawDistance.distance > 2.0 and is_trigger_array[i]:
                is_trigger_array[i] = False
                print("distance sensor ", i, "canceled")
                # stop vibration i
                start_or_stop = 0
                command = {
                    'addr':motor_ids[i],
                    'mode':start_or_stop,
                    'duty':7, # default
                    'freq':2, # default
                    'wave':0, # default
                }
                output = bytearray(json.dumps(command), 'utf-8')
                print(output)
                await client.write_gatt_char(MOTOR_UUID,  output)

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
                    await setMotor(client)

asyncio.run(main())