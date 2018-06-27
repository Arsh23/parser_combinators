from parser import Any, OneOrMore, Char, Ref, Result, Between, End
from operator import add, sub, mul, truediv


def convert_to_int(r):
    if r.success:
        return Result(True, [int(''.join(x[0] for x in r.result))], r.input)
    return r


def eval_exp(r):
    if r.success:
        operators = {'+': add, '-': sub, '*': mul, '/': truediv}
        # format: result=[[[1], '+'], 2]
        n1, n2, op = r.result[0][0][0], r.result[1], r.result[0][1]
        return Result(True, [operators[op](n1, n2)], r.input)
    return r


def exp_parser():
    number = OneOrMore(Any('1234567890')).apply(convert_to_int)

    paran_exp = Between(Char('('), Ref('exp'), Char(')'))
    factor = paran_exp | number

    mul_and_div = (factor + Any('*/') + Ref('term')).apply(eval_exp)
    term = mul_and_div | factor

    add_and_sub = (term + Any('+-') + Ref('exp')).apply(eval_exp)
    exp = add_and_sub | term

    Ref.link('exp', exp).link('term', term)
    return exp + End()


def tree(lst, space=0):
    for item in lst:
        if isinstance(item, list):
            tree(item, space+1)
        else:
            print('    '*space, f'[{item}]')
