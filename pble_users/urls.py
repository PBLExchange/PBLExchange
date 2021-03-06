from django.conf.urls import url, include
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from . import views
from pble_questions.models import Question, Post
from PBLExchangeDjango.settings import PBLE_GROUPS


detail_patterns = [
    url(r'^$', views.detail, name='detail'),
    url(r'^pble_questions$', views.question_list, {
        'questions': Question.objects.by_user,
        'title_prefix': _('Questions by '),
    }, name='pble_questions'),
    url(r'^unanswered$', views.question_list, {
        'questions': Question.objects.unanswered_by_user,
        'title_prefix': _('Unanswered questions by '),
    }, name='unanswered'),
    url(r'^answers$', views.question_list, {
        'questions': Question.objects.answered_by_user,
        'title_prefix': _('Answers by '),
    }, name='answered'),
    url(r'^bonus_points$', views.bonus_points, name='bonus_points')
]


urlpatterns = [
    url(r'^$', views.users, name='overview'),
    url(r'^detail/(?P<user_id>[0-9]+)/', include(detail_patterns)),
    url(r'^language/(?P<lang_code>[a-zA-Z\-]+)$', views.set_language, name='set_language'),
]
