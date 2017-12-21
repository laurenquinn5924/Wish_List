from django.conf.urls import url
from . import views
urlpatterns = [
        url(r'^$', views.index),
        url(r'^register$', views.register),
        url(r'^display$', views.display),
        url(r'^login$', views.login),
        url(r'^logout$', views.logout),
        url(r'^new$', views.new),
        url(r'^create$', views.create),
        url(r'^join/(?P<wish_id>\d+)$', views.join, name='join'),
        url(r'^leave/(?P<wish_id>\d+)$', views.leave, name='leave'),
        url(r'^info/(?P<wish_id>\d+)$', views.info, name='info'),
]
