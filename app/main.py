# Uncomment this to pass the first stage
import logging
import socket

from app.command import PingCommandException
from app.handler import CommandHandler, UnrecogniseCommandException
from app.parser import RespParser
from app.services import convert_to_response
import asyncio

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_request(client_socket: socket, addr: str) -> None:
    loop = asyncio.get_event_loop()
    while True:
        parser = RespParser(client_socket, loop)
        res = await parser.run()
        if not res:
            return
        command = res[0]
        args = res[1:] if len(res) > 1 else list()
        err = False
        try:
            command = CommandHandler(command).execute(*args)
            response = command.execute(*args)
        except (UnrecogniseCommandException, PingCommandException) as ex:
            response, err = [str(ex), ], True
        response_in_bytes = convert_to_response(response, err)
        logger.info(f'send {response_in_bytes} to {addr}')
        await loop.sock_sendall(client_socket, response_in_bytes)


async def main():
    server_socket = socket.create_server(('localhost', 6379), reuse_port=True)
    server_socket.setblocking(False)
    server_socket.listen()
    logger.info('Start listening')
    loop = asyncio.get_event_loop()
    while True:
        client_socket, addr = await loop.sock_accept(server_socket)
        loop.create_task(handle_request(client_socket, addr))


if __name__ == "__main__":
    asyncio.run(main())
