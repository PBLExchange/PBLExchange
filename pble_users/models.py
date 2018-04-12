from django.db import models
from django.contrib.auth.models import User

from django.core.validators import MinValueValidator


# Create your models here.
class UserProfileManager(models.Manager):
    def sorted_score_descending(self):
        return self.all().order_by('-points')


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    points = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=32, default='PBLE-novice')

    objects = UserProfileManager()


class UserSettings(models.Model):
    user = models.OneToOneField(User, unique=True)
    post_notification_enabled = models.BooleanField(default=True)
    subscription_enabled = models.BooleanField(default=True)
