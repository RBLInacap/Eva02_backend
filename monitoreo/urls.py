from django.urls import path
from . import views

urlpatterns = [
    path("", views.panel_monitoreo, name="panel_monitoreo"),
    path("resumen/", views.resumen_monitoreo, name="resumen_monitoreo"),
]