from django.core.management.base import BaseCommand
from progress.models import Part, Judge, Chapter


class Command(BaseCommand):
    help = 'Adds chapters, parts and judges'

    parts = (
        ('main', 10),
        ('simple', 5),
        ('easy', 8),
        ('medium', 10),
        ('hard', 15),
    )

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
        ('Graph Theory', 'ch-ix'),
        ('Adhoc', 'ch-x'),
        ('Geometry', 'ch-xi'),
    )

    def populate(self):
        for p in self.parts:
            self.add_part(*p)
        for j in self.judges:
            self.add_judge(*j)
        for ch in self.chapters:
            self.add_chapter(*ch)

    def add_part(self, p, points):
        part, _ = Part.objects.get_or_create(slug=p, points=points)
        part.save()
        self.stdout.write(self.style.SUCCESS('added part '+str(part)))

    def add_judge(self, name, slug):
        judge, _ = Judge.objects.get_or_create(slug=slug)
        judge.name = name
        judge.slug = slug
        judge.save()
        self.stdout.write(self.style.SUCCESS('added judge '+str(judge)))

    def add_chapter(self, name, slug):
        chapter, _ = Chapter.objects.get_or_create(slug=slug)
        chapter.name = name
        chapter.slug = slug
        chapter.save()
        self.stdout.write(self.style.SUCCESS('added chapter '+str(chapter)))

    def handle(self, *args, **options):
        self.populate()
