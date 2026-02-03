from django.db import models
from postos.models import Posto  # importando o modelo Posto

class Medicamento(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField()
    foto = models.ImageField(upload_to='medicamentos/')
    postos_disponiveis = models.ManyToManyField(Posto, blank=True)  # <--- nome correto do campo

    def __str__(self):
        return self.nome
