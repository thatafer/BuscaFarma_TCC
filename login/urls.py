from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cadastro', views.cadastrar, name = 'cadastro'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/alterar_dados/', views.alterar_dados, name='alterar_dados'),
    path('dashboard/alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('dashboard/solicitacoes/', views.solicitacoes, name='solicitacoes'),
    path('ver_mais/<int:id>/', views.ver_mais, name='ver_mais'),  
] 

