from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from .models import PostoSaude, Estoque, Mensagem
from .forms import PostoForm
from django import template
from postos.models import Posto
from django.contrib.auth.decorators import login_required
from noticias.models import Noticia
from .forms import NoticiaForm  
from medicamentos.models import Medicamento
from home.models import Reserva
from django.contrib.messages import constants

def listar_medicamento(request):
    token = request.session.get('token')
    if not token:
        messages.error(request, 'Você precisa autenticar o token primeiro!')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    medicamentos = Estoque.objects.filter(posto_saude=posto)
    return render(request, 'area_admin_medicamentos/listar_medicamento.html', {'medicamentos': medicamentos})

from postos.models import Posto

def adicionar_medicamento(request):
    #precisamos dessas 3 coisas para identificar o posto e criar o medicamento relacionado a ele
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    if request.method == 'POST':
        id = request.POST.get('id_medicamento')
        nome = request.POST.get('nome_medicamento')
        quantidade = request.POST.get('quantidade')
        foto = request.FILES.get('foto')

        #Verifica se o ID já existe
        if Estoque.objects.filter(id_medicamento=id).exists():
            messages.add_message(request, constants.ERROR, "ID não permitido, insira outro.")
            return redirect('adicionar_medicamento')

        
        if nome and quantidade and id:
            medicamento = Estoque.objects.create(
                posto_saude=posto, 
                id_medicamento=id,
                nome_medicamento=nome,
                quantidade=int(quantidade),
                foto=foto
            )

            return redirect('listar_medicamento')
        
        else:
            messages.add_message(request, constants.ERROR, "Preencha todos os campos obrigatórios.")

            # Adiciona os postos selecionados
            #postos_selecionados = request.POST.getlist('postos')
            #medicamento.postos_disponiveis.set(postos_selecionados)

    return render(request, 'area_admin_medicamentos/adicionar_medicamento.html')


