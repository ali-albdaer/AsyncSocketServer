import asyncio

from config import HOSTNAME, PORT


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    data = None

    while data not in ('exit', 'quit'):
        data = await reader.read(256)
        address = writer.get_extra_info('peername')

        print(f'<{address}>: {data!r}')

        response = f'<<< Server >>>: The server is still under construction.'
        writer.write(response.encode())
        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def start_server() -> None:
    server = await asyncio.start_server(handle_client, HOSTNAME, PORT)
    print(f'Server started at {HOSTNAME}:{PORT}')
    
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start_server())
