from django.contrib import admin
from .models import Tag, Question, Answer, Comment, Category

# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Category)
