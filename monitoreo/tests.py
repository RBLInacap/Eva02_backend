from django.test import TestCase
from django.urls import reverse


class ResumenMonitoreoTests(TestCase):
    def test_resumen_usa_datos_reales_del_json(self):
        response = self.client.get(reverse('resumen_monitoreo'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_funcionarios'], 2)
        self.assertEqual(response.context['avance_promedio'], 85)
        self.assertEqual(response.context['evaluacion_global'], 'Amarillo')
