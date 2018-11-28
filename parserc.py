from collections import namedtuple
from functools import reduce


Result = namedtuple('Result', ['success', 'result', 'input'])
Input = namedtuple('Input', ['text', 'row', 'col'])


class Parser():

    def __init__(self, parse_func):
        self.parse = parse_func

    def __call__(self, inp):
        if isinstance(inp, str):
            inp = Input(inp, 1, 1)
        return self.parse(inp)

    def __add__(self, parser2):
        def parse_func(inp):
            res1 = self(inp)
            if not res1.success:
                return res1
            res2 = parser2(res1.input)
            if not res2.success:
                return res2

            r1 = res1.result
            if len(res1.result) == 1 and not isinstance(res1.result[0], list):
                r1 = [res1.result]

            r2 = res2.result
            if len(res2.result) == 1 and not isinstance(res2.result[0], list):
                r2 = [res2.result]

            return Result(True, r1 + r2, res2.input)
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
        return self._apply(always_true)

    def _apply(self, modify_fn):
        parse_fn = self.parse
        return Parser(lambda inp: modify_fn(parse_fn(inp)))

    def map(self, mod_fn):
        def modify_on_true(r):
            if r.success:
                rs = [mod_fn(r.result)] if mod_fn(r.result) is not None else []
                return Result(True, rs, r.input)
            return r
        return self._apply(modify_on_true)


class Char(Parser):

    def __init__(self, char):
        self.char = char

    def parse(self, inp):
        if not isinstance(inp.text, str) or inp.text == "":
            return Result(False, ['No string found to parse'], inp)
        if inp.text[0] == str(self.char):
            col = 0 if inp.text[0] == '\n' else inp.col + 1
            row = inp.row + 1 if inp.text[0] == '\n' else inp.row
            new_inp = Input(inp.text[1:], row, col)
            return Result(True, [self.char], new_inp)
        else:
            error_msg = (
                f'Expected "{self.char}" but got "{inp.text[0]}"'
                f' at row:{inp.row} col:{inp.col}')
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
        return reduce(lambda x, y: x + y, [Char(x) for x in lst])
    return Parser(lambda inp: Result(False, ['type mismatch in Seq()'], inp))


def ZeroOrMore(parser):
    def new_parser(inp):
        res = parser(inp)
        if not res.success:
            return Result(True, [], inp)
        res2 = new_parser(res.input)
        return Result(True, [res.result] + res2.result, res2.input)
    return Parser(new_parser)


def OneOrMore(parser):
    return parser + ZeroOrMore(parser)


class Ref(Parser):
    linked_parsers = {}

    def __init__(self, parser_name):
        self.name = parser_name

    @classmethod
    def link(cls, mappings):
        cls.linked_parsers.update(mappings)

    def parse(self, inp):
        if self.name in self.linked_parsers:
            return self.linked_parsers[self.name](inp)
        if self.name in globals():
            return globals()[self.name](inp)
        return Result(False, [f'parser of name "{self.name}" not found'], inp)


def Between(p1, p2, p3):
    def new_parser(inp):
        res = p1(inp)
        if not res.success:
            return res
        res2 = p2(res.input)
        if not res2.success:
            return res2
        res3 = p3(res2.input)
        if not res3.success:
            return res3
        return Result(True, res2.result, res3.input)
    return Parser(new_parser)


def End():
    def parse_func(inp):
        if inp.text == '':
            return Result(True, [], inp)
        error_msg = (
            f'Expected end of string, got "{inp.text[0]}"'
            f' at row:{inp.row} col:{inp.col}')
        return Result(False, [error_msg], '')
    return Parser(parse_func)


def StripWhitespace():
    def remove_whitespace(inp):
        new_inp = Input(''.join(inp.text.split()), inp.row, inp.col)
        return Result(True, [], new_inp)
    return Parser(remove_whitespace)
