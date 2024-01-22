from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages

def criar_formulario(request):
    if request.method == 'GET':
        print(Questao.objects.all()[0].tipo)
        return render(request, 'criar_formulario.html')
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        num_questoes = request.POST.get('num_questoes')
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

        for i in range(1, int(num_questoes)):
            questao_texto = request.POST.get(f'questao{i}')
            tipo = request.POST.get(f'tipo{i}')
            questao = Questao.objects.create(
                questao_texto = questao_texto,
                tipo = tipo,
                formulario = formulario
            )
            questao.save()

        messages.success(request, 'Formulário criado com sucesso!')

        return redirect('criar_formulario')


