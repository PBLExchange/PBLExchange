from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from django.utils.translation import ugettext as _, check_for_language
from django.shortcuts import get_object_or_404
from pble_questions.models import Question
from .models import ExternalLink, NewsArticle
from .forms import NewsArticleForm
from django.core.exceptions import PermissionDenied


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
        'news_article': na,
    })


def write_article(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'pblexchange/write_news_article.html', {
            'base_template': base_template,
            'post_form': NewsArticleForm(),
            'error_msg': '',
        })
    else:
        raise PermissionDenied


def submit_article(request, form_type=NewsArticleForm, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        if request.user.is_staff or request.user.is_superuser:
            post_form = form_type(request.POST)
            if post_form.is_valid():
                new_na = post_form.save(commit=False)
                new_na.author = request.user
                new_na.save()
                return HttpResponseRedirect(reverse('news_article', args=(new_na.pk,)))
            else:
                return render(request, 'pblexchange/write_news_article.html', {
                    'base_template': 'pblexchange/base.html',
                    'post_form': post_form,
                })
        else:
            raise PermissionDenied
    else:
        return Http404()


def about(request):
    if not request.user.is_authenticated():
        reverse('login')

    return render(request, 'pblexchange/about.html', {
        'base_template': 'pblexchange/base.html'
    })
