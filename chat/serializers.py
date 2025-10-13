from rest_framework import serializers
from .models import Conversacion

class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ['id', 'usuario', 'titulo', 'fecha_creacion', 'fecha_actualizacion', 'activa']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Evitamos campos anidados, solo representamos el usuario como texto
        representation['usuario'] = instance.usuario.username  # solo nombre de usuario
        return representation
from rest_framework import serializers
from .models import Mensaje

class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = ['id', 'conversacion', 'tipo', 'contenido', 'fecha_envio', 'tokens_usados', 'tiempo_respuesta', 'documentos_consultados', 'entidades_extraidas']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Evitamos campos anidados, solo representamos la conversación y tipo como texto
        representation['conversacion'] = instance.conversacion.id  # solo ID de la conversación
        representation['tipo'] = instance.get_tipo_display()  # Mostramos el tipo en forma legible
        return representation
from rest_framework import serializers
from .models import ConsultaDocumento

class ConsultaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaDocumento
        fields = ['id', 'mensaje', 'documento', 'caso', 'actor', 'tipo_consulta', 'resultado', 'relevancia']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Evitamos campos anidados, solo representamos las relaciones como IDs
        representation['mensaje'] = instance.mensaje.id  # solo ID del mensaje
        representation['documento'] = instance.documento.id if instance.documento else None  # solo ID del documento
        representation['caso'] = instance.caso.id if instance.caso else None  # solo ID del caso
        representation['actor'] = instance.actor.id if instance.actor else None  # solo ID del actor
        return representation
from rest_framework import serializers
from .models import ConfiguracionIA

class ConfiguracionIASerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionIA
        fields = ['id', 'nombre', 'modelo_openai', 'temperatura', 'max_tokens', 'contexto_sistema', 'activo', 'fecha_creacion', 'fecha_actualizacion']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Evitamos campos anidados, solo representamos el nombre del modelo OpenAI
        return representation
