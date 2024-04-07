import asyncio

from config import HOST, PORT
from utils import print_color

CONNECTED = False


async def send_message(writer):
    while CONNECTED:
        message = await loop.run_in_executor(None, input)
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception as e:
            print_color("red", e)
            break

        await asyncio.sleep(0.1)

async def receive_messages(reader):
    global CONNECTED

    while CONNECTED:
        data = await reader.read(1024)
        if not data:
            print_color("red", "Connection closed by server.")
            CONNECTED = False
        
        print(data.decode())
        await asyncio.sleep(0.1)


async def handle_connection():
    global CONNECTED
    reader, writer = await asyncio.open_connection(HOST, PORT)
    CONNECTED = True

    welcome_message = await reader.read(1024)
    print(welcome_message.decode())

    # Tasks for sending and receiving messages concurrently
    send_task = asyncio.create_task(send_message(writer))
    receive_task = asyncio.create_task(receive_messages(reader))

    await asyncio.gather(send_task, receive_task)  # asyncio.gather for concurrent waiting

    writer.close()
    await writer.wait_closed()


async def main():
    global loop  # global loop for send_message
    loop = asyncio.get_event_loop()
    await handle_connection()


if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print_color("red", "Disconnected from server.")
