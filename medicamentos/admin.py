from django.contrib import admin
from .models import Medicamento

class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade', 'mostrar_postos')
    filter_horizontal = ('postos_disponiveis',)  # <- plural, igual ao models.py
    search_fields = ('nome',)
    list_filter = ('postos_disponiveis',)       # <- plural também

    def mostrar_postos(self, obj):
        return ", ".join([posto.nome for posto in obj.postos_disponiveis.all()])
    mostrar_postos.short_description = 'Postos Disponíveis'

admin.site.register(Medicamento, MedicamentoAdmin)
