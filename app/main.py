# Uncomment this to pass the first stage
import socket
import logging
from app.command import PingCommandException
from app.handler import CommandHandler, UnrecogniseCommandException

from app.parser import RespParser
from app.services import convert_to_response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    server_socket = socket.create_server((socket.gethostname(), 6379), reuse_port=True)
    server_socket.listen()
    logger.info('Start listening')
    while True:
        client_socket, addr = server_socket.accept()  # wait for client
        parser = RespParser(client_socket)
        res = parser.run()
        if not res:
            continue
        command = res[0]
        args = res[1:] if len(res) > 1 else list()
        err = False
        try:
            command = CommandHandler(command).execute(args)
            response = command.execute(*args)
        except (UnrecogniseCommandException, PingCommandException) as ex:
            response, err = [str(ex), ], True
        response_in_bytes = convert_to_response(response, err)
        client_socket.sendall(response_in_bytes)


if __name__ == "__main__":
    main()
