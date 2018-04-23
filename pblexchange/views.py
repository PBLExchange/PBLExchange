from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from django.utils.translation import ugettext as _, check_for_language
from pble_questions.models import Question
from .models import ExternalLink


# Create your views here.
def index(request):
    return render(request, 'questions/list.html', {
        'base_template': 'pblexchange/base.html',
        'title': _('questions'),
        'questions': Question.objects.recent(),
        'link_list': ExternalLink.objects.filter(featured=True),
    })


def set_language(request, lang_code):
    if request.user.is_authenticated():
        if lang_code and check_for_language(lang_code):
            request.user.usersettings.language = lang_code
            request.user.usersettings.save()
    redirect = request.META.get('HTTP_REFERER')
    if not redirect:
        redirect = reverse('home')
    return HttpResponseRedirect(redirect)
