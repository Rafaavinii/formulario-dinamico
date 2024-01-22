from django.shortcuts import render, redirect
from datetime import datetime
from .models import FormDinamico
from django.contrib.auth.models import User
from django.contrib import messages

def criar_formulario(request):
    if request.method == 'GET':
        return render(request, 'criar_formulario.html')
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        print(titulo)
        descricao = request.POST.get('descricao')
        data = datetime.now()
        user = 1

        formulario = FormDinamico.objects.create(
            nome=titulo,
            descricao=descricao,
            data_criacao=data,
            user_id=user,
        )

        formulario.save()

        messages.success(request, 'Formulário criado com sucesso!')

        return redirect('criar_formulario')


