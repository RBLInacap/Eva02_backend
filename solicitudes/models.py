from django.db import models


class Actividad(models.Model):
	class Estado(models.TextChoices):
		INGRESADO = "Ingresado", "Ingresado"
		EN_PROCESO = "En Proceso", "En Proceso"
		REALIZADO = "Realizado", "Realizado"

	id_actividad = models.BigAutoField(primary_key=True)
	codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
	id_funcionario = models.ForeignKey(
		"monitoreo.Funcionario",
		on_delete=models.CASCADE,
		db_column="id_funcionario",
		related_name="actividades",
	)
	fecha_actividad = models.DateField()
	actividad_solicitud = models.CharField(max_length=255)
	accion_ejecutada = models.TextField()
	estado = models.CharField(
		max_length=20,
		choices=Estado.choices,
		default=Estado.INGRESADO,
	)
	latitud_longitud = models.DecimalField(
		max_digits=10,
		decimal_places=7,
		null=True,
		blank=True,
		verbose_name="Latitud",
	)
	longitud = models.DecimalField(
		max_digits=10,
		decimal_places=7,
		null=True,
		blank=True,
		verbose_name="Longitud",
	)
	solicitantes = models.ManyToManyField(
		"Solicitante",
		through="Solicitante_Actividad",
		related_name="actividades",
	)

	class Meta:
		verbose_name = "Actividad"
		verbose_name_plural = "Actividades"
		constraints = [
			models.CheckConstraint(
				condition=models.Q(
					estado__in=("Ingresado", "En Proceso", "Realizado")
				),
				name="actividad_estado_valido",
			)
		]

	def __str__(self):
		return f"{self.actividad_solicitud} ({self.fecha_actividad:%d/%m/%Y})"

	def save(self, *args, **kwargs):
		if not self.codigo:
			if self.pk is None:
				super().save(*args, **kwargs)
			self.codigo = f"ACT-{self.pk:06d}"
			super().save(update_fields=("codigo",))
			return
		super().save(*args, **kwargs)


class Evidencia(models.Model):
	id_evidencia = models.BigAutoField(primary_key=True)
	codigo_verificador = models.CharField(
		max_length=20,
		unique=True,
		blank=True,
		null=True,
		editable=False,
	)
	id_actividad = models.ForeignKey(
		Actividad,
		on_delete=models.CASCADE,
		db_column="id_actividad",
		related_name="evidencias",
	)
	id_verificador = models.ForeignKey(
		"monitoreo.Funcionario",
		on_delete=models.RESTRICT,
		db_column="id_verificador",
		related_name="evidencias_verificadas",
	)
	estado = models.CharField(max_length=20)
	observacion = models.TextField()
	archivo = models.FileField(upload_to="evidencias/", blank=True)

	def __str__(self):
		return self.codigo_verificador

	def save(self, *args, **kwargs):
		if not self.codigo_verificador:
			if self.pk is None:
				super().save(*args, **kwargs)
			self.codigo_verificador = f"EVI-{self.pk:06d}"
			super().save(update_fields=("codigo_verificador",))
			return
		super().save(*args, **kwargs)


class Solicitante(models.Model):
	id_solicitante = models.BigAutoField(primary_key=True)
	nombre_contacto = models.CharField(max_length=100)
	organizacion = models.CharField(max_length=150)
	telefono = models.CharField(max_length=20)

	def __str__(self):
		return self.nombre_contacto


class Solicitante_Actividad(models.Model):
	id_solicitante = models.ForeignKey(
		Solicitante,
		on_delete=models.CASCADE,
		db_column="id_solicitante",
		related_name="participaciones",
	)
	id_actividad = models.ForeignKey(
		Actividad,
		on_delete=models.CASCADE,
		db_column="id_actividad",
		related_name="participaciones_solicitantes",
	)
	rol_participacion = models.CharField(max_length=50)
	es_principal = models.BooleanField(default=False)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=("id_solicitante", "id_actividad"),
				name="unico_solicitante_por_actividad",
			)
		]

	def __str__(self):
		return f"Participación {self.id_solicitante_id} - {self.id_actividad_id}"


