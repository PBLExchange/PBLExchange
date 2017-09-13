from django import template
from questions.models import Answer

register = template.Library()


@register.inclusion_tag('questions/question_list.html')
def question_list(questions):
    return {'questions': questions}


@register.inclusion_tag('questions/answer_list.html')
def answer_list(question):
    return {
        'answers': Answer.objects.filter(question=question.pk),
    }
