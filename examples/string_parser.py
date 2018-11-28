import sys
sys.path.append('..')
from parserc import Any, OneOrMore


def string_parser():
    # based on JSON's specs for string

    # ascii chars from 33 to 127 removing " and \
    ascii_char = [chr(x) for x in range(33, 127) if chr(x) not in '"\\']

    # special chars
    special_chars = ['\\', '\/', '\b', '\f', '\n', '\r', '\t', '\v']

    # helper function maps from list of chars to string
    convert = lambda result: ''.join(x[0] for x in result)

    # string = any ascii chars from 33 to 127 + any of the above special chars
    string = OneOrMore(Any(ascii_char + special_chars)).map(convert)
    return string
