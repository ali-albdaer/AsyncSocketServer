import asyncio
import logging

HOST = 'localhost'  # Change to server's IP address
PORT = 8888  # Change to server's port

async def send_message(writer):
    while True:
        message = await loop.run_in_executor(None, input, "Enter message: ")
        try:
            writer.write(message.encode())
            await writer.drain()
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            break  # Exit the loop on error

        await asyncio.sleep(0.1)

async def receive_messages(reader):
    while True:
        data = await reader.read(1024)
        if not data:
            # Connection closed by server
            logging.info("Connection closed by server.")
            return
        
        logging.info(f"Received message: {data.decode()}")
        await asyncio.sleep(0.1)

async def handle_connection():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    # Receive welcome message
    welcome_message = await reader.read(1024)
    logging.info(welcome_message.decode())

    # Create tasks for sending and receiving messages concurrently
    send_task = asyncio.create_task(send_message(writer))
    receive_task = asyncio.create_task(receive_messages(reader))

    # Wait for both tasks to complete (send or receive or error)
    await asyncio.gather(send_task, receive_task)  # Use asyncio.gather for concurrent waiting

    writer.close()
    await writer.wait_closed()


async def main():
    logging.basicConfig(level=logging.INFO)
    global loop  # Declare global loop for send_message
    loop = asyncio.get_event_loop()
    await handle_connection()  # Await the connection handling

if __name__ == "__main__":
    asyncio.run(main())
