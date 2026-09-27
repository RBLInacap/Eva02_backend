from django.contrib import admin
from .models import Delegado


@admin.register(Delegado)
class DelegadoAdmin(admin.ModelAdmin):
	list_display = ("nombre", "avance_diario", "estado_semaforo")
	search_fields = ("nombre", "estado_semaforo")
