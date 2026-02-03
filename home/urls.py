from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('reservar/<int:id>/<int:id2>', views.reservar_medicamento, name='reserva'),
    path('noticia/<int:pk>/', views.noticia_detalhe, name='noticia_detalhe'),
    path('posto/<int:pk>/', views.posto_detalhe, name='posto_detalhe'),
    path('comentarios/', views.comentarios, name='comentarios'),
]

