import asyncio
from bleak import BleakScanner, BleakClient
import json

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e410'

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

async def setMotor(client):
    while True:
        motor_addr = int(input('what is the next motor you want to control?'))
        if motor_addr % 30 == 0:
            duty = int(input('0-31 for intensity?'))
            start_or_stop = int(input('1 for start and 0 for stop?'))
            user_input = {
                'addr':motor_addr,
                'mode':start_or_stop,
                'duty':(duty>>3), # default
                'freq':(duty>>1) & 3, # default
                'wave':(duty & 1), # default
            }
        else:
            duty = int(input('0-15 for duty?'))
            start_or_stop = int(input('1 for start and 0 for stop?'))
            user_input = {
                'addr':motor_addr,
                'mode':start_or_stop,
                'duty':duty, # default
                'freq':3, # default
                'wave':0, # default
            }
        command = bytearray([])
        command = command + create_command(user_input['addr'], user_input['mode'], user_input['duty'], user_input['freq'], user_input['wave'])
        command = command + bytearray([0xFF, 0xFF, 0xFF]) * 19 # Padding
        await client.write_gatt_char(MOTOR_UUID, command)

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