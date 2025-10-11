from django.db import models
from actores.models import Actor, Cliente

# Create your models here.

# ==========================
# CASO
# ==========================
class Caso(models.Model):
    nroCaso = models.CharField(max_length=50, unique=True)     # único (tu diseño lo indica)
    tipoCaso = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, default="ABIERTO")
    prioridad = models.CharField(max_length=20, default="MEDIA")
    fechaInicio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)

    creadoEn = models.DateTimeField(auto_now_add=True)
    actualizadoEn = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["estado", "prioridad"]),
            models.Index(fields=["fechaInicio"]),
        ]

    def __str__(self):
        return f"Caso {self.nroCaso}"


# ==========================
# EQUIPO DE CASO (N:M Actor<->Caso)
# PK compuesta lógica: (idActor, idCaso)
# ==========================
class EquipoCaso(models.Model):
    ROL_CHOICES = (
        ("RESPONSABLE", "Responsable"),
        ("ASOCIADO", "Asociado"),
        ("ASISTENTE", "Asistente"),
    )

    actor = models.ForeignKey(Actor, on_delete=models.PROTECT, db_index=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, db_index=True)
    rolEnEquipo = models.CharField(max_length=20, choices=ROL_CHOICES)
    observaciones = models.TextField(blank=True)
    fechaAsignacion = models.DateField()
    fechaSalida = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (("actor", "caso"),)     # PK compuesta (lógica)
        indexes = [
            models.Index(fields=["caso", "rolEnEquipo"]),
            models.Index(fields=["actor", "caso"]),
        ]

    def __str__(self):
        return f"{self.actor_id} en {self.caso.nroCaso} ({self.rolEnEquipo})"


# ==========================
# PARTE PROCESAL (Cliente<->Caso)
# PK compuesta lógica: (idActor, idCaso) pero idActor refiere a Cliente(idActor)
# ==========================
class ParteProcesal(models.Model):
    ROL_CHOICES = (
        ("DEMANDANTE", "Demandante"),
        ("DEMANDADO", "Demandado"),
        ("TERCERO", "Tercero"),
    )

    # Nota: Cliente tiene PK = idActor, así que el FK va directo al PK del Cliente
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_index=True)
    caso = models.ForeignKey(Caso, on_delete=models.CASCADE, db_index=True)
    rolProcesal = models.CharField(max_length=20, choices=ROL_CHOICES)
    estado = models.CharField(max_length=20, default="ACTIVO")
    fechaInicio = models.DateField()
    fechaFin = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = (("cliente", "caso"),)   # PK compuesta (lógica)
        indexes = [
            models.Index(fields=["caso", "rolProcesal"]),
            models.Index(fields=["cliente", "caso"]),
        ]

    def __str__(self):
        return f"{self.cliente_id} - {self.caso.nroCaso} ({self.rolProcesal})"


# ==========================
# EXPEDIENTE (1–a–1 con Caso)
# ==========================
class Expediente(models.Model):
    caso = models.OneToOneField(Caso, on_delete=models.CASCADE, related_name="expediente")
    nroExpediente = models.CharField(max_length=50)           # si luego quieres UNIQUE, lo añadimos
    estado = models.CharField(max_length=20, default="ABIERTO")
    fechaCreacion = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["fechaCreacion"]),
        ]

    def __str__(self):
        return f"Expediente {self.nroExpediente} / {self.caso.nroCaso}"


# ==========================
# CARPETA (en el EXPEDIENTE, con jerarquía opcional)
# ==========================
class Carpeta(models.Model):
    expediente = models.ForeignKey(Expediente, on_delete=models.CASCADE, related_name="carpetas")
    nombre = models.CharField(max_length=120)
    estado = models.CharField(max_length=20, default="ACTIVO")
    carpetaPadre = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="subcarpetas")

    creadoEn = models.DateTimeField(auto_now_add=True)
    actualizadoEn = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["expediente", "estado"]),
            models.Index(fields=["carpetaPadre"]),
        ]
        # Si prefieres nombre físico exacto:
        # db_table = "carpeta"

    def __str__(self):
        return f"{self.nombre} (Exp: {self.expediente_id})"