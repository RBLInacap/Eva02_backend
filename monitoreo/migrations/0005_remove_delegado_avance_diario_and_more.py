"""Traslada las métricas de Delegado a Funcionario antes de retirar la tabla."""

import unicodedata

import django.db.models.deletion
from django.db import migrations, models


def _normalizar_nombre(nombre):
    texto = unicodedata.normalize("NFKD", nombre)
    return "".join(
        caracter for caracter in texto if not unicodedata.combining(caracter)
    ).strip().casefold()


def _buscar_funcionario(Funcionario, nombre):
    funcionarios = {
        _normalizar_nombre(f"{funcionario.nombre} {funcionario.apellido}"): funcionario
        for funcionario in Funcionario.objects.all()
    }
    if _normalizar_nombre(nombre) == "alex diaz":
        return Funcionario.objects.filter(username="adiaz").first()
    return funcionarios.get(_normalizar_nombre(nombre))


def _trasladar_metricas(apps, schema_editor):
    Delegado = apps.get_model("monitoreo", "Delegado")
    Funcionario = apps.get_model("monitoreo", "Funcionario")
    base_datos = schema_editor.connection.alias

    for delegado in Delegado.objects.using(base_datos).all():
        funcionario = _buscar_funcionario(Funcionario, delegado.nombre)
        if funcionario is None:
            raise RuntimeError(
                f"No se encontró un funcionario para el delegado {delegado.nombre}. "
                "No se eliminaron sus datos."
            )
        funcionario.avance_diario = delegado.avance_diario
        funcionario.estado_semaforo = delegado.estado_semaforo
        funcionario.save(using=base_datos, update_fields=("avance_diario", "estado_semaforo"))


def _restaurar_metricas(apps, schema_editor):
    Delegado = apps.get_model("monitoreo", "Delegado")
    Funcionario = apps.get_model("monitoreo", "Funcionario")
    base_datos = schema_editor.connection.alias

    for funcionario in Funcionario.objects.using(base_datos).exclude(
        avance_diario__isnull=True, estado_semaforo__isnull=True
    ):
        nombre = (
            "Alex Diaz"
            if funcionario.username == "adiaz"
            else f"{funcionario.nombre} {funcionario.apellido}"
        )
        delegado, _ = Delegado.objects.using(base_datos).get_or_create(
            nombre=nombre,
            defaults={
                "avance_diario": funcionario.avance_diario or 0,
                "estado_semaforo": funcionario.estado_semaforo or "Verde",
            },
        )
        delegado.avance_diario = funcionario.avance_diario or 0
        delegado.estado_semaforo = funcionario.estado_semaforo or "Verde"
        delegado.save(using=base_datos, update_fields=("avance_diario", "estado_semaforo"))


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0004_alter_funcionario_id_rol"),
    ]

    operations = [
        migrations.AddField(
            model_name="funcionario",
            name="avance_diario",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="funcionario",
            name="estado_semaforo",
            field=models.CharField(
                blank=True,
                choices=[("Verde", "Verde"), ("Amarillo", "Amarillo"), ("Rojo", "Rojo")],
                max_length=8,
                null=True,
            ),
        ),
        migrations.RunPython(_trasladar_metricas, _restaurar_metricas),
        migrations.RemoveField(
            model_name="delegado",
            name="avance_diario",
        ),
        migrations.AlterField(
            model_name="delegacion",
            name="codigo",
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]
