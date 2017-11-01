#!/usr/bin/python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'psbookprogress.settings')
import django
django.setup()

from progress.models import Chapter, Part, Judge

parts = ('main', 'simple', 'easy', 'medium', 'hard')

judges = (
    ('LightOJ', 'loj'),
    ('UVa', 'uva'),
    ('Codeforces', 'cf'),
    ('Timus', 'timus'),
)

chapters = (
    ('Some Easy Problems', 'ch-ii'),
    ('STL Practice', 'ch-iii'),
    ('Mathematics', 'ch-iv'),
    ('Bruteforce and Backtrack', 'ch-v'),
    ('Data Structure', 'ch-vi'),
    ('Greedy', 'ch-vii'),
    ('Dynamic Programming', 'ch-viii'),
    ('Graph Theory', 'ix'),
    ('Adhoc', 'ch-x'),
    ('Geometry', 'ch-xi'),
)


def populate():
    for p in parts:
        add_part(p)
    for j in judges:
        add_judge(*j)
    for ch in chapters:
        add_chapter(*ch)


def add_part(p):
    part = Part.objects.get_or_create(slug=p)[0]
    print(part)
    part.slug = p
    part.save()
    print(part)


def add_judge(name, slug):
    judge = Judge.objects.get_or_create(slug=slug)[0]
    judge.name = name
    judge.slug = slug
    judge.save()
    print(judge)


def add_chapter(name, slug):
    chapter = Chapter.objects.get_or_create(slug=slug)[0]
    chapter.name = name
    chapter.slug = slug
    chapter.save()
    print(chapter)


if __name__ == '__main__':
    print('Starting population...')
    populate()
