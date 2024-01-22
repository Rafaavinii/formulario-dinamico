from django.urls import path
from . import views

urlpatterns = [
    path('criar_formulario/', views.criar_formulario, name='criar_formulario'),
]