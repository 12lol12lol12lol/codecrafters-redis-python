# Uncomment this to pass the first stage
import logging
import socket

from app.command import PingCommandException
from app.handler import CommandHandler, UnrecogniseCommandException
from app.parser import RespParser
from app.services import convert_to_response

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    server_socket = socket.create_server(('localhost', 6379), reuse_port=True)
    server_socket.listen()
    logger.info('Start listening')
    client_socket, addr = server_socket.accept()
    while True:
        parser = RespParser(client_socket)
        res = parser.run()
        if not res:
            continue
        command = res[0]
        args = res[1:] if len(res) > 1 else list()
        err = False
        try:
            command = CommandHandler(command).execute(*args)
            response = command.execute(*args)
        except (UnrecogniseCommandException, PingCommandException) as ex:
            response, err = [str(ex), ], True
        response_in_bytes = convert_to_response(response, err)
        client_socket.sendall(response_in_bytes)
        logger.info(f'send {response_in_bytes} to {addr}')


# def main_multirpocess():
#     address = ('localhost', 6379)
#     with Listener(address) as listener:
#         with listener.accept() as client_socket:
#             logger.info(f'connection accepted from {listener.last_accepted}')
#             buff = client_socket.recv()
#             parser = RespParser(client_socket)
#             res = parser.run()
#             command = res[0]
#             args = res[1:] if len(res) > 1 else list()
#             err = False
#             try:
#                 command = CommandHandler(command).execute(args)
#                 response = command.execute(*args)
#             except (UnrecogniseCommandException, PingCommandException) as ex:
#                 response, err = [str(ex), ], True
#             response_in_bytes = convert_to_response(response, err)
#             client_socket.send_bytes(response_in_bytes)


if __name__ == "__main__":
    main()
