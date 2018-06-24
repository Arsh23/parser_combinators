from collections import namedtuple


Result = namedtuple('Result', ['success', 'result', 'input'])


class Parser():
    pass


class Char(Parser):

    def __init__(self, char):
        self.char = char

    def __call__(self, inp):
        if not isinstance(inp, str) or inp == "":
            return Result(False, 'No string found to parse', '')
        if inp[0] == self.char:
            return Result(True, self.char, inp[1:])
        else:
            return Result(
                False, f'Expecting "{self.char}" but got "{inp[0]}"', ''
            )
