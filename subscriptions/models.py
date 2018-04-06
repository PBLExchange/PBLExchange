from django.db import models
from django.contrib.auth.models import User
from questions.models import Question, Answer, Comment, Category, Tag
from users.models import UserProfile


# Create your models here.
class Subscription(models.Model):
    NEVER = 'NEVER'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    DIGEST_CHOICES = ((NEVER, 'Never'), (DAILY, 'Daily'), (WEEKLY, 'Weekly'))

    user = models.OneToOneField(User, unique=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    peers = models.ManyToManyField(UserProfile)
    answer_notifications = models.BooleanField(default=True)
    comment_notifications = models.BooleanField(default=True)
    digest = models.CharField(max_length=6, choices=DIGEST_CHOICES, default=DAILY)


class Notification(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(auto_now_add=True)
    #delivered = models.BooleanField(default=False)


class QuestionNotification(Notification):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class AnswerNotification(Notification):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class CommentNotification(Notification):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
