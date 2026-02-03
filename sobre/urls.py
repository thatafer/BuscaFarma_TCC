from django.urls import path
from . import views

urlpatterns = [
    path('', views.sobre, name = 'sobre'),
    path('programadores/', views.programadores, name='programadores'),
    path('sistema/', views.sistema, name='sistema'),
] 