from django.contrib import admin
from .models import Subscription, QuestionNotification

# Register your models here.
admin.site.register(Subscription)
admin.site.register(QuestionNotification)
