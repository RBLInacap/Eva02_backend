"""Rutas principales del proyecto."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.urls import include, path

from solicitudes.views import buscar_global

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda solicitud: redirect("inicio_solicitudes"), name="inicio_principal"),
    path("solicitudes/", include("solicitudes.urls")),
    path("monitoreo/", include("monitoreo.urls")),
    path("buscar/", buscar_global, name="buscar_global"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)