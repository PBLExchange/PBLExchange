from django.shortcuts import render, HttpResponseRedirect, Http404, reverse, get_object_or_404
from questions.forms import QuestionForm, AnswerForm, CommentForm
from questions.models import Question, Answer, QuestionVote, Tag


# Create your views here.
def new(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': 'new',
        'questions': Question.objects.recent()
    })


def unanswered(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': 'unanswered',
        'questions': Question.objects.unanswered()
    })


def hot(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': 'Popular',
        'questions': Question.objects.hot()
    })


def detail(request, question_id, base_template='pblexchange/base.html', **kwargs):
    question = Question.objects.get(pk=question_id)
    if not question:
        return Http404()
    return render(request, 'questions/detail.html', {
        'base_template': base_template,
        'question': question,
        'answer_form': AnswerForm(),
        'comment_form': CommentForm(),
    })


def ask(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'questions/ask.html', {
        'base_template': base_template,
        'post_form': QuestionForm()
    })


def submit(request, question_id=None, answer_id=None, form_type=QuestionForm, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        post_form = form_type(request.POST)
        post = post_form.save(commit=False)
        post.author = request.user
        is_question = True
        if question_id:
            question = get_object_or_404(Question, pk=question_id)
            post.question = question
            if answer_id:
                answer = get_object_or_404(Answer, pk=answer_id)
                post.answer = answer
            is_question = False
        post.save()
        post_form.save_m2m()  # needed to save many-to-many relations.
        if is_question:
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))
    else:
        return Http404()


def vote(request, post_id, amount, post_type=Question, vote_type=QuestionVote, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    post = get_object_or_404(post_type, pk=post_id)

    prev_vote = vote_type.objects.filter(post=post.pk, user=request.user)

    if not prev_vote or prev_vote.first().vote != amount:
        if amount > 0:
            post.up_votes += amount
        else:
            post.down_votes -= amount
        v,_ = vote_type.objects.get_or_create(user=request.user, post=post)
        v.vote += amount
        v.save()
        post.save()

    if isinstance(post, Question):
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))


def accept_answer(request, post_id, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    post = get_object_or_404(Answer, pk=post_id)
    if Answer.objects.accepted(post.question):
        return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))
    post.accepted = True
    post.save()
    return HttpResponseRedirect(reverse('questions:detail', args=(post.question.pk,)))


def tags(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/tags.html', {
        'base_template': base_template,
        'tags': Tag.objects.all(),
    })


def tag(request, tag_text, base_template='pblexchange/base.html', **kwargs):
    t = get_object_or_404(Tag, tag=tag_text)
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': tag_text.replace('_', ' ').replace('-', ' '),
        'questions': t.question_set.all(),
    })
