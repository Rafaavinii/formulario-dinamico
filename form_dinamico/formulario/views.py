from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
import json

def criar_formulario(request):
    if request.method == 'GET':
        print(Questao.objects.get(id=24).itens)
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
        

        for i in range(1, int(num_questoes)+1):
            questao_texto = request.POST.get(f'questao{i}')
            tipo = request.POST.get(f'tipo{i}')
            num_opcoes = request.POST.get(f'num_opcoes{i}')

            itens_lista = []
            for j in range(1, int(num_opcoes)+1):
                itens_lista.append(request.POST.get(f'opcao{j}-text-{i}'))
            itens_json = json.dumps(itens_lista, ensure_ascii=False)

            questao = Questao.objects.create(
                questao_texto = questao_texto,
                tipo = tipo,
                formulario = formulario,
                itens = itens_json
            )
            questao.save()
        
        messages.success(request, 'Formulário criado com sucesso!')

        return redirect('criar_formulario')


