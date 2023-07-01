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


def get_nil_response(*args) -> bytes:
    return b'$-1\r\n'


functions_map = {
    ResponseType.ok: get_ok_response,
    ResponseType.error: get_error_response,
    ResponseType.args: get_args_response,
    ResponseType.nil: get_nil_response,
}


def convert_to_response(values: list[str], response_type: ResponseType) -> bytes:
    try:
        response_func = functions_map[response_type]
        return response_func(values)
    except KeyError:
        raise ResponseConvertException(f'Unknow type of response {response_type=}')
