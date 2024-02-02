from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastro_view, name='cadastro'),
    path('entrar/', views.entrar_view, name='entrar'),

]