"""PBLExchangeDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^stud/', RedirectView.as_view(url='http://stud.pblexchange.aau.dk/')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^pble_questions/', include('pble_questions.urls', namespace='pble_questions'), {'base_template': 'pblexchange/base.html'}),
    url(r'^pble_users/', include('pble_users.urls', namespace='pble_users'), {'base_template': 'pblexchange/base.html'}),
    url(r'^pble_subscriptions/', include('pble_subscriptions.urls', namespace='pble_subscriptions'), {'base_template': 'pblexchange/base.html'}),
    url(r'^', include('pblexchange.urls')),
]
