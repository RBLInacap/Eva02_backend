from django.contrib import admin
from .models import (
	Actividad,
	Compromiso,
	Evidencia,
	Indicador,
	Meta,
	Periodo,
	Reporte,
	Solicitante,
	Solicitante_Actividad,
)


@admin.register(Actividad)
class AdministradorActividad(admin.ModelAdmin):
	list_display = (
		"codigo",
		"fecha_actividad",
		"id_funcionario",
		"actividad_solicitud",
		"estado",
	)
	readonly_fields = ("codigo",)
	search_fields = (
		"codigo",
		"actividad_solicitud",
		"accion_ejecutada",
		"id_funcionario__username",
	)
	list_filter = ("estado", "fecha_actividad")


@admin.register(Compromiso)
class AdministradorCompromiso(admin.ModelAdmin):
	list_display = (
		"id_compromiso",
		"id_actividad",
		"fecha_comprometida",
		"area_apoyo",
		"estado",
	)
	search_fields = ("descripcion", "area_apoyo", "estado")
	list_filter = ("estado", "fecha_comprometida", "area_apoyo")


@admin.register(Evidencia)
class AdministradorEvidencia(admin.ModelAdmin):
	list_display = ("codigo_verificador", "id_actividad", "id_verificador", "estado")
	readonly_fields = ("codigo_verificador",)
	search_fields = ("codigo_verificador", "observacion", "id_verificador__username")
	list_filter = ("estado", "id_actividad")


@admin.register(Solicitante)
class AdministradorSolicitante(admin.ModelAdmin):
	list_display = ("nombre_contacto", "organizacion", "telefono")
	search_fields = ("nombre_contacto", "organizacion", "telefono")


@admin.register(Solicitante_Actividad)
class AdministradorParticipacion(admin.ModelAdmin):
	list_display = ("id_solicitante", "id_actividad", "rol_participacion", "es_principal")
	search_fields = (
		"rol_participacion",
		"id_solicitante__nombre_contacto",
		"id_solicitante__organizacion",
		"id_actividad__codigo",
		"id_actividad__actividad_solicitud",
	)
	list_filter = ("rol_participacion", "es_principal", "id_actividad")


@admin.register(Periodo)
class AdministradorPeriodo(admin.ModelAdmin):
	list_display = ("id_periodo", "nombre", "fecha_inicio", "fecha_termino")
	search_fields = ("nombre", "=id_periodo")
	list_filter = ("fecha_inicio", "fecha_termino")


@admin.register(Meta)
class AdministradorMeta(admin.ModelAdmin):
	list_display = ("id_meta", "cargo", "id_periodo", "valor_objetivo", "ponderador")
	search_fields = ("cargo", "=id_meta", "id_periodo__nombre")
	list_filter = ("id_periodo",)


@admin.register(Indicador)
class AdministradorIndicador(admin.ModelAdmin):
	list_display = (
		"id_indicador",
		"id_meta",
		"fecha_calculo",
		"avance_aprobado",
		"cumplimiento",
		"semaforo",
	)
	search_fields = ("=id_indicador", "id_meta__cargo")
	list_filter = ("fecha_calculo", "semaforo", "id_meta")


@admin.register(Reporte)
class AdministradorReporte(admin.ModelAdmin):
	list_display = ("codigo", "fecha", "funcionario", "territorio", "tipo_gestion", "estado")
	readonly_fields = ("codigo",)
	search_fields = ("codigo", "funcionario__nombre", "funcionario__apellido", "territorio", "tipo_gestion", "estado")
	list_filter = ("estado", "territorio", "fecha")
