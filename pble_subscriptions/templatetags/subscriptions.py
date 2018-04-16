from django import template
from django.contrib.auth.models import User

from pble_subscriptions.models import Subscription

register = template.Library()


@register.inclusion_tag('subscriptions/digest_options.html')
def digest_options(user_id):
    user_sub = Subscription.objects.get(user_id=user_id)
    return {'current_digest': user_sub.digest}