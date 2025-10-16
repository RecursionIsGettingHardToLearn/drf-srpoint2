from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CasoViewSet, EquipoCasoViewSet, ParteProcesalViewSet, ExpedienteViewSet, CarpetaViewSet

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'casos', CasoViewSet)
router.register(r'equipos_caso', EquipoCasoViewSet)
router.register(r'partes_procesales', ParteProcesalViewSet)
router.register(r'expedientes', ExpedienteViewSet)
router.register(r'carpetas', CarpetaViewSet)

app_name = "casos"

urlpatterns = [
    path("", views.caso_list, name="case_list"),
    path("crear/", views.caso_create, name="case_create"),
    path("<int:pk>/editar/", views.caso_edit, name="case_edit"),
    
    
    # EquipoCaso
    path("<int:caso_id>/equipo/", views.equipo_caso_list, name="equipo_list"),
    path("<int:caso_id>/equipo/agregar/", views.equipo_caso_add, name="equipo_add"),

    # Parte Procesal
    path("<int:caso_id>/partes/", views.parte_procesal_list, name="parte_list"),
    path("<int:caso_id>/partes/agregar/", views.parte_procesal_add, name="parte_add"),
       path('', include(router.urls)), 
]
