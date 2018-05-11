from django.conf.urls import url, include
from . import views
from .models import Answer, Comment, AnswerVote, CommentVote
from .forms import AnswerForm, CommentForm


urlpatterns = [
    url(r'^search', views.search, name='search'),
    url(r'^new$', views.new, name='new'),
    url(r'^unanswered$', views.unanswered, name='unanswered'),
    url(r'^hot$', views.hot, name='hot'),
    url(r'^bounties$', views.bounties, name='bounties'),
    url(r'^detail/(?P<question_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^tags$', views.tags, name='tags'),
    url(r'^tags/(?P<tag_text>[a-zA-Z0-9_\-]+)$', views.tag, name='tag'),
    url(r'^categories$', views.categories, name='categories'),
    url(r'^categories/(?P<category_id>[0-9]+)$', views.category, name='category'),
    url(r'^ask', views.ask, name='ask'),
    url(r'^submit$', views.submit, name='submit'),
    url(r'^edit/(?P<post_type>[a-z]+)/(?P<post_id>[0-9]+)$', views.edit, name='edit'),
    url(r'^edit_submit/(?P<post_type>[a-z]+)/(?P<post_id>[0-9]+)$', views.edit_submit, name='edit_submit'),
    url(r'^upvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': 1}, name='upvote'),
    url(r'^downvote/(?P<post_id>[0-9]+)$', views.vote, {'amount': -1}, name='downvote'),

    # Post types
    url(r'^answers/', include('pble_questions.answer_urls', namespace='answers'), {
        'post_type': Answer,
        'form_type': AnswerForm,
        'vote_type': AnswerVote,
    }),
    url(r'^comments/', include('pble_questions.comment_urls', namespace='comments'), {
        'post_type': Comment,
        'form_type': CommentForm,
        'vote_type': CommentVote,
    })
]



