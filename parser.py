from collections import namedtuple, Callable
from functools import reduce


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
            return Result(True, [res1.result] + res2.result, res2.input)
        return Parser(parse_func)

    def __and__(self, parser2):
        def parse_func(inp):
            res1 = self(inp)
            if not res1.success:
                return res1
            res2 = parser2(res1.input)
            if not res2.success:
                return res2
            return Result(True, res1.result + res2.result, res2.input)
        return Parser(parse_func)

    def __or__(self, parser2):
        def parse_func(inp):
            res = self(inp)
            if res.success:
                return res
            return parser2(inp)
        return Parser(parse_func)

    def __invert__(self):
        def always_true(res):
            if not res.success:
                return Result(True, [], res.input)
            return res
        return self.apply(always_true)

    def apply(self, modify_fn):
        if isinstance(modify_fn, Callable):
            parse_fn = self.parse
            return Parser(lambda inp: modify_fn(parse_fn(inp)))
        return self


class Char(Parser):

    def __init__(self, char):
        self.char = char

    def parse(self, inp):
        if not isinstance(inp, str) or inp == "":
            return Result(False, 'No string found to parse', '')
        if inp[0] == str(self.char):
            return Result(True, [self.char], inp[1:])
        else:
            error_msg = f'Expected "{self.char}" but got "{inp[0]}"'
            return Result(False, [error_msg], inp)


def Any(lst):
    if all(isinstance(x, Parser) for x in lst):
        return reduce(lambda x, y: x | y, lst)
    if all(isinstance(x, str) for x in lst):
        return reduce(lambda x, y: x | y, [Char(x) for x in lst])
    return Parser(lambda inp: Result(False, ['type mismatch in Any()'], inp))


def Seq(lst):
    if all(isinstance(x, Parser) for x in lst):
        return reduce(lambda x, y: x + y, lst)
    if all(isinstance(x, str) for x in lst):
        return reduce(lambda x, y: x & y, [Char(x) for x in lst])
    return Parser(lambda inp: Result(False, ['type mismatch in Seq()'], inp))


def ZeroOrMore(parser):
    def new_parser(inp):
        res = parser(inp)
        if not res.success:
            return Result(True, [], inp)
        res2 = new_parser(res.input)
        return Result(True, [res.result] + res2.result, res2.input)
    return Parser(new_parser)


OneOrMore = lambda parser: parser + ZeroOrMore(parser)


class Ref(Parser):

    linked_parsers = {}

    def __init__(self, parser_name):
        self.name = parser_name

    @classmethod
    def link(cls, name, parser):
        cls.linked_parsers[name] = parser.parse
        return cls

    def parse(self, inp):
        if self.name in self.linked_parsers:
            return self.linked_parsers[self.name](inp)
        if self.name in globals():
            return globals()[self.name](inp)
        return Result(False, [f'parser of name "{self.name}" not found'], inp)


def Between(p1, p2, p3):
    def get_middle_result(r):
        if r.success:
            # format: result=[[[p1], p2], p3]
            return Result(True, [r.result[0][1]], r.input)
        return r
    return (p1 + p2 + p3).apply(get_middle_result)


def End():
    def parse_func(inp):
        if inp == '':
            return Result(True, [], '')
        return Result(False, [f'Expected EOF, got "{inp[0]}"'], '')
    return Parser(parse_func)
