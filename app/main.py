# Uncomment this to pass the first stage
import asyncio
import logging
import socket
from app.constants import ResponseType

from app.errors import CommandException, CommandHandlerException
from app.fabrica import CommandFabrica
from app.parser import RespParser
from app.services import convert_to_response
from app.storage import Storage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def handle_request(client_socket: socket, addr: str, fabrica: CommandFabrica) -> None:
    loop = asyncio.get_event_loop()
    while True:
        parser = RespParser(client_socket, loop)
        res = await parser.run()
        if not res:
            return
        command = res[0]
        args = res[1:] if len(res) > 1 else list()
        response_type = ResponseType.ok
        try:
            command = fabrica.get_command(command, *args)
            response, response_type = command.execute(*args)
        except (CommandHandlerException, CommandException) as ex:
            response, response_type = [str(ex), ], ResponseType.error
        response_in_bytes = convert_to_response(response, response_type)
        logger.info(f'send {response_in_bytes} to {addr}')
        await loop.sock_sendall(client_socket, response_in_bytes)


async def main():
    server_socket = socket.create_server(('localhost', 6379), reuse_port=True)
    server_socket.setblocking(False)
    server_socket.listen()
    logger.info('Start listening')
    loop = asyncio.get_event_loop()
    storage = Storage(dict())
    fabrica = CommandFabrica(storage)
    while True:
        client_socket, addr = await loop.sock_accept(server_socket)
        loop.create_task(handle_request(client_socket, addr, fabrica))


if __name__ == "__main__":
    asyncio.run(main())
