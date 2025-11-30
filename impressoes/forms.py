
from django import forms
from .models import PedidoDeImpressao


class PedidoDeImpressaoForm(forms.ModelForm):
    arquivos = forms.FileField(
        required=False,
        label='Arquivo',
        widget=forms.ClearableFileInput()
    )

    class Meta:
        model = PedidoDeImpressao
        fields = [
            'quantidade_documentos',
            'quantidade_folhas',
            'frente_verso',
            'grampear',
            'tipo_impressao',
            'observacao',
        ]
