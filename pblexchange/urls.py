from django.conf.urls import url, include

from pblexchange.models import Menu
from . import views
from django_cas_ng import views as cas_views

Menu.register('Questions', 'home')
Menu.register('Tags', 'questions:tags')
Menu.register('Users', 'users:overview')
Menu.register('Subscriptions', 'subscriptions:categories')
Menu.register('Ask a Question', 'questions:ask')

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', cas_views.login, name='login'),
    url(r'^logout/$', cas_views.logout, name='logout'),
    # Pinax notifications url
    url(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
]
