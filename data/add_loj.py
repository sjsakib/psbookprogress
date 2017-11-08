#!/usr/bin/python3
import json

with open('loj.json', 'r') as f:
    data = json.load(f)

with open('loj_all.json', 'r') as f:
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

        p = allp[int(num)-1000]
        print(num, p)
        try:
            input('Sure?')
            for problem in data:
                if num == problem[0]:
                    print('Already added...')
                    print(problem)
                    break
            else:
                data.append([num, num, p, ch, part, []])
                count += 1
        except KeyboardInterrupt:
            print('Not added...')

    with open('loj.json', 'w') as f:
        json.dump(data, f, indent=4)
        print('Added ', count, 'problems')


if __name__ == '__main__':
    start()
