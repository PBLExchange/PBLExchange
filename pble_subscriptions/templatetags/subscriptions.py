from django import template
from django.contrib.sites.models import Site
from django.shortcuts import reverse
from django.contrib.auth.models import User

from pble_subscriptions.models import Subscription

register = template.Library()


@register.inclusion_tag('subscriptions/digest_options.html')
def digest_options(user_id):
    user_sub = Subscription.objects.get(user_id=user_id)
    return {'current_digest': user_sub.digest}


@register.inclusion_tag('subscriptions/question_href.html')
def question_url(question):
    current_site = Site.objects.get_current()
    q_url = current_site.domain + reverse('pble_questions:detail', args=(
        question.id,))
    return {'q_url': q_url,
            'q_title': question.title,
            }