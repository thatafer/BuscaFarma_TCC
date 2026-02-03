from django.contrib import admin
from .models import PostoSaude, Estoque

@admin.register(PostoSaude)
class PostoSaudeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'token')  # ou os campos que você tiver

admin.site.register(Estoque)