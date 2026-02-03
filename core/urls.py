"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from area_admin import views as area_admin_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')), #adicionando o app home na url e incluindo um grupo de urls pertencentes a ele
    path('login/', include('login.urls')),
    path('sobre/', include('sobre.urls')),
    path('noticias/', include('noticias.urls')),
    path('postos/', include('postos.urls')),
    path("autenticacao/", area_admin_views.autenticar_token, name="autenticar_token"),
    path("area_admin/", include("area_admin.urls")),  
    path('medicamentos/', include('medicamentos.urls')),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
