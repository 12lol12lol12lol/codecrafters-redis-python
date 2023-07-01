from enum import Enum


class ResponseType(Enum):
    ok = 'ok'
    error = 'error'
    args = 'args'
    nil = 'nil'
