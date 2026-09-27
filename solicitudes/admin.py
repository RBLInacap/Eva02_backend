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
	search_fields = ("rol_participacion",)


@admin.register(Periodo)
class AdministradorPeriodo(admin.ModelAdmin):
	list_display = ("id_periodo",)


@admin.register(Meta)
class AdministradorMeta(admin.ModelAdmin):
	list_display = ("id_meta", "id_periodo")


@admin.register(Indicador)
class AdministradorIndicador(admin.ModelAdmin):
	list_display = ("id_indicador", "id_meta")


@admin.register(Reporte)
class AdministradorReporte(admin.ModelAdmin):
	list_display = ("codigo", "fecha", "funcionario", "territorio", "tipo_gestion", "estado")
	readonly_fields = ("codigo",)
	search_fields = ("codigo", "funcionario__nombre", "funcionario__apellido", "territorio", "tipo_gestion", "estado")
	list_filter = ("estado", "territorio", "fecha")
