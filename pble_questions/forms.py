import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Question, Answer, Comment, Tag, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class QuestionForm(forms.ModelForm):
    # TODO: Formatting of forms is best handled in CSS
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': 40}),
                           help_text=_('Tags are comma separated<br><br>'))
    challenge = forms.IntegerField(min_value=0, initial=0)
    prefix = 'question'

    class Meta:
        model = Question
        fields = [
            'title',
            'category',
            'body',
            'bounty',
            'challenge',
            'anonymous',
            'tags',
        ]
        widgets = {'title': forms.TextInput(attrs={'size': 80})}
        # TODO: Formatting of forms is best handled in CSS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Category.objects.count() < 1:
            del self.fields['category']
        else:
            self.fields['category'].empty_label = None

    def clean_tags(self):
        # Removes all spaces in the string (tags cannot contain spaces),
        # replace æøå with normal letters, and splits on ','
        tag_strings = re.sub('[\s+]', '', self.cleaned_data['tags']).lower().replace('æ', 'ae').replace('ø', 'oe')\
            .replace('å', 'aa').split(',')
        tags = []
        for t in tag_strings:
            if t == '':
                continue
            tag, _ = Tag.objects.get_or_create(tag=t)
            tags.append(tag)
        return tags


class AnswerForm(forms.ModelForm):
    body = forms.CharField(label=_('Answer'), widget=CKEditorUploadingWidget())
    prefix = 'answer'

    class Meta:
        model = Answer
        fields = [
            'body',
            'anonymous'
        ]


class CommentForm(forms.ModelForm):
    body = forms.CharField(label=_('Comment'), widget=None)
    prefix = 'comment'

    class Meta:
        model = Comment
        fields = [
            'body',
            'anonymous'
        ]


class SearchForm(forms.Form):
    q = forms.CharField()

    class Meta:
        fields = [
            'q'
        ]
