"""
URL configuration for munilaaserena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from solicitudes.views import buscar_global

urlpatterns = [
    # Redirige la página principal (http://127.0.0.1:8000/) al inicio de solicitudes
    path("", lambda request: redirect("inicio_solicitudes"), name="home"),
    
    # Rutas de tus aplicaciones
    path("solicitudes/", include("solicitudes.urls")),
    path("monitoreo/", include("monitoreo.urls")),
    path("buscar/", buscar_global, name="buscar_global"),
]   