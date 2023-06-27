from dataclasses import dataclass
from abc import ABC

from app.errors import CommandException

PING_COMMAND = 'PING'
PONG_COMMAND = 'PONG'


class PingCommandException(CommandException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

    def __str__(self) -> str:
        return "ERR wrong number of arguments for 'ping' command"


class Command(ABC):
    def execute(self):
        raise NotImplementedError


@dataclass
class PingCommand(Command):
    command: str

    def execute(self, *args) -> list[str]:
        res = [PONG_COMMAND, ]
        if len(args) > 1:
            raise PingCommandException()
        if args and (value := args[0]):
            return [value, ]
        return res
