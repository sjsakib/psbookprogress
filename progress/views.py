from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from progress.models import Problem, Chapter, Part, Judge, UserProfile
import json


def profile(request, username):
    try:
        profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        pass

    chapters = Chapter.objects.all()
    all_parts = Part.objects.all()
    book_all = Problem.objects.all()

    ch_list = []

    for i, chapter in enumerate(chapters):
        chapter_all = book_all.filter(chapter=chapter)
        ch = {'chapter': chapter, 'parts': []}
        ch_total = {'all': chapter_all.count(), 'solved': 0}
        for part in all_parts:
            part_all = chapter_all.filter(part=part)
            part_solved = part_all.filter(userprofile=profile).count()
            ch['parts'].append({'part': part.slug, 'all': part_all.count(), 'solved': part_solved})

            ch_total['solved'] += part_solved
        ch['parts'].append(ch_total)
        ch_list.append(ch)

    return render(request, 'progress/profile.html', context={'profile': profile, 'chapters': ch_list})


@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        for username, item in data.items():
            try:
                profile = UserProfile.objects.get(user__username=username)
            except UserProfile.DoesNotExist:
                continue

            if item['failed']:
                failed_judges = Judge.objects.filter(slug__in=item['failed'])
                profile.status = 'Last update failed for '+', '.join(map(str, failed_judges))
                profile.save()
            profile.last_updated = timezone.now()
            for judge, plist in item['judges'].items():
                for pid in plist:
                    print(judge, profile, pid)
                    try:
                        problem = Problem.objects.get(Q(pid=pid) | Q(problemalias__pid=pid), judge__slug=judge)
                        profile.solved_list.add(problem)
                    except Problem.DoesNotExist:
                        pass
            profile.save()

    return HttpResponse(status=200)


def test(request):
    return render(request, 'progress/test.html')
