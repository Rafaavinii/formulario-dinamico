from django.urls import path
from . import views

urlpatterns = [
    path('criar_formulario/', views.criar_formulario, name='criar_formulario'),
    path('responder_formulario/<int:formulario_id>', views.responder_formulario_view, name='responder_formulario'),

]