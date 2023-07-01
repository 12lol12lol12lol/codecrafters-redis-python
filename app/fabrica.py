from dataclasses import dataclass
from app.command import Command, DocsCommand, EchoCommand, GetCommand, PingCommand, SetCommand
from app.errors import CommandHandlerException
from app.storage import Storage


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
class CommandFabrica:
    storage: Storage

    def get_command(self, command, *args) -> Command:
        if command.upper() == PingCommand.command:
            return PingCommand()
        if command.upper() == 'COMMAND':
            if args and args[0] == DocsCommand.command:
                return DocsCommand()
        if command.upper() == EchoCommand.command:
            return EchoCommand()
        if command.upper() == SetCommand.command:
            return SetCommand(self.storage)
        if command.upper() == GetCommand.command:
            return GetCommand(self.storage)
        raise UnrecogniseCommandException(command, args)
