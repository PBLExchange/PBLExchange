from django.contrib import admin

from pblexchange.models import MiscContent
from .models import Tag, Question, Answer, Comment, Category, FeaturedCategory

# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(FeaturedCategory)
admin.site.register(MiscContent)
