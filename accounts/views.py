from django.shortcuts import render, redirect
from seguridad.models import Usuario, Rol, UsuarioRol
from actores.models import Actor
from django.contrib import messages
from .forms import UserCreateForm, RoleForm, RoleAssignForm, ActorForm, AbogadoForm, ClienteForm, AsistenteForm
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse



# Create your views here.
# accounts/views.py
from django.http import HttpResponse

# Con esto mostramos la lista de usuarios

def users_list(request):
   
    q = request.GET.get("q", "").strip()
    users = Usuario.objects.all().order_by("-date_joined")

    if q:
        users = users.filter(username__icontains=q) | users.filter(email__icontains=q)

    context = {"users": users, "q": q}
    return render(request, "accounts/users_list.html", context)


# Creacion de un nuevo USUARIO 

def user_create(request):

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("accounts:user_list")
    else:
        form = UserCreateForm()

    return render(request, "accounts/user_form.html", {"form": form})


# Listar roles existentes
def roles_list(request):
    roles = Rol.objects.all().order_by("nombre")
    return render(request, "accounts/roles_list.html", {"roles": roles})


# Crear un nuevo rol
def role_create(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol creado correctamente.")
            return redirect("accounts:roles_list")
    else:
        form = RoleForm()
    return render(request, "accounts/role_form.html", {"form": form})


# Asignar roles a un usuario
@transaction.atomic
def assign_roles(request, user_id):
    from seguridad.models import Usuario
    usuario = get_object_or_404(Usuario, pk=user_id)

    if request.method == "POST":
        form = RoleAssignForm(request.POST, usuario=usuario)
        if form.is_valid():
            nuevos = set(form.cleaned_data["roles"])
            actuales = set(Rol.objects.filter(usuariorol__usuario=usuario))

            # Añadir roles nuevos
            for r in nuevos - actuales:
                UsuarioRol.objects.create(usuario=usuario, rol=r)

            # Eliminar roles removidos
            UsuarioRol.objects.filter(usuario=usuario, rol__in=(actuales - nuevos)).delete()

            messages.success(request, "Roles actualizados correctamente.")
            return redirect("accounts:user_list")
    else:
        form = RoleAssignForm(usuario=usuario)

    return render(request, "accounts/assign_roles.html", {"form": form, "usuario": usuario})

# Crear un nuevo Actor asociado a un Usuario

def actor_create(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)

    if hasattr(usuario, "actor"):
        messages.warning(request, "Este usuario ya tiene un actor asociado.")
        return redirect("accounts:user_list")

    if request.method == "POST":
        form = ActorForm(request.POST)
        if form.is_valid():
            actor = form.save(commit=False)
            actor.usuario = usuario
            actor.save()
            messages.success(request, f"Actor creado: {actor.tipoActor} para {usuario.username}.")

            # Redirigir según el tipoActor
            if actor.tipoActor.upper() == "ABOGADO":
                return redirect("accounts:abogado_create", actor_id=actor.id)
            elif actor.tipoActor.upper() == "CLIENTE":
                return redirect("accounts:cliente_create", actor_id=actor.id)
            elif actor.tipoActor.upper() == "ASISTENTE":
                return redirect("accounts:asistente_create", actor_id=actor.id)

            return redirect("accounts:user_list")
    else:
        form = ActorForm()

    return render(request, "accounts/actor_form.html", {"form": form, "usuario": usuario})


# LISTA DE LOS ACTORES CREADOS

def actors_list(request):
    """
    Lista todos los actores, con indicador de si tienen datos específicos completos.
    """
    tipo = request.GET.get("tipo", "").upper().strip()
    actores = Actor.objects.select_related("usuario").all().order_by("tipoActor", "nombres")

    if tipo in ["ABOGADO", "CLIENTE", "ASISTENTE"]:
        actores = actores.filter(tipoActor=tipo)

    # Marcamos si tiene datos específicos creados
    actores_data = []
    for actor in actores:
        info_completa = False
        enlace_completar = None

        if actor.tipoActor.upper() == "ABO":
            if hasattr(actor, "abogado"):
                info_completa = True
            else:
                enlace_completar = reverse("accounts:abogado_create", args=[actor.id])
        elif actor.tipoActor.upper() == "CLI":
            if hasattr(actor, "cliente"):
                 info_completa = True
            else:
                 enlace_completar = reverse("accounts:cliente_create", args=[actor.id])
        elif actor.tipoActor.upper() == "ASI":
            if hasattr(actor, "asistente"):
                info_completa = True
            else:
                enlace_completar = reverse("accounts:asistente_create", args=[actor.id])

        actores_data.append({
            "actor": actor,
            "info_completa": info_completa,
            "enlace_completar": enlace_completar,
        })

    context = {
        "actores_data": actores_data,
        "tipo": tipo,
    }
    return render(request, "accounts/actors_list.html", context)



# CREACION DE LAS CLASES GENERALIZADAS: ABOGADO, CLIENTE, ASISTENTE

def abogado_create(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    if hasattr(actor, "abogado"):
        messages.info(request, "Ya existe un registro de Abogado para este actor.")
        return redirect("accounts:actors_list")

    if request.method == "POST":
        form = AbogadoForm(request.POST)
        if form.is_valid():
            ab = form.save(commit=False)
            ab.idActor = actor
            ab.save()
            messages.success(request, "Datos de abogado guardados correctamente.")
            return redirect("accounts:actors_list")
    else:
        form = AbogadoForm()

    return render(request, "accounts/actor_detail_form.html", {"form": form, "actor": actor, "tipo": "Abogado"})


def cliente_create(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    if hasattr(actor, "cliente"):
        messages.info(request, "Ya existe un registro de Cliente para este actor.")
        return redirect("accounts:actors_list")

    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.idActor = actor
            c.save()
            messages.success(request, "Datos de cliente guardados correctamente.")
            return redirect("accounts:actors_list")
    else:
        form = ClienteForm()

    return render(request, "accounts/actor_detail_form.html", {"form": form, "actor": actor, "tipo": "Cliente"})


def asistente_create(request, actor_id):
    actor = get_object_or_404(Actor, pk=actor_id)
    if hasattr(actor, "asistente"):
        messages.info(request, "Ya existe un registro de Asistente para este actor.")
        return redirect("accounts:actors_list")

    if request.method == "POST":
        form = AsistenteForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.idActor = actor
            a.save()
            messages.success(request, "Datos de asistente guardados correctamente.")
            return redirect("accounts:actors_list")
    else:
        form = AsistenteForm()

    return render(request, "accounts/actor_detail_form.html", {"form": form, "actor": actor, "tipo": "Asistente"})