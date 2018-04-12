from django.contrib import admin
from .models import Subscription, Notification, QuestionNotification, AnswerNotification, CommentNotification

# Register your models here.
admin.site.register(Subscription)
admin.site.register(QuestionNotification)
admin.site.register(AnswerNotification)
admin.site.register(CommentNotification)
