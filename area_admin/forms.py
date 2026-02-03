from django import forms
from postos.models import Posto
from noticias.models import Noticia

class TokenForm(forms.Form):
    token = forms.CharField(label="Digite o token", max_length=50, widget=forms.PasswordInput)

class PostoForm(forms.ModelForm):
    class Meta:
        model = Posto
        fields = '__all__'


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'conteudo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control'}),
            'conteudo': forms.Textarea(attrs={'class':'form-control', 'rows':5}),
        }
