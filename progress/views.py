from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from progress.models import Problem, Chapter, Part, Judge, UserProfile
import json
from math import ceil


def profile(request, username):
    try:
        profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        raise Http404('User Not Found')

    chapters = Chapter.objects.all()
    all_parts = Part.objects.all()
    book_all = Problem.objects.all()

    ch_list = []

    all_chapters = {'chapter': Chapter(name='All Chapters', slug='ch-all'), 'parts': []}
    for part in all_parts:
        all_chapters['parts'].append({'part': part.slug, 'all': 0, 'solved': 0})
    all_chapters['parts'].append({'part': 'all', 'all': book_all.count(), 'solved': 0})

    for chapter in chapters:
        chapter_all = book_all.filter(chapter=chapter)
        ch = {'chapter': chapter, 'parts': []}
        ch_total = {'part': 'all', 'all': chapter_all.count(), 'solved': 0}

        for i, part in enumerate(all_parts):
            part_all = chapter_all.filter(part=part)
            part_solved = part_all.filter(userprofile=profile).count()
            ch['parts'].append({'part': part.slug, 'all': part_all.count(), 'solved': part_solved})

            ch_total['solved'] += part_solved

            all_chapters['parts'][i]['all'] += part_all.count()
            all_chapters['parts'][i]['solved'] += part_solved
            all_chapters['parts'][-1]['solved'] += part_solved

        ch['parts'].append(ch_total)
        ch_list.append(ch)
    ch_list.append(all_chapters)

    return render(request, 'progress/profile.html', context={'profile': profile, 'chapters': ch_list})


def show_problems(request, chapter_slug, part, username=''):
    q = Q()
    if chapter_slug != 'ch-all':
        chapter = Chapter.objects.filter(slug=chapter_slug).first()
        if chapter:
            q &= Q(chapter__pk=chapter.pk)
    else:
        chapter = Chapter(name='All chapters')

    if part != 'all':
        q &= Q(part__slug=part)

    problems = Problem.objects.filter(q)

    for p in problems:
        if p.userprofile_set.filter(user__username=username).exists():
            p.solved = True
        else:
            p.solved = False

    context_dict = {'problems': problems}
    context_dict['chapter'] = chapter
    context_dict['part'] = part
    return render(request, 'progress/show_problems.html', context=context_dict)


def solved_by(request, problem_slug, page):
    page = int(page)
    per_page = 100
    try:
        p = Problem.objects.get(slug=problem_slug)
        solvers = p.userprofile_set.all()
        pages = int(ceil(len(solvers) / per_page))
        if page > pages:
            page = pages
        if page != 0:
            solvers = solvers[(page-1) * per_page: page*per_page]
    except Problem.DoesNotExist:
        p = None
        solvers = None
        pages = 0
    return render(request, 'progress/solved_by.html', context={'problem': p,
                                                               'solvers': solvers,
                                                               'pages': range(pages),
                                                               'page': page})


def ranklist(request, page=1):
    all_users = UserProfile.objects.all()

    return render(request, 'progress/ranklist.html', {'users': all_users})


@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))

        for username, item in data.items():
            try:
                profile = UserProfile.objects.get(user__username=username)
            except UserProfile.DoesNotExist:
                continue

            count = 0
            for judge, plist in item['judges'].items():
                for pid in plist:
                    print(judge, profile, pid)
                    try:
                        problem = Problem.objects.get(Q(pid=pid) | Q(problemalias__pid=pid), judge__slug=judge)
                        if not profile.solved_list.filter(pk=problem.pk).exists():
                            profile.solved_list.add(problem)
                            count += 1
                    except Problem.DoesNotExist:
                        pass
            profile.status = ''
            if count:
                profile.last_updated = timezone.now()
                profile.status = "{} new problem(s) were updated with last request.".format(count)
            else:
                profile.status = 'Nothing updated with last request.'
            if item['failed']:
                failed_judges = Judge.objects.filter(slug__in=item['failed'])
                profile.status += ' Last update failed for '+', '.join(map(str, failed_judges)) + '. Might be down.'
            profile.save()

    return HttpResponse(status=200)


def test(request):
    return render(request, 'progress/test.html')
