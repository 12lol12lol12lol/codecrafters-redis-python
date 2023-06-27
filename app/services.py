response_end = b'\r\n'


def convert_to_response(values: list[str], err: bool) -> bytes:
    start_sign = b'-' if err else b'+'
    res = start_sign+values[0].encode()
    if len(values) == 1:
        return res + response_end
    for val in values:
        res += b'\r\n$' + str(len(val)).encode() + val.encode()
    return res + response_end
