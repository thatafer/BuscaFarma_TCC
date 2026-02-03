from django.db import models

class PostoSaude(models.Model):
    nome = models.CharField(max_length=100)
    token = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome
    
class Estoque(models.Model):
    #id relacionado ao posto de saúde autenticado, para podermos filtrar
    posto_saude = models.ForeignKey(PostoSaude, on_delete=models.CASCADE)
    id_medicamento = models.CharField(max_length=50, primary_key=True)
    foto = models.ImageField(upload_to='medicamentos/', null=True, blank=True)
    nome_medicamento = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    #postos_disponiveis = models.ManyToManyField(PostoSaude, related_name='estoques')

    #def __str__(self):
        #return f"{self.item} - {self.quantidade} unidades no {self.posto_saude.nome}"

class Mensagem(models.Model):
    reserva = models.ForeignKey('home.Reserva', on_delete=models.CASCADE)
    mensagem = models.TextField(blank=True, null=True)
    data_mensagem = models.DateTimeField(auto_now_add=True)