# Generada por Django 6.1 el 2026-09-27 a las 03:28.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("solicitudes", "0005_actividad_codigo_actividad_estado_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="indicador",
            name="avance_aprobado",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="indicador",
            name="cumplimiento",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name="indicador",
            name="fecha_calculo",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="indicador",
            name="semaforo",
            field=models.CharField(blank=True, choices=[("Verde", "Verde"), ("Amarillo", "Amarillo"), ("Rojo", "Rojo")], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name="meta",
            name="cargo",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="meta",
            name="ponderador",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name="meta",
            name="valor_objetivo",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="periodo",
            name="fecha_inicio",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="periodo",
            name="fecha_termino",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="periodo",
            name="nombre",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddConstraint(
            model_name="indicador",
            constraint=models.UniqueConstraint(fields=("id_meta", "fecha_calculo"), name="indicador_unico_por_meta_y_fecha"),
        ),
        migrations.AddConstraint(
            model_name="indicador",
            constraint=models.CheckConstraint(condition=models.Q(("semaforo__in", ("Verde", "Amarillo", "Rojo"))), name="indicador_semaforo_valido"),
        ),
        migrations.AddConstraint(
            model_name="meta",
            constraint=models.UniqueConstraint(fields=("id_periodo", "cargo"), name="meta_unica_por_periodo_y_cargo"),
        ),
        migrations.AddConstraint(
            model_name="periodo",
            constraint=models.CheckConstraint(condition=models.Q(("fecha_termino__gte", models.F("fecha_inicio"))), name="periodo_fechas_validas"),
        ),
    ]
