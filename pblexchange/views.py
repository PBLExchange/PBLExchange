from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from django.utils.translation import ugettext as _
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

