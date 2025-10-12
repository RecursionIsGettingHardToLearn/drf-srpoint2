from django import forms
from .models import Caso,EquipoCaso,ParteProcesal

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ["nroCaso", "tipoCaso", "descripcion", "estado", "prioridad", "fechaInicio", "fechaFin"]
        widgets = {
            "nroCaso": forms.TextInput(attrs={"class": "form-control"}),
            "tipoCaso": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.Select(choices=[
                ("ABIERTO", "Abierto"),
                ("CERRADO", "Cerrado"),
            ], attrs={"class": "form-control"}),
            "prioridad": forms.Select(choices=[
                ("ALTA", "Alta"),
                ("MEDIA", "Media"),
                ("BAJA", "Baja"),
            ], attrs={"class": "form-control"}),
            "fechaInicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fechaFin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class EquipoCasoForm(forms.ModelForm):
    class Meta:
        model = EquipoCaso
        fields = ["actor", "rolEnEquipo", "observaciones", "fechaAsignacion", "fechaSalida"]
        widgets = {
            "actor": forms.Select(attrs={"class": "form-control"}),
            "rolEnEquipo": forms.Select(attrs={"class": "form-control"}),
            "observaciones": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "fechaAsignacion": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fechaSalida": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

class ParteProcesalForm(forms.ModelForm):
    class Meta:
        model = ParteProcesal
        fields = ["cliente", "rolProcesal", "estado", "fechaInicio", "fechaFin"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "rolProcesal": forms.Select(attrs={"class": "form-control"}),
            "estado": forms.Select(attrs={"class": "form-control"}, choices=[
                ("ACTIVO", "Activo"),
                ("INACTIVO", "Inactivo"),
            ]),
            "fechaInicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fechaFin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }