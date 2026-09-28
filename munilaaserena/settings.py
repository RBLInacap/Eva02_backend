"""Configuración del proyecto municipal de La Serena."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Rutas principales del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


# La clave secreta se configura en el archivo local de entorno.
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-for-local-testing-only")

DEBUG = os.getenv("DJANGO_DEBUG", "True").lower() in {"true", "1", "yes"}

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]


# Aplicaciones instaladas.

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "solicitudes",
    "monitoreo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "munilaaserena.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "munilaaserena.wsgi.application"


# Conexión a base de datos. Para desarrollo local se usa SQLite por defecto.
# En producción/AWS se puede configurar MySQL mediante variables de entorno.

if os.getenv("DB_ENGINE") == "mysql" or os.getenv("DB_NAME") and os.getenv("DB_USER"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("DB_NAME", "muni_laserena"),
            "USER": os.getenv("DB_USER", "root"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
                "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Validación de contraseñas de usuarios.

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Idioma, fechas y zona horaria de Chile.

LANGUAGE_CODE = "es-cl"

TIME_ZONE = "America/Santiago"

DATE_FORMAT = "d/m/Y"
SHORT_DATE_FORMAT = "d/m/Y"

USE_I18N = True

USE_TZ = True


# Archivos estáticos.

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# En desarrollo, los correos se imprimen en la consola.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
