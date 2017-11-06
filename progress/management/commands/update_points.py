from django.core.management.base import BaseCommand
from progress.models import UserProfile, Problem, Variable
from functools import reduce


class Command(BaseCommand):
    help = 'Update points of all users'

    def add_arguments(self, parser):
        parser.add_argument('-s', action='store_true', help='silent')

    def handle(self, *args, **options):
        for user in UserProfile.objects.all():
            user.points = reduce(lambda a, b: a + b.part.points, user.solved_list.all(), 0)
            if not options['s']:
                self.stdout.write(self.style.SUCCESS(str(user)+' new points: '+str(user.points)))
            user.save()

        total_points = reduce(lambda a, b: a + b.part.points, Problem.objects.all(), 0)
        Variable.set('total_points', total_points, 'int')
        self.stdout.write(self.style.SUCCESS('\nnew total points: '+str(total_points)))
