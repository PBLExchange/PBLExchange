from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def get_user(user, anonymous=False):
    if anonymous:
        return 'anonymous'
    name = user.get_username()
    if user.get_full_name():
        name = user.get_full_name()
    return mark_safe('<a href="' + reverse('users:detail', args=(user.pk,)) + '" class="pble-user-link">'
                     + name + '</a>')

@register.simple_tag
def userprofile_get_user(userprofile):
    full_name = userprofile.user.get_username()
    if userprofile.user.get_full_name():
        full_name = userprofile.user.get_full_name()
    return mark_safe('<a href="' + reverse('users:detail', args=(userprofile.user.pk,)) + '" class="pble-user-link">'
                     + full_name + '</a>')


#@register.filter
#def sort_score_descending(users_list):
#    return sorted(users_list, key=lambda user: getattr(user.userprofile, 'points'));
