from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm


class UsuarioCreationForm(UserCreationForm):
    tipo = forms.ChoiceField(choices=Usuario.TIPOS, label="Tipo de usuário")
    cpf = forms.CharField(label="CPF", max_length=14, required=True)
    endereco = forms.CharField(label="Endereço", max_length=255, required=True)
    telefone = forms.CharField(label="Telefone", max_length=20, required=True)

    class Meta:
        model = Usuario
        fields = (
            "username",
            "email",
            "tipo",
            "cpf",
            "endereco",
            "telefone",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["password1"].required = False
            self.fields["password2"].required = False
            self.fields["password1"].widget.attrs[
                "placeholder"
            ] = "Deixe em branco para não alterar"
            self.fields["password2"].widget.attrs[
                "placeholder"
            ] = "Deixe em branco para não alterar"

    def save(self, commit=True):
        from django.contrib.auth.models import Group

        user = super().save(commit=False)
        user.tipo = self.cleaned_data["tipo"]
        user.cpf = self.cleaned_data["cpf"]
        user.endereco = self.cleaned_data["endereco"]
        user.telefone = self.cleaned_data["telefone"]
        if commit:
            user.save()
            if user.tipo == "ADMIN":
                grupo = Group.objects.get(name="Administrador")
            else:
                grupo = Group.objects.get(name="Professor")
            user.groups.add(grupo)
        return user
