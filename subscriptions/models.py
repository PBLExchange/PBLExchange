from django.db import models
from django.contrib.auth.models import User
from questions.models import Tag, Category
from users.models import UserProfile


# Create your models here.
class Subscription(models.Model):
    user = models.OneToOneField(User, unique=True)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    peers = models.ManyToManyField(UserProfile)
