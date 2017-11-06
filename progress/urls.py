from django.conf.urls import url
from progress import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name='profile'),
    url(r'^showproblems/(?P<chapter_slug>ch-\w+)/(?P<part>\w+)/(?P<username>[^/]+)/', views.show_problems, name='show_problems'),
    url(r'^problem/(?P<problem_slug>[\w-]+)/solved-by/page/(?P<page>\d+)$', views.solved_by, name='solved_by'),
    url(r'^ranklist/$', views.ranklist, name='ranklist'),
    url(r'^ranklist/page/(?P<page>\d+)/$', views.ranklist, name='ranklist'),
    url(r'^about/$', views.about, name='about'),
    url(r'^update/$', views.update, name='update')
]
