from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse, reverse, get_object_or_404
from django.contrib.auth.models import User
from users import models
from users.forms import BonusPointForm


# Create your views here.
def users(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'users/user_list.html', {
        'base_template': base_template,
        'userprofiles': models.UserProfile.objects.sorted_score_descending(),
    })


def detail(request, user_id, base_template='pblexchange/base.html', **kwargs):
    user_profile = models.UserProfile.objects.get(user=User.objects.get(id=user_id));
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
    })

def bonus_points(request, bonus_points=0, user_profile=None, form_type=BonusPointForm, base_template='pblexchange/base.html', **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        target_profile = models.UserProfile.objects.get(user=user_profile.user.pk)
        target_profile.points + bonus_points

        return render(request,'users/detail.html', {
            'base_template': base_template,
            'user_profile': user_profile
        })
    else:
        return Http404()
