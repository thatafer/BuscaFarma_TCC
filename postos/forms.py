from django import forms
from .models import Posto

class PostoForm(forms.ModelForm):
    class Meta:
        model = Posto
        fields = [
            'nome', 'imagem', 'endereco', 'bairro', 'cep',
            'telefone1', 'telefone2', 'horario_semana', 
            'horario_sabado', 'horario_domingo'
        ]
