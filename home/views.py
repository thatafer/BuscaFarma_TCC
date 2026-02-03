from django.shortcuts import render
from medicamentos.models import Medicamento
from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404
from medicamentos.models import Medicamento
from noticias.models import Noticia  # importe seu modelo de notícias

from django.shortcuts import render, get_object_or_404
from medicamentos.models import Medicamento
from noticias.models import Noticia
from postos.models import Posto  # importe seu modelo de postos

from area_admin.models import Estoque, PostoSaude
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import redirect
from .models import Reserva

from django.contrib.messages import constants
from django.contrib import messages

#pesquisa resolvida :)
def home(request):
    estoque = Estoque.objects.all()
    medicamentos = Estoque.objects.all()  # usado como valor inicial
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    postos = Posto.objects.all()
    postos_pesquisa = PostoSaude.objects.all()
    pesquisa = False

    nome = None
    posto_id = None

    # começamos de um queryset base e adicionamos filtros condicionalmente
    queryset = Estoque.objects.all()

    if request.method == "POST":
        nome = (request.POST.get('medicamento') or "").strip()
        posto_id = request.POST.get('posto')

        if nome:
            queryset = queryset.filter(nome_medicamento__icontains=nome)
            pesquisa = True

        if posto_id:
            try:
                pid = int(posto_id)
                queryset = queryset.filter(posto_saude_id=pid)
                pesquisa = True
            except (TypeError, ValueError):
                # posto inválido — ignora o filtro
                pass

    medicamentos = queryset

    context = {
        "estoque": estoque,
        "postos_pesquisa": postos_pesquisa,
        "medicamentos": medicamentos,
        "noticias": noticias,
        "postos": postos,
        "pesquisa": pesquisa,
        "nome": nome,
        "posto_id": posto_id,
    }

    return render(request, "home/home.html", context)



def reservar_medicamento(request, id, id2):
    if not request.user.is_authenticated:
        messages.add_message(request, constants.ERROR, "Você precisa estar logado para reservar um medicamento.")
        return redirect('home')
    
    if request.method == 'POST':

        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        rg = request.POST.get('rg')
        cpf = request.POST.get('cpf')
        quantidade = request.POST.get('quantidade')
        num_cartao = request.POST.get('num_cartao')
        foto_cartao = request.FILES.get('foto_cartao')
        foto_receita = request.FILES.get('foto_receita')

        medicamento = Estoque.objects.get(id_medicamento=id)
        posto = PostoSaude.objects.get(id=id2)

        #Verificações dos campos

        if len(nome) < 3:
            messages.add_message(request, constants.ERROR, "O nome está incompleto.")
            return redirect('reserva', id=id, id2=id2)
        
        telefone_limpo = ''.join(ch for ch in telefone if ch.isdigit()) #somente números serão contados
        if len(telefone_limpo) < 11:
            messages.add_message(request, constants.ERROR, "O número de telefone está incompleto.")
            return redirect('reserva', id=id, id2=id2)

        if '(' not in telefone or ')' not in telefone:
            messages.add_message(request, constants.ERROR, "O número de telefone deve conter DDD entre parênteses.")
            return redirect('reserva', id=id, id2=id2)

        rg_limpo = ''.join(ch for ch in rg if ch.isdigit()) #somente números serão contados
        if len(rg_limpo) < 9:
            messages.add_message(request, constants.ERROR, "O RG está incompleto.")
            return redirect('reserva', id=id, id2=id2)

        cpf_limpo = ''.join(ch for ch in cpf if ch.isdigit()) #somente números serão contados
        if len(cpf_limpo) < 11:
            messages.add_message(request, constants.ERROR, "O CPF está incompleto.")
            return redirect('reserva', id=id, id2=id2)

        if int(quantidade) > medicamento.quantidade:
            messages.add_message(request, constants.ERROR, "A quantidade solicitada não está disponível no estoque.")
            return redirect('reserva', id=id, id2=id2)
    
        cartao_limpo = ''.join(ch for ch in num_cartao if ch.isdigit()) #somente números serão contados
        if len(cartao_limpo) < 15:
            messages.add_message(request, constants.ERROR, "O número do Cartão SUS está incompleto.")
            return redirect('reserva', id=id, id2=id2)


        reserva = Reserva.objects.create(
            usuario = request.user, #usuário que está logado
            medicamento = medicamento,
            posto = posto, 
            nome = nome,
            telefone = telefone,
            rg = rg,
            cpf = cpf,
            quantidade = quantidade,
            num_cartao = num_cartao,
            foto_cartao = foto_cartao,
            receita = foto_receita,
            status = 'PENDENTE',
        )
        
        reserva.save()
        messages.add_message(request, constants.SUCCESS, "Reserva feita com sucesso!")

    return render(request, 'home/reserva.html')


def noticia_detalhe(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, "home/noticia_detalhe.html", {"noticia": noticia})

def posto_detalhe(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    return render(request, 'home/posto_detalhe.html', {'posto': posto})

def comentarios(request):
    return HttpResponse("Página de comentários em construção.")