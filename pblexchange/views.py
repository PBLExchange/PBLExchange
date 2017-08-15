from django.shortcuts import render
from .forms import QuestionForm


# Create your views here.
def index(request):
    return render(request, 'pblexchange/base.html')


def ask(request):
    return render(request, 'pblexchange/ask.html', {
        'question': QuestionForm()
    })
