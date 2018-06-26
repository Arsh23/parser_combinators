from parser import Any, OneOrMore, Char, Ref, Result, Between
from operator import add, sub, mul, truediv


def flatten(lst):
    if not isinstance(lst, list):
        return [lst]
    else:
        return [x for inner in lst for x in flatten(inner)]


def flatten_number(r):
    if r.success:
        res = int(''.join(str(x) for x in flatten(r.result)))
        return Result(True, res, r.input)
    return r


def eval_exp(r):
    if r.success:
        operators = {'+': add, '-': sub, '*': mul, '/': truediv}
        # format: result=[[1, ['+']], 2]
        n1, n2, op = r.result[0][0], r.result[1], r.result[0][1][0]
        return Result(True, operators[op](n1, n2), r.input)
    return r


def exp_parser():
    number = OneOrMore(Any(range(10))).apply(flatten_number)

    parans_exp = Between(Char('('), Ref('exp'), Char(')'))
    factor = parans_exp | number

    mul_and_div = (factor + Any(['*', '/']) + Ref('term')).apply(eval_exp)
    term = mul_and_div | factor

    add_and_sub = (term + Any(['+', '-']) + Ref('exp')).apply(eval_exp)
    exp = add_and_sub | term

    Ref.link('exp', exp).link('term', term)
    return exp


def tree(lst, space=0):
    for item in lst:
        if isinstance(item, list):
            tree(item, space+1)
        else:
            print('    '*space, f'[{item}]')
