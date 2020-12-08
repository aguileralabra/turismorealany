from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from aplicacion import views
from django.urls import reverse_lazy
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', include('aplicacion.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)