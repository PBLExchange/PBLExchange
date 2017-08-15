from django.contrib import admin
from .models import Tag, Question


# Register your models here.
admin.site.register(Tag)
admin.site.register(Question)
