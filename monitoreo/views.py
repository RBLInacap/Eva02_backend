import json
import os

from django.conf import settings
from django.shortcuts import render


def _leer_personal():
    ruta_json = os.path.join(settings.BASE_DIR, 'data', 'personal.json')
    with open(ruta_json, 'r', encoding='utf-8') as f:
        return json.load(f)


def panel_monitoreo(request):
    personal = _leer_personal()
    return render(request, 'metrica.html', {'personal': personal})


def resumen_monitoreo(request):
    personal = _leer_personal()

    total_funcionarios = len(personal)
    avances = [item.get('avance_diario', 0) for item in personal]
    avance_promedio = round(sum(avances) / total_funcionarios) if total_funcionarios else 0

    if total_funcionarios == 0:
        evaluacion_global = 'Sin datos'
    else:
        semaforos = [item.get('estado_semaforo', '').lower() for item in personal]
        if any(semaforo == 'rojo' for semaforo in semaforos):
            evaluacion_global = 'Rojo'
        elif any(semaforo == 'amarillo' for semaforo in semaforos) or avance_promedio < 80:
            evaluacion_global = 'Amarillo'
        else:
            evaluacion_global = 'Verde'

    contexto = {
        'personal': personal,
        'total_funcionarios': total_funcionarios,
        'avance_promedio': avance_promedio,
        'evaluacion_global': evaluacion_global,
    }
    return render(request, 'resumen.html', contexto)
