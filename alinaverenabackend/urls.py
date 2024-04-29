from django.views.generic import TemplateView
from alinaverenabackend import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from alinaverenaapi.views import ReactRoute

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinaverenaapi.urls')),
    # re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)