from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from solicitudes.models import Reporte
from .models import Delegacion, Funcionario, Rol


class PruebasResumenMonitoreo(TestCase):
    def test_resumen_calcula_metricas_desde_delegados(self):
        rol = Rol.objects.create(nombre=Rol.Nombre.DELEGADO, descripcion="Jefatura territorial")
        Funcionario.objects.create(
            username="delegado-prueba-1",
            nombre="Delegado",
            apellido="Verde",
            email="",
            id_rol=rol,
            estado_semaforo=Funcionario.EstadoSemaforo.VERDE,
        )
        Funcionario.objects.create(
            username="delegado-prueba-2",
            nombre="Delegado",
            apellido="Amarillo",
            email="",
            id_rol=rol,
            estado_semaforo=Funcionario.EstadoSemaforo.AMARILLO,
        )

        respuesta = self.client.get(reverse("resumen_monitoreo"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total_delegados"], 2)
        self.assertEqual(respuesta.context["actividades_registradas"], 0)
        self.assertEqual(respuesta.context["evaluacion_global"], "Amarillo")

    def test_codigo_de_delegacion_se_genera_secuencialmente(self):
        primera = Delegacion.objects.create(
            nombre="Delegación automática 1", codigo=""
        )
        segunda = Delegacion.objects.create(
            nombre="Delegación automática 2", codigo=""
        )

        self.assertTrue(primera.codigo.startswith("DEL-"))
        self.assertTrue(segunda.codigo.startswith("DEL-"))
        self.assertEqual(
            int(segunda.codigo.removeprefix("DEL-")),
            int(primera.codigo.removeprefix("DEL-")) + 1,
        )

    def test_estado_semaforo_solo_tiene_tres_opciones(self):
        self.assertEqual(
            set(Funcionario.EstadoSemaforo.values),
            {"Verde", "Amarillo", "Rojo"},
        )

    def test_lista_filtra_funcionarios_y_muestra_delegacion(self):
        delegacion = Delegacion.objects.create(
            nombre="Delegación de prueba", codigo="TST", direccion="Dirección de prueba"
        )
        rol = Rol.objects.create(nombre=Rol.Nombre.FUNCIONARIO, descripcion="Rol de prueba")
        Funcionario.objects.create(
            username="funcionario-prueba",
            nombre="Nombre",
            apellido="Prueba",
            email="",
            id_delegacion=delegacion,
            id_rol=rol,
        )

        respuesta = self.client.get(
            reverse("panel_monitoreo"), {"busqueda": "TST"}
        )

        self.assertContains(respuesta, "funcionario-prueba")
        self.assertContains(respuesta, "Delegación de prueba")
        self.assertContains(respuesta, reverse("admin:monitoreo_funcionario_add"))


class PruebasImportacionDatos(TestCase):
    def test_importacion_usa_orm_y_se_puede_repetir(self):
        rol = Rol.objects.create(nombre=Rol.Nombre.DELEGADO, descripcion="Jefatura territorial")
        Funcionario.objects.create(
            username="adiaz",
            nombre="Alexodro",
            apellido="Diaz",
            email="",
            id_rol=rol,
        )
        Funcionario.objects.create(
            username="fcaiceo",
            nombre="Francisco",
            apellido="Caiceo",
            email="",
            id_rol=rol,
        )
        salida = StringIO()
        errores = StringIO()

        call_command("importar_datos_json", stdout=salida, stderr=errores)

        self.assertEqual(Funcionario.objects.filter(estado_semaforo__isnull=False).count(), 2)
        self.assertEqual(Reporte.objects.count(), 2)
        self.assertEqual(Funcionario.objects.get(username="adiaz").avance_diario, 95)
        self.assertEqual(errores.getvalue(), "")

        call_command("importar_datos_json", stdout=StringIO(), stderr=StringIO())

        self.assertEqual(Funcionario.objects.filter(estado_semaforo__isnull=False).count(), 2)
        self.assertEqual(Reporte.objects.count(), 2)


class PruebasCargaInicialSGR(TestCase):
    def test_carga_inicial_guarda_metricas_en_funcionario(self):
        call_command("cargar_datos_sgr", stdout=StringIO())

        self.assertEqual(Funcionario.objects.count(), 3)
        self.assertEqual(Funcionario.objects.get(username="adiaz").avance_diario, 95)
        self.assertEqual(
            Funcionario.objects.get(username="fcaiceo").estado_semaforo,
            Funcionario.EstadoSemaforo.AMARILLO,
        )


class PruebasCRUDAdministradorFuncionario(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.administrador = get_user_model().objects.create_superuser(
            username="administrador-prueba",
            email="administrador@ejemplo.cl",
            password="clave-prueba",
        )

        cls.rol = Rol.objects.create(
            nombre=Rol.Nombre.DELEGADO,
            descripcion="Jefatura territorial",
        )

    def test_admin_crea_modifica_y_elimina_funcionario(self):
        self.client.force_login(self.administrador)
        url_agregar = reverse("admin:monitoreo_funcionario_add")

        respuesta = self.client.post(url_agregar, {
            "username": "delegado-crud",
            "nombre": "Delegado",
            "apellido": "CRUD",
            "email": "",
            "id_rol": str(self.rol.pk),
            "estado_semaforo": "Amarillo",
            "_save": "Guardar",
        })
        self.assertEqual(respuesta.status_code, 302)

        funcionario = Funcionario.objects.get(username="delegado-crud")
        url_editar = reverse("admin:monitoreo_funcionario_change", args=[funcionario.pk])
        self.client.post(url_editar, {
            "username": "delegado-crud",
            "nombre": "Delegado actualizado",
            "apellido": "CRUD",
            "email": "",
            "id_rol": str(self.rol.pk),
            "estado_semaforo": "Verde",
            "_save": "Guardar",
        })
        funcionario.refresh_from_db()
        self.assertEqual(funcionario.nombre, "Delegado actualizado")

        url_eliminar = reverse("admin:monitoreo_funcionario_delete", args=[funcionario.pk])
        respuesta = self.client.post(url_eliminar, {"post": "yes"})
        self.assertEqual(respuesta.status_code, 302)
        self.assertFalse(Funcionario.objects.filter(pk=funcionario.pk).exists())
