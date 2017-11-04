from django.conf.urls import url
from progress import views

urlpatterns = [
    url(r'^profile/(?P<username>[^/]+)/$', views.profile, name='profile'),
    url(r'^showproblems/(?P<chapter_slug>ch-\w+)/(?P<part>\w+)/(?P<username>[^/]+)/', views.show_problems, name='show_problems'),
    url(r'^test/$', views.test, name='test'),
    url(r'^update/$', views.update, name='update')
]
