from expression_parser import exp_parser


examples = [
    '1+2',
    '0 + -0 - -123.456E-7',
    ' 1 + 2 * 3 - ( 4 / 5 ) ',
    '-12.34e10 + 32E-3 - 10.67',
    '-9 * (3+4+7) * (3-2-6+45) / 26e2',
    '564327/78642 * 979797 * 234e5',
    '(4-3-6-7) * (5-7-375+456) / (446 * (45 + 5 - 67) * 45e8) * (453/673)',
]
parser = exp_parser()


def demo():
    for i, ex in enumerate(examples):
        print(f'Ex {i + 1}: {ex}')
        print(f'Result: {parser(ex).result}')
        print()


if __name__ == '__main__':
    demo()
    while True:
        print(f'Result: {parser(input("Try some exps:")).result}')
        print()
