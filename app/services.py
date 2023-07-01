from app.constants import ResponseType


response_end = b'\r\n'


class ResponseConvertException(Exception):
    pass


def get_args_response(values: list[str]) -> bytes:
    res = b''
    for val in values:
        res += b'$' + str(len(val)).encode() + response_end
        res += val.encode() + response_end
    return res


def get_error_response(values: list[str]) -> bytes:
    return b'-' + values[0].encode() + response_end


def get_ok_response(values: list[str]) -> bytes:
    return b'+' + values[0].encode() + response_end


def convert_to_response(values: list[str], response_type: ResponseType) -> bytes:
    match response_type:
        case ResponseType.ok:
            return get_ok_response(values)
        case ResponseType.error:
            return get_error_response(values)
        case ResponseType.args:
            return get_args_response(values)
        case _:
            raise ResponseConvertException(f'Unknow type of response {response_type=}')
