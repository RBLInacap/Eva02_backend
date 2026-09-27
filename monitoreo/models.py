from django.db import models


class Delegado(models.Model):
	nombre = models.CharField(max_length=150)
	avance_diario = models.PositiveSmallIntegerField()
	estado_semaforo = models.CharField(max_length=20)

	def __str__(self):
		return self.nombre
