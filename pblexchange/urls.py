from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^upvote/(?P<question_id>[0-9]+)$', views.upvote, name='upvote'),
    url(r'^downvote/(?P<question_id>[0-9]+)$', views.downvote, name='downvote'),
]
