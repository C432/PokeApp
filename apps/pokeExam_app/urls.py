from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dash$', views.dash),
    url(r'^createFriend$', views.createFriend),
    url(r'^friendResults/(?P<user_id>\d+)$', views.friendResults),
]
