from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse, reverse, get_object_or_404
from django.contrib.auth.models import User
from pble_users import models
from pble_users.forms import BonusPointForm
from pble_questions.models import Vote, QuestionVote, CommentVote, AnswerVote

from PBLExchangeDjango import settings #TODO: Am i checking if app exists correctly?


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


def bonus_points(request, user_id, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        form = BonusPointForm(request.POST)
        if 'pble_users' in settings.INSTALLED_APPS:
            if form.is_valid():
                target_profile = get_object_or_404(User, pk=user_id).userprofile
                target_profile.points += form.cleaned_data['points']
                target_profile.save()

                return HttpResponseRedirect(reverse('pble_users:detail', args=(target_profile.user_id,)))
            else:  # TODO: Better error handling
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            raise Http404("'pble_users' module does not exist under INSTALLED_APPS in settings.py")  # TODO: display a proper error message
    else:
        raise Http404()
