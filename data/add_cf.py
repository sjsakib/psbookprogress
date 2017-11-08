#!/usr/bin/python3
import json

with open('cf.json', 'r') as f:
    data = json.load(f)

with open('cf_all.json', 'r') as f:
    allp = json.load(f)

with open('cf_dups.json', 'r') as f:
    dups = json.load(f)


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

        lst = []
        for p in allp:
            if ' '+num+' ' in p[3] or num == str(p[0]):
                lst.append(p)

        for i, p in enumerate(lst):
            print(str(i) + '-->', p[0], p[1], p[2])

        try:
            c = int(input('Choice: '))
            p = lst[c]
            pid = str(p[0]) + '-' + p[1]
            print(p[1], p[2])
            input("Sure ? ")
            if pid in dups:
                d = [dups[pid]]
            else:
                d = []
            data.append([pid, pid, p[2], ch, part, d])
            count += 1
        except KeyboardInterrupt:
            print('Not added...')

    with open('cf.json', 'w') as f:
        json.dump(data, f, indent=4)
        print('Added ', count, 'problems')


if __name__ == '__main__':
    start()
