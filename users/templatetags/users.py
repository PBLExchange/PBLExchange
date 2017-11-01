from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

register = template.Library()


# @register.inclusion_tag('users/user_list.html')
# def user_list(users):
#     return {'users': users}
#
#
# @register.inclusion_tag('users/detail.html')
# def detail(user_profile):
#     return {'user_profile': user_profile}


@register.simple_tag
def get_user(user, anonymous=False):
    if anonymous:
        return 'anonymous'
    name = user.get_username()
    if user.get_full_name():
        name = user.get_full_name()
    return mark_safe('<a href="' + reverse('users:detail', args=(user.pk,)) + '">' + name + '</a>')
