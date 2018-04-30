from PBLExchangeDjango.settings import INSTALLED_APPS
from pblexchange.models import Menu

from django.utils.translation import ugettext as _


Menu.register(_('Questions'), 'home')
if 'pble_questions' in INSTALLED_APPS:
    from pble_questions.models import Category
    if Category.objects.count() > 0:
        Menu.register(_('Categories'), 'pble_questions:categories')
    Menu.register(_('Tags'), 'pble_questions:tags')
Menu.register(_('Users'), 'pble_users:overview')
if 'pble_subscriptions' in INSTALLED_APPS:
    Menu.register(_('Subscriptions'), 'pble_subscriptions:categories')
Menu.register(_('Ask a Question'), 'pble_questions:ask')
