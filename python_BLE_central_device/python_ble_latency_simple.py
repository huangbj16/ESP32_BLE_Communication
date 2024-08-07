import asyncio
from bleak import BleakScanner, BleakClient
import json
import time
import numpy as np

uuid = "f22535de-5375-44bd-8ca9-d0ea9ff9e410"

'''
command format
First byte: 00XXXX0Y, X is serial group number, Y is mode,
Second byte: 01XXXXXX, X is address,
Third byte: 1XXXXYYZ, X is duty, Y is frequency, Z is wave.
'''
def create_command(addr, mode, duty, freq, wave):
    serial_group = addr // 30
    serial_addr = addr % 30
    byte1 = (serial_group << 2) | (mode & 0x01)
    byte2 = 0x40 | (serial_addr & 0x3F)  # 0x40 represents the leading '01'
    byte3 = 0x80 | ((duty & 0x0F) << 3) | ((freq & 0x03) << 1) | (wave & 0x01)  # 0x80 represents the leading '1'
    return bytearray([byte1, byte2, byte3])

async def test_latency(client):
    # Send data
    addr = 1
    mode = 1
    duty = 7
    freq = 2
    wave = 0
    round_time_array = np.zeros(10000)
    for i in range(10000):
        # command = command + create_command(addr, mode, duty, freq, wave)
        # addr = (32 + i) % 120
        for j in range(3):
            command = bytearray([])
            for k in range(10):
                addr = (30 + j*10 + k) % 120
                # addr = i % 120
                command = command + create_command(addr, mode, duty, freq, wave)
            command = command + bytearray([0xFF, 0xFF, 0xFF]) * 10 # Padding
            start_time = time.perf_counter()  # Start timing
            await client.write_gatt_char(uuid, command)
            # response = await client.read_gatt_char(uuid)
            # print(f"Received: {response.decode()}")

            while (time.perf_counter() - start_time) < 0.0025:
                pass
            end_time = time.perf_counter()  # End timing
            print(f"{i+1} Round-trip time: {(end_time - start_time) * 1000:.2f} ms")
            round_time_array[i] = (end_time - start_time) * 1000
    print(f"Average round-trip time: {np.mean(round_time_array):.2f} ms")
    print(f"Round-trip time standard deviation: {np.std(round_time_array):.2f} ms")
    time.sleep(1)


async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'QT Py ESP32-S3':
                print('central unit BLE found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    current_mtu = client.mtu_size
                    print(f"Current MTU: {current_mtu}")
                    await test_latency(client)

asyncio.run(main())