import re

text = '{"key1": "value1"}'

patterns = [
    ('OPEN_CURLYBRACE', r'{'),
    ('KEY', r'(?<=")\w+(?=":)'),
    ('COLON', r':'),
    ('VALUE', r'(?<=")\w+(?="[^:])'),
    ('CLOSE_CURLYBRACES', r'}'),
]

regex = re.compile('|'.join([f'(?P<{x}>{y})' for x, y in patterns]))
print([(x.lastgroup, x.group(x.lastgroup)) for x in regex.finditer(text)])
#  [('OPEN_CURLYBRACE', '{'), ('KEY', 'key1'), ('COLON', ':'), ('VALUE', 'value1'), ('CLOSE_CURLYBRACES', '}')]
