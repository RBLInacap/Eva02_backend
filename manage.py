#!/usr/bin/env python
"""Herramienta de línea de comandos para administrar el proyecto."""
import os
import sys


def main():
    """Ejecuta los comandos de administración de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "munilaaserena.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. Comprueba que esté instalado, "
            "disponible en PYTHONPATH y que el entorno virtual esté activado."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
