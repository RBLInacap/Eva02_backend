from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Actividad, Evidencia


def lista_actividades(solicitud):
    termino_busqueda = solicitud.GET.get("busqueda", "").strip()
    actividades = Actividad.objects.select_related(
        "id_funcionario",
        "compromiso",
    ).all()
    if termino_busqueda:
        filtros = (
            Q(id_funcionario__username__icontains=termino_busqueda)
            | Q(id_funcionario__nombre__icontains=termino_busqueda)
            | Q(id_funcionario__apellido__icontains=termino_busqueda)
            | Q(actividad_solicitud__icontains=termino_busqueda)
            | Q(compromiso__estado__icontains=termino_busqueda)
            | Q(compromiso__area_apoyo__icontains=termino_busqueda)
        )
        if termino_busqueda.isdigit():
            filtros |= Q(id_actividad=int(termino_busqueda))
        actividades = actividades.filter(filtros)
    return render(
        solicitud,
        "reportes.html",
        {"actividades": actividades, "busqueda": termino_busqueda},
    )


def lista_evidencias(solicitud):
    termino_busqueda = solicitud.GET.get("busqueda", "").strip()
    evidencias = Evidencia.objects.select_related(
        "id_actividad",
        "id_verificador",
    ).all()
    if termino_busqueda:
        evidencias = evidencias.filter(
            Q(codigo_verificador__icontains=termino_busqueda)
            | Q(id_actividad__actividad_solicitud__icontains=termino_busqueda)
            | Q(id_verificador__nombre__icontains=termino_busqueda)
            | Q(id_verificador__apellido__icontains=termino_busqueda)
            | Q(estado__icontains=termino_busqueda)
        )
    return render(
        solicitud,
        "evidencias.html",
        {"evidencias": evidencias, "busqueda": termino_busqueda},
    )


def inicio_solicitudes(solicitud):
    return render(solicitud, "inicio.html")

def buscar_global(solicitud):
    consulta = solicitud.GET.get("busqueda", "").strip().lower()
    
    if "inicio" in consulta:
        return redirect("inicio_solicitudes")
    elif "actividad" in consulta or "solicitud" in consulta or "reporte" in consulta:
        return redirect("lista_actividades")
    elif "evidencia" in consulta:
        return redirect("lista_evidencias")
    elif "monitoreo" in consulta or "metrica" in consulta:
        return redirect("panel_monitoreo")
    elif "resumen" in consulta:
        return redirect("resumen_monitoreo")
    else:
        return render(solicitud, "404.html", status=404)