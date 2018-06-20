import re
from collections import namedtuple


Token = namedtuple('Token', ['name', 'value', 'line'])


def tokenize(text):
    """
    This function finds JSON tokens in the given text through regex

    Args:
        text: the string to find tokens in

    Returns:
        A list of tuples with token name and value

    Example:
    >>> for token in tokenize('{"key": "value"}'):
    ...     print(token)
    Token(name='OPEN_CURLYBRACE', value='{', line=1)
    Token(name='KEY', value='key', line=1)
    Token(name='COLON', value=':', line=1)
    Token(name='STRING', value='value', line=1)
    Token(name='CLOSE_CURLYBRACE', value='}', line=1)
    """
    patterns = [
        ('KEY', r'(?<=")[\w\"\\\/\b\f\r\t,\[\]{}]+(?=":)'),
        ('TRUE', r'true(?=(,)|(\s*})|(\s*\]))'),
        ('FALSE', r'false(?=(,)|(\s*})|(\s*\]))'),
        ('NULL', r'null(?=(,)|(\s*})|(\s*\]))'),
        ('NUMBER', r'-?(0|([1-9]\d*))(\.\d+)?([eE][-+]?\d+)?'
            '(?=(,)|(\s*})|(\s*\]))'),
        ('STRING', r'(?<=")[\w\"\\\/\b\f\r\t,\[\]{}]+'
            '(?=(",)|("\s*})|("\s*\]))'),
        ('COLON', r':'),
        ('COMMA', r','),
        ('NEWLINE', r'\n'),
        ('OPEN_SQBRACE', r'\['),
        ('CLOSE_SQBRACE', r'\]'),
        ('OPEN_CURLYBRACE', r'{'),
        ('CLOSE_CURLYBRACE', r'}'),
    ]
    line = 1
    regex = re.compile('|'.join([f'(?P<{x}>{y})' for x, y in patterns]))
    for x in regex.finditer(text):
        if x.lastgroup == 'NEWLINE':
            line += 1
        else:
            yield Token(x.lastgroup, x.group(x.lastgroup), line)
