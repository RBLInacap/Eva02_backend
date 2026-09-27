"""Elimina Delegado después de trasladar sus datos y referencias."""

from django.db import migrations


class Migration(migrations.Migration):

	dependencies = [
		("monitoreo", "0005_remove_delegado_avance_diario_and_more"),
		("solicitudes", "0004_transfiere_reporte_a_funcionario"),
	]

	operations = [
		migrations.DeleteModel(name="Delegado"),
	]