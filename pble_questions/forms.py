import re

from django import forms

from .models import Question, Answer, Comment, Tag
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False)
    prefix = 'question'

    class Meta:
        model = Question
        fields = [
            'title',
            'body',
            'anonymous',
            'tags',
        ]

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
    body = forms.CharField(label='Answer', widget=CKEditorUploadingWidget())
    prefix = 'answer'

    class Meta:
        model = Answer
        fields = [
            'body',
            'anonymous'
        ]


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='Comment', widget=None)
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
