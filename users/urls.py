from django.conf.urls import url
from . import views
from . import models


urlpatterns = [
    url(r'^$', views.users, name='overview'),
    url(r'^detail/(?P<user_id>[0-9]+$)', views.detail, name='detail')
]
