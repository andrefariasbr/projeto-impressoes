from django.urls import path
from impressoes.views import painel_professor
from usuarios.views import CustomLoginView

from .views import registro_view, painel_admin, logout_view
from . import views

urlpatterns = [
    path("painel_professor/", painel_professor, name="painel_professor"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("registro/", registro_view, name="registro"),
    path("painel_usuarios/", painel_admin, name="painel_usuarios"),
    path(
        "editar/<int:usuario_id>/",
        views.editar_usuario,
        name="editar_usuario",
    ),
    path(
        "excluir/<int:usuario_id>/",
        views.excluir_usuario,
        name="excluir_usuario",
    ),
    path("logout/", logout_view, name="logout"),
]
