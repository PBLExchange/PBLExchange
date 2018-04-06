from django.db.models.signals import post_save
from django.core.mail import send_mail

from .models import Question, Answer, Comment


def create_notification(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Question):
            #send_mail('PBL Exchange subscription notification', 'Title:' + instance.title + '\nauthor: ' + instance.author.username, 'pblexchange@aau.dk', ['gblegm13@student.aau.dk'])
            print('TODO!!')
        elif isinstance(instance, Answer):
            print('TODO!!')
        elif isinstance(instance, Comment):
            print('TODO!!')


post_save.connect(create_notification, sender=Question)
post_save.connect(create_notification, sender=Answer)
post_save.connect(create_notification, sender=Comment)
