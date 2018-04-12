from django.contrib import admin
from .models import UserProfile, UserSettings

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSettings)
