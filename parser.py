from collections import namedtuple


Result = namedtuple('Result', ['success', 'result', 'input'])


class Parser():

    def __init__(self, parse_func):
        self.parse = parse_func

    def __call__(self, inp):
        return self.parse(inp)


class Char(Parser):

    def __init__(self, char):
        self.char = char

    def parse(self, inp):
        if not isinstance(inp, str) or inp == "":
            return Result(False, 'No string found to parse', '')
        if inp[0] == self.char:
            return Result(True, self.char, inp[1:])
        else:
            return Result(
                False, f'Expected "{self.char}" but got "{inp[0]}"', ''
            )
