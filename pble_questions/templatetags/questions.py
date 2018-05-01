from django import template
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models import Count
from django.contrib.sites.models import Site
from django.shortcuts import reverse, get_object_or_404

from pble_questions.models import Question, Answer, Comment, Category, FeaturedCategory
from pble_questions.forms import CommentForm, SearchForm
from pble_users.models import UserSetting

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
    what = _('asked')
    if type(post) is Answer:
        what = _('answered')
    return {
        'class_prefix': class_prefix,
        'post': post,
        'what': what,
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


@register.inclusion_tag('questions/categories_list.html')
def categories_list():
    categories = Category.objects.annotate(cardinality=Count('question'))

    return {
        'categories': categories,
    }


# TODO: Make these handle non-existent tables
@register.inclusion_tag('questions/featured_category.html')
def featured_category(user):
    if FeaturedCategory.objects.all().exists():
        featured_cat = FeaturedCategory.objects.all().order_by('-start_date')[0]
        user_setting_lang = get_object_or_404(UserSetting, user=user).language

        if user_setting_lang == 'en':
            return {
                'featured_cat': featured_cat,
                'featured_text': featured_cat.en_text
            }
        elif user_setting_lang == 'da':
            return {
                'featured_cat': featured_cat,
                'featured_text': featured_cat.dk_text
            }
    else:
        return {
            'featured_cat': '',
        }


@register.inclusion_tag('questions/top_challenges.html')
def top_challenges():
    if Question.objects.all():
        top_qc = Question.objects.filter(is_challenge=True).order_by('-created_date')[:8]

        return {
            'top_challenges': top_qc,
        }
    else:
        return {
            'top_challenges': '',
        }
