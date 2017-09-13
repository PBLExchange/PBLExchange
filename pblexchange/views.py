from django.shortcuts import render, HttpResponseRedirect, Http404, reverse
from questions.forms import QuestionForm
from questions.models import Question


# Create your views here.
def index(request):
    return render(request, 'pblexchange/base.html', {
        'questions': Question.objects.all(),
    })

