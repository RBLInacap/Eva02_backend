"""Hace obligatorios los campos cargados para metas e indicadores."""

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("solicitudes", "0006_indicador_avance_aprobado_indicador_cumplimiento_and_more"),
	]

	operations = [
		migrations.AlterField(
			model_name="periodo",
			name="nombre",
			field=models.CharField(max_length=100, unique=True),
		),
		migrations.AlterField(
			model_name="periodo",
			name="fecha_inicio",
			field=models.DateField(),
		),
		migrations.AlterField(
			model_name="periodo",
			name="fecha_termino",
			field=models.DateField(),
		),
		migrations.AlterField(
			model_name="meta",
			name="cargo",
			field=models.CharField(max_length=150),
		),
		migrations.AlterField(
			model_name="meta",
			name="valor_objetivo",
			field=models.PositiveSmallIntegerField(),
		),
		migrations.AlterField(
			model_name="meta",
			name="ponderador",
			field=models.DecimalField(decimal_places=2, max_digits=5),
		),
		migrations.AlterField(
			model_name="indicador",
			name="fecha_calculo",
			field=models.DateField(),
		),
		migrations.AlterField(
			model_name="indicador",
			name="avance_aprobado",
			field=models.PositiveSmallIntegerField(),
		),
		migrations.AlterField(
			model_name="indicador",
			name="cumplimiento",
			field=models.DecimalField(decimal_places=2, max_digits=5),
		),
		migrations.AlterField(
			model_name="indicador",
			name="semaforo",
			field=models.CharField(choices=[("Verde", "Verde"), ("Amarillo", "Amarillo"), ("Rojo", "Rojo")], max_length=8),
		),
	]