def editar_medicamento(request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    medicamento = get_object_or_404(Estoque, id_medicamento=id, posto_saude=posto)
    medicamentos = Estoque.objects.filter(posto_saude=posto)

    if request.method == 'POST':
        medicamento.nome_medicamento = request.POST.get('nome', medicamento.nome_medicamento)
        medicamento.quantidade = request.POST.get('quantidade', medicamento.quantidade)

        if 'foto' in request.FILES:
            medicamento.foto = request.FILES['foto']

        medicamento.save()

        # Atualiza os postos
        #postos_selecionados = request.POST.getlist('postos')
        #medicamento.postos_disponiveis.set(postos_selecionados)

        return redirect('listar_medicamento')

    return render(request, 'area_admin_medicamentos/editar_medicamento.html', {
        'medicamento': medicamento,
    })


def apagar_medicamento(request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    
    medicamento = get_object_or_404(Estoque, id_medicamento=id, posto_saude=posto)

    if request.method == 'POST':
        medicamento.delete()
        return redirect('listar_medicamento')

    return render(request, 'area_admin_medicamentos/deletar_medicamento.html', {'medicamento': medicamento})


def autenticar_token(request):
    if request.method == 'GET':
        return render (request, 'autenticacao.html')
    if request.method == 'POST':
        token_digitado = request.POST.get('token', '').strip()  # limpa espaços

        # Verifica se existe um posto com esse token (ignora maiúsculas/minúsculas)
        if PostoSaude.objects.filter(token__iexact=token_digitado).exists():
            # Marca o usuário como autenticado na sessão
            request.session['autenticado'] = True

            #guarda o token na sessão para uso futuro
            #no caso vai ser para identificar o posto e assim filtrar os medicamentos
            request.session['token'] = token_digitado
            posto = PostoSaude.objects.get(token__iexact=token_digitado)
            print(posto.nome)
            return render(request, 'area.html', {'posto': posto})
        else:
            messages.error(request, 'Token inválido!')
            return redirect('area_admin')
        

def adicionar_posto(request):
    if request.method == "POST":
        form = PostoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('area_admin')
    else:
        form = PostoForm()
    return render(request, 'area_admin/form_posto.html', {'form': form})


def editar_posto(request, id):
    posto = get_object_or_404(Posto, id=id)
    if request.method == "POST":
        form = PostoForm(request.POST, request.FILES, instance=posto)
        if form.is_valid():
            form.save()
            return redirect('area_admin')
    else:
        form = PostoForm(instance=posto)
    return render(request, 'area_admin/form_posto.html', {'form': form})


def apagar_posto(request, id):
    posto = get_object_or_404(Posto, id=id)
    if request.method == "POST":
        posto.delete()
        return redirect('area_admin')
    return render(request, 'area_admin/confirmar_apagar.html', {'posto': posto})


def listar_postos(request):
    if not request.session.get('autenticado'):
        messages.error(request, 'Você precisa autenticar o token primeiro!')
        return redirect('autenticacao')
    
    postos = Posto.objects.all()  # Busca todos os postos
    print(postos)
    return render(request, 'area_admin/listar_postos.html', {'postos': postos})


def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-data_publicacao')
    return render(request, 'area_admin_noticia/lista_noticias.html', {'noticias': noticias})


# Detalhe da notícia
def detalhe_noticia(request, id):
    noticia = get_object_or_404(Noticia, id=id)
    return render(request, 'area_admin_noticia/detalhe_noticia.html', {'noticia': noticia})


# Adicionar notícia
def adicionar_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_noticias')
    else:
        form = NoticiaForm()
    return render(request, 'area_admin_noticia/form_noticia.html', {'form': form, 'acao': 'Adicionar'})


# Editar notícia
def editar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticia)
        if form.is_valid():
            form.save()
            return redirect('listar_noticias')
    else:
        form = NoticiaForm(instance=noticia)
    # Corrigir o caminho do template:
    return render(request, 'area_admin_noticia/form_noticia.html', {'form': form, 'acao': 'Editar'})


# Apagar notícia
def apagar_noticia(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticia.delete()
        return redirect('listar_noticias')
    return render(request, 'area_admin_noticia/confirma_apagar.html', {'noticia': noticia})


def solicitacoes_users(request):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    reservas = Reserva.objects.filter(posto=posto, status='PENDENTE').order_by('-data_solicitacao')
    return render(request, 'area_admin_solicitacoes/solicitacoes_users.html', {"reservas":reservas})


def analise_documentos(request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    reserva = get_object_or_404(Reserva, id=id)
    medicamentos = Estoque.objects.filter(posto_saude=posto)

    # Pega os arquivos da reserva
    receita = reserva.receita.url if reserva.receita else None
    cartao = reserva.foto_cartao.url if reserva.foto_cartao else None
    status_opcoes = Reserva.STATUS_CHOICES

    if request.method == 'POST':
        #Verificação de segurança

        if int(reserva.quantidade) > Estoque.objects.get(id_medicamento=reserva.medicamento.id_medicamento, posto_saude=posto).quantidade:
            messages.add_message(request, constants.ERROR, "A quantidade solicitada não está disponível no estoque.")
            return redirect('analise_documentos', id=id)
        
        novo_status = request.POST.get('status') #nome do campo com as opções no HTML

        #mensagem associada à reserva para devolutiva ao usuário
        mensagem = request.POST.get('mensagem')

        mensagem_reserva = Mensagem.objects.create(
            reserva = reserva,
            mensagem = mensagem
            #a data será salva automaticamente
        )

        mensagem_reserva.save()

        if novo_status:
            reserva.status = novo_status
            reserva.save()

            if reserva.status == 'ACEITA':
                novo_estoque = Estoque.objects.get(id_medicamento=reserva.medicamento.id_medicamento, posto_saude=posto)
                novo_estoque.quantidade -= int(reserva.quantidade)
                novo_estoque.save()
        
            return redirect('solicitacoes_users')

    context = {
        'reserva': reserva,
        'receita': receita,
        'cartao': cartao,
        'status_opcoes': status_opcoes,
    }

    return render(request, 'area_admin_solicitacoes/analise_documentos.html', context)


def solicitacoes_aceitas(request):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    reservas = Reserva.objects.filter(posto=posto, status='ACEITA').order_by('-data_solicitacao')
    return render(request, 'area_admin_solicitacoes/solicitacoes_aceitas.html', {"reservas":reservas})


def analise_documentos_dps_aceitar(request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    reserva = get_object_or_404(Reserva, id=id)
    medicamentos = Estoque.objects.filter(posto_saude=posto)

    # Pega os arquivos da reserva
    receita = reserva.receita.url if reserva.receita else None
    cartao = reserva.foto_cartao.url if reserva.foto_cartao else None

    context = {
        'reserva': reserva,
        'receita': receita,
        'cartao': cartao,
    }

    return render(request, 'area_admin_solicitacoes/analise_documentos_dps_aceitar.html', context)


def solicitacao_cancelar(request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    medicamentos = Estoque.objects.filter(posto_saude=posto)

    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        novo_status = Reserva.objects.get(medicamento=reserva.medicamento.id_medicamento, posto=posto)
        novo_status.status = 'CANCELADA'
        novo_status.save()

        novo_estoque = Estoque.objects.get(id_medicamento=reserva.medicamento.id_medicamento, posto_saude=posto)
        novo_estoque.quantidade += int(reserva.quantidade)
        novo_estoque.save()

        return redirect('solicitacoes_aceitas')
    
    return render(request, "area_admin_solicitacoes/cancelar_solicitacao.html", {'reserva': reserva})

def solicitacoes_recusadas(request):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    reservas = Reserva.objects.filter(posto=posto, status='RECUSADA').order_by('-data_solicitacao')
    
    return render(request, 'area_admin_solicitacoes/solicitacoes_recusadas.html', {"reservas":reservas})


def solicitacao_retirada (request, id):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)
    medicamentos = Estoque.objects.filter(posto_saude=posto)

    reserva = get_object_or_404(Reserva, id=id)

    if request.method == 'POST':
        novo_status = Reserva.objects.get(medicamento=reserva.medicamento.id_medicamento, posto=posto)
        novo_status.status = 'RETIRADA'
        novo_status.save()

    return redirect('solicitacoes_aceitas')

def solicitacoes_retiradas(request):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    reservas = Reserva.objects.filter(posto=posto, status='RETIRADA').order_by('-data_solicitacao')
    return render(request, 'area_admin_solicitacoes/solicitacoes_retiradas.html', {"reservas":reservas})

def solicitacoes_canceladas(request):
    token = request.session.get('token')
    posto_id = request.session.get('posto_id')
    posto = get_object_or_404(PostoSaude, token__iexact=token)

    reservas = Reserva.objects.filter(posto=posto, status='CANCELADA').order_by('-data_solicitacao')
    return render(request, 'area_admin_solicitacoes/solicitacoes_canceladas.html', {"reservas":reservas})