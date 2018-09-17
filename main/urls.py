from django.conf.urls import url
from main import views

urlpatterns = [
    url(regex=r'^$', view=views.home, name='home'),
    url(regex=r'^about/$', view=views.about, name='about'),
    url(regex=r'^delivery/$', view=views.delivery, name='delivery'),
    url(regex=r'^contact/$', view=views.contact, name='contact'),
]
