class CommandHandlerException(Exception):
    default_message = "ERR unknown command"

    def __init__(self, *args: object) -> None:
        if not args:
            super().__init__(self.default_message)
            return
        super().__init__(*args)


class CommandException(Exception):
    default_message = "ERR in execute command"

    def __init__(self, *args: object) -> None:
        if not args:
            super().__init__(self.default_message)
            return
        super().__init__(*args)
