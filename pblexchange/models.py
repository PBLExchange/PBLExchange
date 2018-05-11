from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from PBLExchangeDjango import settings


# Create your models here.
class MenuField:
    def __init__(self, title, lookup):
        self.title = title
        self.lookup = lookup


class Menu:
    fields = []

    @classmethod
    def register(cls, title, lookup):
        cls.fields.append(MenuField(title, lookup))


class Setting(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=128)

    @staticmethod
    def get(name: str):
        try:
            value = Setting.objects.get(name=name)
            return value.value
        except Setting.DoesNotExist:
            return settings.PBLE_DEFAULT_SETTINGS[name]

    @staticmethod
    def set(name: str, value: str):
        obj, _ = Setting.objects.get_or_create(name=name)
        obj.value = value
        obj.save()


class ExternalLink(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, unique=True)
    url = models.URLField(validators=[URLValidator], unique=True)
    featured = models.BooleanField(default=True)

    def __str__(self):
        return self.title


def delta_now():
    return timezone.now()+timedelta(days=14)


class NewsArticle(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User)
    headline = models.CharField(verbose_name=_('headline'), max_length=128)
    lead = models.CharField(verbose_name=_('lead'), max_length=512, blank=True)
    body = RichTextUploadingField(verbose_name=_('body'))
    start_date = models.DateField(verbose_name=_('start date'), default=timezone.now)
    end_date = models.DateField(verbose_name=_('end date'), default=delta_now)

    def save(self, *args, **kw):
        if self.start_date > self.end_date:  # TODO: Better error handling than throwing and not handling an exception
            raise ValidationError('start_date must be before end_date')
        else:
            super(NewsArticle, self).save(*args, **kw)

    def __str__(self):
        return self.headline


class MiscContent(models.Model):
    en_title = models.CharField(max_length=160)
    da_title = models.CharField(max_length=160)
    en_content = RichTextUploadingField()
    da_content = RichTextUploadingField()

    def __str(self):
        return self.en_title
