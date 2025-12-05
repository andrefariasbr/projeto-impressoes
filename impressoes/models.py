from django.conf import settings
from django.db import models
from usuarios.models import Usuario


class PedidoDeImpressao(models.Model):
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("concluido", "Concluído"),
        ("rejeitado", "Rejeitado"),
    ]
    TIPO_IMPRESSAO_CHOICES = [
        ("pb", "Preto e Branco"),
        ("colorida", "Colorida"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pendente"
    )
    data_criacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True)
    quantidade_documentos = models.PositiveIntegerField(default=1)
    quantidade_folhas = models.PositiveIntegerField(default=1)
    frente_verso = models.BooleanField(default=False)
    grampear = models.BooleanField(default=False)
    tipo_impressao = models.CharField(
        max_length=20, choices=TIPO_IMPRESSAO_CHOICES, default="pb"
    )

    def __str__(self):
        return f"{self.usuario.username} - Pedido {self.id} ({self.status})"


class ArquivoPedido(models.Model):
    pedido = models.ForeignKey(
        PedidoDeImpressao, on_delete=models.CASCADE, related_name="arquivos"
    )
    arquivo = models.FileField(upload_to="impressao/")

    def __str__(self):
        return f"Arquivo de {self.pedido.usuario.username} - Pedido {self.pedido.id}"




class Impressao(models.Model):
    TIPO_IMPRESSAO_CHOICES = [
        ("pb", "Preto e Branco"),
        ("colorida", "Colorida"),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    arquivo = models.FileField(upload_to="impressoes/")
    quantidade_folhas = models.PositiveIntegerField()
    frente_verso = models.BooleanField(default=False)
    grampear = models.BooleanField(default=False)
    tipo_impressao = models.CharField(
        max_length=20, choices=TIPO_IMPRESSAO_CHOICES
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    entregue = models.BooleanField(default=False)
    grampeado = models.BooleanField(default=False)
    envelopado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.arquivo.name}"
