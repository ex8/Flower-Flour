from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.cart_add, name='add'),
    url(r'^add-one/(?P<product_id>\d+)/$', views.cart_add_list, name='add-list'),
    url(r'^remove/(?P<product_id>\d+)/$', views.cart_remove, name='remove'),
]
