from django.db import models
from django.contrib.auth.models import User
from medicamentos.models import Medicamento
from postos.models import Posto
from area_admin.models import Estoque, PostoSaude
#importando acima as tabelas das minhas chaves estrangeiras 

#criando a class Reserva para reserva de medicamentos
class Reserva(models.Model):
    #lista com os status possíveis 
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ACEITA', 'Aceita'),
        ('RECUSADA', 'Recusada'),
        ('RETIRADA', 'Retirada'),
        ('CANCELADA', 'Cancelada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Estoque, on_delete=models.CASCADE)
    posto = models.ForeignKey(PostoSaude, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=False, null=False)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    rg = models.CharField(max_length=20, blank=False, null=False)
    cpf = models.CharField(max_length=14, blank=False, null=False)
    quantidade = models.CharField(max_length=3, blank=False, null=False)
    num_cartao = models.CharField(max_length=20, blank=False, null=False)
    foto_cartao = models.FileField(upload_to='cartoes/', blank=False, null=False)
    receita = models.FileField(upload_to='receitas/', blank=False, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDENTE')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
        #return f"Reserva de {self.usuario.username} - {self.medicamento.nome}" #como se fosse um print