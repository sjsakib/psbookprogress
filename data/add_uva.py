#!/usr/bin/python3
import requests
import json

api_url = 'https://uhunt.onlinejudge.org/api/p/num/'

with open('uva.json', 'r') as f:
    data = json.load(f)


def start():
    count = 0
    ch = input('Chapter? ')
    part = input('Part? ')
    while True:
        num = input('\nNumber, x to exit: ')
        if num == 'x':
            print('Added ', count, 'problems')
            break
        if num == 'ch':
            ch = input('Chapter? ')
            continue
        if num == 'prt':
            part = input('Part? ')
            continue

        try:
            p = requests.get(api_url+num).json()
            print(num, '->', p['pid'], p['title'])
            input('Sure?')
            for problem in data:
                if p['pid'] == problem[0]:
                    print('Already added')
                    print(p)
                    break
            else:
                data.append([str(p['pid']), num, p['title'], ch, part])
                count += 1
        except KeyboardInterrupt:
            print('Not added...')
        except KeyError:
            print('Invalid num...')

    with open('uva.json', 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    start()
