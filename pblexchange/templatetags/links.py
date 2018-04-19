from django import template
from pblexchange.models import ExternalLink

register = template.Library()


@register.inclusion_tag('pblexchange/links.html')
def links():
    return {'link_list': ExternalLink.objects.filter(featured=True)}
