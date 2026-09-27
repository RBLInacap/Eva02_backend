# Generada por Django 6.1 el 2026-09-27 a las 00:19.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name="Delegado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150)),
                ("avance_diario", models.PositiveSmallIntegerField()),
                ("estado_semaforo", models.CharField(max_length=20)),
            ],
        ),
    ]
