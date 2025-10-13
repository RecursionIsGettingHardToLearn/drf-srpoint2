from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TipoDocumentoViewSet, EtapaProcesalViewSet, DocumentoViewSet, VersionDocumentoViewSet

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'tipos_documentos', TipoDocumentoViewSet)
router.register(r'etapas_procesales', EtapaProcesalViewSet)
router.register(r'documentos', DocumentoViewSet)
router.register(r'versiones_documentos', VersionDocumentoViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Incluimos las rutas generadas automáticamente
]
