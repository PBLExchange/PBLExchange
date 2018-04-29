from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404, Http404
from django.contrib.auth.models import User
from .models import Subscription
from .forms import SubscriptionSettingsForm
from pble_questions.models import Category, Tag
from pble_users.models import UserProfile
from pble_questions.models import Question, Answer, Comment
from django.core.mail import send_mail, get_connection, EmailMultiAlternatives
from django.template import loader
from django.contrib.sites.models import Site


# Create your views here.
def categories(request, base_template='pblexchange/base.html', error_message='', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_category_subs = user_sub.categories.order_by('name')
    user_category_nonsubs = Category.objects.all().exclude(name__in=list(user_category_subs)).order_by('name')
    answer_notifications = user_sub.answer_notifications
    comment_notifications = user_sub.comment_notifications
    return render(request, 'subscriptions/category_list.html', {
        'base_template': base_template,
        'sub_categories': user_category_subs,
        'not_sub_categories': user_category_nonsubs,
        'answer_notifications': answer_notifications,
        'comment_notifications': comment_notifications,
        'error_message': error_message,
    })


def tags(request, base_template='pblexchange/base.html', error_message='', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_tag_subs = user_sub.tags.order_by('tag')
    user_tag_nonsubs = Tag.objects.all().exclude(tag__in=list(user_tag_subs)).order_by('tag')
    answer_notifications = user_sub.answer_notifications
    comment_notifications = user_sub.comment_notifications
    return render(request, 'subscriptions/tag_list.html', {
        'base_template': base_template,
        'sub_tags': user_tag_subs,
        'not_sub_tags': user_tag_nonsubs,
        'answer_notifications': answer_notifications,
        'comment_notifications': comment_notifications,
        'error_message': error_message,
    })


def peers(request, base_template='pblexchange/base.html', error_message='', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_users_subs = user_sub.peers.order_by('user__username')
    usrs = UserProfile.objects.all().exclude(user=request.user).\
        exclude(user__in=[u.user for u in user_users_subs]).order_by('user__username')
    answer_notifications = user_sub.answer_notifications
    comment_notifications = user_sub.comment_notifications
    return render(request, 'subscriptions/peer_list.html', {
        'base_template': base_template,
        'sub_users': user_users_subs,
        'not_sub_users': usrs,
        'answer_notifications': answer_notifications,
        'comment_notifications': comment_notifications,
        'error_message': error_message,
    })


# TODO: I assume that all categories, tags, and pble_users have unique names
def alter_categories(request, category_text, **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    category = get_object_or_404(Category, name=category_text)
    user_sub, _ = Subscription.objects.get_or_create(user=request.user)

    if category in user_sub.categories.all():
        user_sub.categories.remove(category)
    else:
        user_sub.categories.add(category)

    user_sub.save()
    return HttpResponseRedirect(reverse('pble_subscriptions:categories'))


def alter_tags(request, tag_text, **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    tag = get_object_or_404(Tag, tag=tag_text)
    user_sub, _ = Subscription.objects.get_or_create(user=request.user)

    if tag in user_sub.tags.all():
        user_sub.tags.remove(tag)
    else:
        user_sub.tags.add(tag)

    user_sub.save()
    return HttpResponseRedirect(reverse('pble_subscriptions:tags'))


def alter_peers(request, username, **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    username_usr = User.objects.get(username=username)

    if request.user != username_usr:
        username_up = UserProfile.objects.get(user=username_usr)
        request_usr__sub, _ = Subscription.objects.get_or_create(user=request.user)

        if username_up in request_usr__sub.peers.all():
            request_usr__sub.peers.remove(username_up)
        else:
            request_usr__sub.peers.add(username_up)
        request_usr__sub.save()

    return HttpResponseRedirect(reverse('pble_subscriptions:peers'))


def alter_subscription_settings(request, form_type=SubscriptionSettingsForm, **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    if request.method == 'POST':
        post_form = form_type(request.POST)
        if post_form.is_valid():
            user_subscription = Subscription.objects.get(user=request.user)
            form_data = post_form.cleaned_data
            user_subscription.answer_notifications = form_data.get('answer_check')
            user_subscription.comment_notifications = form_data.get('comment_check')
            user_subscription.digest = form_data.get('subscription_digest')[0]
            user_subscription.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else: # TODO: is there dynamic way to determine referer association?
            if 'categories' in request.META.get('HTTP_REFERER'):
                return categories(request, 'pblexchange/base.html',
                                  error_message='Input error; subscription and notification settings was not changed')
            elif 'tags' in request.META.get('HTTP_REFERER'):
                return tags(request, 'pblexchange/base.html',
                            error_message='Input error; subscription and notification settings was not changed')
            elif 'peers' in request.META.get('HTTP_REFERER'):
                return peers(request, 'pblexchange/base.html',
                             error_message='Input error; subscription and notification settings was not changed')
    else:
        raise Http404


# Notification methods
# TODO: Consider making these functions use celery task methods for asynchronous behaviour
def send_answer_notification(answer, **kwargs):
    a_author_subscription = Subscription.objects.get(user=answer.question.author)
    if a_author_subscription.answer_notifications and answer.author != answer.question.author:
        current_site = Site.objects.get_current()
        q_url = current_site.domain + reverse('pble_questions:detail', args=(
            answer.question.id,))
        if answer.anonymous:
            a_author = 'anonymous'
        else:
            a_author = answer.author.username

        html_message = loader.render_to_string(
            'subscriptions/answer_notification.html',
            {
                'answer_author': a_author,
                'recipient_username': answer.question.author.username,
                'q_url': q_url,
                'answer_text': answer.body,
                'q_title': answer.question.title
            }
        )

        send_mail('PBL Exchange new answer', '', 'pblexchange@aau.dk', [answer.question.author.email],
                  fail_silently=True, html_message=html_message)


def send_comment_notifications(comment):
    receivers_list = set()
    comments = comment.answer.comment_set.filter(author__subscription__comment_notifications=True, answer=comment.answer) if comment.answer \
        else comment.question.comment_set.filter(author__subscription__comment_notifications=True, answer__isnull=True)
    post_author = comment.answer.author if comment.answer else comment.question.author
    current_site = Site.objects.get_current()
    q_url = current_site.domain + reverse('pble_questions:detail', args=(
        comment.question.id,))

    connection = get_connection()  # uses SMTP server specified in settings.py
    connection.open()  # If you don't open the connection manually, Django will automatically open, then tear down the connection in msg.send()

    for e in comments:
        receivers_list.add(e.author)

    if Subscription.objects.get(user=post_author).comment_notifications:
        receivers_list.add(post_author)

    if comment.anonymous:
        c_author = 'anonymous'
    else:
        c_author = comment.author.username

    for user in receivers_list:
        html_message = loader.render_to_string(
            'subscriptions/comment_notification.html',
            {
                'recipient_username': user.username,
                'q_url': q_url,
                'answer_text': comment.answer.body if comment.answer else '',
                'comment_text': comment.body,
                'q_title': comment.question.title,
                'comment_author': c_author,
            }
        )
        message = EmailMultiAlternatives('PBL Exchange daily digest', '', 'pblexchange@aau.dk', [user.email],
                                         connection=connection)
        message.attach_alternative(html_message, 'text/html')
        message.send()

    connection.close()  # Cleanup
