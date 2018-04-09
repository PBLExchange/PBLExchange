from django import template
from django.contrib.auth.models import User

from pble_questions.models import Question, Answer, Comment
from pble_questions.forms import CommentForm

register = template.Library()


@register.inclusion_tag('questions/question_list.html')
def question_list(questions):
    return {'questions': questions}


@register.inclusion_tag('questions/answer_list.html', takes_context=True)
def answer_list(context, question):
    return {
        'answers': Answer.objects.sorted(question),
        'accepted': Answer.objects.accepted(question),
        'question': question,
        'comment_form': CommentForm(),
        'user': context['request'].user,
    }


@register.inclusion_tag('questions/comment_list.html')
def comment_list(question, answer=None):
    comments = Comment.objects.filter(question=question.pk)
    if answer:
        comments = comments.filter(answer=answer.pk)
    else:
        comments = comments.filter(answer__isnull=True)
    return {
        'comments': comments,
    }


@register.inclusion_tag('questions/tag_list.html')
def tag_list(question, class_prefix='pble-q-item'):
    return {
        'class_prefix': class_prefix,
        'tags': question.tags.all(),
    }


@register.inclusion_tag('questions/stats.html')
def question_stats():
    return {
        'questions_count': Question.objects.count(),
        'answers_count': Answer.objects.count(),
        'comments_count': Comment.objects.count(),
        'users_count': User.objects.count(),
    }


@register.inclusion_tag('questions/vote.html')
def voting(post):
    post_upvote = 'pble_questions:upvote'
    post_downvote = 'pble_questions:downvote'
    if type(post) is Answer:
        post_upvote = 'pble_questions:answers:upvote'
        post_downvote = 'pble_questions:answers:downvote'
    if type(post) is Comment:
        post_upvote = 'pble_questions:answers:upvote'
        post_downvote = 'pble_questions:answers:downvote'
    return {
        'post': post,
        'post_upvote': post_upvote,
        'post_downvote': post_downvote,
    }


@register.inclusion_tag('questions/meta.html')
def post_meta(post, class_prefix='pble-q-item'):
    what = 'asked'
    if type(post) is Answer:
        what = 'answered'
    return {
        'class_prefix': class_prefix,
        'post': post,
        'what': what,
    }


@register.simple_tag
def display_name(post):
    if post.anonymous:
        return 'anonymous'
    if post.author.get_full_name():
        return post.author.get_full_name()
    return post.author.get_username()
