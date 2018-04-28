from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from django.utils.translation import ugettext as _, check_for_language
from pble_questions.models import Question
from .models import ExternalLink, NewsArticle


# Create your views here.
def index(request):
    return render(request, 'questions/list.html', {
        'base_template': 'pblexchange/base.html',
        'title': _('questions'),
        'questions': Question.objects.recent(),
        'link_list': ExternalLink.objects.filter(featured=True),
    })


def news_article(request, news_article_id):
    if not request.user.is_authenticated():
        reverse('login')

    na = NewsArticle.objects.get(pk=news_article_id)
    return render(request, 'pblexchange/news_article.html', {
        'base_template': 'pblexchange/base.html',
        'headline': na.headline,
        'lead': na.lead,
        'body': na.body,
    })
