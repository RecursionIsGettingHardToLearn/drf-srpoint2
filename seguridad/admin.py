from django.contrib import admin
from .models import Usuario, Rol, Permiso, UsuarioRol, RolPermiso, Bitacora, DetalleBitacora

# Registro de modelos en el admin

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'estado', 'estadoCuenta', 'creadoEn', 'actualizadoEn')
    search_fields = ('username', 'email')
    list_filter = ('estado', 'estadoCuenta')
    ordering = ('creadoEn',)

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)

@admin.register(Permiso)
class PermisoAdmin(admin.ModelAdmin):
    list_display = ('accion', 'descripcion')
    search_fields = ('accion',)
    ordering = ('accion',)

@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'fechaAsignacion')
    search_fields = ('usuario__username', 'rol__nombre')
    list_filter = ('rol',)
    ordering = ('fechaAsignacion',)

@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ('rol', 'permiso', 'estado')
    search_fields = ('rol__nombre', 'permiso__accion')
    list_filter = ('estado',)
    ordering = ('rol',)

@admin.register(Bitacora)
class BitacoraAdmin(admin.ModelAdmin):
    list_display = ('login', 'idUsuario', 'fecha', 'login_at', 'logout_at')
    search_fields = ('login', 'idUsuario__username')
    list_filter = ('idUsuario',)
    ordering = ('fecha',)

@admin.register(DetalleBitacora)
class DetalleBitacoraAdmin(admin.ModelAdmin):
    list_display = ('accion', 'tabla', 'fecha', 'idBitacora')
    search_fields = ('accion', 'tabla')
    list_filter = ('tabla',)
    ordering = ('fecha',)
