from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

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
]
