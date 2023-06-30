from dataclasses import dataclass
from app.command import DOCS_COMMAND, Command, PING_COMMAND, DocsCommand, PingCommand
from app.errors import CommandHandlerException


class UnrecogniseCommandException(CommandHandlerException):
    def __init__(self, command: str, arguments: list[str], *args: object) -> None:
        super().__init__(*args)
        self.command = command
        self.arguments = arguments

    def __str__(self) -> str:
        if self.args:
            msg = f"ERR unknown command '{self.command}', with args beginning with:"
            if self.arguments:
                for arg in self.arguments:
                    return msg + f" '{arg}'"
        else:
            msg = "ERR unknown command '', with args beginning with:"
        return msg


@dataclass
class CommandHandler:
    command: str

    def execute(self, *args) -> Command:
        if (value := self.command.upper()) in {PING_COMMAND, }:
            return PingCommand(value)
        if (value := self.command.upper()) == 'COMMAND':
            if args and args[0] == DOCS_COMMAND:
                return DocsCommand(args[0])
        raise UnrecogniseCommandException(self.command, args)
