# Parser Combinators

This is a proof-of-concept parser combinator library that I built from scratch as a cool side project and as a means to learn more about parsers and functional programming. Take a look at some of the examples:

- Parser for numbers in [number_parser.py](https://github.com/Arsh23/parser_combinators/blob/master/examples/number_parser.py)

- Parser for strings in [string_parser.py](https://github.com/Arsh23/parser_combinators/blob/master/examples/string_parser.py)

- Parser for algebraic expressions that also evaluates and returns the result in [expression_parser.py](https://github.com/Arsh23/parser_combinators/blob/master/examples/expression_parser.py), along with some usecases [here](https://github.com/Arsh23/parser_combinators/blob/master/examples/expression_parser_usecases.py)

- Parser for JSON in [json_parser.py](https://github.com/Arsh23/parser_combinators/blob/master/examples/json_parser.py), along with [this file](https://github.com/Arsh23/parser_combinators/blob/master/examples/generate_json.py) that generates random JSONs and tests the results of this parser with the python's json module.

If you want to play around with it, have a look at some basic tests in [tests.py](https://github.com/Arsh23/parser_combinators/blob/master/tests.py) and some of the [example](https://github.com/Arsh23/parser_combinators/tree/master/examples) parsers for how the API works until I get around to adding more documentation. Works on python >= 3.6
