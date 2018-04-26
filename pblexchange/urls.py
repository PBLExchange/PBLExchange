from django.conf.urls import url, include
from django.utils.translation import ugettext_lazy as _

from pblexchange.models import Menu
from . import views
from django_cas_ng import views as cas_views
from PBLExchangeDjango.settings import INSTALLED_APPS

Menu.register(_('Questions'), 'home')
Menu.register(_('Tags'), 'pble_questions:tags')
Menu.register(_('Users'), 'pble_users:overview')
if 'pble_subscriptions' in INSTALLED_APPS:
    Menu.register(_('Subscriptions'), 'pble_subscriptions:categories')
Menu.register(_('Ask a Question'), 'pble_questions:ask')

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', cas_views.login, name='login'),
    url(r'^logout/$', cas_views.logout, name='logout'),
]
