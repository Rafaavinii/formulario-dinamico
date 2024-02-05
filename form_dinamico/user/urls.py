from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastro_view, name='cadastro'),
    path('entrar/', views.entrar_view, name='entrar'),
    path('sair/', views.logout, name='sair'),
    path('pagina_inicial/', views.dashboard_view, name='pagina_inicial'),

]