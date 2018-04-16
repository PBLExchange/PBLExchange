from django import forms
from .models import Subscription


class SubscriptionSettingsForm(forms.Form):
    answer_check = forms.BooleanField(required=False)
    comment_check = forms.BooleanField(required=False)
    subscription_digest = forms.MultipleChoiceField(choices=Subscription.DIGEST_CHOICES, label="digest choice", required=True)

    class Meta:
        model = Subscription
        fields = [
            'answer_check',
            'comment_check',
            'subscription_digest'
        ]