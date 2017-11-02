#!/usr/bin/python3
import json

with open('timus.json', 'r') as f:
    data = json.load(f)

with open('timus_all.json', 'r') as f:
    allp = json.load(f)


def start():
    count = 0
    ch = input('Chapter? ')
    part = input('Part? ')
    while True:
        num = input('\nNumber, x to exit: ')
        if num == 'x':
            break
        if num == 'ch':
            ch = input('Chapter? ')
            continue
        if num == 'prt':
            part = input('Part? ')
            continue

        for pr in allp:
            if pr['id'] == num:
                p = pr
                break
        print(num, '->', p['id'], p['name'])
        try:
            input('Sure?')
            for problem in data:
                if p['id'] == problem[0]:
                    print('Already added...')
                    print(problem)
                    break
            else:
                data.append([p['id'], num, p['name'], ch, part, []])
                count += 1
        except KeyboardInterrupt:
            print('Not added...')

    with open('timus.json', 'w') as f:
        json.dump(data, f, indent=4)
        print('Added ', count, 'problems')


if __name__ == '__main__':
    start()
