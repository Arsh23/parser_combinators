import sys
sys.path.append('..')
from number_parser import number_parser
from parserc import (
    Any, Char, Ref, Between, End, ZeroOrMore, StripWhitespace
)


# Grammar for algebraic expressions:
#
# operator -> + | - | * | / | ^
# exp -> exp operator exp | NUMBER
#
# after fixing for operator precedance and removing left recursion:
#
# exponent -> ( exp ) | NUMBER
# factor -> exponent factor'
# factor' -> ^ exponent factor' | NULL
# term -> factor term'
# term' -> * factor term' | / factor term' | NULL
# exp -> term exp'
# exp' -> + term exp' | - term exp' | NULL


def eval_exp(result):
    #  this func evaluates the intermediate parsed expressions
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '^': lambda x, y: x ^ y,
    }

    #  result format: [[n1], [[op], [n2]], [[op], [n3]] .... ]
    res = result[0][0]
    for op, n in result[1:]:
        res = operators[op[0]](res, n[0])
    return res


def exp_parser():
    number = number_parser()

    # exponent -> ( exp ) | NUMBER
    exponent = Between(Char('('), Ref('exp'), Char(')')) | number
    # a reference to 'exp' parser is used since its not defined yet

    # factor -> exponent factor'
    # factor' -> ^ exponent factor' | NULL
    factor = (exponent + ZeroOrMore(Char('^') + exponent)).map(eval_exp)

    # term -> factor term'
    # term' -> * factor term' | / factor term' | NULL
    term = (factor + ZeroOrMore(Any('*/') + factor)).map(eval_exp)

    # exp -> term exp'
    # exp' -> + term exp' | - term exp' | NULL
    exp = (term + ZeroOrMore(Any('+-') + term)).map(eval_exp)

    # linking reference to actual parser
    Ref.link({'exp': exp})

    return StripWhitespace() + exp + End()
