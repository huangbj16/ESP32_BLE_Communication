import asyncio
from bleak import BleakScanner, BleakClient
import json
import time
import numpy as np

uuid = "f22535de-5375-44bd-8ca9-d0ea9ff9e410"

async def test_latency(client):
    # Send data
    command = {
        'addr':0,
        'mode':1,
        'duty':7, # default
        'freq':2, # default
        'wave':0, # default
    }
    round_time_array = np.zeros(1000)
    for i in range(1000):
        # data_to_send = b'{"addr": 1, "mode": 1, "duty": 1, "freq": 2, "wave": 0}'
        command['addr'] = (i % 20) + 1
        output = bytearray(json.dumps(command), 'utf-8')
        start_time = time.perf_counter()  # Start timing
        await client.write_gatt_char(uuid, output)
        # response = await client.read_gatt_char(uuid)
        # print(f"Received: {response.decode()}")

        end_time = time.perf_counter()  # End timing
        print(f"{i+1} Round-trip time: {(end_time - start_time) * 1000:.2f} ms")
        round_time_array[i] = (end_time - start_time) * 1000
    print(f"Average round-trip time: {np.mean(round_time_array):.2f} ms")
    print(f"Round-trip time standard deviation: {np.std(round_time_array):.2f} ms")


async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'QT Py ESP32-S3':
                print('central unit BLE found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    await test_latency(client)

asyncio.run(main())