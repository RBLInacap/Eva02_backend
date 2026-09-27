import json
import unicodedata

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.dateparse import parse_date

from monitoreo.models import Funcionario
from solicitudes.models import Reporte


class Command(BaseCommand):
    help = "Actualiza funcionarios y reportes desde los archivos JSON locales."

    def handle(self, *args, **options):
        directorio_datos = settings.BASE_DIR / "data"
        registros_delegados = self._leer_lista(
            directorio_datos / "personal.json", "delegados"
        )
        registros_reportes = self._leer_lista(
            directorio_datos / "reportes.json", "reportes"
        )

        cantidad_funcionarios_actualizados = 0
        cantidad_reportes_creados = 0
        cantidad_reportes_actualizados = 0
        cantidad_reportes_omitidos = 0

        with transaction.atomic():
            funcionarios_por_nombre = {
                self._normalizar_nombre(f"{funcionario.nombre} {funcionario.apellido}"): funcionario
                for funcionario in Funcionario.objects.all()
            }
            funcionarios_por_nombre["alex diaz"] = funcionarios_por_nombre.get(
                "alexodro diaz"
            )
            nombres_importados = set()
            for registro in registros_delegados:
                if not isinstance(registro, dict):
                    raise CommandError("Cada funcionario debe estar representado por un objeto JSON.")

                nombre = (registro.get("nombre") or registro.get("funcionario") or "").strip()
                if not nombre:
                    raise CommandError("Hay un funcionario sin nombre en personal.json.")

                estado_semaforo = registro.get(
                    "estado_semaforo", Funcionario.EstadoSemaforo.VERDE
                )
                if estado_semaforo not in Funcionario.EstadoSemaforo.values:
                    raise CommandError(
                        f"El estado de semáforo de {nombre} no es válido."
                    )

                funcionario = funcionarios_por_nombre.get(self._normalizar_nombre(nombre))
                if funcionario is None:
                    raise CommandError(
                        f"No existe un funcionario asociado a {nombre}."
                    )
                nombre_normalizado = self._normalizar_nombre(nombre)
                if nombre_normalizado in nombres_importados:
                    raise CommandError(f"El nombre {nombre} está duplicado en personal.json.")
                nombres_importados.add(nombre_normalizado)
                funcionario.avance_diario = int(registro["avance_diario"])
                funcionario.estado_semaforo = estado_semaforo
                funcionario.save(update_fields=("avance_diario", "estado_semaforo"))
                cantidad_funcionarios_actualizados += 1

            for registro in registros_reportes:
                if not isinstance(registro, dict):
                    raise CommandError("Cada reporte debe estar representado por un objeto JSON.")

                codigo = (registro.get("codigo") or "").strip()
                nombre_funcionario = (
                    registro.get("delegado") or registro.get("responsable") or ""
                ).strip()
                funcionario = funcionarios_por_nombre.get(
                    self._normalizar_nombre(nombre_funcionario)
                )
                if funcionario is None:
                    self.stderr.write(
                        self.style.WARNING(
                            f"Se omitió el reporte {codigo}: no hay un funcionario coincidente "
                            f"para {nombre_funcionario}."
                        )
                    )
                    cantidad_reportes_omitidos += 1
                    continue

                fecha = parse_date(str(registro.get("fecha", "")))
                if fecha is None:
                    raise CommandError(f"La fecha del reporte {codigo} no es válida.")
                if not codigo:
                    raise CommandError("Hay un reporte sin código en reportes.json.")

                reporte, creado = Reporte.objects.update_or_create(
                    codigo=codigo,
                    defaults={
                        "fecha": fecha,
                        "territorio": self._normalizar_territorio(
                            registro.get("territorio", "")
                        ),
                        "tipo_gestion": registro.get("tipo_gestion", ""),
                        "estado": registro.get("estado", ""),
                        "funcionario": funcionario,
                    },
                )
                if creado:
                    cantidad_reportes_creados += 1
                else:
                    cantidad_reportes_actualizados += 1

        self.stdout.write(
            self.style.SUCCESS(
                "Importación terminada: "
                f"{cantidad_funcionarios_actualizados} funcionarios actualizados; "
                f"{cantidad_reportes_creados} reportes creados, "
                f"{cantidad_reportes_actualizados} actualizados y "
                f"{cantidad_reportes_omitidos} omitidos por falta de coincidencia."
            )
        )

    @staticmethod
    def _normalizar_nombre(nombre):
        nombre_sin_acentos = unicodedata.normalize("NFKD", nombre)
        return "".join(
            caracter
            for caracter in nombre_sin_acentos
            if not unicodedata.combining(caracter)
        ).strip().casefold()

    @staticmethod
    def _normalizar_territorio(territorio):
        if territorio == "La Florida":
            return "Sector Rural"
        return territorio

    @staticmethod
    def _leer_lista(ruta, tipo_registros):
        try:
            with ruta.open("r", encoding="utf-8") as archivo:
                registros = json.load(archivo)
        except (OSError, json.JSONDecodeError) as error:
            raise CommandError(f"No se pudieron leer los {tipo_registros}: {error}") from error

        if not isinstance(registros, list):
            raise CommandError(f"El archivo de {tipo_registros} debe contener una lista JSON.")
        return registros