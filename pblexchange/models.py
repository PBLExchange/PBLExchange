from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=60)


class Course(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=160)


class Category(models.Model):
    name = models.CharField(max_length=160)


class Question(models.Model):
    title = models.CharField(max_length=160)
    category = models.ForeignKey(Category)
    course = models.ManyToManyField(Course)
    body = RichTextField()
    author = models.ForeignKey(User)
    anonymous = models.BooleanField()
    tags = models.ManyToManyField(Tag)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    votes = models.IntegerField()

