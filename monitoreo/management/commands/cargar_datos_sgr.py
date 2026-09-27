from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from monitoreo.models import Delegacion, Funcionario, Rol
from solicitudes.models import (
	Actividad,
	Compromiso,
	Evidencia,
	Indicador,
	Meta,
	Periodo,
	Solicitante,
	Solicitante_Actividad,
)


class Command(BaseCommand):
	help = "Carga los datos iniciales proporcionados para el sistema SGR."

	@transaction.atomic
	def handle(self, *args, **options):
		roles_iniciales = {
			"ADMINISTRADOR": "Acceso total al sistema y configuración global.",
			"COORDINADOR": "Supervisión comunal y gestión de metas.",
			"DELEGADO": "Jefatura territorial, valida evidencias.",
			"FUNCIONARIO": "Personal de terreno, registra actividades.",
		}
		roles = {
			nombre: Rol.objects.get_or_create(
				nombre=nombre,
				defaults={"descripcion": descripcion},
			)[0]
			for nombre, descripcion in roles_iniciales.items()
		}

		delegaciones_iniciales = (
			("Las Compañías", "CIA", "Esmeralda 2422."),
			("La Antena", "ANT", "18 de Septiembre s/n, Plaza de Abastos."),
			("Avenida del Mar", "MAR", "Avenida del Mar 2000."),
			("Sector Rural", "RUR", "Ruta 41, Km 15."),
		)
		delegaciones = {
			codigo: Delegacion.objects.get_or_create(
				codigo=codigo,
				defaults={"nombre": nombre, "direccion": direccion, "activo": True},
			)[0]
			for nombre, codigo, direccion in delegaciones_iniciales
		}

		funcionarios_iniciales = (
			("rbrizuela", "Rodrigo", "Brizuela", None, "COORDINADOR", None, None),
			("adiaz", "Alexodro", "Diaz", "CIA", "DELEGADO", 95, "Verde"),
			("fcaiceo", "Francisco", "Caiceo", "ANT", "FUNCIONARIO", 75, "Amarillo"),
		)
		funcionarios = {}
		for (
			username,
			nombre,
			apellido,
			codigo_delegacion,
			nombre_rol,
			avance_diario,
			estado_semaforo,
		) in funcionarios_iniciales:
			funcionario, _ = Funcionario.objects.get_or_create(
				username=username,
				defaults={
					"nombre": nombre,
					"apellido": apellido,
					"email": "",
					"id_delegacion": delegaciones.get(codigo_delegacion),
					"id_rol": roles[nombre_rol],
					"avance_diario": avance_diario,
					"estado_semaforo": estado_semaforo,
				},
			)
			funcionarios[username] = funcionario

		solicitantes_iniciales = (
			("María Rojas", "JJVV San Bartolomé", "+56911223344"),
			("Pedro Alarcón", "Club Adulto Mayor Renacer (La Pampa)", "+56955667788"),
		)
		solicitantes = {}
		for nombre_contacto, organizacion, telefono in solicitantes_iniciales:
			solicitante, _ = Solicitante.objects.get_or_create(
				nombre_contacto=nombre_contacto,
				organizacion=organizacion,
				telefono=telefono,
			)
			solicitantes[nombre_contacto] = solicitante

		actividad_luminaria, _ = Actividad.objects.get_or_create(
			id_funcionario=funcionarios["fcaiceo"],
			fecha_actividad=date(2026, 9, 26),
			actividad_solicitud="Despeje de luminaria tapada por árboles",
			defaults={
				"accion_ejecutada": "Inspección visual y levantamiento de requerimiento de poda.",
				"latitud_longitud": Decimal("-29.9027000"),
				"longitud": Decimal("-71.2519000"),
			},
		)
		actividad_bache, _ = Actividad.objects.get_or_create(
			id_funcionario=funcionarios["adiaz"],
			fecha_actividad=date(2026, 9, 25),
			actividad_solicitud="Reparación bache",
			defaults={
				"accion_ejecutada": "Medición de evento asfáltico en calle principal.",
				"latitud_longitud": Decimal("-29.9045000"),
				"longitud": Decimal("-71.2480000"),
			},
		)

		Compromiso.objects.get_or_create(
			id_actividad=actividad_luminaria,
			defaults={
				"descripcion": "Coordinar camión alza hombre para poda de pimiento que tapa luminaria pública.",
				"fecha_comprometida": date(2026, 10, 5),
				"area_apoyo": "Operaciones",
				"estado": "En Proceso",
			},
		)
		Compromiso.objects.get_or_create(
			id_actividad=actividad_bache,
			defaults={
				"descripcion": "Ingresar requerimiento a bacheo municipal con asfalto en frío.",
				"fecha_comprometida": date(2026, 10, 10),
				"area_apoyo": "Dirección de Tránsito",
				"estado": "En Proceso",
			},
		)

		Evidencia.objects.get_or_create(
			codigo_verificador="CIA-712",
			defaults={
				"id_actividad": actividad_bache,
				"id_verificador": funcionarios["adiaz"],
				"estado": "APROBADA",
				"observacion": "Fotografía clara del bache con medidas.",
			},
		)

		Solicitante_Actividad.objects.get_or_create(
			id_solicitante=solicitantes["María Rojas"],
			id_actividad=actividad_luminaria,
			defaults={
				"rol_participacion": "Solicitante principal",
				"es_principal": True,
			},
		)

		periodo, _ = Periodo.objects.get_or_create(
			nombre="Trimestre 3 - 2026",
			defaults={
				"fecha_inicio": date(2026, 7, 1),
				"fecha_termino": date(2026, 9, 30),
			},
		)
		meta, _ = Meta.objects.get_or_create(
			id_periodo=periodo,
			cargo="Operativos de Inspección Territorial",
			defaults={
				"valor_objetivo": 10,
				"ponderador": Decimal("50.0"),
			},
		)
		Indicador.objects.get_or_create(
			id_meta=meta,
			fecha_calculo=timezone.localdate(),
			defaults={
				"avance_aprobado": 8,
				"cumplimiento": Decimal("80.00"),
				"semaforo": Indicador.Semaforo.VERDE,
			},
		)

		self.stdout.write(
			self.style.SUCCESS(
				"Datos SGR cargados o ya existentes: 4 roles, 4 delegaciones, "
				"3 funcionarios, 2 solicitantes, 2 actividades, 2 compromisos, "
				"1 evidencia, 1 participación, 1 período, 1 meta y 1 indicador."
			)
		)