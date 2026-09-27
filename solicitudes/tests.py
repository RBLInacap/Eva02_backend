from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from monitoreo.models import Funcionario, Rol
from .models import Actividad, Compromiso, Evidencia, Reporte


class PruebasListadoActividades(TestCase):
    def test_busqueda_fecha_y_estado_del_compromiso(self):
        rol = Rol.objects.create(nombre=Rol.Nombre.FUNCIONARIO, descripcion="Rol de prueba")
        funcionario = Funcionario.objects.create(
            username="funcionario-actividad",
            nombre="Nombre",
            apellido="Responsable",
            email="",
            id_rol=rol,
        )
        actividad = Actividad.objects.create(
            id_funcionario=funcionario,
            fecha_actividad=date(2026, 9, 26),
            actividad_solicitud="Inspección de prueba",
            accion_ejecutada="Inspección realizada.",
        )
        self.assertEqual(actividad.codigo, f"ACT-{actividad.pk:06d}")
        Compromiso.objects.create(
            id_actividad=actividad,
            descripcion="Compromiso de prueba.",
            fecha_comprometida=date(2026, 10, 5),
            area_apoyo="Operaciones",
            estado="En Proceso",
        )

        respuesta = self.client.get(
            reverse("lista_actividades"), {"busqueda": "Operaciones"}
        )

        self.assertContains(respuesta, "Inspección de prueba")
        self.assertContains(respuesta, "En Proceso")
        self.assertContains(respuesta, "26/09/2026")


class PruebasListadoEvidencias(TestCase):
    def test_lista_muestra_actividad_estado_y_verificador(self):
        rol = Rol.objects.create(nombre=Rol.Nombre.DELEGADO, descripcion="Rol de prueba")
        funcionario = Funcionario.objects.create(
            username="delegado-evidencia",
            nombre="Alexodro",
            apellido="Diaz",
            email="",
            id_rol=rol,
        )
        actividad = Actividad.objects.create(
            id_funcionario=funcionario,
            fecha_actividad=date(2026, 9, 25),
            actividad_solicitud="Reparación bache de prueba",
            accion_ejecutada="Inspección.",
        )
        Evidencia.objects.create(
            codigo_verificador="CIA-712",
            id_actividad=actividad,
            id_verificador=funcionario,
            estado="APROBADA",
            observacion="Evidencia de prueba.",
        )
        evidencia_automatica = Evidencia.objects.create(
            id_actividad=actividad,
            id_verificador=funcionario,
            estado="PENDIENTE",
            observacion="Código generado automáticamente.",
        )
        self.assertEqual(
            evidencia_automatica.codigo_verificador,
            f"EVI-{evidencia_automatica.pk:06d}",
        )

        respuesta = self.client.get(
            reverse("lista_evidencias"), {"busqueda": "CIA-712"}
        )

        self.assertContains(respuesta, "CIA-712")
        self.assertContains(respuesta, "Reparación bache de prueba")
        self.assertContains(respuesta, "Alexodro Diaz")
        self.assertContains(respuesta, reverse("admin:solicitudes_evidencia_add"))


class PruebasCRUDAdministradorReporte(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrador = get_user_model().objects.create_superuser(
            username="administrador-reportes-prueba",
            email="administrador-reportes@ejemplo.cl",
            password="clave-prueba",
        )
        cls.rol = Rol.objects.create(
            nombre=Rol.Nombre.DELEGADO,
            descripcion="Jefatura territorial",
        )
        cls.funcionario = Funcionario.objects.create(
            username="delegado-reportes-prueba",
            nombre="Delegado",
            apellido="Prueba",
            email="",
            id_rol=cls.rol,
            estado_semaforo=Funcionario.EstadoSemaforo.VERDE,
        )

    def test_admin_crea_modifica_y_elimina_reporte(self):
        self.client.force_login(self.administrador)
        url_agregar = reverse("admin:solicitudes_reporte_add")
        respuesta = self.client.post(url_agregar, {
            "codigo": "CRUD001",
            "fecha": "2026-09-26",
            "territorio": "Sector Rural",
            "tipo_gestion": "Prueba CRUD",
            "estado": "En Proceso",
            "funcionario": str(self.funcionario.pk),
            "_save": "Guardar",
        })
        self.assertEqual(respuesta.status_code, 302)

        reporte = Reporte.objects.get(
            funcionario=self.funcionario,
            tipo_gestion="Prueba CRUD",
        )
        self.assertTrue(reporte.codigo.startswith("REP-"))
        url_editar = reverse("admin:solicitudes_reporte_change", args=[reporte.pk])
        self.client.post(url_editar, {
            "fecha": "2026-09-26",
            "territorio": "La Antena",
            "tipo_gestion": "Prueba CRUD actualizada",
            "estado": "Realizado",
            "funcionario": str(self.funcionario.pk),
            "_save": "Guardar",
        })
        reporte.refresh_from_db()
        self.assertEqual(reporte.territorio, "La Antena")

        url_eliminar = reverse("admin:solicitudes_reporte_delete", args=[reporte.pk])
        respuesta = self.client.post(url_eliminar, {"post": "yes"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Reporte.objects.filter(pk=reporte.pk).exists())

    def test_choices_territoriales_y_estados_son_cerrados(self):
        valores_estados = {"Ingresado", "En Proceso", "Realizado"}
        valores_territorios = {
            "Las Compañías",
            "La Antena",
            "Avenida del Mar",
            "Sector Rural",
        }

        self.assertEqual(set(Reporte.Estado.values), valores_estados)
        self.assertEqual(set(Actividad.Estado.values), valores_estados)
        self.assertEqual(set(Compromiso.Estado.values), valores_estados)
        self.assertEqual(set(Reporte.Territorio.values), valores_territorios)
