from django import template
from django.utils import timezone
from django.contrib.sites.models import Site
from django.shortcuts import reverse
from pblexchange.models import NewsArticle

register = template.Library()


@register.inclusion_tag('pblexchange/news_articles.html')
def news_articles():
    now = timezone.now().date()
    return {'news_articles': NewsArticle.objects.filter(start_date__lte=now, end_date__gt=now).order_by('-start_date')}


@register.inclusion_tag('pblexchange/news_article_href.html')
def news_article_url(news_article):
    current_site = Site.objects.get_current()
    na_url = current_site.domain + reverse('news_article', args=(
        news_article.id,))
    return {'na_url': na_url,
            'na_headline': news_article.headline,
            }
