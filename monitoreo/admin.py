from django.contrib import admin
from .models import Delegacion, Funcionario, Rol


@admin.register(Delegacion)
class AdministradorDelegacion(admin.ModelAdmin):
	list_display = ("id_delegacion", "codigo", "nombre", "activo")
	readonly_fields = ("codigo",)
	list_filter = ("activo",)
	search_fields = ("codigo", "nombre")


@admin.register(Funcionario)
class AdministradorFuncionario(admin.ModelAdmin):
	list_display = (
		"id_funcionario",
		"username",
		"nombre",
		"apellido",
		"email",
		"id_delegacion",
		"id_rol",
		"avance_diario",
		"estado_semaforo",
	)
	search_fields = ("username", "nombre", "apellido", "email", "estado_semaforo")
	list_filter = ("id_delegacion", "id_rol", "estado_semaforo")


@admin.register(Rol)
class AdministradorRol(admin.ModelAdmin):
	list_display = ("id_rol", "nombre", "descripcion")
	search_fields = ("nombre", "descripcion")
