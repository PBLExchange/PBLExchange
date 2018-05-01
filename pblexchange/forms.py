from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import NewsArticle
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.admin import widgets


class DateInput(forms.DateInput):
    input = 'date'


class NewsArticleForm(forms.ModelForm):
    lead = forms.CharField(widget=forms.Textarea, label=_('lead'))
    body = forms.CharField(widget=CKEditorUploadingWidget(), label=_('body'))

    class Meta:
        model = NewsArticle
        fields = [
            'headline',
            'lead',
            'body',
            'start_date',
            'end_date'
        ]
        widgets = {'headline': forms.TextInput(attrs={'size': 80})}
        # TODO: Formatting of forms is best handled in CSS
