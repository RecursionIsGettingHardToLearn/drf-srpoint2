
from django.db import models
from django.conf import settings
# Create your models here.

# ==========================
# ACTOR (1–a–1 con Usuario)
# ==========================
class Actor(models.Model):
    TIPO_CHOICES = (
        ("ABO", "Abogado"),
        ("CLI", "Cliente"),
        ("ASI", "Asistente"),
    )

    ESTADOS = (
        ("ACTIVO", "Activo"),
        ("INACTIVO", "Inactivo"),
    )
    # 1–a–1/única con Usuario (tu mapeo: idUsuario → Usuario(id))
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,      # no perder integridad si intentan borrar el usuario
        related_name="actor"
    )

    tipoActor = models.CharField(max_length=5, choices=TIPO_CHOICES)
    nombres = models.CharField(max_length=120)
    apellidoPaterno = models.CharField(max_length=80)
    apellidoMaterno = models.CharField(max_length=80, blank=True)
    ci = models.CharField(max_length=30, unique=True)        # usualmente único
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.TextField(blank=True)
    estadoActor = models.CharField(max_length=20, choices=ESTADOS, default="ACTIVO")

    creadoEn = models.DateTimeField(auto_now_add=True)
    actualizadoEn = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["tipoActor"]),
            models.Index(fields=["estadoActor"]),
        ]
        # Si quieres nombre físico exacto:
        # db_table = "actor"

    def __str__(self):
        return f"{self.nombres} {self.apellidoPaterno} ({self.get_tipoActor_display()})"


# ===================================
# SUBTIPOS (PK = FK a Actor.id)
# ===================================

class Abogado(models.Model):
    # PK = FK → idActor
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,      # si cae el Actor, cae el subtipo
        primary_key=True,
        related_name="abogado"
    )
    nroCredencial = models.CharField(max_length=50)
    especialidad = models.CharField(max_length=100, blank=True)
    estadoLicencia = models.CharField(max_length=50, default="VIGENTE")

    class Meta:
        # db_table = "abogado"
        indexes = [models.Index(fields=["estadoLicencia"])]

    def __str__(self):
        return f"Abg. {self.actor.nombres} {self.actor.apellidoPaterno}"


class Cliente(models.Model):
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="cliente"
    )
    TIPO_CHOICES = (("NATURAL", "Natural"), ("JURIDICO", "Jurídico"))
    tipoCliente = models.CharField(max_length=10, choices=TIPO_CHOICES)
    observaciones = models.TextField(blank=True)

    class Meta:
        # db_table = "cliente"
        indexes = [models.Index(fields=["tipoCliente"])]

    def __str__(self):
        return f"Cliente {self.actor.nombres} {self.actor.apellidoPaterno}"


class Asistente(models.Model):
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="asistente"
    )
    area = models.CharField(max_length=100, blank=True)
    cargo = models.CharField(max_length=100, blank=True)

    class Meta:
        # db_table = "asistente"
        indexes = [models.Index(fields=["area", "cargo"])]

    def __str__(self):
        return f"Asistente {self.actor.nombres} {self.actor.apellidoPaterno}"