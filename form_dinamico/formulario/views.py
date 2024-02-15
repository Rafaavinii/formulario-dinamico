from django.shortcuts import render, redirect
from datetime import datetime
from django.db.models import Count, Value
from django.db.models.functions import Coalesce
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
        descricao = request.POST.get('descricao', '')
        data = datetime.now()
        user = request.user

        formulario = FormDinamico.objects.create(
            nome=titulo,
            descricao=descricao,
            data_criacao=data,
            user=user,
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

            resposta = request.POST.get(f'resposta_{questao}')
            if Questao.objects.get(id=questao).tipo == 'multipla_escolha':
                resposta = request.POST.getlist(f'resposta_{questao}')

            resposta = Resposta.objects.create(
                resposta_texto = resposta,
                questao_id = questao,
                data_resposta = datetime.now().strftime("%Y-%m-%d"),
                hora = datetime.now().strftime("%H:%M:%S"),
                user_id = 1,
            )

            resposta.save()

        return HttpResponse('Respondido!')

def dashboard_respostas_view(request, formulario_id):
    if request.method == "GET":
        questoes = Questao.objects.filter(formulario_id=formulario_id)

        resultado = Resposta.objects.filter(questao__formulario_id=formulario_id).values('questao_id').annotate(total=Count('questao_id'))
        quantidade_resposta = max(resultado.values('total'), key=lambda x: x['total'])['total']

        estatistica = {}
        estatistica['quantidade_resposta'] = quantidade_resposta

        for questao in questoes:

            questao_data = {
                'id_questao': questao.id,
                'questao_texto': questao.questao_texto,
                'questao_tipo': questao.tipo,
            }

            if questao.tipo == 'escolha_unica':
                respostas = Resposta.objects.filter(questao_id=questao.id).values('resposta_texto').annotate(total=Coalesce(Count('resposta_texto'), Value(0)))
                respostas = list(respostas)

                opcoes = {elemento: 0 for elemento in eval(questao.itens)}
                opcao_total = {'opcoes': [], 'totais': []}
                for resposta in respostas:
                    opcao_total['opcoes'].append(resposta['resposta_texto'])
                    opcao_total['totais'].append(resposta['total'])
                opcao_total.update({'questao': questao_data})
                estatistica[f'questao_{questao.id}'] = opcao_total

            if questao.tipo == 'multipla_escolha':
                opcoes = {elemento: 0 for elemento in eval(questao.itens)}
                respostas = Resposta.objects.filter(questao_id=questao.id)
                for resposta in respostas:
                    resposta = eval(resposta.resposta_texto)
                    for res_texto in resposta:
                        if res_texto in opcoes.keys():
                            opcoes[res_texto] += 1
                
                estatistica[f'questao_{questao.id}'] = {
                    'opcoes': list(opcoes.keys()),
                    'totais': list(opcoes.values()),
                    'questao': questao_data,
                }
            
            if questao.tipo == 'texto':
                respostas = Resposta.objects.filter(questao_id=questao.id)
                valor_resposta = []

                for resposta in respostas:
                    valor_resposta.append(resposta.resposta_texto)
                
                estatistica[f'questao_{questao.id}'] = {
                    'respostas': valor_resposta,
                    'questao': questao_data,
                }
            
            if questao.tipo == 'true_false':
                respostas = Resposta.objects.filter(questao_id=questao.id)
                opcoes = {'verdade': 0, 'falso': 0}

                for resposta in respostas:
                    if resposta.resposta_texto == 'falso':
                        opcoes['falso'] += 1
                    else: 
                        opcoes['verdade'] += 1
                
                estatistica[f'questao_{questao.id}'] = {
                    'opcoes': list(opcoes.keys()),
                    'totais': list(opcoes.values()),
                    'questao': questao_data,
                }
            
            if questao.tipo == 'data':
                respostas = Resposta.objects.filter(questao_id=questao.id)
                valor_resposta = []

                for resposta in respostas:
                    valor_resposta.append(resposta.resposta_texto)
                
                estatistica[f'questao_{questao.id}'] = {
                    'respostas': valor_resposta,
                    'questao': questao_data,
                }
            
            if questao.tipo == 'numero':
                respostas = Resposta.objects.filter(questao_id=questao.id)
                valor_resposta = []

                for resposta in respostas:
                    valor_resposta.append(resposta.resposta_texto)
                
                estatistica[f'questao_{questao.id}'] = {
                    'respostas': valor_resposta,
                    'questao': questao_data,
                }
            
        print(estatistica)
                

        return render(request, 'respostas.html', {'questoes': estatistica})




