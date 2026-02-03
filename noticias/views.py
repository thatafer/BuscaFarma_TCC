from django.shortcuts import render
from .models import Noticia 

# Create your views here.
def pagina_noticias(request):
    if request.method == 'GET':
        noticias = Noticia.objects.order_by('-data_publicacao')
        return render(request, 'noticias.html', {'noticias': noticias})