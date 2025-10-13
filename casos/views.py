from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Caso
from .forms import CasoForm, EquipoCasoForm, ParteProcesalForm
from actores.models import Actor, Cliente
from rest_framework import viewsets
def caso_list(request):
    casos = Caso.objects.all().order_by("-fechaInicio")
    return render(request, "casos/caso_list.html", {"casos": casos})

def caso_create(request):
    if request.method == "POST":
        form = CasoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Caso creado correctamente.")
            return redirect("casos:case_list")
    else:
        form = CasoForm()
    return render(request, "casos/caso_form.html", {"form": form})

def caso_edit(request, pk):
    caso = get_object_or_404(Caso, pk=pk)
    if request.method == "POST":
        form = CasoForm(request.POST, instance=caso)
        if form.is_valid():
            form.save()
            messages.success(request, "Caso actualizado correctamente.")
            return redirect("casos:case_list")
    else:
        form = CasoForm(instance=caso)
    return render(request, "casos/caso_form.html", {"form": form, "caso": caso})


# ======= EQUIPO DE CASO ======= #
def equipo_caso_list(request, caso_id):
    caso = get_object_or_404(Caso, pk=caso_id)
    equipo = caso.equipocaso_set.select_related("actor")
    return render(request, "casos/equipo_list.html", {"caso": caso, "equipo": equipo})


def equipo_caso_add(request, caso_id):
    caso = get_object_or_404(Caso, pk=caso_id)
    if request.method == "POST":
        form = EquipoCasoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.caso = caso
            equipo.save()
            messages.success(request, "Actor agregado al equipo del caso.")
            return redirect("casos:equipo_list", caso_id=caso.id)
    else:
        form = EquipoCasoForm()
    return render(request, "casos/equipo_form.html", {"form": form, "caso": caso})


# ======= PARTE PROCESAL ======= #
def parte_procesal_list(request, caso_id):
    caso = get_object_or_404(Caso, pk=caso_id)
    partes = caso.parteprocesal_set.select_related("cliente")
    return render(request, "casos/parte_list.html", {"caso": caso, "partes": partes})


def parte_procesal_add(request, caso_id):
    caso = get_object_or_404(Caso, pk=caso_id)
    if request.method == "POST":
        form = ParteProcesalForm(request.POST)
        if form.is_valid():
            parte = form.save(commit=False)
            parte.caso = caso
            parte.save()
            messages.success(request, "Parte procesal añadida correctamente.")
            return redirect("casos:parte_list", caso_id=caso.id)
    else:
        form = ParteProcesalForm()
    return render(request, "casos/parte_form.html", {"form": form, "caso": caso})

