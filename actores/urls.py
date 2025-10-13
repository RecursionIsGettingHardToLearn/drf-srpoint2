from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActorViewSet, AbogadoViewSet, ClienteViewSet, AsistenteViewSet

# Definimos el router y registramos los viewsets
router = DefaultRouter()
router.register(r'actors', ActorViewSet)
router.register(r'abogados', AbogadoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'asistentes', AsistenteViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Incluimos las rutas generadas por el router
]
