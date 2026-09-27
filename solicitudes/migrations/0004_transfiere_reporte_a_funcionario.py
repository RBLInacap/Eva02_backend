"""Migra las referencias legacy de Reporte a Funcionario sin perder vínculos."""

import unicodedata

import django.db.models.deletion
from django.db import migrations, models


def _normalizar_nombre(nombre):
	texto = unicodedata.normalize("NFKD", nombre)
	return "".join(
		caracter for caracter in texto if not unicodedata.combining(caracter)
	).strip().casefold()


def _buscar_funcionario(Funcionario, nombre):
	funcionarios = {
		_normalizar_nombre(f"{funcionario.nombre} {funcionario.apellido}"): funcionario
		for funcionario in Funcionario.objects.all()
	}
	if _normalizar_nombre(nombre) == "alex diaz":
		return Funcionario.objects.filter(username="adiaz").first()
	return funcionarios.get(_normalizar_nombre(nombre))


def _trasladar_reportes(apps, schema_editor):
	Delegado = apps.get_model("monitoreo", "Delegado")
	Funcionario = apps.get_model("monitoreo", "Funcionario")
	Reporte = apps.get_model("solicitudes", "Reporte")
	base_datos = schema_editor.connection.alias

	for reporte in Reporte.objects.using(base_datos).all():
		delegado = Delegado.objects.using(base_datos).get(pk=reporte.delegado_id)
		funcionario = _buscar_funcionario(Funcionario, delegado.nombre)
		if funcionario is None:
			raise RuntimeError(
				f"No se encontró un funcionario para el delegado {delegado.nombre}. "
				f"El reporte {reporte.codigo} permanece intacto."
			)
		reporte.funcionario_id = funcionario.pk
		reporte.save(using=base_datos, update_fields=("funcionario",))


def _restaurar_reportes(apps, schema_editor):
	Delegado = apps.get_model("monitoreo", "Delegado")
	Reporte = apps.get_model("solicitudes", "Reporte")
	Funcionario = apps.get_model("monitoreo", "Funcionario")
	base_datos = schema_editor.connection.alias

	for reporte in Reporte.objects.using(base_datos).all():
		funcionario = Funcionario.objects.using(base_datos).get(pk=reporte.funcionario_id)
		nombre = (
			"Alex Diaz"
			if funcionario.username == "adiaz"
			else f"{funcionario.nombre} {funcionario.apellido}"
		)
		delegado, _ = Delegado.objects.using(base_datos).get_or_create(
			nombre=nombre,
			defaults={"estado_semaforo": "Verde"},
		)
		reporte.delegado_id = delegado.pk
		reporte.save(using=base_datos, update_fields=("delegado",))


class Migration(migrations.Migration):

	dependencies = [
		("monitoreo", "0005_remove_delegado_avance_diario_and_more"),
		("solicitudes", "0003_meta_periodo_solicitante_alter_actividad_options_and_more"),
	]

	operations = [
		migrations.AlterField(
			model_name="reporte",
			name="delegado",
			field=models.ForeignKey(
				blank=True,
				db_column="delegado_id",
				null=True,
				on_delete=django.db.models.deletion.CASCADE,
				related_name="reportes",
				to="monitoreo.delegado",
			),
		),
		migrations.AddField(
			model_name="reporte",
			name="funcionario",
			field=models.ForeignKey(
				blank=True,
				null=True,
				on_delete=django.db.models.deletion.CASCADE,
				related_name="reportes_legacy",
				to="monitoreo.funcionario",
			),
		),
		migrations.RunPython(_trasladar_reportes, _restaurar_reportes),
		migrations.AlterField(
			model_name="reporte",
			name="funcionario",
			field=models.ForeignKey(
				on_delete=django.db.models.deletion.CASCADE,
				related_name="reportes_legacy",
				to="monitoreo.funcionario",
			),
		),
		migrations.RemoveField(
			model_name="reporte",
			name="delegado",
		),
	]