class Compromiso(models.Model):
	class Estado(models.TextChoices):
		INGRESADO = "Ingresado", "Ingresado"
		EN_PROCESO = "En Proceso", "En Proceso"
		REALIZADO = "Realizado", "Realizado"

	id_compromiso = models.BigAutoField(primary_key=True)
	id_actividad = models.OneToOneField(
		Actividad,
		on_delete=models.CASCADE,
		db_column="id_actividad",
		related_name="compromiso",
	)
	descripcion = models.TextField()
	fecha_comprometida = models.DateField()
	area_apoyo = models.CharField(max_length=100)
	estado = models.CharField(max_length=20, choices=Estado.choices)

	class Meta:
		constraints = [
			models.CheckConstraint(
				condition=models.Q(
					estado__in=("Ingresado", "En Proceso", "Realizado")
				),
				name="compromiso_estado_valido",
			)
		]

	def __str__(self):
		return self.descripcion


class Periodo(models.Model):
	id_periodo = models.BigAutoField(primary_key=True)
	nombre = models.CharField(max_length=100, unique=True)
	fecha_inicio = models.DateField()
	fecha_termino = models.DateField()

	class Meta:
		constraints = [
			models.CheckConstraint(
				condition=models.Q(fecha_termino__gte=models.F("fecha_inicio")),
				name="periodo_fechas_validas",
			)
		]

	def __str__(self):
		return self.nombre


class Meta(models.Model):
	id_meta = models.BigAutoField(primary_key=True)
	cargo = models.CharField(max_length=150)
	valor_objetivo = models.PositiveSmallIntegerField()
	ponderador = models.DecimalField(max_digits=5, decimal_places=2)
	id_periodo = models.ForeignKey(
		Periodo,
		on_delete=models.RESTRICT,
		db_column="id_periodo",
		related_name="metas",
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=("id_periodo", "cargo"),
				name="meta_unica_por_periodo_y_cargo",
			)
		]

	def __str__(self):
		return self.cargo


class Indicador(models.Model):
	class Semaforo(models.TextChoices):
		VERDE = "Verde", "Verde"
		AMARILLO = "Amarillo", "Amarillo"
		ROJO = "Rojo", "Rojo"

	id_indicador = models.BigAutoField(primary_key=True)
	fecha_calculo = models.DateField()
	avance_aprobado = models.PositiveSmallIntegerField()
	cumplimiento = models.DecimalField(max_digits=5, decimal_places=2)
	semaforo = models.CharField(max_length=8, choices=Semaforo.choices)
	id_meta = models.ForeignKey(
		Meta,
		on_delete=models.CASCADE,
		db_column="id_meta",
		related_name="indicadores",
	)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=("id_meta", "fecha_calculo"),
				name="indicador_unico_por_meta_y_fecha",
			),
			models.CheckConstraint(
				condition=models.Q(semaforo__in=("Verde", "Amarillo", "Rojo")),
				name="indicador_semaforo_valido",
			),
		]

	def __str__(self):
		return f"{self.id_meta.cargo}: {self.fecha_calculo:%d/%m/%Y}"


class Reporte(models.Model):
	class Territorio(models.TextChoices):
		LAS_COMPANIAS = "Las Compañías", "Las Compañías"
		LA_ANTENA = "La Antena", "La Antena"
		AVENIDA_DEL_MAR = "Avenida del Mar", "Avenida del Mar"
		SECTOR_RURAL = "Sector Rural", "Sector Rural"

	class Estado(models.TextChoices):
		INGRESADO = "Ingresado", "Ingresado"
		EN_PROCESO = "En Proceso", "En Proceso"
		REALIZADO = "Realizado", "Realizado"

	codigo = models.CharField(max_length=20, unique=True, blank=True, null=True, editable=False)
	fecha = models.DateField()
	territorio = models.CharField(max_length=120, choices=Territorio.choices)
	tipo_gestion = models.CharField(max_length=150)
	estado = models.CharField(max_length=30, choices=Estado.choices)
	funcionario = models.ForeignKey(
		"monitoreo.Funcionario",
		on_delete=models.CASCADE,
		related_name="reportes_legacy",
	)

	class Meta:
		constraints = [
			models.CheckConstraint(
				condition=models.Q(
					territorio__in=(
						"Las Compañías",
						"La Antena",
						"Avenida del Mar",
						"Sector Rural",
					)
				),
				name="reporte_territorio_valido",
			),
			models.CheckConstraint(
				condition=models.Q(
					estado__in=("Ingresado", "En Proceso", "Realizado")
				),
				name="reporte_estado_valido",
			),
		]

	def __str__(self):
		return self.codigo or f"Reporte {self.pk}"

	def save(self, *args, **kwargs):
		if not self.codigo:
			if self.pk is None:
				super().save(*args, **kwargs)
			self.codigo = f"REP-{self.pk:06d}"
			super().save(update_fields=("codigo",))
			return
		super().save(*args, **kwargs)
