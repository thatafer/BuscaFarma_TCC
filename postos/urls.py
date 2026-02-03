from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_postos, name='postos'),
    path('editar/<int:id>/', views.editar_posto, name='editar_posto'),
    path('excluir/<int:id>/', views.excluir_posto, name='excluir_posto'),
    path('adicionar/', views.adicionar_posto, name='adicionar_posto'),

]
