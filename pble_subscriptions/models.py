from django.db import models
from django.contrib.auth.models import User
from pble_questions.models import Question
from pble_users.models import UserProfile


# Create your models here.
class Subscription(models.Model):
    NEVER = 'NEVER'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    DIGEST_CHOICES = ((NEVER, 'Never'), (DAILY, 'Daily'), (WEEKLY, 'Weekly'))

    user = models.OneToOneField(User, unique=True)
    categories = models.ManyToManyField('pble_questions.Category')
    tags = models.ManyToManyField('pble_questions.Tag')
    peers = models.ManyToManyField(UserProfile)
    answer_notifications = models.BooleanField(default=True)
    comment_notifications = models.BooleanField(default=False)
    digest = models.CharField(max_length=6, choices=DIGEST_CHOICES, default=NEVER)


class Notification(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True)


class QuestionNotification(Notification):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
