from django.conf.urls import url
from menu import views


urlpatterns = [
    url(regex=r'^$', view=views.menu_list, name='list'),
    url(regex=r'^(?P<category_slug>[-\w]+)/$', view=views.menu_list, 
    name='menu_list_by_category'),
    url(regex=r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', view=views.menu_detail, 
    name='menu_detail'),
]
