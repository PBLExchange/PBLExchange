from django import template
from pblexchange.models import Menu

register = template.Library()


@register.inclusion_tag('pblexchange/menu.html')
def menu(user):
    return {'menu': Menu.fields, 'user':user}
