from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import QuestionForm
from .models import Question


# Create your views here.
def index(request):
    return render(request, 'pblexchange/base.html', {
        'questions': Question.objects.all()
    })


def ask(request):
    return render(request, 'pblexchange/ask.html', {
        'question': QuestionForm()
    })


def upvote(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question:
        question.votes += 1
        question.save()
    return HttpResponseRedirect(reverse('home'))

def downvote(request, question_id):
    question = Question.objects.get(pk=question_id)
    if question:
        question.votes -= 1
        question.save()
    return HttpResponseRedirect(reverse('home'))
