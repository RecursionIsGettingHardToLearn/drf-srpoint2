
#TipoDocumentoViewSet
from rest_framework import viewsets
from .models import TipoDocumento
from .serializers import TipoDocumentoSerializer

class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

#EtapaProcesalViewSet
from .models import EtapaProcesal
from .serializers import EtapaProcesalSerializer

class EtapaProcesalViewSet(viewsets.ModelViewSet):
    queryset = EtapaProcesal.objects.all()
    serializer_class = EtapaProcesalSerializer

#DocumentoViewSet
from .models import Documento
from .serializers import DocumentoSerializer

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

#VersionDocumentoViewSet
from .models import VersionDocumento
from .serializers import VersionDocumentoSerializer

class VersionDocumentoViewSet(viewsets.ModelViewSet):
    queryset = VersionDocumento.objects.all()
    serializer_class = VersionDocumentoSerializer
