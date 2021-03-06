from django.core.exceptions import ValidationError
from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.utils.translation import check_for_language

from pble_users import models
from pble_users.forms import BonusPointForm
from pblexchange.models import ExternalLink
from PBLExchangeDjango import settings
from .decorators import group_required


# Create your views here.
def users(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'users/user_list.html', {
        'base_template': base_template,
        'userprofiles': models.UserProfile.objects.sorted_score_descending(),
        'link_list': ExternalLink.objects.filter(featured=True), 
    })


def detail(request, user_id, base_template='pblexchange/base.html', **kwargs):
    user_profile = models.UserProfile.objects.get(user=User.objects.get(id=user_id))
    return render(request, 'users/detail.html', {
        'base_template': base_template,
        'user_profile': user_profile
    })


def question_list(request, user_id, questions, title_prefix='', base_template='pblexchange/base.html', **kwargs):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'users/user_questions.html', {
        'base_template': base_template,
        'user_profile': user.userprofile,
        'title': title_prefix + user.get_full_name(),
        'questions': questions(user),
        'link_list': ExternalLink.objects.filter(featured=True),
    })


@group_required()  # Leave blank to only allow admins
def bonus_points(request, user_id, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated() and request.user.is_superuser:
        form = BonusPointForm(request.POST)
        if 'pble_users' in settings.INSTALLED_APPS:
            if form.is_valid():
                target_profile = get_object_or_404(User, pk=user_id).userprofile
                target_profile.points += form.cleaned_data['points']
                target_profile.challenge_points += form.cleaned_data['challenge_points']
                target_profile.save()

                return HttpResponseRedirect(reverse('pble_users:detail', args=(target_profile.user_id,)))
            else:  # TODO: Better error handling
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise Http404("'pble_users' module does not exist under INSTALLED_APPS in settings.py")  # TODO: display a proper error message
    else:
        raise Http404()


def set_language(request, lang_code, **kwargs):
    if request.user.is_authenticated():
        if lang_code and check_for_language(lang_code):
            request.user.usersetting.language = lang_code
            request.user.usersetting.save()
    redirect = request.META.get('HTTP_REFERER')
    if not redirect:
        redirect = reverse('home')
    return HttpResponseRedirect(redirect)
