from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^$', views.order_list, name='list'),
    url(r'^notify/$', views.notify, name='notify'),
    url(r'^custom/$', views.order_custom, name='custom'),
    url(r'^delivery/$', views.order_delivery, name='delivery'),
    url(r'^create/$', views.order_create, name='create')
]
