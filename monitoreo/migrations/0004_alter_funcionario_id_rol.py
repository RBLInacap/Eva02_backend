# Generada para hacer obligatorio el rol después de cargar los funcionarios iniciales.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		("monitoreo", "0003_rol_alter_delegacion_options_alter_funcionario_email_and_more"),
	]

	operations = [
		migrations.AlterField(
			model_name="funcionario",
			name="id_rol",
			field=models.ForeignKey(
				db_column="id_rol",
				on_delete=django.db.models.deletion.RESTRICT,
				related_name="funcionarios",
				to="monitoreo.rol",
			),
		),
	]