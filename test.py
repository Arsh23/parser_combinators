import re

text = '''{
    "key1": "value1",
    "key2": "value2",
    "t":  true,  
    "f": false,
    "n": null,
    "a": [1, 2, "3", true,
    "fal\\se"
    ],
    "ke\"y3\\\/": -823793.013e+19891,
    "key419Ae": +0.013E-19891
}
'''

patterns = [
    ('OPEN_CURLYBRACE', r'{'),
    ('KEY', r'(?<=")[\w\"\\\/\b\f\n\r\t]+(?=":)'),
    ('COLON', r':'),
    ('COMMA', r','),
    ('TRUE', r'true(?=(,)|(\s*})|(\s*\]))'),
    ('FALSE', r'false(?=(,)|(\s*})|(\s*\]))'),
    ('NULL', r'null(?=(,)|(\s*})|(\s*\]))'),
    ('NUMBER', r'-?(0|([1-9]\d*))(\.\d+)?([eE][-+]?\d+)?(?=(,)|(\s*})|(\s*\]))'),
    ('STRING', r'(?<=")[\w\"\\\/\b\f\n\r\t]+(?=(",)|("\s*})|("\s*\]))'),
    ('OPEN_SQBRACE', r'\['),
    ('CLOSE_SQBRACE', r'\]'),
    ('CLOSE_CURLYBRACES', r'}'),
]

regex = re.compile('|'.join([f'(?P<{x}>{y})' for x, y in patterns]))
#  print([(x.lastgroup, x.group(x.lastgroup)) for x in regex.finditer(text)])
for x in regex.finditer(text):
    print((x.lastgroup, x.group(x.lastgroup)))
