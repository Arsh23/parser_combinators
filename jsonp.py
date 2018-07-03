from parser import Char, Any, Seq, Between, ZeroOrMore, OneOrMore, Ref, End


def string_parser():
    # ascii chars from 33 to 127 removing " and \
    ascii_char = [chr(x) for x in range(33, 127) if chr(x) not in '"\\']

    # special chars
    special_chars = ['\\', '\/', '\b', '\f', '\n', '\r', '\t', '\v']

    # parser for json string
    string = OneOrMore(Any(ascii_char + special_chars))
    convert = lambda result: [''.join(result)]
    json_string = Between(Char('"'), string, Char('"')).on_success(convert)
    return json_string


def number_parser():
    # one or more of any char from 0 - 9
    digits = OneOrMore(Any('0123456789'))

    # optional minus sign, followed by a 0 OR digits without a leading 0
    integer = ~Char('-') & (Char('0') | (Any('123456789') & ~digits))

    # point followed by digits
    decimal = Char('.') & digits

    # e or E with a optional sign followed by digits
    exp = Any('eE') & ~Any('+-') & digits

    # all combinations of these 3
    convert_int = lambda result: [int(''.join(result))]
    convert_float = lambda result: [float(''.join(result))]
    number = (
        (integer & decimal & exp).on_success(convert_float) |
        (integer & decimal).on_success(convert_float) |
        (integer & exp).on_success(convert_float) |
        integer.on_success(convert_int)
    )
    return number


def json_parser():
    # null, true and false parser
    null = Seq('null').on_success(lambda r: [None])
    true = Seq('true').on_success(lambda r: [True])
    false = Seq('false').on_success(lambda r: [False])
    string, number = string_parser(), number_parser()
    ws = ZeroOrMore(Any(' \t\n\r\v\f')).on_success(lambda r: [])

    # value -> STRING | NUMBER | TRUE | FALSE | NULL | list | object
    value = Any([string, number, null, true, false, Ref('lst'), Ref('obj')])

    # pair -> STRING COLON value
    to_dict = lambda result: [{result[0]: result[2]}]
    pair = (string & ws & Char(':') & ws & value).on_success(to_dict)

    # pairs_list -> pair COMMA pairs_list | pair
    def add_pairs(result):
        new_result = {}
        [new_result.update(x) for x in result if isinstance(x, dict)]
        return [new_result]
    pairs_list = (pair & ws & Char(',') & ws & Ref('pairs_list')) | pair
    pairs_list = pairs_list.on_success(add_pairs)

    # object -> OPEN_CURLYBRACE pairs_list CLOSE_CURLYBRACE
    obj = Between((Char('{') + ws), pairs_list, (ws + Char('}')))

    # values_list -> value COMMA values_list | value
    values_list = (value & ws & Char(',') & ws & Ref('values_list')) | value

    # list -> OPEN_SQBRACE values_list CLOSE_BRACE
    lst = Between((Char('[') + ws), values_list, (ws + Char(']')))
    lst = lst.on_success(lambda result: [result[::2]])

    Ref.link({'lst': lst, 'obj': obj, 'pairs_list': pairs_list,
              'values_list': values_list})
    # json -> value
    return ws & value & ws & End()
