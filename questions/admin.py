from django.contrib import admin
from .models import Tag, Question, Comment, Category

# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Category)