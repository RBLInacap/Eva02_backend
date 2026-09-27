from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
	list_display = ("codigo", "fecha", "delegado", "territorio", "tipo_gestion", "estado")
	search_fields = ("codigo", "delegado__nombre", "territorio", "tipo_gestion", "estado")
