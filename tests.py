import unittest
from parserc import Char, Any, Seq, ZeroOrMore, OneOrMore, Between


class TestParser(unittest.TestCase):

    def test_single_char(self):
        parse_A = Char('A')
        self.assertEqual(parse_A('ABC').result, ['A'])
        self.assertEqual(parse_A('DBC').success, False)

    # -------
    def test_and(self):
        parser = Char('A') + Char('B')
        result = parser('ABC').result
        self.assertEqual(result, [['A'], ['B']])

    def test_and_multiple(self):
        parser = Char('A') + Char('B') + Char('C') + Char('D') + Char('E')
        result = parser('ABCDE').result
        self.assertEqual(result, [['A'], ['B'], ['C'], ['D'], ['E']])

    def test_and_complex(self):
        parser_AB = Char('A') + Char('B')
        parser_CD = Char('C') + Char('D')
        parser = parser_AB + parser_CD
        result = parser('ABCDE').result
        self.assertEqual(result, [['A'], ['B'], ['C'], ['D']])

    def test_or(self):
        parser = Char('A') | Char('B')
        result = parser('ABC').result
        self.assertEqual(result, ['A'])

    def test_or_multiple(self):
        parser = Char('A') | Char('B') | Char('C') | Char('D') | Char('E')
        result = parser('CDE').result
        self.assertEqual(result, ['C'])

    # -------
    def test_any(self):
        parser = Any([Char('A'), Char('B'), Char('C')])
        result = parser('BC').result
        self.assertEqual(result, ['B'])

        parser = Any('ABC')
        result = parser('BC').result
        self.assertEqual(result, ['B'])

    def test_seq(self):
        parser = Seq([Char('A'), Char('B'), Char('C')])
        result = parser('ABC').result
        self.assertEqual(result, [['A'], ['B'], ['C']])

        parser = Seq('ABC')
        result = parser('ABC').result
        self.assertEqual(result, [['A'], ['B'], ['C']])

    # -------
    def test_optional(self):
        parser = ~Char('A')
        self.assertEqual(parser('X').result, [])
        self.assertEqual(parser('A').result, ['A'])

        parser = ~Char('A') + Char('B')
        self.assertEqual(parser('B').result, [['B']])
        self.assertEqual(parser('AB').result, [['A'], ['B']])

    def test_ZeroOrMore(self):
        parser = ZeroOrMore(Char('A'))
        self.assertEqual(parser('X').result, [])
        self.assertEqual(parser('A').result, [['A']])
        self.assertEqual(parser('AAAA').result, [['A'], ['A'], ['A'], ['A']])

        parser = ZeroOrMore(Any('12345'))
        self.assertEqual(parser('X').result, [])
        self.assertEqual(parser('1').result, [['1']])
        self.assertEqual(parser('1234').result, [['1'], ['2'], ['3'], ['4']])

    def test_OneOrMore(self):
        parser = OneOrMore(Char('A'))
        self.assertEqual(parser('X').success, False)
        self.assertEqual(parser('A').result, [['A']])
        self.assertEqual(parser('AAAA').result, [['A'], ['A'], ['A'], ['A']])

        parser = OneOrMore(Any('12345'))
        self.assertEqual(parser('X').success, False)
        self.assertEqual(parser('1').result, [['1']])
        self.assertEqual(parser('1234').result, [['1'], ['2'], ['3'], ['4']])

    # -------
    def test_between(self):
        parser = Between(Char('A'), Char('B'), Char('C'))
        self.assertEqual(parser('ABC').result, ['B'])

        parser = Between(Char('A'), (Char('B') + Char('C')), Char('D'))
        self.assertEqual(parser('ABCD').result, [['B'], ['C']])


if __name__ == '__main__':
    unittest.main()
