from django.contrib import admin
from .models import Caso, EquipoCaso, ParteProcesal, Expediente, Carpeta

# Registro de modelos en el admin

@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = ('nroCaso', 'tipoCaso', 'estado', 'prioridad', 'fechaInicio', 'fechaFin', 'creadoEn', 'actualizadoEn')
    search_fields = ('nroCaso', 'tipoCaso', 'descripcion')
    list_filter = ('estado', 'prioridad')
    ordering = ('fechaInicio',)

@admin.register(EquipoCaso)
class EquipoCasoAdmin(admin.ModelAdmin):
    list_display = ('actor', 'caso', 'rolEnEquipo', 'fechaAsignacion', 'fechaSalida')
    search_fields = ('actor__nombres', 'actor__apellidoPaterno', 'caso__nroCaso', 'rolEnEquipo')
    list_filter = ('rolEnEquipo', 'caso__estado')

@admin.register(ParteProcesal)
class ParteProcesalAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'caso', 'rolProcesal', 'estado', 'fechaInicio', 'fechaFin')
    search_fields = ('cliente__actor__nombres', 'cliente__actor__apellidoPaterno', 'caso__nroCaso', 'rolProcesal')
    list_filter = ('rolProcesal', 'estado')

@admin.register(Expediente)
class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('nroExpediente', 'caso', 'estado', 'fechaCreacion')
    search_fields = ('nroExpediente', 'caso__nroCaso')
    list_filter = ('estado',)
    ordering = ('fechaCreacion',)

@admin.register(Carpeta)
class CarpetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'expediente', 'estado', 'carpetaPadre', 'creadoEn', 'actualizadoEn')
    search_fields = ('nombre', 'expediente__nroExpediente', 'estado')
    list_filter = ('estado', 'carpetaPadre')
    ordering = ('creadoEn',)
