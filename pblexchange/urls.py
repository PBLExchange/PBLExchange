from django.conf.urls import url

from pblexchange.models import Menu
from . import views
from django_cas_ng import views as cas_views

Menu.register('Tags', 'questions:tags')
Menu.register('Users', 'users:overview')
Menu.register('Ask a Question', 'questions:ask')

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', cas_views.login, name='login'),
    url(r'^logout/$', cas_views.logout, name='logout'),
]
