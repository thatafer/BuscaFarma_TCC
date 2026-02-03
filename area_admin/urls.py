from django.urls import path
from . import views

urlpatterns = [
    path('', views.autenticar_token, name='area_admin'),  # caminho raiz   # caminho diferente

    path('postos/', views.listar_postos, name='listar_postos'),
    path('postos/adicionar/', views.adicionar_posto, name='adicionar_posto'),
    path('postos/editar/<int:id>/', views.editar_posto, name='editar_posto'),
    path('postos/apagar/<int:id>/', views.apagar_posto, name='apagar_posto'),

    path('adicionar/', views.adicionar_noticia, name='adicionar_noticia'),
    path('editar/<int:pk>/', views.editar_noticia, name='editar_noticia'),  # <- usar pk
    path('apagar/<int:pk>/', views.apagar_noticia, name='apagar_noticia'),
    path('detalhe/<int:id>/', views.detalhe_noticia, name='detalhe_noticia'),
    path('noticias/', views.lista_noticias, name='listar_noticias'),
    path('medicamentos/', views.listar_medicamento, name='listar_medicamento'),
    path('medicamentos/adicionar/', views.adicionar_medicamento, name='adicionar_medicamento'),
    path('medicamentos/<int:id>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:id>/apagar/', views.apagar_medicamento, name='deletar_medicamento'),
    path('solicitacoes_users/', views.solicitacoes_users, name='solicitacoes_users'),
    path('analise_documentos/<int:id>/', views.analise_documentos, name='analise_documentos'),
    path('solicitacoes_aceitas/', views.solicitacoes_aceitas, name='solicitacoes_aceitas'),
    path('analise_documentos_dps_aceitar/<int:id>/', views.analise_documentos_dps_aceitar, name='analise_documentos_dps_aceitar'),
    path('solicitacao_cancelar/<int:id>/', views.solicitacao_cancelar, name='solicitacao_cancelar'),
    path('solicitacoes_recusadas/', views.solicitacoes_recusadas, name='solicitacoes_recusadas'),
    path('solicitacao_retirada/<int:id>/', views.solicitacao_retirada, name='solicitacao_retirada'),
    path('solicitacoes_retiradas/', views.solicitacoes_retiradas, name='solicitacoes_retiradas'),
    path('solicitacoes_canceladas/', views.solicitacoes_canceladas, name='solicitacoes_canceladas'),
]

