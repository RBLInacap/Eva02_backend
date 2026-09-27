# Generada por Django 6.1 el 2026-09-27 a las 01:58.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0002_delegacion_funcionario"),
        ("solicitudes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Actividad",
            fields=[
                ("id_actividad", models.BigAutoField(primary_key=True, serialize=False)),
                ("fecha_actividad", models.DateField()),
                ("actividad_solicitud", models.CharField(max_length=255)),
                ("accion_ejecutada", models.TextField()),
                ("latitud_longitud", models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ("id_funcionario", models.ForeignKey(db_column="id_funcionario", on_delete=django.db.models.deletion.CASCADE, related_name="actividades", to="monitoreo.funcionario")),
            ],
        ),
        migrations.CreateModel(
            name="Compromiso",
            fields=[
                ("id_compromiso", models.BigAutoField(primary_key=True, serialize=False)),
                ("descripcion", models.TextField()),
                ("fecha_comprometida", models.DateField()),
                ("area_apoyo", models.CharField(max_length=100)),
                ("estado", models.CharField(max_length=20)),
                ("id_actividad", models.OneToOneField(db_column="id_actividad", on_delete=django.db.models.deletion.CASCADE, related_name="compromiso", to="solicitudes.actividad")),
            ],
        ),
    ]
