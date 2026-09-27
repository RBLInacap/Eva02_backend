# Generada por Django 6.1 el 2026-09-27 a las 03:07.

from django.db import migrations, models


def normalizar_datos_existentes(apps, schema_editor):
    Actividad = apps.get_model("solicitudes", "Actividad")
    Compromiso = apps.get_model("solicitudes", "Compromiso")
    Evidencia = apps.get_model("solicitudes", "Evidencia")
    Reporte = apps.get_model("solicitudes", "Reporte")
    base_datos = schema_editor.connection.alias
    estados_validos = {"Ingresado", "En Proceso", "Realizado"}
    conversion_estados = {
        "PENDIENTE": "En Proceso",
        "EN_PROCESO": "En Proceso",
    }

    for actividad in Actividad.objects.using(base_datos).all():
        if not actividad.codigo:
            actividad.codigo = f"ACT-{actividad.pk:06d}"
            actividad.save(using=base_datos, update_fields=("codigo",))

    for compromiso in Compromiso.objects.using(base_datos).all():
        compromiso.estado = conversion_estados.get(compromiso.estado, compromiso.estado)
        if compromiso.estado not in estados_validos:
            raise RuntimeError(
                f"Estado de compromiso desconocido: {compromiso.estado}. "
                "La migración se canceló sin aplicar las restricciones."
            )
        compromiso.save(using=base_datos, update_fields=("estado",))

    for reporte in Reporte.objects.using(base_datos).all():
        if reporte.territorio == "La Florida":
            reporte.territorio = "Sector Rural"
        if reporte.territorio not in {
            "Las Compañías",
            "La Antena",
            "Avenida del Mar",
            "Sector Rural",
        }:
            raise RuntimeError(
                f"Territorio de reporte desconocido: {reporte.territorio}. "
                "La migración se canceló sin aplicar las restricciones."
            )
        if reporte.estado not in estados_validos:
            raise RuntimeError(
                f"Estado de reporte desconocido: {reporte.estado}. "
                "La migración se canceló sin aplicar las restricciones."
            )
        if not reporte.codigo:
            reporte.codigo = f"REP-{reporte.pk:06d}"
        reporte.save(using=base_datos, update_fields=("territorio", "codigo"))

    for evidencia in Evidencia.objects.using(base_datos).all():
        if not evidencia.codigo_verificador:
            evidencia.codigo_verificador = f"EVI-{evidencia.pk:06d}"
            evidencia.save(using=base_datos, update_fields=("codigo_verificador",))


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0007_alter_delegacion_codigo"),
        ("solicitudes", "0004_transfiere_reporte_a_funcionario"),
    ]

    operations = [
        migrations.AddField(
            model_name="actividad",
            name="codigo",
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="actividad",
            name="estado",
            field=models.CharField(choices=[("Ingresado", "Ingresado"), ("En Proceso", "En Proceso"), ("Realizado", "Realizado")], default="Ingresado", max_length=20),
        ),
        migrations.AlterField(
            model_name="compromiso",
            name="estado",
            field=models.CharField(choices=[("Ingresado", "Ingresado"), ("En Proceso", "En Proceso"), ("Realizado", "Realizado")], max_length=20),
        ),
        migrations.AlterField(
            model_name="evidencia",
            name="codigo_verificador",
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="reporte",
            name="codigo",
            field=models.CharField(blank=True, editable=False, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="reporte",
            name="estado",
            field=models.CharField(choices=[("Ingresado", "Ingresado"), ("En Proceso", "En Proceso"), ("Realizado", "Realizado")], max_length=30),
        ),
        migrations.AlterField(
            model_name="reporte",
            name="territorio",
            field=models.CharField(choices=[("Las Compañías", "Las Compañías"), ("La Antena", "La Antena"), ("Avenida del Mar", "Avenida del Mar"), ("Sector Rural", "Sector Rural")], max_length=120),
        ),
        migrations.RunPython(
            normalizar_datos_existentes,
            migrations.RunPython.noop,
        ),
        migrations.AddConstraint(
            model_name="actividad",
            constraint=models.CheckConstraint(condition=models.Q(("estado__in", ("Ingresado", "En Proceso", "Realizado"))), name="actividad_estado_valido"),
        ),
        migrations.AddConstraint(
            model_name="compromiso",
            constraint=models.CheckConstraint(condition=models.Q(("estado__in", ("Ingresado", "En Proceso", "Realizado"))), name="compromiso_estado_valido"),
        ),
        migrations.AddConstraint(
            model_name="reporte",
            constraint=models.CheckConstraint(condition=models.Q(("territorio__in", ("Las Compañías", "La Antena", "Avenida del Mar", "Sector Rural"))), name="reporte_territorio_valido"),
        ),
        migrations.AddConstraint(
            model_name="reporte",
            constraint=models.CheckConstraint(condition=models.Q(("estado__in", ("Ingresado", "En Proceso", "Realizado"))), name="reporte_estado_valido"),
        ),
    ]
