import sys
sys.path.append('..')
from parserc import Char, Any, Seq, OneOrMore, ZeroOrMore


def number_parser():
    # based on JSON's specs for number

    # digit: any char from 0 - 9
    digit = Any('0123456789')

    # non zero numbers: digits without a leading 0
    non_zero = Any('123456789') + ZeroOrMore(digit)

    # int: optional minus sign, followed by a 0 OR non zero numbers
    integer = ~Char('-') + (Char('0') | non_zero)

    # decimal: point followed by digits
    decimal = Char('.') + OneOrMore(digit)

    # exponent: e or E with a optional sign followed by digits
    exp = Seq([Any('eE'), ~Any('+-'), OneOrMore(digit)])

    # all combinations of integer, decimal and exponent
    number = (
        (integer + decimal + exp) |
        (integer + decimal) |
        (integer + exp) |
        integer
    ).map(lambda result: float(''.join(x[0] for x in result)))
    # ^ map the result list to float
    return number
