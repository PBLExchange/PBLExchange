from django.conf.urls import url
from . import views
from django_cas_ng import views as cas_views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', cas_views.login, name='login'),
    url(r'^logout/$', cas_views.logout, name='logout'),
    url(r'^about/$', views.about, name='about'),
    #  News article urls TODO: use include
    url(r'^news_article/(?P<news_article_id>[0-9]+)$', views.news_article, name='news_article'),
    url(r'^news_article/write', views.write_article, name='news_article_write'),
    url(r'^news_article/submit$', views.submit_article, name='news_article_submit'),
]
