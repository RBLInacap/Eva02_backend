from django.urls import path
from . import views

urlpatterns = [
    path("", views.inicio_solicitudes, name="inicio_solicitudes"),
    path("lista/", views.lista_actividades, name="lista_actividades"),
    path("evidencias/", views.lista_evidencias, name="lista_evidencias"),
]

