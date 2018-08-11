"""URLs of the app UI."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^partials/(?P<path>.+)$', views.serve_partials),
]
