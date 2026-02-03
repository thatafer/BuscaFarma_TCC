from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User 
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import AtualizacaoDeUsuario
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from home.models import Reserva
from area_admin.models import Mensagem

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # Autenticando o usuário 
        user = authenticate(request, username=username, password=senha)
        if user:
            auth_login(request, user)
            return redirect('dashboard')  # Redireciona para a dashboard após logar
        
        messages.add_message(request, constants.ERROR, "Usuário ou senha inválidos")
        return redirect('login')


def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validações
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "A senha deve conter pelo menos 6 caracteres")
            return redirect('cadastro')
        
        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas não coincidem")
            return redirect('cadastro')
        
        if len(nome) < 2:
            messages.add_message(request, constants.ERROR, "O nome deve conter pelo menos 2 caracteres")
            return redirect('cadastro')
        
        if not nome.replace(" ", "").isalpha():
            messages.add_message(request, constants.ERROR, "O nome deve conter apenas letras.")
            return redirect('cadastro')
        
        if '@' not in email:
            messages.add_message(request, constants.ERROR, "O email deve conter '@'.")
            return redirect('cadastro')
        
        if User.objects.filter(username=username).exists():
            messages.add_message(request, constants.ERROR, "O nome de usuário já está em uso.")
            return redirect('cadastro')
        
        # Salvando o usuário no banco de dados
        User.objects.create_user(username=username, first_name=nome, email=email, password=senha)
        messages.add_message(request, constants.SUCCESS, "Cadastro realizado com sucesso!")
        return redirect('login')


def logout_view(request):
    auth_logout(request)
    return redirect('home')

#@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'dashboard.html')

def alterar_dados(request):
    if request.method == 'GET':
        #a instância do formulário com os dados do usuário atual
        atualizar = AtualizacaoDeUsuario(instance=request.user)

    elif request.method == 'POST':
        #pegando os dados do formulário e atualizando o usuário atual
        atualizar = AtualizacaoDeUsuario(request.POST, instance=request.user)

        if atualizar.is_valid():
            atualizar.save()
            #messages.add_message(request, constants.SUCCESS, "Dados alterados com sucesso!")
            return redirect('dashboard')
        else:
            messages.add_message(request, constants.ERROR, "Erro ao atualizar os dados. Verifique os campos.")


    context = {
        'atualizar': atualizar
    }

    return render(request, 'atualizar_dados.html', context)

def alterar_senha(request):
    return render(request, 'alterar_senha.html')

def solicitacoes(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'solicitacoes.html', {'reservas': reservas})

def ver_mais(request, id):
    reserva = Reserva.objects.get(id=id)
    mensagem = Mensagem.objects.filter(reserva=reserva)
    return render(request, 'ver_mais.html', {'mensagem': mensagem})