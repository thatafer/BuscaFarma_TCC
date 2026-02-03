from django import forms
from django.contrib.auth.models import User

class AtualizacaoDeUsuario(forms.ModelForm):
    username = forms.CharField(
        label='Nome de usuário',
        help_text='',  # Remove help text
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name']
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'first_name': 'Nome',
        }