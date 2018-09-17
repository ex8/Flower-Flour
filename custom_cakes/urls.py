from django.conf.urls import url
from custom_cakes import views

urlpatterns = [
    url(r'^$', views.gallery_list, name='list'),
    url(r'^(?P<id>\d+)/$', view=views.gallery_detail, name='detail'),
]
