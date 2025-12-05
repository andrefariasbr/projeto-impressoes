from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import PedidoDeImpressao, ArquivoPedido
from .forms import PedidoDeImpressaoForm


# View para editar pedido de impressão
@login_required
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(
        PedidoDeImpressao, id=pedido_id, usuario=request.user
    )
    if pedido.status != "pendente":
        messages.error(request, "Só é possível editar pedidos pendentes.")
        return redirect("painel_professor")
    if request.method == "POST":
        form = PedidoDeImpressaoForm(
            request.POST, request.FILES, instance=pedido
        )
        if form.is_valid():
            form.save()
            # Atualizar arquivos se enviados
            arquivos = request.FILES.getlist("arquivos")
            if arquivos:
                ArquivoPedido.objects.filter(pedido=pedido).delete()
                for arq in arquivos:
                    ArquivoPedido.objects.create(pedido=pedido, arquivo=arq)
            messages.success(request, "Pedido editado com sucesso!")
            return redirect("painel_professor")
    else:
        form = PedidoDeImpressaoForm(instance=pedido)
    return render(
        request,
        "impressoes/editar_pedido.html",
        {"form": form, "pedido": pedido},
    )


# Função para verificar se o usuário é admin
def is_admin(user):
    return user.is_authenticated and (
        hasattr(user, "tipo") and user.tipo == "admin"
    )


# Detalhar pedido para administrador (com ações)
@user_passes_test(is_admin)
def detalhar_pedido_admin(request, pedido_id):
    pedido = get_object_or_404(PedidoDeImpressao, id=pedido_id)
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "aprovar":
            pedido.status = "concluido"
            pedido.save()
            messages.success(request, "Pedido concluído!")
        elif acao == "rejeitar":
            pedido.status = "rejeitado"
            pedido.save()
            messages.success(request, "Pedido rejeitado!")
        elif acao == "excluir":
            pedido.delete()
            messages.success(request, "Pedido excluído!")
            return redirect("painel_admin")
        return redirect("detalhar_pedido_admin", pedido_id=pedido.id)
    return render(
        request, "impressoes/detalhar_pedido_admin.html", {"pedido": pedido}
    )


# Detalhar pedido para professor (apenas visualização)
@login_required
def detalhar_pedido_professor(request, pedido_id):
    pedido = get_object_or_404(
        PedidoDeImpressao, id=pedido_id, usuario=request.user
    )
    return render(
        request,
        "impressoes/detalhar_pedido_professor.html",
        {"pedido": pedido},
    )


@login_required
def criar_pedido(request):
    if request.method == "POST":
        form = PedidoDeImpressaoForm(request.POST, request.FILES)
        if form.is_valid():
            pedido = PedidoDeImpressao.objects.create(
                usuario=request.user,
                observacao=form.cleaned_data["observacao"],
                quantidade_documentos=form.cleaned_data[
                    "quantidade_documentos"
                ],
                quantidade_folhas=form.cleaned_data["quantidade_folhas"],
                frente_verso=form.cleaned_data["frente_verso"],
                grampear=form.cleaned_data["grampear"],
                tipo_impressao=form.cleaned_data["tipo_impressao"],
            )
            arquivos = request.FILES.getlist("arquivos")
            for arq in arquivos:
                ArquivoPedido.objects.create(pedido=pedido, arquivo=arq)
            messages.success(
                request, "Pedido de impressão enviado com sucesso!"
            )
            return redirect("painel_professor")
        else:
            messages.error(
                request, "Preencha todos os campos obrigatórios corretamente."
            )
    else:
        form = PedidoDeImpressaoForm()
    return render(request, "impressoes/criar_pedido.html", {"form": form})


def is_admin(user):
    return user.is_authenticated and (
        hasattr(user, "tipo") and user.tipo == "admin"
    )


@login_required
def painel_admin(request):
    if not is_admin(request.user):
        messages.error(request, "Acesso restrito ao painel do administrador.")
        return redirect("painel_professor")
    status = request.GET.get("status", "")
    busca = request.GET.get("q", "")
    pedidos = PedidoDeImpressao.objects.all().order_by("-data_criacao")
    if status:
        pedidos = pedidos.filter(status=status)
    if busca:
        pedidos = pedidos.filter(
            Q(usuario__username__icontains=busca)
            | Q(arquivos__arquivo__icontains=busca)
        )
    paginator = Paginator(pedidos, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Contagem dos pedidos por status
    total_pendentes = PedidoDeImpressao.objects.filter(
        status="pendente"
    ).count()
    total_rejeitados = PedidoDeImpressao.objects.filter(
        status="rejeitado"
    ).count()
    total_entregues = PedidoDeImpressao.objects.filter(
        status="concluido"
    ).count()

    if request.method == "POST":
        acao = request.POST.get("acao")
        pedido_id = request.POST.get("pedido_id")
        pedido = PedidoDeImpressao.objects.get(id=pedido_id)
        if acao == "aprovar":
            pedido.status = "concluido"
            pedido.save()
            messages.success(request, "Pedido concluído!")
        elif acao == "rejeitar":
            pedido.status = "rejeitado"
            pedido.save()
            messages.success(request, "Pedido rejeitado!")
        elif acao == "excluir":
            pedido.delete()
            messages.success(request, "Pedido excluído!")
        return redirect("painel_admin")
    return render(
        request,
        "impressoes/painel_admin.html",
        {
            "pedidos": page_obj,
            "page_obj": page_obj,
            "status": status,
            "busca": busca,
            "total_pendentes": total_pendentes,
            "total_rejeitados": total_rejeitados,
            "total_entregues": total_entregues,
        },
    )


@login_required
def painel_professor(request):
    if not hasattr(request.user, "tipo") or request.user.tipo != "professor":
        messages.error(request, "Acesso restrito ao painel do professor.")
        return redirect("painel_admin")
    status = request.GET.get("status", "")
    busca = request.GET.get("q", "")
    pedidos = PedidoDeImpressao.objects.filter(usuario=request.user).order_by(
        "-data_criacao"
    )
    if status:
        pedidos = pedidos.filter(status=status)
    if busca:
        pedidos = pedidos.filter(arquivos__arquivo__icontains=busca)

    paginator = Paginator(pedidos, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Contadores para o painel do professor
    total_impressoes = PedidoDeImpressao.objects.filter(
        usuario=request.user
    ).count()
    total_pendentes = PedidoDeImpressao.objects.filter(
        usuario=request.user, status="pendente"
    ).count()
    total_entregues = PedidoDeImpressao.objects.filter(
        usuario=request.user, status="concluido"
    ).count()

    if request.method == "POST":
        acao = request.POST.get("acao")
        pedido_id = request.POST.get("pedido_id")
        pedido = PedidoDeImpressao.objects.get(
            id=pedido_id, usuario=request.user
        )
        if acao == "excluir":
            pedido.delete()
            messages.success(request, "Pedido excluído!")
        return redirect("painel_professor")
    return render(
        request,
        "impressoes/painel_professor.html",
        {
            "pedidos": page_obj,
            "page_obj": page_obj,
            "status": status,
            "busca": busca,
            "total_impressoes": total_impressoes,
            "total_pendentes": total_pendentes,
            "total_entregues": total_entregues,
        },
    )
