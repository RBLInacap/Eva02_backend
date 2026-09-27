# Generada por Django 6.1 el 2026-09-27 a las 01:58.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Delegacion",
            fields=[
                ("id_delegacion", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("codigo", models.CharField(max_length=10, unique=True)),
                ("direccion", models.CharField(blank=True, max_length=255, null=True)),
                ("activo", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Funcionario",
            fields=[
                ("id_funcionario", models.BigAutoField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=150, unique=True)),
                ("nombre", models.CharField(max_length=100)),
                ("apellido", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("id_delegacion", models.ForeignKey(blank=True, db_column="id_delegacion", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="funcionarios", to="monitoreo.delegacion")),
            ],
        ),
    ]
