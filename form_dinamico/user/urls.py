from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastro_view, name='cadastro'),
    path('entrar/', views.entrar_view, name='entrar'),
    path('sair/', views.logout, name='sair'),
    path('pagina_inicial/', views.dashboard_view, name='pagina_inicial'),
    path('formulario/', views.buscar_formulario_view, name='buscar_formulario'),
    path('visualizar/', views.buscar_formulario_view, name='buscar_formulario'),
]