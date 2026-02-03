from django.db import models

class Posto(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='fotos', null=True, blank=True)
    endereco = models.TextField()
    link = models.URLField(max_length=500, null=True, blank=True)  # <--- Novo campo
    bairro = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    telefone1 = models.CharField(max_length=20)
    telefone2 = models.CharField(max_length=20)
    horario_semana = models.CharField(max_length=100)
    horario_sabado = models.CharField(max_length=100)
    horario_domingo = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

