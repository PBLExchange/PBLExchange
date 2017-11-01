from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse, reverse, get_object_or_404
from django.contrib.auth.models import User
from users import models


# Create your views here.
def users(request, base_template='pblexchange_base.html', **kwargs):
    return render(request, 'users/user_list.html', {
        'base_template': base_template,
        'users': User.objects.all(),
    })

def detail(request, user_id, base_template='pblexchange_base.html', **kwargs):
    user_profile = models.UserProfile.objects.get(user=User.objects.get(id=user_id));
    return render(request, 'users/detail.html', {
        'base_template': base_template,
        'user_profile': user_profile
    })
