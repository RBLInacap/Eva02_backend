from django.db import models


class Delegacion(models.Model):
	PREFIJO_CODIGO = "DEL"

	id_delegacion = models.BigAutoField(primary_key=True)
	nombre = models.CharField(max_length=100, unique=True)
	codigo = models.CharField(max_length=10, unique=True, blank=True, null=True)
	direccion = models.CharField(max_length=255, null=True, blank=True)
	activo = models.BooleanField(default=True)

	class Meta:
		verbose_name = "Delegación"
		verbose_name_plural = "Delegaciones"

	def __str__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		if not self.codigo:
			if self.pk is None:
				super().save(*args, **kwargs)
			self.codigo = f"{self.PREFIJO_CODIGO}-{self.pk:06d}"
			super().save(update_fields=("codigo",))
			return
		super().save(*args, **kwargs)


class Rol(models.Model):
	class Nombre(models.TextChoices):
		ADMINISTRADOR = "ADMINISTRADOR", "ADMINISTRADOR"
		COORDINADOR = "COORDINADOR", "COORDINADOR"
		DELEGADO = "DELEGADO", "DELEGADO"
		FUNCIONARIO = "FUNCIONARIO", "FUNCIONARIO"

	id_rol = models.BigAutoField(primary_key=True)
	nombre = models.CharField(max_length=20, choices=Nombre.choices, unique=True)
	descripcion = models.TextField()

	def __str__(self):
		return self.nombre


class Funcionario(models.Model):
	class EstadoSemaforo(models.TextChoices):
		VERDE = "Verde", "Verde"
		AMARILLO = "Amarillo", "Amarillo"
		ROJO = "Rojo", "Rojo"

	id_funcionario = models.BigAutoField(primary_key=True)
	username = models.CharField(max_length=150, unique=True)
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)
	email = models.EmailField(max_length=254, blank=True)
	avance_diario = models.PositiveSmallIntegerField(null=True, blank=True)
	estado_semaforo = models.CharField(
		max_length=8,
		choices=EstadoSemaforo.choices,
		null=True,
		blank=True,
	)
	id_delegacion = models.ForeignKey(
		Delegacion,
		on_delete=models.SET_NULL,
		db_column="id_delegacion",
		null=True,
		blank=True,
		related_name="funcionarios",
	)
	id_rol = models.ForeignKey(
		Rol,
		on_delete=models.RESTRICT,
		db_column="id_rol",
		related_name="funcionarios",
	)

	def __str__(self):
		return f"{self.nombre} {self.apellido}"
