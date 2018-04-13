from django import forms
from .models import Subscription


class SubscriptionSettingsForm(forms.Form):
    answer_checked = forms.BooleanField(required=True)
    comment_checked = forms.BooleanField(required=True)
    subscription_digest = forms.MultipleChoiceField(choices=Subscription.DIGEST_CHOICES, label="digest choice", required=True)

    class Meta:
        model = Subscription
        fields = [
            'answer_checked',
            'comment_checked',
            'subscription_digest'
        ]