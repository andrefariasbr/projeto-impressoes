from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.utils.http import urlencode
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.db.models import Q
from .forms import UsuarioCreationForm
from .models import Usuario


# Middleware para mensagem automática ao redirecionar para login
class LoginRequiredMessageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if (
            request.path == settings.LOGIN_URL
            and "next" in request.GET
            and not request.user.is_authenticated
        ):
            if not any(
                m.message == "Você precisa estar logado para acessar esta página."
                for m in messages.get_messages(request)
            ):
                messages.warning(
                    request, "Você precisa estar logado para acessar esta página."
                )
        return None


# Views de autenticação
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        senha = request.POST["senha"]
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            login(request, user)
            if user.tipo == "professor":
                return redirect("/painel_professor/")
            elif user.tipo == "admin":
                return redirect("/painel_admin/")
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return render(request, "usuarios/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"

    def form_invalid(self, form):
        messages.error(
            self.request, "Usuário ou senha inválidos, ou tipo de usuário não definido."
        )
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, "tipo") and user.tipo:
            if user.tipo == "professor":
                return "/impressoes/meus-envios/"
            elif user.tipo == "admin":
                return "/impressoes/painel/"
        messages.error(
            self.request,
            "Seu perfil não possui tipo definido. Contate o administrador.",
        )
        return "/usuarios/login/"


# Views de registro e painel de usuários
def registro_view(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário registrado com sucesso!")
            return redirect("login")
    else:
        form = UsuarioCreationForm()
    return render(request, "usuarios/registro.html", {"form": form})


@login_required
@permission_required("usuarios.can_manage_users", raise_exception=True)
def painel_admin(request):
    query = request.GET.get("q", "")
    tipo = request.GET.get("tipo", "")
    usuarios = Usuario.objects.all()
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query)
            | Q(email__icontains=query)
            | Q(cpf__icontains=query)
        )
    if tipo:
        usuarios = usuarios.filter(tipo=tipo)
    return render(request, "usuarios/painel_admin.html", {"usuarios": usuarios})


# Views de edição e exclusão de usuário
@login_required
@permission_required("usuarios.can_manage_users", raise_exception=True)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect(reverse("painel_usuarios"))
    else:
        form = UsuarioCreationForm(instance=usuario)
    return render(
        request,
        "usuarios/registro.html",
        {"form": form, "edicao": True, "usuario": usuario},
    )


@login_required
@permission_required("usuarios.can_manage_users", raise_exception=True)
def excluir_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuário excluído com sucesso!")
        return redirect(reverse("painel_usuarios"))
    return redirect(reverse("painel_usuarios"))
