# Municipalidad La Serena

Sistema web modular para gestión de solicitudes, seguimiento y monitoreo municipal.

## Requisitos

- Python 3.11+
- Virtualenv / venv
- MySQL (opcional para producción)
- AWS EC2 / Elastic Beanstalk (opcional para despliegue)

## Configuración local

1. Crear entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activar entorno:
   ```bash
   .\venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Copiar el ejemplo de entorno:
   ```bash
   copy .env.example .env
   ```

5. Ajustar variables en `.env`.

6. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

7. Cargar datos iniciales:
   ```bash
   python manage.py cargar_datos_sgr
   ```

8. Ejecutar el proyecto:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Variables de entorno

```env
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_SETTINGS_MODULE=munilaaserena.settings

DB_ENGINE=mysql
DB_NAME=muni_laserena
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

## Funcionalidades principales

- Gestión de actividades y compromisos
- Listado de reportes y evidencias
- Panel de monitoreo municipal
- Indicadores de resumen y semáforo
- Búsqueda global
- Interfaz responsive con Bootstrap
- Importación de datos desde JSON locales
- Carga inicial de datos SGR

## Validación del proyecto

Se ejecutaron pruebas del sistema con Django:

```bash
python manage.py test
```

Resultado esperado: todas las pruebas pasan.

Asimismo, se validó el arranque del servidor local:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Despliegue en AWS

Para desplegar en AWS se recomienda:

- EC2 o Elastic Beanstalk
- Base de datos MySQL en RDS
- Variables de entorno configuradas en el servicio de despliegue
- `DEBUG=False`
- `ALLOWED_HOSTS` con el dominio público
- archivos estáticos recopilados con `collectstatic`
- servidor WSGI con `gunicorn`

Ejemplo de variables para producción:

```env
DJANGO_SECRET_KEY=clave_segura_de_produccion
DJANGO_DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
DJANGO_SETTINGS_MODULE=munilaaserena.settings_production
DB_ENGINE=mysql
DB_NAME=muni_laserena
DB_USER=admin
DB_PASSWORD=contraseña_segura
DB_HOST=endpoint-rds.amazonaws.com
DB_PORT=3306
```

## Notas

Este proyecto está preparado para un entorno de desarrollo local con SQLite por defecto y para producción con MySQL usando entorno configurado.

La intención de la documentación también incluye el uso de inteligencia artificial como apoyo al diseño y estructuración, validado en el proceso de desarrollo del proyecto.
