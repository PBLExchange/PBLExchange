from django.conf.urls import url, include
from . import views

submit_patterns = [
    url(r'^(?P<question_id>[0-9]+)$', views.submit, name='q'),
    url(r'^(?P<question_id>[0-9]+)/(?P<answer_id>[0-9]+)$', views.submit, name='a'),
]

urlpatterns = [
    url(r'^submit/', include(submit_patterns, namespace='submit')),
    url(r'^upvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': 1}, name='upvote'),
    url(r'^downvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': -1}, name='downvote'),
]
