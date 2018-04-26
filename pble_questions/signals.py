from django.db.models.signals import post_save

from .models import Question, Answer, Comment
from pble_subscriptions.models import QuestionNotification
from pble_subscriptions.views import send_answer_notification, send_comment_notifications
from PBLExchangeDjango.settings import INSTALLED_APPS


def create_notification(sender, instance, created, **kwargs):
    if 'pble_subscriptions' in INSTALLED_APPS:
        if created:
            if isinstance(instance, Question):
                new_question_notification = QuestionNotification(question=instance)
                new_question_notification.save()
            elif isinstance(instance, Answer):
                send_answer_notification(instance)
            elif isinstance(instance, Comment):
                send_comment_notifications(instance)


#post_save.connect(create_notification, sender=Question)
#post_save.connect(create_notification, sender=Answer)
#post_save.connect(create_notification, sender=Comment)
