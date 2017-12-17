from django import template
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from itertools import chain, count as it_count
from django.contrib.auth.models import User

from users.models import UserProfile
from questions.models import *

register = template.Library()

@register.simple_tag
def get_user(user, anonymous=False):
    if anonymous:
        return 'anonymous'
    name = user.get_username()
    if user.get_full_name():
        name = user.get_full_name()
    return mark_safe('<a href="' + reverse('users:detail', args=(user.pk,)) + '" class="pble-user-link">'
                     + name + '</a>')

@register.simple_tag
def userprofile_get_user(userprofile):
    full_name = userprofile.user.get_username()
    if userprofile.user.get_full_name():
        full_name = userprofile.user.get_full_name()
    return mark_safe('<a href="' + reverse('users:detail', args=(userprofile.user.pk,)) + '" class="pble-user-link">'
                     + full_name + '</a>')

@register.simple_tag
def user_questions_quantity(user):
    return Question.objects.filter(author=user.pk).count()

@register.simple_tag
def user_comments_quantity(user):
    return Comment.objects.filter(author=user.pk).count()

@register.simple_tag
def user_question_votes(user):
    return QuestionVote.objects.filter(post__author=user.pk).count()

@register.simple_tag
def user_answer_votes(user):
    return AnswerVote.objects.filter(post__author=user.pk).count()

@register.simple_tag
def user_accepted_answers(user):
    return Question.objects.filter(author=user.pk, answer__accepted=True).count()

@register.simple_tag
def user_answers(user):
    return Answer.objects.filter(author=user.pk).count()

@register.simple_tag
def user_answers_chosen(user):
    return Answer.objects.filter(author=user.pk, accepted=True).count()

@register.simple_tag
def user_upvotes_given(user):
    return QuestionVote.objects.filter(user=user.pk, vote__gt=0).count() + \
                         AnswerVote.objects.filter(user=user.pk, vote__gt=0).count() + \
                         CommentVote.objects.filter(user=user.pk, vote__gt=0).count()

@register.simple_tag
def user_downvotes_given(user):
    return QuestionVote.objects.filter(user=user.pk, vote__lt=0).count() + \
                         AnswerVote.objects.filter(user=user.pk, vote__lt=0).count() + \
                         CommentVote.objects.filter(user=user.pk, vote__lt=0).count()
@register.simple_tag
def user_upvotes_received(user):
    return QuestionVote.objects.filter(post__author=user.pk, vote__gt=0).count() + \
                         AnswerVote.objects.filter(post__author=user.pk, vote__gt=0).count() + \
                         CommentVote.objects.filter(post__author=user.pk, vote__gt=0).count()

@register.simple_tag
def user_downvotes_received(user):
    return QuestionVote.objects.filter(post__author=user.pk, vote__lt=0).count() + \
                         AnswerVote.objects.filter(post__author=user.pk, vote__lt=0).count() + \
                         CommentVote.objects.filter(post__author=user.pk, vote__lt=0).count()

@register.filter(name='get_rank')
def get_user_rank(val, user_points):
    return UserProfile.objects.filter(points__gte=user_points).count()
