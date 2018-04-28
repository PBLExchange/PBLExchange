from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group

from django.core.validators import MinValueValidator

from PBLExchangeDjango import settings


# Create your models here.
class UserProfileManager(models.Manager):
    def sorted_score_descending(self):
        return self.all().order_by('-points')


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    points = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    title = models.CharField(max_length=32, default=settings.PBLE_GROUPS[0][0])  # By default join "lowest" user group

    objects = UserProfileManager()

    def save(self, *args, **kw):
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        if old and old.points != self.points:
            for k, v in reversed(settings.PBLE_GROUPS):
                if self.points >= v:
                    self.user.groups.clear()  # TODO: should the user belong to one or multiple groups?
                    k_group = Group.objects.get(name=k)
                    k_group.user_set.add(self.user)
                    self.title = k
                    break
        super(UserProfile, self).save(*args, **kw)


class UserSetting(models.Model):
    user = models.OneToOneField(User, unique=True)
    post_notification_enabled = models.BooleanField(default=True)
    subscription_enabled = models.BooleanField(default=True)
    language = models.CharField(verbose_name=_('language'), max_length=4, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE)
