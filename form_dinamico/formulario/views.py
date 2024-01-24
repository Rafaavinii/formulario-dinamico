from django.shortcuts import render, redirect
from datetime import datetime
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from .models import FormDinamico, Questao, Resposta
from django.http import HttpResponse
import json

def criar_formulario(request):
    if request.method == 'GET':
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
            

            itens_json = None
            if num_opcoes != '':
                itens_lista = []
                num_opcoes = int(num_opcoes)

                for j in range(1, num_opcoes+1):
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

def responder_formulario_view(request, formulario_id):
    if request.method == 'GET':
        resposta = Resposta.objects.all()
        print(resposta)
        formulario = FormDinamico.objects.get(id=formulario_id)
        context = {
            'formulario_id': formulario.id,
            'nome': formulario.nome,
            'descricao': formulario.descricao,
            'questoes': [],
        }

        questoes = Questao.objects.filter(formulario_id=formulario.id)

        for questao in questoes:
            questao_dict = {}
            questao_dict['questao_id'] = questao.id 
            questao_dict['questao_texto'] = questao.questao_texto
            questao_dict['tipo'] = questao.tipo
            if questao.tipo == 'escolha_unica' or questao.tipo == 'multipla_escolha':
                questao_dict['itens'] = json.loads(questao.itens)
        
            context['questoes'].append(questao_dict)

        return render(request, 'responder_formulario.html', context)
    
    if request.method == 'POST':
        questoes = request.POST.getlist('questao_id')
        for questao in questoes:
            resposta_texto = request.POST.get(f'resposta_texto_{questao}')
            resposta_escolha_unica = request.POST.get(f'resposta_escolha_unica_{questao}')
            resposta_multipla_escolha = request.POST.getlist(f'resposta_multipla_escolha_{questao}')
            resposta_true_false = request.POST.get(f'resposta_true_false_{questao}')
            resposta_data = request.POST.get(f'resposta_data_{questao}')
            resposta_numero = request.POST.get(f'resposta_numero_{questao}')

            resposta_valor = obter_valor_nao_none(
                resposta_texto,
                resposta_escolha_unica,
                resposta_multipla_escolha,
                resposta_true_false,
                resposta_data,
                resposta_numero
            )

            resposta = Resposta.objects.create(
                resposta_texto = resposta_valor,
                questao_id = questao,
                data_resposta = '2024-02-14',
                hora = '13',
                user_id = 1,
            )

            resposta.save()

        return HttpResponse('Respondido!')



def obter_valor_nao_none(*valores):
    for valor in valores:
        if valor is not None:
            return valor
    return None  # Retorna None se todos os valores forem None



