from django.urls import path
from . import views

urlpatterns = [
    path("criar/", views.criar_pedido, name="criar_pedido"),
    path("painel/", views.painel_admin, name="painel_admin"),
    path("painel-admin/", views.painel_admin, name="painel_admin_alias"),
    path("meus-envios/", views.painel_professor, name="painel_professor"),
    path(
        "pedido/<int:pedido_id>/admin/",
        views.detalhar_pedido_admin,
        name="detalhar_pedido_admin",
    ),
    path(
        "pedido/<int:pedido_id>/professor/",
        views.detalhar_pedido_professor,
        name="detalhar_pedido_professor",
    ),
    path("pedido/<int:pedido_id>/editar/", views.editar_pedido, name="editar_pedido"),
]
