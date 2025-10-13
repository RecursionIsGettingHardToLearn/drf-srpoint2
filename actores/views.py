from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Actor, Abogado, Cliente, Asistente
from .serializers import ActorSerializer, AbogadoSerializer, ClienteSerializer, AsistenteSerializer

# ==========================
# Actor ViewSet
# ==========================
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    # Puedes agregar métodos personalizados aquí si es necesario
    # Ejemplo de un endpoint adicional (si lo necesitaras)
    @action(detail=True, methods=['get'])
    def obtener_nombre(self, request, pk=None):
        actor = self.get_object()
        return Response({"nombre_completo": f"{actor.nombres} {actor.apellidoPaterno} {actor.apellidoMaterno}"})

# ==========================
# Abogado ViewSet
# ==========================
class AbogadoViewSet(viewsets.ModelViewSet):
    queryset = Abogado.objects.all()
    serializer_class = AbogadoSerializer

# ==========================
# Cliente ViewSet
# ==========================
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

# ==========================
# Asistente ViewSet
# ==========================
class AsistenteViewSet(viewsets.ModelViewSet):
    queryset = Asistente.objects.all()
    serializer_class = AsistenteSerializer
