import json
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404

def lista_reportes(request):
    # Ruta al archivo reportes.json
    ruta_json = os.path.join(settings.BASE_DIR, "data", "reportes.json")
    
    with open(ruta_json, "r", encoding="utf-8") as f:
        reportes = json.load(f)
        
    return render(request, "reportes.html", {"reportes": reportes})

def inicio_solicitudes(request):
    return render(request, "inicio.html")

def buscar_global(request):
    query = request.GET.get("q", "").strip().lower()
    
    if "inicio" in query:
        return redirect("inicio_solicitudes")
    elif "reporte" in query or "solicitud" in query:
        return redirect("lista_reportes")
    elif "monitoreo" in query or "metrica" in query:
        return redirect("panel_monitoreo")
    elif "resumen" in query:
        return redirect("resumen_monitoreo")
    else:
        return render(request, "404.html", status=404)