from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from .models import Subscription
from questions.models import Category, Tag
from users.models import UserProfile


# Create your views here.
def categories(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_category_subs = user_sub.categories.order_by('name')
    user_category_nonsubs = Category.objects.all().exclude(name__in=list(user_category_subs)).order_by('name')
    return render(request, 'subscriptions/category_list.html', {
        'base_template': base_template,
        'sub_categories': user_category_subs,
        'not_sub_categories': user_category_nonsubs
    })


def tags(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_tag_subs = user_sub.tags.order_by('tag')
    user_tag_nonsubs = Tag.objects.all().exclude(tag__in=list(user_tag_subs)).order_by('tag')
    return render(request, 'subscriptions/tag_list.html', {
        'base_template': base_template,
        'sub_tags': user_tag_subs,
        'not_sub_tags': user_tag_nonsubs
    })


# TODO: I am not sure using UerProfile instead of User (both in .models and here) is a good idea
def peers(request, base_template='pblexchange/base.html', **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    user_sub, _ = Subscription.objects.get_or_create(user=request.user)
    user_users_subs = user_sub.peers.order_by('username')
    usrs = UserProfile.objects.all()
    return render(request, 'subscriptions/peer_list.html', {
        'base_template': base_template,
        'sub_users': user_users_subs,
        'not_sub_users': usrs
    })


# TODO: I assume that all categories, tags, and users have unique names
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
    # TODO: should we redirect back to overview or keep using meta.referer?
    return HttpResponseRedirect(reverse('categories'))


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
    # TODO: should we redirect back to overview or keep using meta.referer?
    return HttpResponseRedirect(reverse('subscriptions:tags'))


def alter_peers(request, username, **kwargs):
    if not request.user.is_authenticated():
        HttpResponseRedirect(reverse('login'))

    usr = User.objects.get(username=username)
    user_sub, _ = Subscription.objects.get_or_create(user=request.user)

    if usr in user_sub.users.all():
        user_sub.users.remove(usr)
    else:
        user_sub.users.add(usr)
    user_sub.save()
    # TODO: should we redirect back to overview or keep using meta.referer?
    return HttpResponseRedirect(reverse('subscriptions:tags'))