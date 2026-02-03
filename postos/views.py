from django.shortcuts import render
from .models import Posto

def lista_postos(request):
    postos = Posto.objects.all()
    return render(request, 'postos.html', {'postos': postos})

from django.contrib.auth.decorators import login_required

def editar_posto(request, id):
    posto = get_object_or_404(Posto, id=id)
    
    if request.user.is_authenticated:
        # Usuário logado: formulário editável
        if request.method == 'POST':
            form = PostoForm(request.POST, request.FILES, instance=posto)
            if form.is_valid():
                form.save()
                return redirect('postos')
        else:
            form = PostoForm(instance=posto)
        return render(request, 'editar_posto.html', {'form': form, 'editable': True})
    else:
        # Usuário não logado: formulário apenas leitura
        form = PostoForm(instance=posto)
        for field in form.fields.values():
            field.disabled = True  # desativa todos os campos
        return render(request, 'editar_posto.html', {'form': form, 'editable': False})


from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def excluir_posto(request, id):
    posto = get_object_or_404(Posto, id=id)
    posto.delete()
    return redirect('postos')


@login_required(login_url='/login/')
def adicionar_posto(request):
    if request.method == 'POST':
        form = PostoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('postos')
    else:
        form = PostoForm()
    return render(request, 'adicionar_posto.html', {'form': form})
