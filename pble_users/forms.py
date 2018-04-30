from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import UserProfile


class BonusPointForm(forms.ModelForm):
    error_css_class = 'error'
#    points = forms.IntegerField(
#        validators=[MinValueValidator(1), MaxValueValidator(500)]
#    )

    class Meta:
        model = UserProfile
        fields = [
            'points',
            'challenge_points'
        ]
