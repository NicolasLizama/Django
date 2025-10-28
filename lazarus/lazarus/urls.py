"""
URL configuration for lazarus project.

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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.paginator),
    path('fail/', views.paginatorfail),
    path('introduccion/', views.introduccion, name='introduccion'),
    path('ingresar/', views.ingresar),
    path('crear/', views.paginator2),
    path('recuperar_contraseña/', views.recuperar_contraseña, name='recuperar_contraseña'),
   # path('mostrarCambioPassword/', views.mostrarCambioPassword, name='mostrarCambioPassword'),
   # path('HacercambiarPassword/', views.HacercambiarPassword, name='HacercambiarPassword'), 
    path('usercreate/', views.usercreate),
    path('oficial/', views.oficial),
    path('phq9/', views.phq9, name='phq9'),
    path('phq9_enviar/', views.phq9_enviar, name='phq9_enviar'),
    path('gad7/', views.gad7, name='gad7'),
    path('gad7_enviar/', views.gad7_enviar, name='gad7_enviar'),
    path('Test_reconocimiento', views.Test_reconocimiento, name='Test_reconocimiento'),
    path('TestRecco_enviar/', views.TestRecco_enviar, name='TestRecco_enviar'),
    path('logout_view/', views.logout_view,),
    path('ver_test/', views.ver_test, name='ver_test'),
    path('ver_perfil/', views.ver_perfil, name='ver_perfil')
]




#lo que esta marcado como comentario son vistas con funcionas no hechas correctamente