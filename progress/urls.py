from django.conf.urls import url
from progress import views, views_api

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='my_profile'),
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name='profile'),
    url(r'^update-info/$', views.update_info, name='update_info'),
    url(r'^showproblems/(?P<chapter_slug>ch-\w+)/(?P<part>\w+)/(?P<username>[^/]+)/', views.show_problems, name='show_problems'),
    url(r'^problem/(?P<problem_slug>[\w-]+)/solved-by/page/(?P<page>\d+)$', views.solved_by, name='solved_by'),
    url(r'^ranklist/$', views.ranklist, name='ranklist'),
    url(r'^ranklist/page/(?P<page>\d+)/$', views.ranklist, name='ranklist'),
    url(r'^help/$', views.help, name='help'),
    url(r'^update/$', views.update, name='update'),
    url(r'^request/(?P<username>[^/]+)$', views_api.start_spider, name='request'),
]
