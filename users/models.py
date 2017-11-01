from django.db import models
from questions import models as questions_models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User, unique=True) #TODO: should this be a OnetoOne or FoerignKey field instead? (django proposes OneToOne)
    points=models.PositiveIntegerField(default=0)
