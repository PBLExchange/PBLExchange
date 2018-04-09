from django.db.models.signals import post_save
from django.shortcuts import reverse
from django.core.mail import send_mail
from django.template import loader

from .models import Question, Answer, Comment
from pble_subscriptions.models import Subscription, QuestionNotification
from PBLExchangeDjango.settings import INSTALLED_APPS


def create_notification(sender, instance, created, **kwargs):
    if created and 'pble_subscriptions' in INSTALLED_APPS:
        if isinstance(instance, Question):
            print('TODO:Q!!')
            new_question_notification = QuestionNotification(question=instance)
            new_question_notification.save()
        elif isinstance(instance, Answer):
            # TODO: Do not send notifications whn user accepts hers/his own answer
            q_author_subscription = Subscription.objects.get(user=instance.question.author)
            if q_author_subscription.answer_notifications:
                q_url = reverse('pble_questions:detail', args=(instance.question.id,))
                html_message = loader.render_to_string(
                    'questions/answer_notification.html',
                    {
                        'answer_author': instance.author.username,
                        'recipient_username': instance.question.author.username,
                        'q_url': q_url,
                        'answer_text': instance.body, # TODO: This body contains html p tags by default, remove them
                        'q_title': instance.question.title
                    }
                )
                send_mail('PBL Exchange new answer', '', 'pblexchange@aau.dk', [instance.question.author.email], fail_silently=True, html_message=html_message)
                #send_mail('PBL Exchange answer notification', 'Title:' + instance.title + '\nauthor: ' + instance.author.username + , 'pblexchange@aau.dk', [instance.question.author.email])
        elif isinstance(instance, Comment):
            # send_mail('PBL Exchange subscription notification', 'Title:' + instance.title + '\nauthor: ' + instance.author.username, 'pblexchange@aau.dk', ['gblegm13@student.aau.dk'])
            print('TODO:C!!')


post_save.connect(create_notification, sender=Question)
post_save.connect(create_notification, sender=Answer)
post_save.connect(create_notification, sender=Comment)
