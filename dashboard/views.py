from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count
from casos.models import Caso
from documentos.models import Documento, VersionDocumento
# Si necesitas datos del actor:
from actores.models import Actor

class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/panel.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # KPIs globales básicos
        ctx["total_casos"] = Caso.objects.count()
        ctx["total_documentos"] = Documento.objects.count()
        ctx["total_versiones"] = VersionDocumento.objects.count()

        # KPIs del usuario (si tiene Actor):
        actor = getattr(self.request.user, "actor", None)
        if actor:
            casos_usuario = Caso.objects.filter(equipocaso__actor=actor).distinct()
            ctx["mis_casos"] = casos_usuario.count()
            ctx["mis_documentos"] = Documento.objects.filter(
                carpeta__expediente__caso__in=casos_usuario
            ).count()
        else:
            ctx["mis_casos"] = 0
            ctx["mis_documentos"] = 0

        # Ranking simple (top 5 por # documentos)
        ctx["top_casos_docs"] = (
            Caso.objects.annotate(num_docs=Count("expediente__carpetas__documentos"))
                .order_by("-num_docs")[:5]
        )
        return ctx

