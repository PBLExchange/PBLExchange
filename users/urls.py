from django.conf.urls import url, include
from . import views, forms
from questions.models import Question


detail_patterns = [
    url(r'^$', views.detail, name='detail'),
    url(r'^questions$', views.question_list, {
        'questions': Question.objects.by_user,
        'title_prefix': 'Questions by ',
    }, name='questions'),
    url(r'^unanswered$', views.question_list, {
        'questions': Question.objects.unanswered_by_user,
        'title_prefix': 'Unanswered questions by ',
    }, name='unanswered'),
    url(r'^answers$', views.question_list, {
        'questions': Question.objects.answered_by_user,
        'title_prefix': 'Answers by ',
    }, name='answered'),
    url(r'^bonus_points$', views.bonus_points, {
        'form_type': forms.BonusPointForm
    }, name='bonus_points')
]


urlpatterns = [
    url(r'^$', views.users, name='overview'),
    url(r'^detail/(?P<user_id>[0-9]+)/', include(detail_patterns)),
]
