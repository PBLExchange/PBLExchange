from django.db.models import Count
from django.shortcuts import render, HttpResponseRedirect, Http404, reverse, get_object_or_404
from django.utils.translation import ugettext as _
from pble_questions.forms import QuestionForm, AnswerForm, CommentForm, SearchForm
from pble_questions.models import Question, Answer, QuestionVote, Tag, Category
from PBLExchangeDjango import settings
from pble_users.points import post_vote, answer_accept, post_bounty


# Create your views here.
def new(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': _('new'),
        'questions': Question.objects.recent(),
    })


def unanswered(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': _('unanswered'),
        'questions': Question.objects.unanswered(),
    })


def hot(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': _('popular'),
        'questions': Question.objects.hot(),
    })


def bounties(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/list.html', {
        'base_template': base_template,
        'title': _('bounty questions'),
        'questions': Question.objects.filter(bounty__gt=0).order_by('-created_date'),
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
    form = QuestionForm()
    if request.user.userprofile.challenge_points < 1:
        del form.fields['challenge']
    return render(request, 'questions/ask.html', {
        'base_template': base_template,
        'post_form': form,
    })


def submit(request, question_id=None, answer_id=None, form_type=QuestionForm, **kwargs):
    if request.method == 'POST' and request.user.is_authenticated():
        post_form = form_type(request.POST)
        if request.user.userprofile.challenge_points < 1 and isinstance(post_form, QuestionForm):
            del post_form.fields['challenge']
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
        if is_question and 'pble_users' in settings.INSTALLED_APPS:
            post_bounty(
                request.user,
                post,
                post_form.cleaned_data['bounty'],
                post_form.cleaned_data['challenge'] if request.user.userprofile.challenge_points > 0 else 0
            )
        post.save()
        post_form.save_m2m()  # needed to save many-to-many relations.
        if is_question:
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('pble_questions:detail', args=(post.question.pk,)))
    else:
        return Http404()


def vote(request, post_id, amount, post_type=Question, vote_type=QuestionVote, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    post = get_object_or_404(post_type, pk=post_id)
    prev_vote = vote_type.objects.filter(post=post.pk, user=request.user)

    if not prev_vote or prev_vote.first().vote != amount:
        if 'pble_users' in settings.INSTALLED_APPS:
            post_vote(request.user, post, vote_type, amount)
        else:
            raise Http404("'pble_users' module does not exist under INSTALLED_APPS in settings.py")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def accept_answer(request, post_id, **kwargs):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    post = get_object_or_404(Answer, pk=post_id)

    if not Answer.objects.accepted(post.question) or (Answer.objects.accepted(post.question) and post.accepted):
        if 'pble_users' in settings.INSTALLED_APPS:
            # Assign points and set post.accepted
            answer_accept(request.user, post)
        else:
            raise Http404("'pble_users' module does not exist under INSTALLED_APPS in settings.py")

        post.accepted = not post.accepted
        post.save()

    return HttpResponseRedirect(reverse('pble_questions:detail', args=(post.question.pk,)))


def tags(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/tags.html', {
        'base_template': base_template,
        'tags': Tag.objects.annotate(cardinality=Count('question')).order_by('-cardinality'),
    })


def tag(request, tag_text, base_template='pblexchange/base.html', **kwargs):
    t = get_object_or_404(Tag, tag=tag_text)
    return render(request, 'questions/questions.html', {
        'base_template': base_template,
        'title': tag_text,
        'questions': t.question_set.order_by('-created_date'),
    })


def categories(request, base_template='pblexchange/base.html', **kwargs):
    return render(request, 'questions/categories.html', {
        'base_template': base_template,
        'title': _('Categories'),
        'categories': Category.objects.all(),
    })


def category(request, category_id, base_template='pblexchange/base.html', **kwargs):
    cat = get_object_or_404(Category, id=category_id)
    return render(request, 'questions/category.html', {
        'base_template': base_template,
        'title': cat.name,
        'questions': cat.question_set.order_by('-created_date'),
    })


def search(request, base_template='pblexchange/base.html', **kwargs):
    query = SearchForm(request.GET)
    if query.is_valid():
        q = query.cleaned_data['q']
    else:
        q = ''
    questions = Question.objects.query(q)
    return render(request, 'questions/search.html', {
        'base_template': base_template,
        'questions': questions,
    })
