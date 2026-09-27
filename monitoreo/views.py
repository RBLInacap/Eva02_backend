from django.db.models import Q
from django.shortcuts import render

from solicitudes.models import Actividad
from .models import Funcionario, Rol


def panel_monitoreo(solicitud):
    termino_busqueda = solicitud.GET.get("busqueda", "").strip()
    funcionarios = Funcionario.objects.select_related("id_delegacion").all()
    if termino_busqueda:
        funcionarios = funcionarios.filter(
            Q(username__icontains=termino_busqueda)
            | Q(nombre__icontains=termino_busqueda)
            | Q(apellido__icontains=termino_busqueda)
            | Q(id_delegacion__nombre__icontains=termino_busqueda)
            | Q(id_delegacion__codigo__icontains=termino_busqueda)
        )
    return render(
        solicitud,
        "monitoreo.html",
        {"funcionarios": funcionarios, "busqueda": termino_busqueda},
    )


def resumen_monitoreo(solicitud):
    delegados = Funcionario.objects.filter(id_rol__nombre=Rol.Nombre.DELEGADO)
    total_delegados = delegados.count()
    actividades_registradas = Actividad.objects.count()

    if total_delegados == 0:
        evaluacion_global = "Sin datos"
    elif delegados.filter(estado_semaforo=Funcionario.EstadoSemaforo.ROJO).exists():
        evaluacion_global = "Rojo"
    elif delegados.filter(estado_semaforo=Funcionario.EstadoSemaforo.AMARILLO).exists():
        evaluacion_global = "Amarillo"
    else:
        evaluacion_global = "Verde"

    contexto = {
        "delegados": delegados,
        "total_delegados": total_delegados,
        "actividades_registradas": actividades_registradas,
        "evaluacion_global": evaluacion_global,
    }
    return render(solicitud, "resumen.html", contexto)
