import sys
sys.path.append('..')
from number_parser import number_parser
from string_parser import string_parser
from parserc import (
    Char, Any, Seq, Between, ZeroOrMore, Ref, End, StripWhitespace
)


# Grammar for json:
#
# value -> STRING | NUMBER | TRUE | FALSE | NULL | list | object
#
# pair -> STRING COLON value
# pairs_list -> pair COMMA pairs_list | pair
# object -> OPEN_CURLYBRACE pairs_list CLOSE_CURLYBRACE
#
# list -> OPEN_SQBRACE values_list CLOSE_BRACE
# values_list -> value COMMA values_list | value
#
# json -> value


def concat_dicts(result):
    # helper func to concat json pairs
    # result format: [[dict1], [[,], [dict2]], [[,], [dict3]] .... ]
    new_dict = result[0][0]
    for _, other_dict in result[1:]:
        new_dict.update(other_dict[0])
    return new_dict


def concat_lists(result):
    # helper func to concat json lists
    # result format: [list1, [[,], list2], [[,], list3] .... ]
    new_list = result[0][:]
    for _, other_list in result[1:]:
        new_list += other_list
    return [new_list]


def json_parser():
    # NULL, TRUE, FALSE parser
    null = Seq('null').map(lambda r: None)
    true = Seq('true').map(lambda r: True)
    false = Seq('false').map(lambda r: False)

    # NUMBER and STRING parser
    number = number_parser()
    # json string: QUOTE string QUOTE
    string = Between(Char('"'), string_parser(), Char('"'))

    # value -> STRING | NUMBER | TRUE | FALSE | NULL | list | object
    value = Any([string, number, null, true, false, Ref('lst'), Ref('obj')])
    # references to 'lst' and 'obj' are use since they are not defined yet

    # pair -> STRING COLON value
    to_dict = lambda result: {result[0][0]: result[2][0]}
    pair = (string + Char(':') + value).map(to_dict)

    # pairs_list -> pair COMMA pairs_list | pair
    pairs_list = (pair + ZeroOrMore(Char(',') + pair)).map(concat_dicts)

    # object -> OPEN_CURLYBRACE pairs_list CLOSE_CURLYBRACE
    obj = Between(Char('{'), pairs_list, Char('}'))

    # values_list -> value COMMA values_list | value
    values_list = (value + ZeroOrMore(Char(',') + value)).map(concat_lists)

    # list -> OPEN_SQBRACE values_list CLOSE_BRACE
    lst = Between(Char('['), values_list, Char(']'))

    # linking references to actual parsers
    Ref.link({'lst': lst, 'obj': obj})

    # json -> value
    parser = StripWhitespace() + value + End()
    parser.map(lambda result: result[0][0])
    return parser


if __name__ == '__main__':
    p = json_parser()
    print(p('{"test": "pass"}'))
