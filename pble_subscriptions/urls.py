from django.conf.urls import url, include
from . import views

subscribe_patterns = [
    url(r'category/(?P<category_text>[a-zA-Z0-9_\-]+)$', views.alter_categories, name='subscribe_category'),
    url(r'tag/(?P<tag_text>[a-zA-Z0-9_\-]+)$', views.alter_tags, name='subscribe_tag'),
    url(r'peer/(?P<username>[a-zA-Z0-9_\-]+)$', views.alter_peers, name='subscribe_peer')   # TODO: Use uid instead of username
]
# TODO: these urls and views should use the pk of the respective items

urlpatterns = [
    url(r'^categories$', views.categories, name='categories'),
    url(r'^tags$', views.tags, name='tags'),
    url(r'^peers$', views.peers, name='peers'),
    url(r'^alter_subscription/', include(subscribe_patterns)),
    url(r'^alter_subscription_settings', views.alter_subscription_settings, name='alter_subscription_settings'),
]
