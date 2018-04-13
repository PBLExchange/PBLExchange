from django.db import models
from django.core.validators import URLValidator
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
