from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Question, Answer, Comment
from subscriptions.views import post_notification


@receiver(post_save, sender=Question)
def send_notifications(sender, instance, created, **kwargs):
    print('Q saved!!')
    if created:
        post_notification(instance)


@receiver(post_save, sender=Answer)
def send_notifications(sender, instance, created, **kwargs):
    print('A saved!!')
    if created:
        post_notification(instance)


@receiver(post_save, sender=Comment)
def send_notifications(sender, instance, created, **kwargs):
    if created:
        print('C saved!!')
        post_notification(instance)

# @receiver(post_save, sender=Question)
# def save_user_profile(sender, instance, **kwargs):
    # TODO: should we notify users when edits happen? if so, do it here.
