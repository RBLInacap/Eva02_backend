from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_solicitudes, name="inicio_solicitudes"),
    path("lista/", views.lista_reportes, name="lista_reportes"),
]

