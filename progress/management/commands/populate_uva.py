import json
from django.core.management.base import BaseCommand
from progress.models import Problem, Part, Judge, Chapter


class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def start(self):
        with open('data/uva.json', 'r') as f:
            self.data = json.load(f)
        self.judge = Judge.objects.get(slug='uva')
        for p in self.data:
            self.add_problem(*p)

    def handle(self, *args, **options):
        self.start()

    def add_problem(self, pid, pnum, name, ch, prt):
        ch = 'ch-' + ch
        chapter = Chapter.objects.get(slug=ch)
        part = Part.objects.get(slug=prt)

        problem, _ = Problem.objects.get_or_create(pid=pid, judge=self.judge, chapter=chapter, part=part)
        problem.name = self.judge.name + ' ' + pnum + ' - ' + name
        problem.slug = 'uva-'+pnum

        problem.save()

        print(problem)
