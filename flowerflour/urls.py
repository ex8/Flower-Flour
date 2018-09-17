from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^',include('main.urls', namespace='main')),
    url(r'^menu/',include('menu.urls', namespace='menu')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^order/', include('orders.urls', namespace='order')),
    url(r'^custom-cakes/', include('custom_cakes.urls', namespace='custom-cake')),
    url(r'^clover/', include('clover.urls', namespace='clover')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
