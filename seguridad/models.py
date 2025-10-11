from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# ==========================
# USUARIO (CustomUser)
# ==========================
class Usuario(AbstractUser):
    
    email = models.EmailField(unique=True)   # en tu diseño email es atributo; lo hacemos único
    estado = models.CharField(max_length=20, default="ACTIVO")
    estadoCuenta = models.CharField(max_length=20, default="HABILITADA")
    creadoEn = models.DateTimeField(auto_now_add=True)
    actualizadoEn = models.DateTimeField(auto_now=True)

    # Acceso con el nombre de tu mapeo (sin duplicar columnas)
    @property
    def nombreUser(self):
        return self.username

    @property
    def contrasena(self):
        # Es el hash interno; no se debe leer directamente en UI.
        return self.password

    def __str__(self):
        return f"{self.username} ({self.email})"


# ==========================
# ROLES / PERMISOS
# ==========================
class Rol(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Permiso(models.Model):
    descripcion = models.CharField(max_length=150)
    accion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.accion


class UsuarioRol(models.Model):
    """
    PK (compuesta lógica): (idUsuario, idRol)
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_index=True)
    fechaAsignacion = models.DateField()

    class Meta:
        unique_together = (("usuario", "rol"),)
        indexes = [
            models.Index(fields=["usuario", "rol"]),
        ]

    def __str__(self):
        return f"{self.usuario} -> {self.rol}"


class RolPermiso(models.Model):
    """
    PK (compuesta lógica): (idRol, idPermiso)
    """
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_index=True)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE, db_index=True)
    estado = models.CharField(max_length=20, default="ACTIVO")

    class Meta:
        unique_together = (("rol", "permiso"),)
        indexes = [
            models.Index(fields=["rol", "permiso"]),
        ]

    def __str__(self):
        return f"{self.rol} -> {self.permiso}"


# ==========================
# BITÁCORA
# ==========================

class Bitacora(models.Model):
    # === Según tu mapeo (NO tocar nombres) ===
    login = models.CharField(max_length=100)       
    ip = models.GenericIPAddressField(null=True, blank=True)  
    userAgent = models.TextField(blank=True)
    fecha = models.DateTimeField()                 
    login_at = models.DateTimeField(null=True, blank=True)    # hora de inicio de sesión (si aplica)
    logout_at = models.DateTimeField(null=True, blank=True)   # hora de cierre (si aplica)
    device = models.CharField(max_length=255, null=True, blank=True)

    # === FK al usuario ===
    idUsuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,                   # conservar auditoría si borran usuario
        related_name="bitacoras",
        db_index=True
    )

    class Meta:
        db_table = "bitacora"                       # opcional: fija el nombre físico
        indexes = [
            models.Index(fields=["idUsuario", "fecha"]),
            models.Index(fields=["login", "fecha"]),
        ]

    def __str__(self):
        return f"{self.login} - {self.idUsuario} @ {self.fecha:%Y-%m-%d %H:%M}"


class DetalleBitacora(models.Model):
    idBitacora = models.ForeignKey(
        Bitacora,
        on_delete=models.CASCADE,
        related_name="detalles"
    )
    accion = models.CharField(max_length=100)       # mantengo 100 (coherente con compa); si quieres 150, sube a 150
    fecha = models.DateTimeField()
    tabla = models.CharField(max_length=100)        # tu mapeo tenía 100
    detalle = models.TextField(blank=True)          # se mantiene del mapeo

    class Meta:
        db_table = "detallebitacora"                # opcional: nombre físico
        indexes = [
            models.Index(fields=["tabla", "fecha"]),
            models.Index(fields=["accion", "fecha"]),
        ]

    def __str__(self):
        return f"{self.tabla} - {self.accion} ({self.fecha:%Y-%m-%d %H:%M})"
