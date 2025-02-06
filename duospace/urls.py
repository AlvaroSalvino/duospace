from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from core.views import *
from perfil.views import *
from vitrine.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('perfil.urls')),
    path('', include('vitrine.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
