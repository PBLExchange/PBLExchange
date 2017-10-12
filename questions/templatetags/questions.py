from django import template
from questions.models import Answer, Comment
from questions.forms import CommentForm

register = template.Library()


@register.inclusion_tag('questions/question_list.html')
def question_list(questions):
    return {'questions': questions}


@register.inclusion_tag('questions/answer_list.html')
def answer_list(question):
    return {
        'answers': Answer.objects.filter(question=question.pk),
        'question': question,
        'comment_form': CommentForm(),
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
def tag_list(question):
    return {
        'tags': question.tags.all()
    }


@register.simple_tag
def display_name(post):
    if post.anonymous:
        return 'anonymous'
    if post.author.get_full_name():
        return post.author.get_full_name()
    return post.author.get_username()
