from django.conf.urls import url, include
from . import views

subscribe_patterns = [
    url(r'category/(?P<category_id>[0-9]+)$', views.alter_categories, name='subscribe_category'),
    url(r'tag/(?P<tag_id>[0-9]+)$', views.alter_tags, name='subscribe_tag'),
    url(r'peer/(?P<userid>[0-9]+)$', views.alter_peers, name='subscribe_peer')
]

urlpatterns = [
    url(r'^categories$', views.categories, name='categories'),
    url(r'^tags$', views.tags, name='tags'),
    url(r'^peers$', views.peers, name='peers'),
    url(r'^alter_subscription/', include(subscribe_patterns)),
    url(r'^alter_subscription_settings', views.alter_subscription_settings, name='alter_subscription_settings'),
]
