import unittest
from parser import Char, Result


class TestParser(unittest.TestCase):

    def test_single_char(self):
        parse_A = Char('A')
        inp = 'ABC'
        test_res = Result(True, 'A', 'BC')
        res = parse_A(inp)
        self.assertEqual(res, test_res)

        inp = 'DBC'
        test_res = Result(False, 'Expected "A" but got "D"', '')
        res = parse_A(inp)
        self.assertEqual(res, test_res)


if __name__ == '__main__':
    unittest.main()
