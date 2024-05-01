from django.views.generic import TemplateView
from alinaverenabackend import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from alinaverenaapi.views import ReactRoute

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('alinaverenaapi.urls')),
    path('heels/', TemplateView.as_view(template_name="index.html")),
    path('product/<id>', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="index.html")),
    # re_path(r'^.*$', TemplateView.as_view(template_name="index.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)