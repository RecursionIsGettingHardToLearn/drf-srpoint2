from django.contrib import admin
from .models import Actor, Abogado, Cliente, Asistente

# Registro de modelos en el admin
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidoPaterno', 'tipoActor', 'estadoActor', 'ci', 'telefono', 'direccion', 'creadoEn', 'actualizadoEn')
    search_fields = ('nombres', 'apellidoPaterno', 'ci')
    list_filter = ('tipoActor', 'estadoActor')
    ordering = ('nombres', 'apellidoPaterno')

@admin.register(Abogado)
class AbogadoAdmin(admin.ModelAdmin):
    list_display = ('actor', 'nroCredencial', 'especialidad', 'estadoLicencia')
    search_fields = ('actor__nombres', 'actor__apellidoPaterno', 'nroCredencial', 'especialidad')
    list_filter = ('estadoLicencia',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('actor', 'tipoCliente', 'observaciones')
    search_fields = ('actor__nombres', 'actor__apellidoPaterno', 'tipoCliente')
    list_filter = ('tipoCliente',)

@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('actor', 'area', 'cargo')
    search_fields = ('actor__nombres', 'actor__apellidoPaterno', 'area', 'cargo')
    list_filter = ('area', 'cargo')
