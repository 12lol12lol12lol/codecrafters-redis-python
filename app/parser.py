from socket import socket
from dataclasses import dataclass

ARRAY_SIGN = b'*'
DELIMETER_SIGN = b'\r'
START_OF_VALUE_SIGN = b'$'


class RespParseException(Exception):
    pass


@dataclass
class RespParser:
    socket2parse: socket

    def parse_value(self) -> str:
        count_bytes = b''
        while (value := self.socket2parse.recv(1)) != DELIMETER_SIGN:
            count_bytes += value
        self.socket2parse.recv(1)
        return self.socket2parse.recv(int(count_bytes)).decode()

    def parse_string_array(self) -> str:
        count_bytes = b''
        while (value := self.socket2parse.recv(1)) != DELIMETER_SIGN:
            count_bytes += value
        self.socket2parse.recv(1)
        count = int(count_bytes)
        values = []
        while count > 0:
            if self.socket2parse.recv(1) != START_OF_VALUE_SIGN:
                raise RespParseException(f'Expected {START_OF_VALUE_SIGN} did not accepted')
            values.append(self.parse_value())
            self.socket2parse.recv(2)
            count -= 1
        return values

    def run(self) -> list[str]:
        res = []
        while (value := self.socket2parse.recv(1)):
            if value == ARRAY_SIGN:
                res.extend(self.parse_string_array())
            return res
        return res
