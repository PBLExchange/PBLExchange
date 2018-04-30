from django import template
from pblexchange.models import Menu
import pblexchange.menu

register = template.Library()


@register.inclusion_tag('pblexchange/menu.html', takes_context=True)
def menu(context):
    return {'menu': Menu.fields, 'user': context['request'].user}
