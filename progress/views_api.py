from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from progress.models import UserProfile
from scrapinghub import ScrapinghubClient, DuplicateJobError
from psbookprogress.settings import SHUB_KEY, SHUB_PROJECT
import json


def start_spider(request, username):
    try:
        profile = UserProfile.objects.get(user__username=username)
    except UserProfile.DoesNotExist:
        raise Http404()
    data = {'id': username}
    if profile.cf_id:
        data['cf'] = profile.cf_id
    if profile.loj_id:
        data['loj'] = profile.loj_id
    if profile.uva_id:
        data['uva'] = profile.uva_id
    if profile.timus_id:
        data['timus'] = profile.timus_id

    client = ScrapinghubClient(SHUB_KEY)
    project = client.get_project(SHUB_PROJECT)
    try:
        project.jobs.run('listmaker', job_args={'lst': json.dumps([data])})
        profile.status = 'Request queued'
        profile.save()
    except DuplicateJobError:
        pass

    return HttpResponseRedirect(reverse('profile', args=[username]))
