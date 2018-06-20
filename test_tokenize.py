import unittest
from tokenizer import tokenize


class TestTokenize(unittest.TestCase):

    def test_empty(self):
        text = '{}'
        output = [('OPEN_CURLYBRACE', '{'), ('CLOSE_CURLYBRACE', '}')]
        self.assertEqual(tokenize(text), output)

    def test_single(self):
        text = '{"key1": "value1"}'
        output = [('OPEN_CURLYBRACE', '{'),
                  ('KEY', 'key1'),
                  ('COLON', ':'),
                  ('STRING', 'value1'),
                  ('CLOSE_CURLYBRACE', '}')]
        self.assertEqual(tokenize(text), output)

    def test_multiple(self):
        text = '''{
            "str": "value1",
            "num": 2,
            "t": true,
            "f": false,
            "n": null,
            "list": [
                "text", 1, true, {"nested": "inside"}
            ],
            "la\"st\\": -1234.123123e+123123
        }'''
        output = [('OPEN_CURLYBRACE', '{'),
                  ('KEY', 'str'),
                  ('COLON', ':'),
                  ('STRING', 'value1'),
                  ('COMMA', ','),
                  ('KEY', 'num'),
                  ('COLON', ':'),
                  ('NUMBER', '2'),
                  ('COMMA', ','),
                  ('KEY', 't'),
                  ('COLON', ':'),
                  ('TRUE', 'true'),
                  ('COMMA', ','),
                  ('KEY', 'f'),
                  ('COLON', ':'),
                  ('FALSE', 'false'),
                  ('COMMA', ','),
                  ('KEY', 'n'),
                  ('COLON', ':'),
                  ('NULL', 'null'),
                  ('COMMA', ','),
                  ('KEY', 'list'),
                  ('COLON', ':'),
                  ('OPEN_SQBRACE', '['),
                  ('STRING', 'text'),
                  ('COMMA', ','),
                  ('NUMBER', '1'),
                  ('COMMA', ','),
                  ('TRUE', 'true'),
                  ('COMMA', ','),
                  ('OPEN_CURLYBRACE', '{'),
                  ('KEY', 'nested'),
                  ('COLON', ':'),
                  ('STRING', 'inside'),
                  ('CLOSE_CURLYBRACE', '}'),
                  ('CLOSE_SQBRACE', ']'),
                  ('COMMA', ','),
                  ('KEY', 'la\"st\\'),
                  ('COLON', ':'),
                  ('NUMBER', '-1234.123123e+123123'),
                  ('CLOSE_CURLYBRACE', '}')]
        self.assertEqual(tokenize(text), output)


if __name__ == '__main__':
    unittest.main()
