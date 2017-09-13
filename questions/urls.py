from django.conf.urls import url, include
from . import views
from .models import Answer
from .forms import AnswerForm

urlpatterns = [
    url(r'^detail/(?P<question_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^upvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': 1}, name='upvote'),
    url(r'^downvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': -1}, name='downvote'),

    # Post types
    url(r'^answers/', include('questions.answer_urls', namespace='answers'), {
        'post_type': Answer,
        'form_type': AnswerForm,
    }),
]



