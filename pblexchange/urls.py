from django.conf.urls import url
from . import views
from django_cas_ng import views as cas_views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', cas_views.login, name='login'),
    url(r'^logout/$', cas_views.logout, name='logout'),
]
