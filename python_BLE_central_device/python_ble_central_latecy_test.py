import asyncio
from bleak import BleakScanner, BleakClient
import json
import time
import numpy as np

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e410'
CURRENTSENSING_UUID = "640b8bf5-3c88-44f6-95e0-f5813b390d73"
is_notified = False
time_recv = 0

async def notification_handler(sender, data):
    """
    Notification handler which prints the data received.
    """
    print(f"Notification from {sender}: {data}")
    global time_recv, is_notified
    is_notified = True
    time_recv = time.time()


async def setMotor(client):
    global time_recv, is_notified
    while True:
        motor_addr = int(input('what is the next motor you want to control?'))
        if motor_addr % 30 == 0:
            duty = int(input('0-31 for intensity?'))
            start_or_stop = int(input('1 for start and 0 for stop?'))
            command = {
                'addr':motor_addr,
                'mode':start_or_stop,
                'duty':(duty>>3), # default
                'freq':(duty>>1) & 3, # default
                'wave':(duty & 1), # default
            }
        else:
            duty = int(input('0-15 for duty?'))
            start_or_stop = int(input('1 for start and 0 for stop?'))
            command = {
                'addr':motor_addr,
                'mode':start_or_stop,
                'duty':duty, # default
                'freq':2, # default
                'wave':0, # default
            }
        output = bytearray(json.dumps(command), 'utf-8')
        print(output)
        # calculate the time difference between sending the command and receiving the notification
        # time_sent = time.time()
        # await client.write_gatt_char(MOTOR_UUID,  output)
        # await client.start_notify(CURRENTSENSING_UUID, notification_handler)
        # while not is_notified:
        #     pass
        # print('Elapsed time = ', time_recv-time_sent)
        # is_notified = False

        elapsed_time_array = np.zeros(20)
        for i in range(20):
            time_sent = time.time()
            await client.write_gatt_char(MOTOR_UUID,  output)
            ### bandwidth test
            # count = 0
            # while count < 100:
            #     await client.write_gatt_char(MOTOR_UUID,  output)
            #     count += 1
            # time_recv = time.time()
            # print('Elapsed time = ', time_recv-time_sent)
            
            ### one BLE loop latency
            await client.start_notify(CURRENTSENSING_UUID, notification_handler)
            while not is_notified:
                pass
            print('Elapsed time = ', time_recv-time_sent)
            elapsed_time_array[i] = time_recv-time_sent
            is_notified = False
        print('Average elapsed time = ', np.mean(elapsed_time_array))
        print('Standard deviation of elapsed time = ', np.std(elapsed_time_array))
        

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'QT Py ESP32-S3':
                print('central unit BLE found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    val = await client.read_gatt_char(MOTOR_UUID)
                    print('Motor read = ', val)
                    await setMotor(client)

asyncio.run(main())