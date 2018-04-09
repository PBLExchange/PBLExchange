from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from pble_questions.models import Question


# Create your views here.
def index(request):
    return render(request, 'questions/list.html', {
        'base_template': 'pblexchange/base.html',
        'title': 'questions',
        'questions': Question.objects.recent(),
    })

