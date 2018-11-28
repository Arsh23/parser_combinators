import json
import time
import random
from json_parser import json_parser


limit = 5


def random_string():
    N = random.randint(1, 100)
    ascii_char = [chr(x) for x in range(33, 127) if chr(x) not in '"\\']
    return ''.join(random.choices(ascii_char, k=N))


def random_values(depth):
    vals = [
        True, False, float(random.randint(-1e10, 1e10)), random_string(),
        random_list(depth), random_dict(depth)
    ]
    return vals[random.randint(0, len(vals) - 1)]


def random_list(depth):
    if depth + 1 > limit:
        return True
    return [random_values(depth + 1) for _ in range(random.randint(1, 10))]


def random_dict(depth):
    if depth + 1 > limit:
        return True
    return {random_string(): random_values(depth + 1)
            for _ in range(random.randint(1, 10))}


if __name__ == '__main__':
    json1, json2 = True, True
    while json1 == json2:
        print('Generating JSON ...')
        random_json_string = json.dumps(random_dict(0))
        print('Randomly generated a JSON string')
        #  print(random_json_string)

        start_time_1 = time.time()
        json1 = json.loads(random_json_string)
        stop_time_1 = time.time()

        start_time_2 = time.time()
        json2 = json_parser()(random_json_string).result[0][0]
        stop_time_2 = time.time()

        print(f'json.loads == json_parser ? {json1 == json2}')
        print(f'TIme for json.loads: {stop_time_1 - start_time_1} secs')
        print(f'TIme for json_parser: {stop_time_2 - start_time_2} secs')

        with open('json1.json', 'w') as f:
            f.write(json.dumps(json1))

        with open('json2.json', 'w') as f:
            f.write(json.dumps(json2))
