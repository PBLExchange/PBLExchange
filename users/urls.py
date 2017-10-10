from django.conf.urls import url
from . import views
from . import models


urlpatterns = [
    url(r'^users', views.users(), name='overview')
]