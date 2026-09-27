from django.db.models import Avg
from django.shortcuts import render

from .models import Delegado


def panel_monitoreo(request):
    personal = Delegado.objects.all()
    return render(request, 'metrica.html', {'personal': personal})


def resumen_monitoreo(request):
    personal = Delegado.objects.all()
    total_delegados = personal.count()
    promedio = personal.aggregate(promedio=Avg('avance_diario'))['promedio']
    avance_promedio = round(promedio) if promedio is not None else 0

    if total_delegados == 0:
        evaluacion_global = 'Sin datos'
    elif personal.filter(estado_semaforo__iexact='rojo').exists():
        evaluacion_global = 'Rojo'
    elif personal.filter(estado_semaforo__iexact='amarillo').exists() or avance_promedio < 80:
        evaluacion_global = 'Amarillo'
    else:
        evaluacion_global = 'Verde'

    contexto = {
        'personal': personal,
        'total_delegados': total_delegados,
        'avance_promedio': avance_promedio,
        'evaluacion_global': evaluacion_global,
    }
    return render(request, 'resumen.html', contexto)
