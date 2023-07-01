from dataclasses import dataclass
from abc import ABC
from app.constants import ResponseType

from app.errors import CommandException
from app.storage import Storage, ValueDoesNotExist

PONG_COMMAND = 'PONG'
OK_COMMAND = 'OK'


class PingCommandException(CommandException):
    default_message = "ERR wrong number of arguments for 'ping' command"


class EchoCommandException(CommandException):
    default_message = "ERR wrong number of arguments for 'echo' command"


class SetCommandException(CommandException):
    default_message = "ERR wrong number of arguments for 'set' command"


class GetCommandException(CommandException):
    default_message = "ERR wrong number of arguments for 'get' command"


class Command(ABC):
    def execute(self) -> tuple[list[str], ResponseType]:
        raise NotImplementedError


@dataclass
class PingCommand(Command):
    command: str = 'PING'

    def execute(self, *args) -> tuple[list[str], ResponseType]:
        res = [PONG_COMMAND, ]
        if len(args) > 1:
            raise PingCommandException()
        if args and (value := args[0]):
            return [value, ]
        return res, ResponseType.ok


@dataclass
class DocsCommand(Command):
    command: str = 'DOCS'

    def execute(self, *args) -> tuple[list[str], ResponseType]:
        return ['DOCS', ], ResponseType.ok


@dataclass
class EchoCommand(Command):
    command: str = 'ECHO'

    def execute(self, *args) -> tuple[list[str], ResponseType]:
        if not args or len(args) > 1:
            raise EchoCommandException()
        return [args[0]], ResponseType.args


@dataclass
class SetCommand(Command):
    storage: Storage
    command: str = 'SET'
    expire_commands = {'PX', }

    def execute(self, *args) -> tuple[list[str], ResponseType]:
        if len(args) == 2:
            self.storage.set(args[0], args[1])
            return [OK_COMMAND, ], ResponseType.ok
        elif len(args) == 4:
            if args[2].upper() not in self.expire_commands:
                raise SetCommandException('ERR syntax error')
            try:
                v = int(args[3])
                if v <= 0:
                    raise SetCommandException("ERR invalid expire time in 'set' command")
                self.storage.set(args[0], args[1], v)
                return [OK_COMMAND, ], ResponseType.ok
            except ValueError:
                raise SetCommandException("ERR invalid expire time in 'set' command")
        raise SetCommandException()


@dataclass
class GetCommand(Command):
    storage: Storage
    command: str = 'GET'

    def execute(self, *args) -> tuple[list[str], ResponseType]:
        if len(args) != 1:
            raise SetCommandException()
        value = self.storage.get(args[0])
        if value == ValueDoesNotExist:
            return None, ResponseType.nil
        return [value, ], ResponseType.args
