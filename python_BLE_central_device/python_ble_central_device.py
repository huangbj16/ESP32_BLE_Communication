import socket
import asyncio
from bleak import BleakScanner, BleakClient

MOTOR_UUID = 'f22535de-5375-44bd-8ca9-d0ea9ff9e419'

async def setMotor(client, socket_conn):
    while True:
        data = socket_conn.recv(1024)
        if not data:
            break
        print('TCP data recv = ', data)
        motor = int(data.decode('utf-8'))
        if motor >= 0 and motor < 5:
            await client.write_gatt_char(MOTOR_UUID,  int.to_bytes(motor, 2, 'little'))

async def main(socket_conn):
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
                    while True:
                        await setMotor(client, socket_conn)

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 9051  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    print('python server start listening')
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"TCP socket connected by {addr}")
        asyncio.run(main(conn))