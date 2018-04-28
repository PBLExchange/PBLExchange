import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import NewsArticle
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsArticleForm(forms.ModelForm):
    #tags = forms.CharField(required=False)
    #prefix = 'question'

    class Meta:
        model = NewsArticle
        fields = [
            'headline',
            'lead',
            'body',
            'start_date',
            'end_date'
        ]
