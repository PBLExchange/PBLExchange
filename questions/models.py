from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User


# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length=60)

    def __str__(self):
        return self.tag


class Course(models.Model):
    short_name = models.CharField(max_length=10)
    name = models.CharField(max_length=160)


class Category(models.Model):
    name = models.CharField(max_length=160)


class Post(models.Model):
    class Meta:
        abstract = True
    body = RichTextUploadingField()
    author = models.ForeignKey(User)
    anonymous = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    votes = models.IntegerField(default=0)


class Question(Post):
    title = models.CharField(max_length=160)
    category = models.ForeignKey(Category, null=True, blank=True)
    course = models.ManyToManyField(Course, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Answer(Post):
    question = models.ForeignKey(Question)


class Comment(Post):
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer, null=True)
