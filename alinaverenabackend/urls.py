from alinaverenabackend import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from alinaverenaapi.views import ReactRoute

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinaverenaapi.urls')),
    path('', ReactRoute.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)