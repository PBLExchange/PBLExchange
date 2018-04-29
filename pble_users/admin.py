from django.contrib import admin
from .models import UserProfile, UserSetting

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSetting)
