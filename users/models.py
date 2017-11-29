from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfileManager(models.Manager):
    def sorted_score_descending(self):
        return UserProfile.objects.all().order_by('-points')

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    points = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=32, default='PBLE-novice')

    objects = UserProfileManager()
