import asyncio
from bleak import BleakScanner, BleakClient
import json

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e419'

async def setMotor(client):
    while True:
        motor_addr = int(input('what is the next motor you want to control?'))
        start_or_stop = int(input('1 for start and 0 for stop?'))
        command = {
            'addr':motor_addr,
            'mode':start_or_stop,
            'duty':3, # default
            'freq':2, # default
            'wave':0, # default
        }
        output = bytearray(json.dumps(command), 'utf-8')
        await client.write_gatt_char(MOTOR_UUID,  output)

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print('device name = ', d.name)
        if d.name != None:
            if d.name == 'BINGJIAN_FEATHER':
                print('feather device found!!!')
                async with BleakClient(d.address) as client:
                    print(f'BLE connected to {d.address}')
                    val = await client.read_gatt_char(MOTOR_UUID)
                    print('Motor read = ', val)
                    await setMotor(client)

asyncio.run(main())