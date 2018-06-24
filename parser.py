from collections import namedtuple


Result = namedtuple('Result', ['success', 'result', 'input'])


def char(char):
    def parser(inp):
        nonlocal char
        if not isinstance(inp, str) or inp == "":
            return Result(False, 'No string found to parse', '')
        if inp[0] == char:
            return Result(True, char, inp[1:])
        else:
            return Result(False, f'Expecting "{char}" but got "{inp[0]}"', '')
    return parser
