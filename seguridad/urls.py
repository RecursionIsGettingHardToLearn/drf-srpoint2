# urls.py en tu aplicación (por ejemplo, seguridad)
from django.urls import path
from . import views  # Importa las vistas desde views.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, UsuarioViewSet,LogoutView,RolViewSet, PermisoViewSet, UsuarioRolViewSet, RolPermisoViewSet, BitacoraViewSet, DetalleBitacoraViewSet
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "seguridad"
urlpatterns = [
]

# Crear el router y registrar los viewsets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'roles', RolViewSet)
router.register(r'permisos', PermisoViewSet)
router.register(r'usuarios_roles', UsuarioRolViewSet)
router.register(r'roles_permisos', RolPermisoViewSet)
router.register(r'bitacoras', BitacoraViewSet)
router.register(r'detalles_bitacora', DetalleBitacoraViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Incluimos las rutas generadas automáticamente
    #path('login/', LoginView.as_view(), name='login'),
    #path('csrf-token/', views.CSRFTokenView.as_view(), name='csrf_token'),  
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]
