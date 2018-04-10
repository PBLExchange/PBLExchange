from datetime import timedelta

from django.db.models.functions import Coalesce
from django.utils import timezone
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db.models import F, Count, Value, Sum
# Imports for Answer.save overwrite
from PBLExchangeDjango.settings import INSTALLED_APPS
from django.apps import apps
from django.contrib.sites.models import Site
from django.template import loader
from django.core.mail import send_mail
from django.shortcuts import reverse


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=60)

    def __str__(self):
        return self.tag


class Course(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=160)


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
    name = models.CharField(max_length=160)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        abstract = True

    body = RichTextUploadingField()
    author = models.ForeignKey(User)
    anonymous = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body


class QuestionManager(models.Manager):
    def unanswered(self):
        return self.recent().filter(answer=None)

    def recent(self):
        return self.order_by('-created_date')

    def hot(self):
        one_day_ago = timezone.now() - timedelta(days=1)
        return self.annotate(
            hotness=
            Count(F('answer'))
            + Count(F('comment'))
            + Count(F('questionvote'))
            + Count(F('answer__answervote'))
            + Count(F('comment__commentvote'))
        ).order_by('-hotness')

    def by_user(self, user):
        return self.recent().filter(author=user.pk, anonymous=False)

    def unanswered_by_user(self, user):
        return self.by_user(user).filter(answer=None)

    def answered_by_user(self, user):
        return self.recent().filter(answer__author=user, answer__anonymous=False).distinct()


class Question(Post):
    title = models.CharField(max_length=160)
    category = models.ForeignKey(Category, null=True, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = QuestionManager()

    @property
    def votes(self):
        return self.questionvote_set.aggregate(Sum('vote'))['vote__sum'] or 0

    def __str__(self):
        return self.title


class AnswerManager(models.Manager):
    def accepted(self, question):
        return self.filter(question=question.pk, accepted=True).count() > 0

    def sorted(self, question):
        return self.filter(question=question.pk).annotate(votes_sum=Coalesce(Sum('answervote__vote'), 0)).order_by('-accepted', F('votes_sum').desc())


class Answer(Post):
    question = models.ForeignKey(Question)
    accepted = models.BooleanField(default=False)

    objects = AnswerManager()

    @property
    def votes(self):
        return self.answervote_set.aggregate(Sum('vote'))['vote__sum'] or 0

    def save(self, *args, **kw):    # OBS: See signals used for emailing under signals.py
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        super(Answer, self).save(*args, **kw)
        if 'pble_subscriptions' in INSTALLED_APPS:
            if old and old.accepted != self.accepted:  # accepted has changed, notify author
                m = apps.get_model('pble_subscriptions', 'Subscription')
                if m.answer_notifications and m.user != self.author:
                    current_site = Site.objects.get_current()
                    q_url = current_site.domain + reverse('pble_questions:detail', args=(
                        self.question.id,))  # TODO: On release set django_site domain field to pblexchange.aau.dk

                    accept_action = ''
                    if self.accepted:
                        accept_action = 'accepted'
                    else:
                        accept_action = 'unaccepted'

                    html_message = loader.render_to_string(
                        'subscriptions/accepted_notification.html',
                        {
                            'recipient_username': self.author.username,
                            'q_url': q_url,
                            'question_author': self.question.author.username,
                            'q_title': self.question.title,
                            'accept_action': accept_action,
                        }
                    )
                    send_mail('PBL Exchange new answer', '', 'pblexchange@aau.dk', [self.question.author.email],
                              fail_silently=True, html_message=html_message)


class Comment(Post):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True)

    @property
    def votes(self):
        return self.commentvote_set.aggregate(Sum('vote'))['vote__sum'] or 0


class Vote(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(User)
    vote = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post)
    date = models.DateTimeField(auto_now=True)


class QuestionVote(Vote):
    post = models.ForeignKey(Question)


class AnswerVote(Vote):
    post = models.ForeignKey(Answer)


class CommentVote(Vote):
    post = models.ForeignKey(Comment)
