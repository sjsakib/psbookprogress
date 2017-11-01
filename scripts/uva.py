#!/usr/bin/python3
import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'psbookprogress.settings')
import django
os.chdir('..')
django.setup()

from progress.models import Problem, Part, Judge, Chapter

judge = Judge.objects.get(slug='uva')

with open('data/uva.json', 'r') as f:
    data = json.load(f)


def main():
    for p in data:
        add_problem(*p)


def add_problem(pid, pnum, name, ch, prt):
    chapter = Chapter.objects.get(slug=ch)
    part = Part.objects.get(slug=prt)

    problem, _ = Problem.objects.get_or_create(pid=pid, judge=judge)

    problem.name = judge.name + ' ' + pnum + ' - ' + name
    problem.part = part
    problem.chapter = chapter

    problem.save()

    print(problem)


if __name__ == '__main__':
    main()
