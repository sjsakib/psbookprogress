import json
from django.core.management.base import BaseCommand
from progress.models import Problem, ProblemAlias, Part, Judge, Chapter


class Command(BaseCommand):
    help = 'Populate problems form json files in the data directory'

    def add_arguments(self, parser):
        parser.add_argument('-j', type=str, help='judge slug')
        parser.add_argument('-f', type=str, help='filename in the data directory')

    def start(self):
        for p in self.data:
            self.add_problem(*p)

    def handle(self, *args, **options):
        with open('data/'+options['f'], 'r') as f:
            self.data = json.load(f)
        self.judge = Judge.objects.get(slug=options['j'])

        self.start()

    def add_problem(self, pid, pnum, name, ch, prt, aliases):
        ch = 'ch-' + ch
        chapter = Chapter.objects.get(slug=ch)
        part = Part.objects.get(slug=prt)

        problem, _ = Problem.objects.get_or_create(pid=pid, judge=self.judge, chapter=chapter, part=part)
        problem.name = self.judge.name + ' ' + pnum + ' - ' + name
        problem.slug = self.judge.slug + '-' + pnum

        problem.save()
        self.stdout.write(self.style.SUCCESS('added '+str(problem)))

        for al in aliases:
            alias, _ = ProblemAlias.objects.get_or_create(problem=problem, pid=al)
            alias.save()
            self.stdout.write(self.style.SUCCESS('  -- added alias '+str(alias)))
