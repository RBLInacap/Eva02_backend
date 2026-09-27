# Generada por Django 6.1 el 2026-09-27 a las 02:12.

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0003_rol_alter_delegacion_options_alter_funcionario_email_and_more"),
        ("solicitudes", "0002_actividad_compromiso"),
    ]

    operations = [
        migrations.CreateModel(
            name="Meta",
            fields=[
                ("id_meta", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Periodo",
            fields=[
                ("id_periodo", models.BigAutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name="Solicitante",
            fields=[
                ("id_solicitante", models.BigAutoField(primary_key=True, serialize=False)),
                ("nombre_contacto", models.CharField(max_length=100)),
                ("organizacion", models.CharField(max_length=150)),
                ("telefono", models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterModelOptions(
            name="actividad",
            options={"verbose_name": "Actividad", "verbose_name_plural": "Actividades"},
        ),
        migrations.AddField(
            model_name="actividad",
            name="longitud",
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name="Longitud"),
        ),
        migrations.AlterField(
            model_name="actividad",
            name="latitud_longitud",
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True, verbose_name="Latitud"),
        ),
        migrations.CreateModel(
            name="Evidencia",
            fields=[
                ("id_evidencia", models.BigAutoField(primary_key=True, serialize=False)),
                ("codigo_verificador", models.CharField(max_length=20, unique=True)),
                ("estado", models.CharField(max_length=20)),
                ("observacion", models.TextField()),
                ("archivo", models.FileField(blank=True, upload_to="evidencias/")),
                ("id_actividad", models.ForeignKey(db_column="id_actividad", on_delete=django.db.models.deletion.CASCADE, related_name="evidencias", to="solicitudes.actividad")),
                ("id_verificador", models.ForeignKey(db_column="id_verificador", on_delete=django.db.models.deletion.RESTRICT, related_name="evidencias_verificadas", to="monitoreo.funcionario")),
            ],
        ),
        migrations.CreateModel(
            name="Indicador",
            fields=[
                ("id_indicador", models.BigAutoField(primary_key=True, serialize=False)),
                ("id_meta", models.ForeignKey(db_column="id_meta", on_delete=django.db.models.deletion.CASCADE, related_name="indicadores", to="solicitudes.meta")),
            ],
        ),
        migrations.AddField(
            model_name="meta",
            name="id_periodo",
            field=models.ForeignKey(db_column="id_periodo", on_delete=django.db.models.deletion.RESTRICT, related_name="metas", to="solicitudes.periodo"),
        ),
        migrations.CreateModel(
            name="Solicitante_Actividad",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rol_participacion", models.CharField(max_length=50)),
                ("es_principal", models.BooleanField(default=False)),
                ("id_actividad", models.ForeignKey(db_column="id_actividad", on_delete=django.db.models.deletion.CASCADE, related_name="participaciones_solicitantes", to="solicitudes.actividad")),
                ("id_solicitante", models.ForeignKey(db_column="id_solicitante", on_delete=django.db.models.deletion.CASCADE, related_name="participaciones", to="solicitudes.solicitante")),
            ],
        ),
        migrations.AddField(
            model_name="actividad",
            name="solicitantes",
            field=models.ManyToManyField(related_name="actividades", through="solicitudes.Solicitante_Actividad", to="solicitudes.solicitante"),
        ),
        migrations.AddConstraint(
            model_name="solicitante_actividad",
            constraint=models.UniqueConstraint(fields=("id_solicitante", "id_actividad"), name="unico_solicitante_por_actividad"),
        ),
    ]
