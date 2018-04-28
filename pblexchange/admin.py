from django.contrib import admin
from .models import ExternalLink, NewsArticle

# Register your models here.
admin.site.register(ExternalLink)
admin.site.register(NewsArticle)
