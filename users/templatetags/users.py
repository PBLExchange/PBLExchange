from django import template

register = template.Library()


@register.inclusion_tag('users/user_list.html')
def user_list(users):
    return {'users': users}

@register.inclusion_tag('users/detail.html')
def detail(user_profile):
    return {'user_profile': user_profile}
