from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversacionViewSet, MensajeViewSet, ConsultaDocumentoViewSet, ConfiguracionIAViewSet

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'conversaciones', ConversacionViewSet)
router.register(r'mensajes', MensajeViewSet)
router.register(r'consultas_documentos', ConsultaDocumentoViewSet)
router.register(r'configuraciones_ia', ConfiguracionIAViewSet)
app_name = 'chat'

urlpatterns = [
    # Vista principal del chat
    path('', views.ChatView.as_view(), name='chat'),
    
    # API endpoints
    path('api/enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('api/conversacion/<int:conversacion_id>/', views.obtener_conversacion, name='obtener_conversacion'),
    path('api/conversaciones/', views.obtener_conversaciones, name='obtener_conversaciones'),
    path('api/crear-conversacion/', views.crear_conversacion, name='crear_conversacion'),
    path('api/eliminar-conversacion/<int:conversacion_id>/', views.eliminar_conversacion, name='eliminar_conversacion'),
    path('api/sugerencias/', views.obtener_sugerencias, name='obtener_sugerencias'),
    path('', include(router.urls)), 
]
