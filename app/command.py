from dataclasses import dataclass
from abc import ABC
from app.constants import ResponseType

from app.errors import CommandException

PONG_COMMAND = 'PONG'


class PingCommandException(CommandException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "ERR wrong number of arguments for 'ping' command"


class EchoCommandException(CommandException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "ERR wrong number of arguments for 'echo' command"


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
