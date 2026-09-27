# Generada por Django 6.1 el 2026-09-27 a las 03:07.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("monitoreo", "0006_delete_delegado"),
    ]

    operations = [
        migrations.AlterField(
            model_name="delegacion",
            name="codigo",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
