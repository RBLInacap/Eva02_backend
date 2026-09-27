from django.db import models


class Reporte(models.Model):
	codigo = models.CharField(max_length=20, unique=True)
	fecha = models.DateField()
	territorio = models.CharField(max_length=120)
	tipo_gestion = models.CharField(max_length=150)
	estado = models.CharField(max_length=30)
	delegado = models.ForeignKey(
		"monitoreo.Delegado",
		on_delete=models.CASCADE,
		related_name="reportes",
	)

	def __str__(self):
		return self.codigo
