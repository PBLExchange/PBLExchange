from django import template
from questions.models import Answer, Comment

register = template.Library()


@register.inclusion_tag('questions/question_list.html')
def question_list(questions):
    return {'questions': questions}


@register.inclusion_tag('questions/answer_list.html')
def answer_list(question):
    return {
        'answers': Answer.objects.filter(question=question.pk),
    }


@register.inclusion_tag('questions/comment_list.html')
def comment_list(question, answer=None):
    comments = Comment.objects.filter(question=question.pk)
    if answer:
        comments = comments.filter(answer=answer.pk)
    else:
        comments = comments.filter(answer=None)
    return {
        'answers': comments,
    }
