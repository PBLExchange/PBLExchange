from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models import Count
from django.utils import timezone
from django.shortcuts import reverse, get_object_or_404

from pble_questions.models import Question, Answer, Comment, Category, FeaturedCategory
from pble_questions.forms import CommentForm, SearchForm
from pble_users.models import UserSetting

register = template.Library()


@register.inclusion_tag('questions/question_list.html', takes_context=True)
def question_list(context, questions):
    return {
        'questions': questions,
        'request': context['request']
    }


@register.inclusion_tag('questions/answer_list.html', takes_context=True)
def answer_list(context, question):
    return {
        'answers': Answer.objects.sorted(question),
        'accepted': Answer.objects.accepted(question),
        'question': question,
        'comment_form': CommentForm(),
        'user': context['request'].user,
    }


@register.inclusion_tag('questions/comment_list.html', takes_context=True)
def comment_list(context, question, answer=None):
    comments = Comment.objects.filter(question=question.pk)
    if answer:
        comments = comments.filter(answer=answer.pk)
    else:
        comments = comments.filter(answer__isnull=True)
    try:
        user = context['request'].user
    except KeyError:
        user = context['user']
    return {
        'comments': comments,
        'user': user
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


@register.inclusion_tag('questions/meta.html', takes_context=True)
def post_meta(context, post, class_prefix='pble-q-item'):
    what = _('asked')
    if type(post) is Answer:
        what = _('answered')

    try:
        user = context['request'].user
    except KeyError:
        user = context['user']
    return {
        'class_prefix': class_prefix,
        'post': post,
        'what': what,
        'user': user
    }


@register.simple_tag
def display_name(post):
    if post.anonymous:
        return _('anonymous')
    if post.author.get_full_name():
        return post.author.get_full_name()
    return post.author.get_username()


@register.inclusion_tag('questions/search_tag.html')
def question_search():
    return {
        'form': SearchForm()
    }


@register.inclusion_tag('questions/categories_list.html', takes_context=True)
def categories_list(context):
    categories = Category.objects.annotate(cardinality=Count('question'))
    return {
        'categories': categories,
        'user': context['request'].user
    }


@register.inclusion_tag('questions/featured_category.html', takes_context=True)
def featured_category(context):
    if FeaturedCategory.objects.filter(start_date__lte=timezone.now()).exists():
        featured_cat = FeaturedCategory.objects.filter(start_date__lte=timezone.now()).order_by('-start_date')[0]
        user_setting_lang = get_object_or_404(UserSetting, user=context['request'].user).language

        if user_setting_lang == 'en':
            return {
                'featured_cat': featured_cat,
                'featured_text': featured_cat.en_text,
                'user': context['request'].user,
            }
        elif user_setting_lang == 'da':
            return {
                'featured_cat': featured_cat,
                'featured_text': featured_cat.da_text,
                'user': context['request'].user,
            }
    else:
        return {
            'featured_cat': '',
        }


@register.inclusion_tag('questions/top_challenges.html')
def top_challenges():
    if Question.objects.all():
        top_qc = Question.objects.active_bounties()[:5]

        return {
            'top_challenges': top_qc,
        }
    else:
        return {
            'top_challenges': '',
        }


@register.simple_tag(takes_context=True)
def get_category_name(context, category):
    return category.user_get_i18n_name(context['user'])


@register.simple_tag(takes_context=True)
def get_category_description(context, category):
    return ''
