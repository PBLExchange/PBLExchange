from django.shortcuts import render, HttpResponseRedirect, Http404, reverse, get_object_or_404
from questions.forms import QuestionForm, AnswerForm
from questions.models import Question


# Create your views here.
def detail(request, question_id, base_template='pblexchange/base.html', **kwargs):
    question = Question.objects.get(pk=question_id)
    if not question:
        return Http404()
    return render(request, 'questions/detail.html', {
        'base_template': base_template,
        'question': question,
        'answer_form': AnswerForm(),
    })


def ask(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'questions/ask.html', {
        'base_template': base_template,
        'post_form': QuestionForm()
    })


def submit(request, form_type=QuestionForm, question_id=None, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        post = form_type(request.POST)
        post = post.save(commit=False)
        post.author = request.user
        is_question = True
        if question_id:
            question = get_object_or_404(Question, pk=question_id)
            post.question = question
            is_question = False
        post.save()
        if is_question:
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))
    else:
        return Http404()


def vote(request, post_id, amount, post_type=Question, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    post = post_type.objects.get(pk=post_id)
    if post:
        post.votes += amount
        post.save()

    if isinstance(post, Question):
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))
