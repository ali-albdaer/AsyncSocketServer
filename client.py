import asyncio

from config import HOSTNAME, PORT


async def connect_to_server():
    reader, writer = await asyncio.open_connection(HOSTNAME, PORT)

    message = input('>>> ')
    writer.write(message.encode())
    await writer.drain()

    while True:
        data = await reader.read(256)

        if not data:
            break

        response = data.decode()
        print(response)
    
    print('Connection lost or you were kicked from the server.')
    
    writer.close()
    await writer.wait_closed()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(connect_to_server())
