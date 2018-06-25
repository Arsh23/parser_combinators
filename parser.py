from collections import namedtuple


Result = namedtuple('Result', ['success', 'result', 'input'])


class Parser():

    def __init__(self, parse_func):
        self.parse = parse_func

    def __call__(self, inp):
        return self.parse(inp)

    def __add__(self, parser2):
        def parse_func(inp):
            res1 = self(inp)
            if not res1.success:
                return res1
            res2 = parser2(res1.input)
            if not res2.success:
                return res2
            return Result(True, [res1.result, res2.result], res2.input)
        return Parser(parse_func)

    def __or__(self, parser2):
        def parse_func(inp):
            res1 = self(inp)
            if res1.success:
                return res1
            return parser2(inp)
        return Parser(parse_func)


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
