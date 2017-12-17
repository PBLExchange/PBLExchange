from django import forms
from django.core.validators import MinValueValidator

from .models import UserProfile, User

class BonusPointForm(forms.ModelForm):
    points = forms.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )