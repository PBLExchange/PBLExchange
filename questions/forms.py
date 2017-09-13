from django import forms
from .models import Question, Answer
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class QuestionForm(forms.ModelForm):
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

    class Meta:
        model = Answer
        fields = [
            'body',
            'anonymous'
        ]
