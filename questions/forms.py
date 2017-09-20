from django import forms
from .models import Question, Answer, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class QuestionForm(forms.ModelForm):
    prefix = 'question'

    class Meta:
        model = Question
        fields = [
            'title',
            'body',
            'anonymous',
            'tags',
        ]


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
