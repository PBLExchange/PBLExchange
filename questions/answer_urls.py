from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^submit/(?P<question_id>[0-9]+)$', views.submit, name='submit'),
    url(r'^upvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': 1}, name='upvote'),
    url(r'^downvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': -1}, name='downvote'),
]
