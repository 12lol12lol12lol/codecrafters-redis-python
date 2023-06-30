import asyncio
from dataclasses import dataclass
from socket import socket

ARRAY_SIGN = b'*'
DELIMETER_SIGN = b'\r'
START_OF_VALUE_SIGN = b'$'


class RespParseException(Exception):
    pass


@dataclass
class RespParser:
    socket2parse: socket
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    async def parse_value(self) -> str:
        count_bytes = b''
        while (value := (await self.loop.sock_recv(self.socket2parse, 1))) != DELIMETER_SIGN:
            count_bytes += value
        await self.loop.sock_recv(self.socket2parse, 1)
        return (await self.loop.sock_recv(self.socket2parse, int(count_bytes))).decode()

    async def parse_string_array(self) -> list[str]:
        count_bytes = b''
        while (value := (await self.loop.sock_recv(self.socket2parse, 1))) != DELIMETER_SIGN:
            count_bytes += value
        await self.loop.sock_recv(self.socket2parse, 1)
        count = int(count_bytes)
        values = []
        while count > 0:
            if (await self.loop.sock_recv(self.socket2parse, 1)) != START_OF_VALUE_SIGN:
                raise RespParseException(f'Expected {START_OF_VALUE_SIGN} did not accepted')
            values.append(await self.parse_value())
            await self.loop.sock_recv(self.socket2parse, 2)
            count -= 1
        return values

    async def run(self) -> list[str]:
        res = []
        while (value := (await self.loop.sock_recv(self.socket2parse, 1))):
            if value == ARRAY_SIGN:
                array_result = await self.parse_string_array()
                res.extend(array_result)
            return res
        return res
