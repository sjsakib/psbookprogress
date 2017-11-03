from django.conf.urls import url
from progress import views

urlpatterns = [
    url(r'^profile/(?P<username>.+)/$', views.profile, name='profile'),
    url(r'^test/$', views.test, name='test'),
    url(r'^update/$', views.update, name='update')
]
