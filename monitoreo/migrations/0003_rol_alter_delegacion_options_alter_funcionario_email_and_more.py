# Generada por Django 6.1 el 2026-09-27 a las 02:12.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0002_delegacion_funcionario"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rol",
            fields=[
                ("id_rol", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(choices=[("ADMINISTRADOR", "ADMINISTRADOR"), ("COORDINADOR", "COORDINADOR"), ("DELEGADO", "DELEGADO"), ("FUNCIONARIO", "FUNCIONARIO")], max_length=20, unique=True)),
                ("descripcion", models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name="delegacion",
            options={"verbose_name": "Delegación", "verbose_name_plural": "Delegaciones"},
        ),
        migrations.AlterField(
            model_name="funcionario",
            name="email",
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name="funcionario",
            name="id_rol",
            field=models.ForeignKey(blank=True, db_column="id_rol", null=True, on_delete=django.db.models.deletion.RESTRICT, related_name="funcionarios", to="monitoreo.rol"),
        ),
    ]
