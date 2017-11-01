from django.conf.urls import url, include
from . import views
from questions.models import Question


detail_patterns = [
    url(r'^$', views.detail, name='detail'),
    url(r'^questions$', views.question_list, {
        'questions': Question.objects.by_user,
    }, name='questions'),
    url(r'^unanswered$', views.question_list, {
        'questions': Question.objects.unanswered_by_user,
    }, name='unanswered'),
    url(r'^answered$', views.question_list, {
        'questions': Question.objects.answered_by_user,
    }, name='answered')
]


urlpatterns = [
    url(r'^$', views.users, name='overview'),
    url(r'^detail/(?P<user_id>[0-9]+)', include(detail_patterns)),
]
