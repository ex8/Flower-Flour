from django.conf.urls import url
from clover import views


urlpatterns = [
    url(regex=r'^$', view=views.authorize, name='auth'),
    url(regex=r'^oauth_callback/$', view=views.oauth_callback, name='oauth_callback'),
]
