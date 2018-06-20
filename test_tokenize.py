import unittest
from tokenizer import Token, tokenize


class TestTokenize(unittest.TestCase):

    def test_empty(self):
        text = '{}'
        output = [
            Token(name='OPEN_CURLYBRACE', value='{', line=1),
            Token(name='CLOSE_CURLYBRACE', value='}', line=1)
        ]
        self.assertEqual(list(tokenize(text)), output)

    def test_single(self):
        text = '{"key1": "value1"}'
        output = [
            Token(name='OPEN_CURLYBRACE', value='{', line=1),
            Token(name='KEY', value='key1', line=1),
            Token(name='COLON', value=':', line=1),
            Token(name='STRING', value='value1', line=1),
            Token(name='CLOSE_CURLYBRACE', value='}', line=1)
        ]
        self.assertEqual(list(tokenize(text)), output)

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
        output = [
            Token(name='OPEN_CURLYBRACE', value='{', line=1),
            Token(name='KEY', value='str', line=2),
            Token(name='COLON', value=':', line=2),
            Token(name='STRING', value='value1', line=2),
            Token(name='COMMA', value=',', line=2),
            Token(name='KEY', value='num', line=3),
            Token(name='COLON', value=':', line=3),
            Token(name='NUMBER', value='2', line=3),
            Token(name='COMMA', value=',', line=3),
            Token(name='KEY', value='t', line=4),
            Token(name='COLON', value=':', line=4),
            Token(name='TRUE', value='true', line=4),
            Token(name='COMMA', value=',', line=4),
            Token(name='KEY', value='f', line=5),
            Token(name='COLON', value=':', line=5),
            Token(name='FALSE', value='false', line=5),
            Token(name='COMMA', value=',', line=5),
            Token(name='KEY', value='n', line=6),
            Token(name='COLON', value=':', line=6),
            Token(name='NULL', value='null', line=6),
            Token(name='COMMA', value=',', line=6),
            Token(name='KEY', value='list', line=7),
            Token(name='COLON', value=':', line=7),
            Token(name='OPEN_SQBRACE', value='[', line=7),
            Token(name='STRING', value='text', line=8),
            Token(name='COMMA', value=',', line=8),
            Token(name='NUMBER', value='1', line=8),
            Token(name='COMMA', value=',', line=8),
            Token(name='TRUE', value='true', line=8),
            Token(name='COMMA', value=',', line=8),
            Token(name='OPEN_CURLYBRACE', value='{', line=8),
            Token(name='KEY', value='nested', line=8),
            Token(name='COLON', value=':', line=8),
            Token(name='STRING', value='inside', line=8),
            Token(name='CLOSE_CURLYBRACE', value='}', line=8),
            Token(name='CLOSE_SQBRACE', value=']', line=9),
            Token(name='COMMA', value=',', line=9),
            Token(name='KEY', value='la"st\\', line=10),
            Token(name='COLON', value=':', line=10),
            Token(name='NUMBER', value='-1234.123123e+123123', line=10),
            Token(name='CLOSE_CURLYBRACE', value='}', line=11)
        ]
        self.assertEqual(list(tokenize(text)), output)

    def test_keywords(self):
        text = '{"key,[1]": "{value1}"}'
        output = [
            Token(name='OPEN_CURLYBRACE', value='{', line=1),
            Token(name='KEY', value='key,[1]', line=1),
            Token(name='COLON', value=':', line=1),
            Token(name='STRING', value='{value1}', line=1),
            Token(name='CLOSE_CURLYBRACE', value='}', line=1)
        ]
        self.assertEqual(list(tokenize(text)), output)

    def test_generated(self):
        text = '{\n'
        output = [Token(name='OPEN_CURLYBRACE', value='{', line=1)]
        n = 10000
        for x in range(n):
            text += f'"key{x}": "value{x}",\n'
            output += [
                Token(name='KEY', value=f'key{x}', line=x+2),
                Token(name='COLON', value=':', line=x+2),
                Token(name='STRING', value=f'value{x}', line=x+2),
                Token(name='COMMA', value=',', line=x+2),
            ]

        text += '"last": "value"}'
        output += [
            Token(name='KEY', value='last', line=n+2),
            Token(name='COLON', value=':', line=n+2),
            Token(name='STRING', value='value', line=n+2),
            Token(name='CLOSE_CURLYBRACE', value='}', line=n+2)
        ]
        self.assertEqual(list(tokenize(text)), output)


if __name__ == '__main__':
    unittest.main()
