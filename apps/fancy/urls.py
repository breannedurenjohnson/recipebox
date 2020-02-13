from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^submit_registration$', views.submit_registration),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^recipes/(?P<id>\d+)$', views.recipe),
    url(r'^user/(?P<user_id>\d+)$', views.profile),
    url(r'^meals/(?P<meal>\w+)$', views.meal),
    url(r'^recipes/(?P<id>\d+)/like$', views.like_recipe), 
    url(r'^recipes/(?P<id>\d+)/unlike$', views.unlike_recipe),
    # url(r'^recipes/(?P<id>\d+)/edit$', views.edit_recipe),
    # url(r'^recipes/(?P<id>\d+)/update$', views.update_recipe),
    # url(r'^recipes/(?P<id>\d+)/delete$', views.delete_recipe),
    url(r'^logout$', views.logout),
]