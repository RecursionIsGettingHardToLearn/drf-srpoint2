from django.contrib import admin
from .models import TipoDocumento, EtapaProcesal, Documento, VersionDocumento

# Registro de modelos en el admin

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)
    ordering = ('nombre',)

@admin.register(EtapaProcesal)
class EtapaProcesalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'estado')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('estado',)
    ordering = ('nombre',)

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombreDocumento', 'carpeta', 'tipoDocumento', 'etapaProcesal', 'estado', 'fechaDoc', 'tamano', 'palabraClave')
    search_fields = ('nombreDocumento', 'carpeta__nombre', 'tipoDocumento__nombre', 'etapaProcesal__nombre', 'palabraClave')
    list_filter = ('estado', 'carpeta', 'tipoDocumento', 'etapaProcesal')
    ordering = ('fechaDoc',)

@admin.register(VersionDocumento)
class VersionDocumentoAdmin(admin.ModelAdmin):
    list_display = ('documento', 'numeroVersion', 'usuario', 'fechaCambio', 'comentario')
    search_fields = ('documento__nombreDocumento', 'usuario__username', 'comentario')
    list_filter = ('numeroVersion', 'usuario')
    ordering = ('-fechaCambio',)
