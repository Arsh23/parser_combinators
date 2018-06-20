import re


patterns = [
    ('OPEN_CURLYBRACE', r'{'),
    ('KEY', r'(?<=")[\w\"\\\/\b\f\n\r\t]+(?=":)'),
    ('COLON', r':'),
    ('COMMA', r','),
    ('TRUE', r'true(?=(,)|(\s*})|(\s*\]))'),
    ('FALSE', r'false(?=(,)|(\s*})|(\s*\]))'),
    ('NULL', r'null(?=(,)|(\s*})|(\s*\]))'),
    ('NUMBER', r'-?(0|([1-9]\d*))(\.\d+)?([eE][-+]?\d+)?'
        '(?=(,)|(\s*})|(\s*\]))'),
    ('STRING', r'(?<=")[\w\"\\\/\b\f\n\r\t]+(?=(",)|("\s*})|("\s*\]))'),
    ('OPEN_SQBRACE', r'\['),
    ('CLOSE_SQBRACE', r'\]'),
    ('CLOSE_CURLYBRACE', r'}'),
]


def tokenize(text):
    """
    This function finds JSON tokens in the given text through regex

    Args:
        text: the string to find tokens in

    Returns:
        A list of tuples with token name and value

    Examples:
    >>> for token in tokenize('{"key": "value"}'):
    ...     print(token)
    ('OPEN_CURLYBRACE', '{')
    ('KEY', 'key')
    ('COLON', ':')
    ('STRING', 'value')
    ('CLOSE_CURLYBRACE', '}')
    """
    regex = re.compile('|'.join([f'(?P<{x}>{y})' for x, y in patterns]))
    return [(x.lastgroup, x.group(x.lastgroup)) for x in regex.finditer(text)]
