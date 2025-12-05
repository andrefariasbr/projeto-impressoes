from django.contrib import admin
from .models import Impressao


@admin.register(Impressao)
class ImpressaoAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "tipo_impressao",
        "quantidade_folhas",
        "frente_verso",
        "grampear",
        "entregue",
    )
