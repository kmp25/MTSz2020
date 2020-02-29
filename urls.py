from django.conf.urls import url
import django.contrib.auth.views
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    url(r'^$', views.kategoria, name='kategoria'),
    url(r'^m/(?P<pid>\d+)$', views.pokazMenu, name='pokazMenu'),
    url(r'^a/(?P<pid>\d+)$', views.pokazArtykul, name='pokazArtykul'),
    url(r'tpay$', views.tpay , name='tpay'),
    url(r'mtsz/(.+)$', views.pliki , name='pliki'),
    url(r'(.+)$', views.brakStrony , name='brakStrony'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



