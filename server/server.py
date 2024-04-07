import asyncio
import logging

HOST = 'localhost'  # Change to desired host IP if needed
PORT = 8888  # Change to desired port

clients = set()  # Store connected clients


async def handle_client(reader, writer):
    client_addr = writer.get_extra_info('peername')
    logging.info(f"Client connected: {client_addr}")
    clients.add(writer)  # Add client to the set of connected clients

    # Send welcome message
    welcome_message = "Welcome to the chat server!\n".encode()
    writer.write(welcome_message)
    await writer.drain()

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                logging.info(f"Client {client_addr} disconnected.")
                break

            # Broadcast message to all connected clients (excluding sender)
            for other_writer in clients.difference({writer}):
                print("entering this loop")
                try:
                    other_writer.write(data)
                    await other_writer.drain()
                except Exception as e:
                    logging.error(f"Error sending to client {other_writer.get_extra_info('peername')}: {e}")
                    clients.remove(other_writer)  # Remove disconnected client

            # Print received message
            logging.info(f"Client {client_addr}: {data.decode()}")

            await asyncio.sleep(0.1)  # Short sleep to avoid busy waiting


    finally:
        clients.remove(writer)
        writer.close()


async def main():
    logging.basicConfig(level=logging.INFO)
    server = await asyncio.start_server(handle_client, HOST, PORT)  # Start the server

    # Run the server indefinitely using a loop
    async with server:
        while True:
            await asyncio.sleep(0.1)  # Short sleep to avoid busy waiting

if __name__ == "__main__":
    asyncio.run(main())
