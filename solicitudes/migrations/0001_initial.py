# Generada por Django 6.1 el 2026-09-27 a las 00:19.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("monitoreo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Reporte",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(max_length=20, unique=True)),
                ("fecha", models.DateField()),
                ("territorio", models.CharField(max_length=120)),
                ("tipo_gestion", models.CharField(max_length=150)),
                ("estado", models.CharField(max_length=30)),
                ("delegado", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reportes", to="monitoreo.delegado")),
            ],
        ),
    ]
