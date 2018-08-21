from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),

    url(r'^logout$', views.logout),

    url(r'^home$', views.home ),
    url(r'^add$', views.add ),
    url(r'^process$', views.process),
    url(r'^(?P<id>\d+)/join$', views.join ),
    url(r'^(?P<id>\d+)/cancel$', views.cancel ),
    url(r'^(?P<id>\d+)/delete$', views.delete ),

    url(r'^(?P<id>\d+)/show$', views.show ),
    # url(r'^(?P<id>\d+)/update$', views.update ),

]
