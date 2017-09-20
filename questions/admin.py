from django.contrib import admin
from .models import Tag, Question, Comment

# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Comment)
