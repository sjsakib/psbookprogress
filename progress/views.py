from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from progress.models import Problem, Chapter, Part, Judge, UserProfile
from progress.forms import UserForm, UserProfileForm
import json
from math import ceil


def index(request):
    top_users = UserProfile.objects.all().order_by('-points', 'last_updated')[:20]
    recently_active = UserProfile.objects.all().order_by('-last_updated')[:20]
    return render(request, 'progress/index.html', context={'top_users': top_users,
                                                           'recently_active': recently_active})


def profile(request, username=None):
    if username is None and request.user.is_authenticated():
        username = request.user.username
    elif username is None:
        return HttpResponseRedirect(reverse('auth_login') + '?next=' + reverse('my_profile'))

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


def update_info(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'progress/update_info.html', context={'user_form': user_form,
                                                                 'profile_form': profile_form})


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
    if username:
        try:
            name = UserProfile.objects.get(user__username=username).get_name()
        except UserProfile.DoesNotExist:
            name = ''

    context_dict = {'problems': problems}
    context_dict['chapter'] = chapter
    context_dict['part'] = part
    context_dict['name'] = name
    return render(request, 'progress/show_problems.html', context=context_dict)


def solved_by(request, problem_slug, page=1):
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
    page = int(page)
    per_page = 50
    all_users = UserProfile.objects.all().order_by('-points', 'last_updated')
    user_rank = 1
    for i, usr in enumerate(all_users):
        if request.user.pk == usr.user.pk:
            user_rank == i+1
            break

    pages = int(ceil(all_users.count() / per_page))
    if page > pages:
            page = pages
    if page != 0:
        all_users = all_users[(page-1) * per_page: page*per_page]
    return render(request, 'progress/ranklist.html', {'users': all_users,
                                                      'pages': range(pages),
                                                      'page': page,
                                                      'user_rank': user_rank,
                                                      'user_bottom': page*per_page < user_rank})


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


def help(request):
    return render(request, 'progress/help.html')
